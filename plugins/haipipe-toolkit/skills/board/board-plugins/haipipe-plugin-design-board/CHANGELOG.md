# Changelog

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
