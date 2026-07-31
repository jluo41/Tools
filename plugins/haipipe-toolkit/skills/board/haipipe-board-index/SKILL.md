---
name: haipipe-board-index
description: >-
  The BOARD and GROUP altitude of a board: propose a board's structure with the human before any file exists, materialize it, and own the two canvases the index carries: the board-level map of how groups connect, and one engine·pages·folder lane block per group. Use when starting a new board from a topic, when adding or renaming a page group, when the index no longer explains the board, or when the user says board structure, board index, page group, group map, board canvas, lanes, regroup, or /haipipe-board-index. It does NOT render HTML: haipipe-board owns build, serve, page and sentence.
metadata:
  version: "0.1.0"
  last_updated: "2026-07-30"
  summary: "First cut: the two canvas altitudes (JL 260730), the B0-B9 index anatomy, and src/lanes.py round-tripping one lane block per group."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-index · the board and the group, before the page

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

## 🧭 Two canvases, two altitudes

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

## 🏷 What the index is made of

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

## 🛠 Verbs

### `propose` · before any file exists

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

### `materialize` · after approval

`board.md` (title · spine · close · `## Topic` · `## Pipeline` · `## Board Structure` · `## Pages`), one folder per group, one page file per listed page, then hand off to `haipipe-board` to build.

### `lanes` · refresh the per-group blocks

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

### `regroup` · move pages into one folder per group

Wraps `haipipe-board/regroup.py`, which is the migration tool for any group rename or split:

```bash
python3 ../haipipe-board/regroup.py <board-dir>            # plan
python3 ../haipipe-board/regroup.py <board-dir> --apply    # git mv
```

Renaming a group letter is a THREE-part change and all three must land together: `git mv` the folder and files, keep the old id as a declared alias so existing citations resolve, then grep the repo for the old id and fix every hit.

### `check` · index-level only

```
· every group has an intro sentence            (line 1 always shows)
· every group has a lane block                 (src/lanes.py reports gaps)
· every id inside a figure resolves            (an unlinked token is dead text)
· the board canvas is not a copy of the index
```

Page-level and sentence-level checks belong to `haipipe-board/check.py`.

## 📂 Files

```
haipipe-board-index/
├── SKILL.md            this contract
├── CHANGELOG.md        version history
└── src/lanes.py        the per-group lane block, round-tripped
```

Reads and writes `board.md` only.
Never touches `board.html`, never touches a page file, never imports `haipipe-board/src/`.
A board's `## Pages` plus each page's `# ` line is the whole input, so the two skills ship on their own clocks.
