haipipe-board-index · Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.2.1 - 2026-08-02

- The boundary line sending one-page-section work elsewhere named `QAa` and said
  it "will move to `haipipe-board-page`". That skill shipped, and the QAa face
  group was folded into QB4 and archived on 260801, so the pointer named a page
  that no longer exists and a move that already happened.

## 0.2.0 - 2026-08-01

- Aligns the Index contract with the canonical generated `board/` site rather than the retired `board.html` packaging.
- Replaces the stale B0-B9 monolith anatomy with the generated Index that actually ships: Heading, Spine, Board Map, optional Related Folders, Section Matrix, All Pages, and Activity.
- Makes Topic, Pipeline, and Board Structure explicitly source-only documentation. Board Structure now records Board-Folder versus the Index, group, and page routes under Board-Webpage.

## 0.1.0 - 2026-07-30

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
