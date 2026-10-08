## 0.19.0 · 2026-10-07 · A telling on the ladder; Narrative and the audience review (b16 Q04, Q05)

- The Story is not a Page on the ladder: a new section says where each part lives and is written. §1 · §2 · §4 and the drawings in the telling's studio topic (`studio/sNN-story-<desk>-<idea>/`), §3 as Board Questions with `reports/qNN_`, §5–§7 in the topic face and each report's Work, §8 and the compile order in each version face's `## Narrative`, related papers in `related/related.md`. An older Board's Story Page is still read; `carry_over/topics_paper.py` moves it.
- The telling's id is `sNN-story-<desk>-<idea-slug>`; `Story<Letter>-…` is read on older Boards.
- Drawings are studio topics, each with its `build_*.py`, shown in the Idea Studio; a person's marks survive a rebuild. The example that named one project's Board is generalized.
- New `ref/narrative.md`: the Board's Narrative view, N1 says · N2 drawn · N3 told · N4 attracts (JL 261007), and the audience review `run-review-audience-<who>` (editor · reviewer · public), done by a reviewer that wrote none of the telling.
- `ref/integration.md`: §8 and the compile order are the version face's; the example ids are `tNN_`.

## 0.18.0 · 2026-10-02 · The P-board says why we keep a paper

