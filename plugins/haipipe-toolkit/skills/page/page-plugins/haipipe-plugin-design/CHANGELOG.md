# Changelog

## 0.9.0 — 2026-09-17

- Batch buttons above the cards: Release all · Queue all · Adopt all
  verified, each shown only when it has work; one name and sentence for the
  batch, one decision Run per item.
- Goal Space: "Ask the agent to draft the missing N" writes a draft request
  (goal, insights with FINDING / CONSEQUENCE / DO / DO NOT, count); the open
  request is shown until the register is filled.
- Insight Space lists the rules each insight implies (its DO / DO NOT lines);
  `counsel_rules` turns every DO NOT into an acceptance rule.
- `mode` left the card; `cli/design_queue.py` lists and runs the agent queue
  from a terminal (`claude -p`), closing each run with the records check.
- Old `2-DS-design/DS01-…` links redirect to the full-name folders.
- `release_worker`: a dead worker's run goes back to planned with the lost
  worker named on the receipt; the runner stops on the first dead worker.

## 0.8.1 — 2026-09-16

- Full names: Design Folders live at `2-Design/Design-NN-<audience>-<job>-<venue>/`
  (never `DS`). Goal Space reads an optional `insight` column on the Brief
  line, the Insight board that task draws from; empty means the board's
  `reads:`. A named board that is not found shows in red.

## 0.8.0 — 2026-09-16

- Five Spaces in time order (JL): `Goal Space` (the Brief line that names
  the folder: venue · who · their job · how many designs wanted/registered/
  adopted · the Insight board), `Design Space` (the cards), `Insight Space`
  (per item, the supporting insights: signed by whom, what they say from the
  handoff's FINDING/CONSEQUENCE, pinned or not, "needs an insight", and the
  board's signed pages no item uses), `Run Space`, `Delivery Space`.
- Plain words on the surface: the Brief and its lines (never roster), signed
  insight (never handoff), run record (never Ticket), draft (never
  candidate), records check (never check_unit). The card's long evidence row
  became a one-line `insight` pointer.
- The Brief table gained a `designs` column (how many the line asks for).

## 0.7.0 — 2026-09-16

- Plain words (JL): the first Space is `Design Space` (query `space=design`;
  `intent` still resolves), Design Item ids are `ITEM01…` (DI read as
  Data→Information next to the Insight plugin), and the register field
  `intent:` is `goal:`. Run slugs follow (`rd02_generate_item01`).
- Header cut to one line, `Page level · <folder>` with a link up to the Board
  level; the source, register, signal, and waiting lines are gone. A red line
  appears only for a legacy folder or an unsigned handoff.
- Card rows: `goal` (the sentence), `why` in plain words (follows the
  evidence · built on evidence · written fresh, contract words in
  parentheses), `evidence`, `predict`, `rules`, `runs`.

## 0.6.0 — 2026-09-16

- Made the Design Item the row of the tab: a register at
  `outline/<stem>-design-items.md` (intent only) and `item:` on every Ticket;
  state is derived by folding the item's Runs, with an explicit "waiting on"
  (agent or the named person) beside it.
- Reduced the surface to three Spaces: Intent (register), Run (per-item
  timeline with who/when/outcome/next, folded checks and candidate text,
  live `check_unit` audit), Delivery (one card per adopted item pinned to the
  exact candidate hash and the adopter's words). Signal moved to a header line.
- The presenter now reads the v2 contract files (`runtime.yaml`,
  `checks.yaml`, `result.yaml` artifacts, `decision.yaml`, config
  `design_intent`/`criteria`) instead of guessing from file names; removed the
  `adopt|accept` filename heuristic, the counters, the static Flow Table, and
  the Anchor/Shape/Trial/Commit vocabulary.
- Design Space became one card per item that shows the design text, the bet
  (intent · stance · basis · mode), the evidence rows with signature and
  Ticket pin, the prediction (expected · falsified if), the acceptance rules,
  and the Runs; the register grew `stance`, `basis`, `mode`, `expected`,
  `falsified`, and `evidence` lines.
- Added the actions: `POST /_board/design-act` (`live/design_actions.py`)
  writes Commission release/hold and Adopt adopt/decline/revise/hold as the
  person's decision Runs, queues planned Generate/Verify/revise Tickets for
  the agent, and appends a new item to the register; the button an item shows
  is the one its state licenses.
- Added `design_actions.complete_run`: the caller-side close of a worker Run
  that gates the returned Result with `check_unit` and writes the receipt
  truthfully (`complete` + next route, or `failed` with the gate's words);
  a review that fails the gate shows as `verify invalid · agent · verify`.
  `queue_verify` now carries the item's evidence inputs, so an
  evidence-informed Verify Ticket passes the gate.
- Added `tests/fixture_design_v2.py`, which builds contract-valid Design
  Folders (and the one-page InsightBoard they read) for the tests and
  regenerates the demo boards.

## 0.5.1 — 2026-09-16

- Reworked the Design presenter to use the Outline plugin's shared reader
  presentation: compact Space tabs, quiet page chrome, lightweight cards, and
  source-first tables.
- Kept Design's own four Space meanings and transformation Flow unchanged.

## 0.5.0 — 2026-09-16

- Made the designed artifact directly inspectable in Run Space → Shape and
  Delivery Space instead of exposing only file paths.
- Kept candidate display, verification receipt, source artifact, and commit
  status visibly separate.

## 0.4.0 — 2026-09-16

- Restored fixed `Run Space` and `Delivery Space` names required by the Page
  plugin vocabulary.
- Renamed the two Design-specific spaces to `Design Space` and `Signal Space`.
- Kept the Design-native `Anchor → Signal → Shape → Trial → Commit` Flow Table
  inside Run Space.

## 0.3.0 — 2026-09-16

- Replaced the borrowed Draft/Evidence/Run/Delivery vocabulary with the
  Design-native Frame, Signal, Shape, and Launch spaces.
- Replaced the Space matrix with a transformation-oriented Design Flow
  Table: Anchor → Signal → Shape → Trial → Commit.
- Added a distinct console visual language and kept old `space`/`run` query
  values as compatibility aliases while new links use `space`/`flow`.

## 0.2.0 — 2026-09-16

- Reframed the Page-level surface as Draft Space, Evidence Space, Run Space,
  and Delivery Workspace, matching the Page workflow presentation pattern.
- Added a read-only Run Space Workflow map with Design Run Specs as rows and
  the four Spaces as columns.
- Connected Evidence Space to the owning DesignBoard `reads:` allowlist and
  person-signed InsightBoard Wisdom Handoffs; unsigned or undeclared sources
  remain blocked.

## 0.1.0 — 2026-09-16

- Added the first page-folder-level Design category plugin contract.
- Defined Plan, Create, Review, Run, and Delivery as internal read-only workspaces.
- Kept Design Folder, Run, Result, adoption, and Page CHECK authority with their owning contracts.
