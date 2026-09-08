## 0.9.0 · 2026-09-08

- Renamed `haipipe-page-ideation` to `haipipe-paper-ideation` and moved the
  contract from `paper/page-types/` to `paper/workflow-phases/` so P0 follows
  the same Paper-family naming law as Story, Section, and Round.
- Retained `page-type: ideation` and the shared `haipipe-page` lifecycle; the
  rename changes the semantic owner, not the Page Face or G0 authority.

## 0.8.1 · 2026-09-07

- Added explicit retrofit adapters for `i1` → `i01`, flat novelty claims,
  archived QA, and legacy Story paths without destructive renaming.
- Defined when existing regressions qualify as a retrospective Task-owned
  pilot and made clear that an unsupported `SKIPPED` line cannot pass G0.
- Unified G0 selection around human PROCEED or risk-accepted PROCEED WITH
  CAUTION plus the intended target/category.

## 0.8.0 · 2026-09-07

- Added one visible Journal / Venue Fit field per admitted Idea and a venue-fit
  plus target column to the comparison table.
- Extended G0 so a selected Idea needs complete deep fit, a current Venue
  contract, and a person's intended target/category in addition to novelty and
  feasibility.
- Kept target recommendation machine-authored and target selection human-owned;
  the Page consumes Fit/contract paths without copying desk rules.

## 0.7.4 · 260907

- Defined `iNN` assignment as Idea admission: admitted cards keep divisions,
  while rejected pre-admission framings may remain only in Eliminated Ideas.
- Made retrofit naming non-destructive: historical SD paths remain readable
  until a separately authorized migration, while canonical Story roles and
  two-way bindings are recorded on revision.

## 0.7.3 · 260907

- Renamed `haipipe-paper-ideation` → `haipipe-page-ideation` and moved to
  `paper/page-types/` (JL 260907: Page Types are named like every other
  `haipipe-page-<type>`). Contract body unchanged from 0.7.2. Written by Claude Peer.

## 0.7.2 · 260907

- Fixed the reader-facing shell as Opening → Outline → Content → Aims while
  keeping Outline and Content as the two primary working surfaces.
- Made the number of admitted ideas dynamic, defined ranked order as a
  comparison aid rather than automatic selection, and allowed zero, one, or
  several human-selected ideas with one distinct Story route each.
- Made Novelty Check explicit inside each Idea's Core Claims and aligned the
  handoff tree with the current one-Story control-center contract.
- Separated Page Shape approval and Page CHECK acceptance from the per-Idea G0
  PROCEED decision so an accepted evergreen page does not imply selection.

## 0.7.1 · 260907

- Route new semantic ideation and claim pressure-testing through sibling
  `haipipe-ideation`; retain the Discovery Idea name only for historical
  compatibility while Discovery Search remains the external evidence route.

## 0.6.2 · 260907
- Tree at the paper root, no `0-paperboard/`; the winning idea becomes
  `Story01-<idea-slug>/` with roadmap and narrative children; a second surviving
  idea is `Story02-<slug>` in the same board (the number counts ideas).
  Mint rule: repo starts with `board.md` + `A1-Story/Story00-ideation/`.
  group-token "SD" → "Story00".

## 0.6.1 · 260831
- Home renamed A1-Story/Story00-ideation (SD/NA retired, JL 260831); the tellings close the same group.

## 0.6.0 — 2026-08-31

- **Renamed and moved** (JL 260831: "replace page-types to be workflow-phases"):
  `paper/page-types/haipipe-page-for-ideation/` is now `paper/workflow-phases/haipipe-paper-ideation/`.
  The skill is one paper JOURNEY PHASE and still owns its `page-type:` key;
  a new `## 🧭 Journey phase` block places the phase and its gates, and the
  description carries the P-number. Contract body unchanged.

## 0.5.2 — 2026-08-24

- **Fork clause repaired** (pre-commit audit, JL 260824): the grain-and-home
  section still read "a second ideation page … takes the next free SD number",
  a rule journey 0.5.0 had silently broken by fixing the story group's four
  roles one each (SD00 ideation · SD01 seed · SD02 roadmap · SD03 collection).
  A second ideation page would both violate "one each" and sort a P0 page after
  the P3 page. Now: a board holds exactly ONE ideation page, and a direction
  that genuinely forks mints its own `Paper-<Slug>/` with its own SD00, the two
  linked through the originating row's `went to`. No other rule changed.

## 0.5.1 — 2026-08-24

