## 0.4.0 — 2026-08-24

- **The nursery joins the story group as page zero** (JL 260824: no separate
  A0 group; home A1-SD-story/SD00-ideation, token SD, the seed shifts to SD01;
  a second ideation page takes the next free SD number).

## 0.3.0 — 2026-08-24

- **Renamed: explore → IDEATION** (JL 260824: "我们不叫 exploration 了,我们改叫
  ideation 吧(想 idea 的过程),然后才是 seed"): the P0 act is thinking up
  ideas, and the name now says so. Page type `ideation`, group token `ID`,
  home `A0-ID-ideation/`, skill `haipipe-page-for-ideation`, door verb
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