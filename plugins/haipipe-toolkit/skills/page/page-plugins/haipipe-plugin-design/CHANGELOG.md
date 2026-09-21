# Changelog

## 0.11.1 — 2026-09-20

- Align current docs with Commission → Generate → independent Verify and ready
  Delivery. Runs are recorded work; Delivery is a projection and internal Steps
  do not add Run identities. Historical Adopt rows keep their original ids.
- Distinguish a human `commission held` decision from a `blocked` worker Run;
  show the blocked Run and repair owner without Commission controls.
- Read optional hash-bound render evidence from the candidate's own Result.
  Existing Delivery manifests remain a fallback only when no Result manifest
  exists; an invalid current manifest never falls back to an older picture.
- Clarify held/released Commission counts, valid completed-review retry limits,
  and the allowed operation-specific fields derived from released config.
- Revalidate the exact Generate and independent Verify Results before Delivery.
  Changed artifacts, checks, config or render pins display `records invalid`
  and are excluded from ready totals and CSV exports.

## 0.11.0 — 2026-09-18

- Delivery handoff now follows a passed independent Verify directly. The live
  surface no longer creates or shows an Adopt action, state, counter, or batch
  button; Goal and Board count `ready` items, and Delivery lists only ready
  candidates. Historical `rdNN_adopt_*` bytes remain readable as legacy
  records but are never created by the current writer.