- Two optional P-board columns: `keep` (why this study keeps the paper, shown on the card as "Why we keep it") and `bears on` (this study's questions with one verdict each: supports, limits, contradicts, method, frames). JL 261002: "make the related works be something we should keep … add a table like its High Logic and Low Work".
- The paper's own logic and work lives in its Paper Run's `logic-work.yaml` (haipipe-discovery 0.21.0), not in the Story, so every Story citing the Run reads the same account.

## 0.17.0 · 2026-09-30 · Story parts are §N; C-numbers are claims; draw mode

- A Story part is written `§N` or by its name (§7, the Task Roadmap), as the Story file's own headings are, never `C1`-`C8`; `C1`, `C2` … are claim ids only, and `C1.P1.B1` stays the Page's Bullet address (JL 260930, "go ahead and update them accordingly", on aligning the paper skills with the Paper Workbench, which shows Question N, Hypothesis 1a and Claim 1a). Swept through this skill, `ref/integration.md` and the other paper skills.
- **Evidence obligations** in §7 is now **Evidence needs**, and the Story CHECK reads the Story "not as a record of finished work" (AGENTS rule 9 bans both old words).
- New section: Drawings of the Story. A drawing in `studio/` is written by its own `studio/make_<name>.py`, which reads the Story when it runs; **draw** mode reruns those scripts (the `Redraw` card on Story › RoadMap Draw). The first is Paper-ScalingGlucose-NatSeries2026's `studio/make_paper_workflow.py`.
- The description names what the Workbench shows (research questions, hypotheses, claims, related papers, RoadMap Draw) so those words reach this skill.

## 0.16.0 · 2026-09-30 · Question 0 states the tasks

- §3 may open with `#### 3.0 · Question 0 · RQ0`, a question that sets the pretraining task and the downstream tasks instead of testing a guess, with a **Tasks** group (`- Pretraining · Name: sentence`, `- Downstream · Name: sentence`) and `- none: …` in its other groups (JL 260930: "what is the pretraining task, and also the downstream task, we haven't specified them"). Questions 1-5 keep their numbers, so every 1a and C1 reference still holds.
- Paper-ScalingGlucose-NatSeries2026 StoryA: Question 0 "Pretraining and downstream tasks", read from the code: next-reading pretraining over up to 576 readings (numeric: mean squared error; token: one token per mg/dL value 11-400, cross-entropy); the 2-hour forecast with no fine-tuning, RMSE per step; the low and high alerts (T6, not built). §3's opening, §3.6, A3 and a Law line updated. The Methods page's "256 bins" disagrees with the code and is left for its writing pass.
- Paper-ScalingGlucose-NatSeries2026 StoryA: Question 6 "Fairness" (JL 260930: "I still remember we have another question about the fairness"): hypotheses 6a (a bigger model does not shrink the gap to new patients) and 6b (patient-group gaps stay), claim 6a (C6), E11 (an exploratory read of the b04.j02.t01 tables, 360 models) and E12 (absent), T13 (Task b04.j02.t01, which no row had named) and T14 (no task yet); Question logic and Answer form move to §3.7 and §3.8. Question 0 now says the forecast is scored on two test sets, later days of the training patients and patients never seen, and T10 and T12 say the same.

## 0.15.0 · 2026-09-30 · Task and Discovery rows have a short name too

- §7 and §6 rows gain a `name` column after the id: a short phrase of five words or fewer, with the `question` cell now one plain sentence saying what we do, as a §3 question has (JL 260930: "the Label, + Short names, and a new line to explain what it is"). The Paper Workbench prints the name beside the stage pill and the sentence below (haipipe-workbench-paper 0.17.0).
- A question's Name need not be a question (JL 260930 named Question 3 "Different Prediction Horizon"); 0.14.1's "short question phrase" becomes "a short phrase, often a question".
- Paper-ScalingGlucose-NatSeries2026 StoryA: T1-T12 and D1-D6 names and plain sentences; Question 3 is Different Prediction Horizon, and C4 turns (JL 260930): the gain from scale is strongest at 5 minutes and fades toward 2 hours because CGM cannot see meals or exercise, so a glucose foundation model must be event-aware. Updated with it: hypothesis 3a, claim 3a (C4), its contribution, E6, T3, the Pitch box, §3.6, §4.3, §8's box, arc and Results and Discussion rows, and a Law line.

## 0.14.1 · 2026-09-30 · A question is a short phrase and one plain sentence

- `- **Name**:` is a short question phrase of five words or fewer, and `- **Question**:` is one plain sentence saying what the paper does to answer it, so the Paper Workbench reads "Question 1  Model or data?" with the plain line below (JL 260930: "I want the question to be Question NN Short question phrase, and next line is the plain language to explain the question", "the question here we have are just too long"). Replaces 0.13.1's "two or three plain words".
- Paper-ScalingGlucose-NatSeries2026 StoryA: Names and plain Questions for Questions 1-5 (Model or data?, Reuse the same patients?, Further ahead?, Numbers or tokens?, Predict bigger data?); the long technical questions are gone and their precise wording stays in the hypotheses and claims.

## 0.14.0 · 2026-09-30 · §5.3 P-board: the target venue's related papers

- §5.3 Novelty basis holds a P-board: one row per related paper, the venue the paper is written for first (JL 260930: "我们选 paper 一定要选一个 venue 的 … 在 NMI 上找一些相关的 paper"), other venues allowed (JL 260930: "this is not limited to NMI"), `P | paper | role | question | why it matters | Discovery Run`. Role is `closest`, `question`, `background` or `caution`; question is an RQ id or `all`; each row names the Discovery Paper Run that holds the paper, and a §6 row names the Discovery Task. The Paper Workbench draws it as Story › Related Papers (haipipe-workbench-paper 0.15.0).
- Paper-ScalingGlucose-NatSeries2026 StoryA: P1-P15, 15 Nature Machine Intelligence papers (Discovery b01.j02.t01 plus Frey 2023 and Xiao 2025 in b01.j01.t01); §6 gains D6 and now names the two Discovery Tasks that exist (it said no Discovery block existed).

## 0.13.1 · 2026-09-30 · A question has a short Name

- Each §3 question block may carry `- **Name**: <two or three plain words>` above `- **Question**`, so a question reads like a hypothesis or claim: short name first, sentence second (JL 260930: "Question: short name, then the sentences that describe this question"). The Paper Workbench prints it beside the Question pill. First used on Paper-TestToLearn-MS2026 StoryA and StoryC.

## 0.13.0 · 2026-09-29 · Codes by question; short name and sentence; foundation in every block

- §3 items are coded by question (1a, 1b under Question 1; JL 260929: "if this is for Question 1, then the hypothesis and claims should be 1a, 1b"). A hypothesis and its claim share a code; a claim keeps its paper-wide id (C1–C5) right after the code, so the Pitch, §8 and the Section Pages' C1–C5 still point at it (a find-and-replace was not safe: C1 is also a Section plan's division id, as in `C1.P1.B1`).
- Every hypothesis, claim and contribution is `Short name: one sentence` (JL 260929: "both the hypotheses and claims to be short-phrase-name: explanation").
- No separate foundation question (JL 260929: "just the research questions … the question level foundation work … can be shared"): a §7 row marked `every question` belongs to every question block.
- Paper-ScalingGlucose-NatSeries2026 StoryA: hypotheses 1a, 1b, 2a, 3a, 4a, 5a; claims 1a (C1), 1b (C2), 2a (C3), 3a (C4), 4a (C5).

