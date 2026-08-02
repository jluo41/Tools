# haipipe-board-index · v0.1.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand
session: dff70bd0-2dc2-425e-882b-bdcd25df0013

## Opening
Does `haipipe-board-index` define a clear path from a raw topic to an approved Board and group structure?

This skill owns the view above individual pages: the spine, close condition, groups, relationships, and Index reading path.
The hard part is showing how groups connect without copying the page roster or taking over page-level decisions.
Its choices shape how every newcomer enters the Board and understands where work belongs.
It is healthy when an approved proposal can be materialized and refreshed without losing human-written group meaning.

## Diagram
<!-- haipipe:skill:tree:start fc83db2b18aea7b1 board/haipipe-board-index -->

```
haipipe-board-index/
  src/
    lanes.py           253 ln  One `⚙️ engine · 📋 pages · 📂 folder` lane block per group, in board.md.
  CHANGELOG.md          27 ln  haipipe-board-index · Changelog
  SKILL.md             159 ln  /haipipe-board-index · the board and the group, before the page
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start fc83db2b18aea7b1 board/haipipe-board-index -->

**haipipe-board-index** · `0.1.0` · last shipped 2026-07-30

- folder   `board/haipipe-board-index/`
- tools    not declared
- summary  First cut: the two canvas altitudes (JL 260730), the B0-B9 index anatomy, and src/lanes.py round-tripping one lane block per group.

### SKILL.md




`haipipe-board` turns a board folder into a live page.
This skill decides **what that board is made of**: its groups, which pages sit in them, how they connect, and what the reader meets at `#top` before entering any page.

**The boundary, and it is a hard one:**

```
haipipe-board-index          haipipe-board
─────────────────────        ──────────────────────────────
board.md's shape             build.py · board.html
groups + their order         page rendering · sentence
how groups connect           serve · comments · chat
the index's own sections     the checker
proposing a NEW board        (this skill never emits HTML)
```

If a change is about ONE page's sections, it is not this skill.
That is `QAa`, and it will move to `haipipe-board-page`.


- 1 · 🧭 Two canvases, two altitudes
      The mistake worth not repeating (JL 260730): the board level does **not** need the page roster.
      The index already lists every page below it.
      So the board-level canvas shows what the index cannot, and the roster lives one altitude down.
      ```
      🗂 BOARD level · in board.md's ## Board Map
         how the GROUPS connect: the main line, the parallel layers, what
         ships, plus the handful of real cross-group page edges.
         One ``` figure, rendered as a shuttable disclosure at the very top
         of the index. NOT a second copy of the index.
         `## Board Structure` is a different section: the source-to-webpage
         shape, in prose, further down.

      📋 GROUP level · in each ### group's intro, inside ## Pages
         one row per page:  ⚙️ engine  ◀──  📋 page  ──▶  📂 folder
         which engine file governs this page, what artifact it produces.
      ```
      A page is a **working record**, not merely an undecided question, so the middle lane is labelled `📋 PAGES · the working record`.
      Both canvases are ASCII inside a fence, which means every id in them is a real link: `haipipe-board` 0.53.0 wraps any page or group id inside a figure as an anchor, alignment untouched, working with scripts off.

- 2 · 🏷 What the index is made of
      Nine sections, in render order.
      Five survive when a page is open, because they are the board's chrome; the rest are index-only.
      ```
      #   section            element             source in board.md    at #<page-id>
      ────────────────────────────────────────────────────────────────────────────────
      B0  Heading            .board-heading      `# ` title            ✅ stays
      B1  Spine              .spine              spine: · close:       ✅ stays
      B2  Progress           p.bar               derived               ❌ hidden
      B3  Board Map          .board-map          ## Board Map (ASCII)  ❌ hidden
                             details, shuttable   or board-map: · scene
      B4  Topic              details.ctx         ## Topic              ✅ stays
      B5  Pipeline           details.ctx         ## Pipeline           ✅ stays
      B6  Board-Structure    details.ctx         ## Board Structure    ✅ stays
      B7  All Pages          h3#qlist + .idx     ## Pages              ❌ hidden
      B8  Activity           section.activity    every page's ## Log   ❌ hidden
      B9  Foot               p.foot              generated             ❌ hidden
      ```
      Hiding is one rule in `assets/board.css`: `body:has(.q:target)` hides `.idx .bar .board-map .activity h3.sec .foot`.
      Everything absent from that list stays, restyled small and muted.
      Change the list, not individual sections.
      A group anchors at `#group-<token>` (`QA · Design` → `#group-QA`).
      A group is **not** a page: the anchor scrolls the index, it never opens a card, and it never enters the settled count.

- 3 · 🛠 Verbs

- 3.1 · `propose` · before any file exists
      Talk first, write nothing.
      From a topic, propose and show:
      ```
      1. spine        one sentence: what is being pinned down
      2. close        what must be true for the board to be done
      3. groups       3-7 of them, each a responsibility, not a phase
      4. pages        the questions each group owns, with ids
      5. connections  which group depends on which, and why
      6. skills       which skill this board may change (optional)
      ```
      Then **stop and get approval.** Nothing is materialized on a proposal.
      The group letters chosen here are cited by every future page, so a rename later is a migration, not an edit.

- 3.2 · `materialize` · after approval
      `board.md` (title · spine · close · `## Topic` · `## Pipeline` · `## Board Structure` · `## Pages`), one folder per group, one page file per listed page, then hand off to `haipipe-board` to build.

