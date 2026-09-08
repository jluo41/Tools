## 0.9.2 · 260908
- Story id grammar is `Story<Letter>-<desk>-<idea-slug>` (JL 260908: "letter should be good", after "why this is just A? really silly"): the letter orders, the desk names the telling, the slug names the idea; `Story-A` is out, `Story01-…` stays rejected. New "🔤 The Story id" block; group-token updated; first instance `StoryA-misq-phytrait-discretion`.

## 0.9.1 · 260908 · Paper Story naming correction

- At the user's explicit request, renamed `haipipe-page-story` to
  `haipipe-paper-story`, displayed as Paper Story, and moved beside the other
  Paper journey contracts under `paper/workflow-phases/`.
- Updated installed entry points and active references. Page remains the
  underlying carrier (`page-type: story`), not the public skill name.
- Naming-only correction: the eight-division semantics and 0.9.1 draft
  version remain unchanged; no outline or v1 approval is implied.

## 0.9.1 · 260907 · draft repair; v1 remains unauthorized

- Withdrew the unauthorized 1.0.0 control-page rewrite; restored the prospective
  eight-division blueprint and the C6 Discovery / C7 Task / C8 Narrative roles.
- Separated propositions, research questions, work progress, and human approval;
  added adverse-evidence states, core/optional work, and eight Aim read-through tests.
- Kept interface details in ref/integration.md and aligned downstream routers.
- Added opt-in exact fixed-title checking so an eight-division operational
  layout cannot silently pass as the requested Story shape.
- Both this skill and new Story outlines remain v0.x. A test pass or edit
  request does not authorize either promotion; explicit user approval is required.

## 0.9.1 · 260907 · draft, not v1

- Renamed `haipipe-paper-story` → `haipipe-page-story` and moved to
  `paper/page-types/` (JL 260907: Page Types are named like every other
  `haipipe-page-<type>`, cf. `task/page-types/haipipe-page-insight`). Contract
  body unchanged from 0.9.0. Written by Claude Peer.
- The Story design and all generated outlines remain `v0.x`, `approved: ⬜`;
  the rename does not imply human approval or permit `v1.0` promotion.

## 0.9.0 · 260907 · draft, not v1

- Reframed Story as a prospective guide to the whole paper rather than a work
  manual or control center.
- Integrated the former three planning surfaces into eight Content divisions:
  C1–C5 are the Seed, C6 is Discovery Roadmap, C7 is Task Roadmap, and C8 is
  Section Narrative.
- Restored discovery gaps and expected syntheses; paper-level evidence
  obligations, designs, and interpretation branches; and the Narrative's
  venue decision, claim system, argument arc, reader journey, per-section
  narrative, evidence/display allocation, transitions, and compile order.
- Kept Evidence as the through-line from starting basis to Discovery, produced
  study evidence, and Section use. Demoted runs, receipts, laps, release states,
  and commands to optional traceability rather than Story structure.
- Recast CHECK as the whole-paper read-through test. This is a discussion draft
  only: outlines remain `v0.x`, `approved: ⬜`, and no `v1.0` promotion is
  implied.

## 0.8.1 · 260907
- "The flow inside one Story" block (JL 260907): Seed → Research Questions →
  Task (Task table + Discovery table on the roadmap child) → Narrative
  (Narrative table on the narrative child), with who owns which table.

## 0.8.0 · 260907

