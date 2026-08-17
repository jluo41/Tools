# Changelog · haipipe-page-workflow

## 0.4.0 — 2026-08-17

Expands the auditable route grammar to OUTLINE→DRAFT→PROBE→EVIDENCE→REVISE→
COMPILE→CHECK and aligns receipts, builders, and the legacy PROBE alias.

## 0.3.0 — 2026-08-17

**§🃏 settles where an evidence card is born**, which three member skills had
been answering three different ways (`haipipe-page-draft` said DRAFT,
`haipipe-page-evidence` said "already PROPOSED by DRAFT",
`haipipe-plugin-outline` said PROBE). One rule now, and it reads down the loop:
the MARK at OUTLINE, the AIM at DRAFT, the CARD at PROBE, the ANSWER at
EVIDENCE, the SENTENCE at REVISE.

- The display unit is the one exception and it goes LATER, not earlier: EVIDENCE
  creates it, because declaring a unit nothing can fill yet is how a page shipped
  "1 display declared · 0 unit folders on disk".
- The member table's PROBE row points at `../haipipe-page-probe`, which now
  exists, instead of borrowing `../haipipe-page-evidence` "until split out".

## 0.2.0 — 2026-08-16

The loop is DERC, and it ends at a deliverable (JL 260816).

- `PROBE` became `EVIDENCE`; the member list, the loop figure, and the routing
  tables were rewritten. `PROBE` still parses as a phase and route token.
- The four members now read as one arc rather than four authorities:
  DRAFT plans and owes an outline, EVIDENCE lands every promised claim's card,
  REVISE renders and rebuilds latex + word, CHECK judges what was built.
- `ref/page-run-contract.md` carries the alias rule beside its transition table.

## 0.1.1 · 2026-08-16

- The receipt section now names its shipped reader: the 🪜 Workflow menu's
  `📄 Page phases` stepper (`65-plugin-pageflow.js` + `GET /_board/pageruns`),
  read-only, fed by `_runs/page/` and nothing else.

## 0.1.0 · 2026-08-15

- Born by MOVING, not adding: `haipipe-page`'s RUN verb and its
  `ref/page-run-contract.md` relocated here, so the page workflow has one
  nameable head skill beside its four member contracts, matching the
  one-folder-one-workflow shape `page-workflows/` now names (JL 260815,
  ruled in the Page-Workflow session).
- `haipipe-page` keeps CREATE and WORK ON and points here for RUN; two doors
  to one loop is the drift this move exists to prevent.
- The run contract's relative paths gained one `../` for the deeper folder;
  its content is otherwise untouched.