- 3.3 · `lanes` · refresh the per-group blocks
      ```bash
      python3 src/lanes.py <board-dir>            # dry run: what would change
      python3 src/lanes.py <board-dir> --apply    # write board.md
      ```
      It ROUND-TRIPS.
      The page roster is generated from `## Pages` so it can never disagree with the index, but every cell a person typed is kept:
      ```
      · a row whose page still exists   → engine · name · folder all KEPT
      · a page with no row yet          → arrives with `?`, which is the to-do list
      · a row whose page is gone        → DROPPED
      ```
      Same bargain as `xcal.py` keeping a human's frame position: the generator owns the skeleton, the person owns the meaning, so re-running is never destructive.
      A page's `# ` title only SEEDS a new row's name; the column is 29 characters and a real title rarely fits it.

- 3.4 · `regroup` · move pages into one folder per group
      Wraps `haipipe-board/regroup.py`, which is the migration tool for any group rename or split:
      ```bash
      python3 ../haipipe-board/regroup.py <board-dir>            # plan
      python3 ../haipipe-board/regroup.py <board-dir> --apply    # git mv
      ```
      Renaming a group letter is a THREE-part change and all three must land together: `git mv` the folder and files, keep the old id as a declared alias so existing citations resolve, then grep the repo for the old id and fix every hit.

- 3.5 · `check` · index-level only
      ```
      · every group has an intro sentence            (line 1 always shows)
      · every group has a lane block                 (src/lanes.py reports gaps)
      · every id inside a figure resolves            (an unlinked token is dead text)
      · the board canvas is not a copy of the index
      ```
      Page-level and sentence-level checks belong to `haipipe-board/check.py`.

- 4 · 📂 Files
      ```
      haipipe-board-index/
      ├── SKILL.md            this contract
      ├── CHANGELOG.md        version history
      └── src/lanes.py        the per-group lane block, round-tripped
      ```
      Reads and writes `board.md` only.
      Never touches `board.html`, never touches a page file, never imports `haipipe-board/src/`.
      A board's `## Pages` plus each page's `# ` line is the whole input, so the two skills ship on their own clocks.
### The other files

1 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
src/lanes.py     253 ln  One `⚙️ engine · 📋 pages · 📂 folder` lane block per group, in board.md.
```

<!-- haipipe:skill:body:end -->

## Items to Finish
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## Where we are
Page generated 260730 1720. Health still unruled, but the COPY is now verified: on 260801 all three managed spans were regenerated from `board/haipipe-board-index/` and compared byte for byte against what sits on this page, and all three were identical. A second pass confirmed the transform is lossless: every one of SKILL.md's 109 content lines reaches `## Content`, with only the frontmatter and the `# ` title dropped by design.

Worth knowing before trusting a green `check`: `skillpage.py check` hashes the frontmatter's derived facts ONLY (`name` `version` `last_updated` `summary` `allowed-tools`), by `digest()`'s own docstring, "so prose edits never look like drift". A ✅ therefore means the metadata is current, NOT that the prose matches. Byte equality needs the regenerate-and-diff done above. That gap belongs to `skillpage.py`, which ships in `haipipe-board`, so it is [Skill-0-haipipe-board](QC-engine/Skill-0-haipipe-board.md)'s to carry, not this skill's.

## Log
260801 0107 · verified the three managed spans against `board/haipipe-board-index/`: tree, body and log all regenerate byte-identical, no SKILL.md line missing. Noted that `check`'s hash covers frontmatter only.
260730 1720 · page generated from `board/haipipe-board-index/` by `skillpage.py new`

<!-- haipipe:skill:log:start fc83db2b18aea7b1 board/haipipe-board-index -->

Converted from the skill's own `CHANGELOG.md`: 1 releases.

260730 · `0.1.0`
      - First cut, extracted from `haipipe-board` at JL's request ("did you build the haipipe-board-index? please do it now").
        It owns the BOARD and GROUP altitude: proposing a board's structure before any file exists, materializing it, and the two canvases the index carries.
        It does not render HTML, a page, or a sentence.
      - **The two canvas altitudes** (JL 260730).
        The board level shows how GROUPS connect and nothing else, because the index already lists every page below it; a board-level roster is the same information twice.
        The per-page `⚙️ engine · 📋 page · 📂 folder` mapping lives one altitude down, in each group's own intro.
        A page is a WORKING RECORD, so the middle lane is labelled that, not "what is undecided".
      - `src/lanes.py` generates one lane block per group and ROUND-TRIPS: the roster comes from `## Pages` so it can never disagree with the index, while every cell a person typed (engine, name, folder) is read back and kept.
        A new page arrives with `?`, which is honest and doubles as QAa7's to-do list; a retired page's row is dropped, the rule `xcal.py` already applies to a retired page's frame.
        A page's `# ` title only SEEDS a new row's name: the column is 29 characters and a real title rarely fits it ("How to design the haipipe-board folder structure?" truncates to noise where a person writes "the folder structure").
      - Kept cells are collected GLOBALLY (`collect_kept`), keyed by page id across the whole file, not per block.
        Proven the same day by the Design → Delivery → Engine → Execute restructure of `01-boardform-260722`: 31 of 42 pages changed group, and every typed cell travelled with its page instead of resetting to `?`.
        `dropped` is likewise judged against the whole roster: after a regroup a page has merely moved, and only a page in no group is gone.
      - Documents the B0-B9 index anatomy and, with it, the one CSS rule that decides which sections are board chrome and which are index-only: `body:has(.q:target)` hides `.idx .bar .board-map .activity h3.sec .foot`, and everything absent from that list stays, restyled muted.
        B0 B1 B4 B5 B6 stay; B2 B3 B7 B8 B9 do not.
      - Records that a group anchors at `#group-<token>` and is not a page: the anchor scrolls the index, never opens a card, never enters the settled count.

<!-- haipipe:skill:log:end -->