- Renamed `haipipe-paper-seed` → `haipipe-paper-story` (JL 260907: "we should
  have the haipipe-paper-story"). The journey phase is P1 Story; the page type
  is `story` (`seed` accepted as alias). New "🧭 What the Story page IS" block:
  the one address for one paper, holding the Seed (identity divisions), the RQ
  table, the E-board, and the handoff to its two child plans; it controls and
  never does. Content contract otherwise unchanged from 0.7.0.

## 0.7.0 · 260907

- The Seed lives ON the Story page `A1-Story/Story<NN>-<idea-slug>/` (JL
  260907: one Story = one idea); its roadmap and narrative children nest inside.
- Division 3 becomes the Research Question TABLE: RQ<n> · question · ⬜ open /
  🔨 exploring / ✅ answered · collect (roadmap block) · show (narrative
  section). New "❓ The Research Question table" law: an RQ asks, an E-row
  records; one E-row per RQ, the RQ id is an E-board column; the Seed alone
  flips states. Outline shape string updated. group-token "SD" → "Story<NN>".

## 0.6.1 · 260831
- Home renamed A1-Story/Story01-seed (SD/NA retired, JL 260831); group tree gains the narrative pages that close the group.

## 0.6.0 — 2026-08-31

- **Renamed and moved** (JL 260831: "replace page-types to be workflow-phases"):
  `paper/page-types/haipipe-page-for-seed/` is now `paper/workflow-phases/haipipe-paper-seed/`.
  The skill is one paper JOURNEY PHASE and still owns its `page-type:` key;
  a new `## 🧭 Journey phase` block places the phase and its gates, and the
  description carries the P-number. Contract body unchanged.

## 0.5.0 — 2026-08-24

- **The story group becomes the venue-free P0-P3 head** (JL 260824, journey
  0.5.0): SD02-roadmap and SD03-collection join beside the seed; narratives
  leave for A2-NA-narrative. The Seed is the establish loop's SCOREBOARD:
  Roadmap plans against §6's gaps, Collection proposes settles, and this page
  alone writes E-row flips, each citing the landed QA path.

## 0.4.4 — 2026-08-24

- **Ideation 0.5.0 vocabulary** (JL 260824): the origin page's exit cell is
  `went to` (was `graduated-to`); the birth-certificate clause and closing
  checks drop the ledger/nursery/graduation wording. Binding mechanics
  unchanged.

## 0.4.3 — 2026-08-24

- **Ideation-first story order** (JL 260824): the seed lives at SD01-seed;
  its birth certificate binds SD00-ideation beside it in the story group.

## 0.4.2 — 2026-08-24

- **Explore renamed IDEATION** (with ideation 0.3.0): §5's first row points at
  this board's `A0-ID-ideation/` group; "Ideation Page" and "Ideation ledger"
  throughout the birth-certificate clause and closing checks.

## 0.4.1 — 2026-08-23

- **The birth certificate becomes same-board by default**, following explore
  0.2.0 (JL 260823: the nursery lives at `paperboard/A0-EX-explore/`, before
  the seed): §5's first row normally binds the A0 group on this same board;
  cross-repo pagex survives only for an idea graduating out of ANOTHER
  paper's nursery.

## 0.4.0 — 2026-08-23

- **Every ✅/🔨 E-row carries a novelty reading**: closest prior work, the
  delta, HIGH/MEDIUM/LOW — judged per CLAIM, never for the paper as a blob
  (the ARIS idea-discovery lesson, Tools/references/aris), traced to
  discovery-layer QA files with id-verified citations; `[UNVERIFIED]` is
  honest, silence is not. Idea quality becomes a readable property of the
  board: how many rows can flip ✅ and what their deltas are worth.
- **The birth certificate**: §5's first row binds the Explore Page this paper
  graduated from (cross-repo pagex, the bank-page pattern) and the ledger's
  graduated-to points back; retrofit Seeds say so in the Log instead.
- **Runtime home renamed** to `paperboard/A1-SD-story/` under the 260823
  scaffold grammar; `0-SD-seed/` boards are grandfathered.

## 0.3.0 — 2026-08-21

- **Pitch returns, at division 2, as BLUF.** JL 260821: the pitch is the
  one-minute story told to others, placed "before the research question and
  after the identity", with placeholders when the answer is not yet known.
  This is NOT the venue-embedded pitch 0.2.0 moved to Narrative: that one is
  desk-shaped and stays there. This one is the GENERAL listener's telling and
  survives retargeting, which is the Seed's own membership test.
- **Placeholder discipline**: every pitch sentence selling a finding cites an
  ✅ E-row or carries `⟦pending E<n>⟧`. Day-1 aspirational, convergence
  visible: zero placeholders = the paper found its bottom line.
- **Old division 5 split on its lifetime seam**: the volatile Establishment
  Board (E<n> rows, ✅/🔨/⬜, unranked) separates from stable Boundaries, so a
  diff outside the moving divisions is identity drift by construction.
- **Source Pages named the PageX seedbed**: §5 rows the read scope, `pagex/`
  binds exactly what is rowed, §6 cites what §5 rows.
- Shape is now eight divisions: Identity → Pitch → RQ → Stakes → Source
  Pages → Establishment Board → Boundaries → Narrative Handoff.
- Frontmatter gains version, summary, and `group-token: SD` with the runtime
  address `0-SD-seed/SD00-seed/`.
- Same day, JL ruled the story group SHARED: Narratives live beside the Seed
  as `SD<NN>-narrative-<venue>` in `0-SD-seed/` (narrative 0.4.0), the MT-group
  shape applied to paper.

## 0.2.0 — 2026-08-19

- **Renamed `for-opening` to `for-seed`, and made VENUE-FREE by rule.** JL 260819:
  "maybe we can change it to Seed (which is venue free). And narrative, it is
  venue embedded, each of them should have it."
- The venue-aligned layer this contract already named (selected venue, audience,
  editor question, pitch, framing) moves to `haipipe-paper-narrative`, one per
  venue.
- The layers were already separated here, with retargeting told to "reread the
  first layer and rewrite the second". Making them two PAGES is what makes the
  stable half provably untouched: a page whose second half is rewritten per venue
  cannot also be the readable record of what the paper is about.
- A seed that names a venue is now a defect.

haipipe-paper-seed · Changelog
====================================

Historical notes retained from the former Opening contract. New development is
documented by the current Seed contract and repository history.

## 0.1.0 - 2026-08-17

- Added one Opening Page Type per paper.
- Opening owns paper identity, research question, source-page inventory, headline establishment and limit, venue position, editor promise, and the bounded handoff to Narrative.
- PageX reads existing Pages while Probe remains a parallel route to Task and Discovery folders; Opening owns no local Probe folder.
- Legacy Seed, Venue, and Pitch pages remain readable compatibility inputs until an explicit runtime migration.