- Home figure gains the story group's two new siblings — SD02-roadmap and
  SD03-collection per journey 0.5.0 — and notes the tellings live next door
  in A2-NA-narrative.

## 0.5.0 — 2026-08-24

- **The page adopts the source reports' own structure** (JL 260824: "尽量 map
  他们的 structure…永远不要创建一些'一眼 AI'的词"): coined vocabulary dropped —
  no more Idea Ledger / nursery / Graduations / batch intake. Divisions are
  now Direction · Ideas (ranked) · one `Idea <n>: <title>` division per idea
  carrying IDEA_REPORT.md's own fields (Method · Hypothesis · Minimum
  experiment · Expected outcome · Core Claims · Pilot result · Risk ·
  Reviewer's likely objection · Recommendation) · Eliminated Ideas (the
  report's table, rows permanent) · Suggested Execution Order. The summary
  table's exit column is `went to`; verdicts use the Novelty Report's own
  words (PROCEED / PROCEED WITH CAUTION / ABANDON, plus ⬜ open). The 0.4.1
  routing, grain adapters, and human-authority rules carry over unchanged.

## 0.4.1 — 2026-08-24

- **The outline shape hardens its intake interfaces** (JL 260824: "我们是想把
  novelty check 和 ideation 的内容存到这个 file 里面去"): every `i<n>` division
  carries three fixed bullets — claims · novelty · pilot — and the Ledger
  carries a batch-intake bullet naming each generate run's `ideas.md` + QA.
  The 📮 routing is written into the shape itself: novelty →
  `/haipipe-discovery-idea` novelty_check QA, pilot → task-layer QA, batches →
  `/haipipe-discovery-idea` generate. The ARIS `idea-creator` and
  `novelty-check` skills stay methodology references — their output enters the
  page only as discovery-/task-layer QA files, never by direct write. A
  retrofit single-idea ledger may nest `i1` as a Ledger sub-division
  (`#### 2.1`); the three-bullet law applies inside it. Two grain adapters
  close the audit's vocabulary gap: per-claim novelty = one commissioned
  question per claim (one QA file each), and the executor's verdict vocabulary
  maps `novel → HIGH · partial → MEDIUM · preempted → LOW · inconclusive →
  ⬜/[UNVERIFIED]`, the cell summarizing the worst claim.

## 0.4.0 — 2026-08-24

- **The nursery joins the story group as page zero** (JL 260824: no separate
  A0 group; home A1-SD-story/SD00-ideation, token SD, the seed shifts to SD01;
  a second ideation page takes the next free SD number).

## 0.3.0 — 2026-08-24

- **Renamed: explore → IDEATION** (JL 260824: "我们不叫 exploration 了,我们改叫
  ideation 吧(想 idea 的过程),然后才是 seed"): the P0 act is thinking up
  ideas, and the name now says so. Page type `ideation`, group token `ID`,
  home `A0-ID-ideation/`, skill `haipipe-paper-ideation`, door verb
  `/haipipe-paper ideate`. Contract content unchanged; the engine whitelist
  swaps `explore` for `ideation` with no shipped page on the old key.

## 0.2.0 — 2026-08-23

- **The nursery moves into the paper's own board** (JL 260823: "应该放到对应的
  那个 paper board 里面去,在 seed 之前"): home is now
  `Paper-<Slug>/paperboard/A0-EX-explore/`, ordered before `A1-SD-story/`; the
  standing `<Program>-IdeaBoard/` of 0.1.0 is retired unshipped. Same locality
  law that puts an InsightBoard inside its application.
- **The repo precedes the Seed**: minting a paper's first Explore Page creates
  `Paper-<Slug>/` as a submodule with only the A0 group inside; a dead
  direction leaves the repo standing as its own graveyard.
- Graduation is normally same-board (`graduated-to: SD00 (here)`); an idea
  leaving for a different paper names that repo instead, and the cross-repo
  binding survives for that case only.

## 0.1.0 — 2026-08-23

- **Created as the P0 nursery contract** (JL 260823): one research direction
  per page on a standing IdeaBoard; idea ledger with claim-level novelty,
  pilot receipts, and the fixed verdict vocabulary; graduation gate to a Seed
  with two-way binding; ABANDONED rows never deleted. Methodology informed by
  the ARIS idea-discovery/novelty-check references (Tools/references/aris):
  claim-level novelty, independent-context verdicts, verified citations,
  budgeted pilots. Group token EX; the page executes nothing — discovery and
  task layers hold the receipts.
