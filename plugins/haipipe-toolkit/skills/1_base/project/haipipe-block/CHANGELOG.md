haipipe-block · Changelog
=========================

**[2.1.0] · 2026-10-12 · Named after its level**

Renamed from haipipe-board to haipipe-block, so the three level skills read haipipe-block,
haipipe-job and haipipe-task (JL 261012: "yes, rename haipipe-board to haipipe-block"; b10 Q05).
`aliases: [haipipe-board]` keeps `/haipipe-board` and its link working. Every mention in Tools and
WellDoc moved with it, and haipipe-board-reviewer-agent is now haipipe-block-reviewer-agent. Left as
they were: the face file `board.md` (a later, separate step), the `.haipipe-board/` state folder,
`HAIPIPE_BOARD_URL`, older names already renamed to something else, closed passes, chat
transcripts and run receipts.

**[2.0.2] · 2026-10-10 · Studio topic count**

Recommend at most 10 sNN topics per Block; preserve existing ids and files.

## [2.0.1] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [2.0.0] · 2026-10-07 · The Block level (b03 s21)

- The name returns for the Block level (JL 261007: "I think we should have the haipipe-block,
  and haipipe-job, and also haipipe-studio and haipipe-report, and haipipe-run"). The skill of
  that name deleted on 261005 (1.1.8) built the static `board/` site, which stays retired; this
  one owns the Block's face and its level of the frame, so its major version moves on.
- `ref/board-contract.md`: where a Block sits; the face `board.md` (title line, board-kind,
  spine, close, optional workbench:, Topic, the optional registers); the six Spaces at Block
  level and the buttons this skill owns (Update the description, Add a Job, Build the
  delivery, the last an open point); which theme reads a Block (Theme.claims, then the Theme
  folder, then vanilla).
- `scripts/new_board.py`: new, the new-Block scaffold (next free bNN, the folder's default
  board-kind, face only).
