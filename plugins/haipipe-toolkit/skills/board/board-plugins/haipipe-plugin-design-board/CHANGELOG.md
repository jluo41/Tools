# Changelog

## 0.7.1 — 2026-09-20

- Align current guidance with Verify-passed `ready` items and Delivery as a
  projection; CSV exports only eligible ready drafts. Commission, Generate,
  and Verify are the workflow's Run types.
- Revalidate the exact reviewed candidate and its independent Verify before
  projecting Delivery. Changed artifacts, checks, results, frozen config, or
  render evidence make the records invalid and remove the item from ready/CSV.
- Preserve historical `rdNN_adopt_*` IDs in text, links, and tooltips; label
  their recorded type `Adopt (historical)` and distinguish queue actions.
- Document `new-folder.row` as the parsed Brief row key (`R3`, for example),
  separate from the human-readable task title and an integer row position.
- Fresh-context validation found sparse Boards could omit the promised
  presentation entry. `new-folder` now creates `## Pages` when missing and
  preserves existing groups/sections; repeat requests still create no duplicate.

  Ready/Delivery and historical-ID runtime changes were coordinated with
  the Design family repair; this patch aligns the Board plugin contract.

## 0.7.0 — 2026-09-18

- A retired record parks under the board's `_archive/` instead of being
  migrated or deleted: the checker judges no `_` folder, so `2-DS-design/DS*`
  keeps its bytes for the Log to cite while the board claims only its live
  design tasks (B00's DS01, JL 260918).

- Tasks show by their full name, `<job> <venue> for <who>`; the Brief's row
  id (`R1`) is a key in the file and never a name on screen, refusals
  included (JL 260918).
- The task list is the first Brief table whose header names `audience`,
  `job` and `venue` together, so an audience table elsewhere is never read as
  the list. A Brief with no `line` column numbers its rows R1, R2 … in order,
  and `new-folder` writes the folder cell on that same row, so a second click
  is refused instead of opening a duplicate folder.
- `new-folder` writes a page that passes the board checker: `state: 🔴 OPEN ·
  no design registered yet`, `owner:` (the board's, else the Brief's), an
  Opening question, and an entry in board.md `## Pages` under its Design
  heading.
- The csv gains a `state` column and lists the adopted draft, else the
  latest draft that passed the records check; a failed draft is never listed.
  The send system takes the rows whose state is `adopted`; declined rows stay
  in with state `declined`.
- Insight Space groups "used by" per folder (`Design-01 · 6 items`, linked to
  that folder's Insight Space), adds a table of the other pages the designs
  use (not signed insights), and shows a red line when no design rests on a
  signed insight. The Insight board picker offers only boards that resolve,
  by folder name. Design Space shows each item's design text under its title.
- The header is one line; a bare `/_board/design-board` with several boards
  answers 200 with the list; an ambiguous Page-level `?folder=` answers 404
  with a page listing each board that holds it, never a guess.
- The board checker knows `board-kind: design-board` and `insight-board`,
  accepts a `reads:` entry that is a `../` path staying inside the checkout,
  and audits folders holding only Commission and Adopt runs.
- Docs: the board-kind and board-name rules, the csv columns, the gallery and
  the declined fold are now in the SKILL body; the examples match the demo
  (10 wanted · 10 registered · 1 adopted).

## 0.6.0 — 2026-09-18

- Delivery Space shows a folder of screens as a picture gallery (the Page
  level's rendered pictures); text designs keep the table. The csv gains a
  `render` column naming each screen's picture.
- A Project folder can be the server root: boards under its `applications/`
  are found, and `reads:` may name an Insight board in another Project by a
  path relative to the board's parent (first use: `Project-Application-
  AuthenUIDesign` reading `Project-Application-SMSDesign`'s A00).

## 0.5.3 — 2026-09-17

- New Design Folders are titled `<job> <venue> for <who>` (`design_title`),
  the same plain phrase the Page level shows.

## 0.5.2 — 2026-09-17

- Delivery Space is a quick list of every design, one table per folder:
  item (id · title) and the design text; no adoption status. The csv
  download became **Download all designs**, one row per design.

## 0.5.1 — 2026-09-17

- Delivery Space lists every design: **Adopted** cards, then **Not adopted
  yet** cards with the latest draft text, state, and waiting-on.
- New folders are named from the first three content words of each Brief
  cell, filler dropped (`Design-03-young-male-age-prescription-review-sms`).

## 0.5.0 — 2026-09-17

- Delivery Space: **Download the bundle**, `GET /_board/design-bundle`, one
  csv row per adopted draft with its Brief line, text, hash, verifier, and
  adopter.
- Insight Space shows the DO / DO NOT rules each signed page implies.

## 0.4.0 — 2026-09-16

- Five Spaces at board grain, Goal · Design · Insight · Run · Delivery. Goal
  Space is the list of design tasks from the Brief (who · their job · venue ·
  how many wanted/registered/adopted · insight board · folder · status) with
  the **New design tasks** form: subgroups one per line, their job, venue,
  how many each, which Insight board, open folders now. Insight Space lists
  every signed page the programme draws on and which folder · item uses it.
- Second write `add-tasks`: one Brief line per subgroup (adds the `designs`,
  `insight`, `folder` columns or the whole section when missing), then a
  Design Folder per line. Refusals write nothing.
- Full names (JL): the group is `2-Design/`, folders are `Design-NN-…`;
  `DS` is gone from disk, code, tests, and docs.

## 0.3.0 — 2026-09-16

- Plain words: "From the Brief" with `line · who · their job · venue · wanted ·
  folder · status` (never roster); signed insights; draft; records check.
  Snapshot keys `brief_rows` / `unlisted`; `new_folder` returns
  `brief_updated`. The Page level now has Goal and Insight Spaces; the Board
  keeps Design · Run · Delivery at board grain.

## 0.2.0 — 2026-09-16

- Follows the Page level's plain words: `Design Space` (query `space=design`),
  `ITEM01…` ids, register field `goal:`. The Brief's spine left the header.

## 0.1.0 — 2026-09-16

- First Board-level grain of the Design plugin (`live/designboard.py`,
  route `/_board/design-board`, static `board/design.html`): the Brief's
  roster against the folders on disk, every Design Item across folders with
  its state and waiting-on, the cross-folder queue (person first), every Run
  newest first, every adopted version, and the Design Unit gate result across
  folders. Same three Space names as the Page level, one grain up; every row
  links down to the Page-level card.
- One write: `new-folder` opens a Design Folder for a roster row that has
  none and names it on that row.
