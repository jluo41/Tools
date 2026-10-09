# Changelog

## 0.2.1 · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## 0.2.0 · 2026-10-04

- Jobs (JL 261004: "we should have the job, otherwise the work is hard to do"): a Block
  keeps `board.md`, `studio/`, `reports/`, `_old/` at its top; everything else lives in
  `jNN_<job>/`, one line of work each (one request to one office, one change, one stage).
- The job page `jNN_<job>/jNN_<job>.md` holds the Job's state in its header (`job-kind:
  cowork-job`, state, waiting-on, since, next, ticket, url); `Timeline.md` and
  `CHECKLIST.md` sit beside it, and `design/`, `materials/`, `emails/`, `meetings/` only
  when the Job has them. The board.md Tickets register is gone. `ref/job-page-template.md`.
- People are a Job too (JL: "who to ask for help"): `j00_people/`, state 📇 REFERENCE.
- No `tNN` level: a Job's items are single files.

## 0.1.0 · 2026-10-04

- New skill (JL 261004: "make the block as well"): a CoWork Block is one coordination
  topic, `cowork/bNN_<topic>/` with `board.md` (`board-kind: cowork-block`). Ranges
  `b0x` gates, `b1x` systems, `b2x` partners, `b3x` study operations.
- `board.md` header (state, owner, spine, close, status, waits-for, onedrive), then the
  text, then the `## Tickets` and `## Questions` registers; `ref/block-board-template.md`.
- The shared folders are the Block's Jobs (people, design, materials, ticket, emails,
  meetings, studio, reports, and the OneDrive folders named in the header); no jNN/tNN
  inside cowork. Steps and drafts live in `ticket/CHECKLIST.md`.
- First applied to Project-Samsung: b01_irb, b11_azure_account, b12_epic_streaming,
  b13_smartwatch_connector, b21_welldoc_app; the root `Tickets/` moved into the Blocks.