## 0.12.0 · 2026-09-29 · The question block holds the whole chain; §7 work runs in order

- §3 question blocks have four groups under the question (JL 260929: "the question is the main block, then … Hypothesis 1, 2, 3, what are the potential claims, what are the potential contributions, and what are the potential work"): **Hypotheses** (`H1` · short guess · tested by E1), **Potential claims** (`C1` · from H1 · statement, with Role, Now, If it fails), **Potential contributions** (rests on C1, C2 · what the reader gains) and **Potential work** (`T1` · for H1, H2; addresses may narrow a shared row). Every link is written once, pointing up. Replaces 0.11.0's `**Cn · Hypothesis · phrase**` records.
- §7 rows are named as the question they answer and carry a stage (data · training · evaluation · results · analysis · figures), in run order (JL 260929: "where is the work for data, for the model training, for the results analysis … the work should follow the logics", "name them in the question format"). The upstream data, training and evaluation work gets its own rows; a row every research question needs says `every question`.
- Applied first to Paper-ScalingGlucose-NatSeries2026 StoryA: H1–H6, C1–C5, one contribution per question, T10–T12 (training set, model grid, scores) added, T1–T9 renamed as plain questions, T4 gained the epoch analysis folder `b04.j02.t05`.

## 0.11.0 · 2026-09-29 · §3 is one block per question (JL 260929)

- §3 Research Questions writes one block per research question: `#### 3.N · Question N · RQn`, the question's fields (Question, Why the paper needs it, Answer form, Discovery, Task, Section, Answer state, Contribution), then one `**Cn · Hypothesis · short phrase**` record per hypothesis (Statement, Tests, Role, Now, If it fails). JL 260929: "one question will be one block", holding its hypotheses, claims and contribution. The hypotheses are the planned claims, so they keep the claim ids; a hypothesis reads as a claim once every §5 evidence row (E1, E2, …) that tests it is established. The one-row-per-RQ table is still read.
- §8 Section Narrative's claim system may point to the §3 hypotheses and name their roles instead of restating each statement.
- First Story written this way: Paper-ScalingGlucose-NatSeries2026 StoryA (C1–C5 moved from §8.1 into §3.1–§3.5).

## 0.10.1 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.

## 0.10.0 · 2026-09-29 · The Roadmap is question first

- §6 opens with a `Q | general question | serves` table (JL 260928: "each item a more general
  question, under it the T and D, under T and D the BJTR"). Every D and T row leads with a short
  plain question, carries a `folder` cell (BJTR address, a range such as `b03.j02.t01–t03`, or
  `none yet`) and ends with a `Q` cell. Row ids are `D<n>` and `T<n>`, never `B<n>`. The Paper
  workbench Story › Roadmap reads this as the tree general question → T and D → folders.

## 0.9.3 · 2026-09-20

- Bind prospective §1–§8 Story work to the current Page/Run contracts and Paper Specs. CHECK remains a controller judgment and does not establish planned findings or authorize execution. No Page outline or human approval is promoted.

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
  eight-division blueprint and the §6 Discovery / §7 Task / §8 Narrative roles.
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
  `haipipe-page-<type>`, cf. `insight/haipipe-page-insight`). Contract
  body unchanged from 0.9.0. Written by Claude Peer.
- The Story design and all generated outlines remain `v0.x`, `approved: ⬜`;
  the rename does not imply human approval or permit `v1.0` promotion.

## 0.9.0 · 260907 · draft, not v1

- Reframed Story as a prospective guide to the whole paper rather than a work
  manual or control center.
- Integrated the former three planning surfaces into eight Content divisions:
  §1–§5 are the Seed, §6 is Discovery Roadmap, §7 is Task Roadmap, and §8 is
  Section Narrative.
- Restored discovery gaps and expected syntheses; paper-level evidence
  needs, designs, and interpretation branches; and the Narrative's
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
  checks drop the old nursery/graduation wording. Binding mechanics
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
  graduated from (cross-repo pagex, the bank-page pattern) and the idea table's
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