- A legacy folder parked under the board's `_archive/` no longer holds its
  old links at 410: the file it names is gone, so the link heals to the
  `Design-NN` folder that replaced it (B00's DS01 link now opens Design-01).

- The card rewrite (JL 260918). Each item is one fixed-height row (46px):
  id, title, the design in one line (a screen previews its goal), state, and
  who is waited on; on a phone the preview hides. A row opens into a
  fixed-height card (560px) that scrolls inside; `open all · close all` sits
  above the list. The design sits on the left and stays in view while the
  explanation scrolls; the decision form and buttons sit under the design, so
  they are never below the fold. The explanation is a bordered two-column
  table: Why this design, From insight to design, The bet, Rules, Steps.
- From insight to design is a flow of the item's pages by rung, Data →
  Information → Knowledge → Wisdom → This design, with an Also read rung for
  a source that is not an insight page and `· avoid` on a page the register
  avoids. Each insight page shows as its label and title (`full-D02`, never
  the file id `FD02`), linked to the Insight view only when the page is under
  the server root. The one-line insight pointer of 0.8.0 is gone.
- Rules are marked by the Verify of the draft the card shows, else by that
  draft's self-check, else "not checked yet"; a hand-written config shows its
  own criteria in words. The card warns when the register changed after
  release. Steps mark a run that failed the records check with `✗` and skip
  superseded runs.
- A card shows the adopted draft, else the latest draft that passed the
  records check; a failed draft is never shown, in Design Space, Delivery
  Space, or the csv.
- Waiting on "agent" only while a run is queued or running; otherwise the
  person, with the step (queue the draft, queue the review, queue again, …).
  New states `commission open`, `adoption open`, and `queued run out of date`
  (a queued run whose pinned file changed), with the button "Queue again with
  today's insight files": the old run becomes `superseded` with its reason.
- Every state that waits on a click shows its button (a held Commission gets
  its Release form back, a held Adopt its Adopt form, `verify invalid` its
  Queue Verify); the page refuses any other action, naming the state and who
  is waited on. One Commission per item. A draft that passed its review is
  revised only through a person's Revise decision.
- Generate and Verify copy the released Commission's config and evidence, so
  a later register edit never reaches this item's drafts. The config's `goal`
  is the goal sentence.
- Rule compiling: not, does not, doesn't, don't count as negative; `ends
  with 'X'` and `starts with 'X'` are their own checks; "under N characters"
  allows N − 1; every quoted phrase of a rule is compiled; apostrophes inside
  words are never quotes.
- Routing: a draft that fails the records check goes back to Generate, a
  review that fails it goes back to Verify, a fail verdict goes to a revise.
- Run Space: a revise reads `Generate · revise of rdNN` with its feedback;
  checks name their rule in words; a fail verdict is red with its checks
  open; a superseded run is grey with its reason.
- Insight Space: pages by label and title; "what it says" never shows an
  opening question; "Available, unused: none …" when every signed insight is
  used; `?item=` says "showing ITEM02 only · show every item".
- `?item=` opens and marks the card and scrolls to it; every item button lands
  back on Design Space at the item.
- The Adopt preview is one copy per draft, versioned per item, with the
  draft's own suffix, for all four decisions.
- Short links: an ambiguous `?folder=` answers with a page listing each board
  that holds it (404), never a guess; `Design-1` reads as `Design-01`.
- Legacy `2-DS-design/DS*` folders are refused with 410; an old DS link is
  rewritten only when the file it names is gone.
- The New Design Item form uses plain labels (approach, built on, expected,
  wrong if, insights, rules); stance `generate` reads "a new design".
- Docs: the register and card examples judge design quality (no arm, winner,
  or re-fielding); the contract word no longer follows a plain word in
  parentheses; the demo rebuild refuses without `--force`.

## 0.10.0 — 2026-09-18

- Screens read as pictures (JL: "design the UI for the whole population"):
  `delivery/render/manifest.json` names the rendered picture of a draft;
  the Design Space card shows it beside the facts (`the HTML behind this
  screen` folds the source), and Delivery Space shows every screen as a
  gallery. `_render_for` matches the picture to the exact draft shown.
- `compile_criteria`: a rule "judged on the render" is a `visual` check.
- A declined item is retired from the Delivery overview and folded under
  `Declined, kept for the record · N` (Page and Board level).
- First real use: `B01_DesignBoard-AuthenUI-260917`, six screens for all
  patients, measured at 390 x 844 in headless Chrome.

## 0.9.5 — 2026-09-17

- An old link is only rewritten to a current folder name when that folder
  exists. A legacy folder (`2-DS-design/DS01-…`, `design/DU*`) is now read as
  given and served 410 with "legacy design/DU* storage is not a current
  Design Folder", instead of a bare 404 from the rewritten path.

## 0.9.4 — 2026-09-17

- Titles read as one plain phrase (JL: "the name here is not good"):
  `design_title(row)` gives `<job> <venue> for <who>`, e.g. `Prescription
  review SMS for all patients`; Goal Space says `10 prescription review SMS
  designs for all patients`. The demo Brief's audience became `all patients`,
  so the folder is `Design-01-all-patients-prescription-review-sms`.

## 0.9.3 — 2026-09-17

- Delivery Space is a quick overview of what we designed (JL: "it is not
  about what to adopt"): one table, one row per item, item (id · title) and
  the design text. The Adopted / Not adopted yet groups, hashes, verifier,
  preview, and adopt words left the Space; they remain in Design Space and
  Run Space. `shown_design(item)` picks the adopted draft, else the latest.

## 0.9.2 — 2026-09-17

- Delivery Space lists every item (JL): **Adopted** cards first, then **Not
  adopted yet** cards with the latest draft text, state, waiting on, and a
  link to decide in Design Space; they say "not adopted, so not delivered".
- Folder names say the goal: the first three content words of the Brief's
  audience, job, and venue, filler dropped. The demo folders became
  `Design-01-all-patients-prescription-review-sms` and
  `Design-02-patients-refill-due-refill-review-ui-card`, titled from their
  Brief line. `renamed_folder` sends an old link or `?folder=` to the folder
  with the same `Design-NN` number.

## 0.9.1 — 2026-09-17

- Decision forms are folded by default (JL): each item's name + words +
  buttons sit under one line (`Adopt, decline, revise, or hold`, `Release or
  hold the commission`, `Queue a revise, with feedback`), open for the item
  selected with `?item=`. The batch bar folds the same way (`For all items at
  once: …`). A single agent-queue button stays in view.

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
