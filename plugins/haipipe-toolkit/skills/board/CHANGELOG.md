board — Changelog
=================

Family-level changes. Skill implementation history remains in
`haipipe-board/CHANGELOG.md`; agent history remains in `agents/CHANGELOG.md`.

## [0.3.0] — 2026-07-26

- Compressed the direct Board closing block from ten fenced lines to three
  Markdown lines while retaining Board, queue/focus, status/mode, next action,
  and a clickable deep link.

## [0.2.1] — 2026-07-26

- Defined direct-versus-composed Closing Block precedence so a Paper session
  carries one block with a deep Board link rather than two competing tails.
- Corrected the checker boundary: checkbox/state alignment belongs to Q
  rulings; an S page's emoji is its independent lifecycle gate.

## [0.2.0] — 2026-07-26

- Added a visible session-attachment contract: every Board-attached reply ends
  with a deterministic strip showing Board, queue, focus, mode, next action,
  deep link, and file.
- Kept live status in each session transcript rather than a shared status file;
  durable outcomes continue to sync into Board pages.

## [0.1.1] — 2026-07-26

- Unified the Board family on one state contract: the first emoji is the four-value machine status and optional following text is human-readable detail.
- Aligned the mechanical checker with runtime Board routes and the renderer's normalized state token.

## [0.1.0] — 2026-07-26

- Promoted Board from `skills/0_utils/haipipe-board/` to the first-class
  `skills/board/haipipe-board/` family beside paper, probe, and task.
- Kept the design Board at `skills/diagrams/01-boardform-260722/`.
- Added the family-level, read-only `haipipe-board-reviewer-agent`.
