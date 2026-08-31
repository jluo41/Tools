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