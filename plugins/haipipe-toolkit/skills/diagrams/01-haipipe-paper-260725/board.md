# /haipipe-paper: Design → Delivery → Engine → Execute

spine: A paper is a delivery system. Design first fixes what the Paper system is and who owns it; Delivery then names what readers receive; Engine supplies the callable skill routes; Execute records what actually ran and whether it reopens an owner.
dialect: paper
paper-root: _fixture
close: Every Delivery target has an owning Engine route and Execute evidence or an explicit open gap; every design question is ruled or deliberately parked; fresh-agent evidence validates completed skill work.
session: 8d4c966d-8db2-443b-9194-8dcb8a14b600
## Topic

This is a **Skill-Board** for the Paper family, organized like the `/haipipe-board` Skill-Board.

- **QA · Design** defines the Paper system, its eleven folders, and ownership boundaries, including the four shared families the paper calls and owns none of.
- **QB · Delivery** defines what the paper must give readers and collaborators, in the paper-facing order below, and nothing else: ten concerns read top to bottom, plus the one page that draws the whole paper board at once.
- **QBe · Delivery Element** holds the rules whose unit is smaller than a concern, one series per unit, numbered from the smallest up: one sentence, one float, one whole section. It is not an eleventh Delivery concern either: a concern says what the reader GETS, and a series says what a rule APPLIES TO, which is why it is entered by dropping into a series head rather than by reading it through.
- **QBv · Delivery Venue** holds what each venue KNOWS, one page per venue TARGET: 14 journals plus grant and patent. It is not an eleventh Delivery concern: `QB1` still owns which venue this paper picked, and this group owns what that venue rewards, desk-rejects, and requires of every section.
- **QC · Engine** defines the reusable skills and contracts that can produce those deliveries.
- **QF · Execute** records bounded runs, checks, receipts, and fresh-agent evidence.

`QD · Working` and `QE · Sharing` are intentionally absent. Their current concerns—live Board interaction, hosting, mounts, and Tailnet access—are owned by `/haipipe-board`; this Paper Skill-Board uses that shared substrate instead of duplicating it. The Paper Board nevertheless owns its own writing dialect: the manuscript meaning and acceptance requirements of sections, paragraphs, sentences, citations, values, and displays. Venue stays inside Opening, Present includes slides and posters, Build includes diffusion/distribution, and reviewer batches remain Round.

## Pipeline

```text
QA · DESIGN     what the Paper system is and who owns its boundaries
       │ shapes
       ▼
QB · DELIVERY   what readers and collaborators receive
       Opening → Work → Literature → Value → Display → Main → Appendix
       → Present → Build → Round
       │
       │ ◀── governed by ── QBe · DELIVERY ELEMENT  one series per UNIT,
       │              smallest first: QBe1 one sentence · QBe2 one float
       │              QBe3 a whole ## Content · a concern GETS, a series APPLIES TO
       │
       │ ◀── reads ── QBv · DELIVERY VENUE  one page per TARGET
       │              QB1 picks the venue · QBv holds its rewards,
       │              desk signals, and per-section norms
       │ served by
       ▼
QC · ENGINE     which reusable Paper / Probe / Display route may produce each delivery,
                on the shared Board substrate; the Paper Board fixes manuscript-specific
                section, paragraph, sentence, and evidence requirements
       │ demonstrated by
       ▼
QF · EXECUTE    what actually ran, passed, failed, or reopened work
```

Delivery order is the reader-facing concern order. It does not replace Engine dependencies: a stage may revisit an earlier delivery concern, and execution order remains declared by the relevant skill contract.

## Board Map

```text
          what the Paper system IS       what the reader GETS       how it is MADE
          ┌───────────────────────┐     ┌────────────────────────┐ ┌──────────────────────┐
          │ QA · Design           │────▶│ QB · Delivery          │◀│ QC · Engine          │
          │ 11 folders · 6 pairs  │     │ QB0   the whole layout │ │ skill routes ·       │
          │ Paper · Board · Probe │     │ QB1–QB10 the concerns, │ │ Paper/Probe/Display  │
          │ Display · Writing     │     │   in reader order      │ │ + Board substrate    │
          │                       │     │ read with QBe by UNIT  │ │                      │
          │                       │     │ and QBv by TARGET      │ │                      │
          └───────────────────────┘     └───────────┬────────────┘ └──────────┬───────────┘
                                                      │                         │
                                                      └───────────┬─────────────┘
                                                                  ▼
                                                     ┌────────────────────────┐
                                                     │ QF · Execute           │
                                                     │ bounded run · evidence │
                                                     │ failure → reopen owner │
                                                     └────────────────────────┘

QA1   Eleven folders in six pairs. A board may serve two things; ② serves ① the paper skill and ⑪ the prose verb.
QA10  The prose verb is argued HERE because it owns no artifact kind and therefore has no board of its own.
QB1   Opening includes Seed, Venue, and Pitch.
QB2   Work grows the discovery and task banks through explicit probes, and owns the Narrative arc built from the claim ledger.
QB9   Build includes projection, diffusion/distribution, compile, and promotion.
QB10  Round contains one review/rebuttal/revision/resubmission batch.
QBe   Split out of Delivery on 260803 (JL: "divide the QB11 to QB13c as a new Question Group"), then numbered by unit size the same day (JL: sentence, display, section). QB's own copy had admitted the seam for a round, saying the group was "read in two passes", and thirteen of its twenty-four pages were in the second one.
QBe1  Sentence series: four attachment types, one marker grammar, differing only in who may complete one.
QBe2  Float series: what Paper owns about a display between the render and the sentence that points at it. It is numbered second because that is where it sits, between the sentence and the section.
QBe3  Section series: a rule here cannot be checked one sentence at a time, and it fails that check in
      two ways. A SEQUENCE rule is about order, and the paragraphs cannot be shuffled. An AGGREGATE rule
      is about amount, survives the shuffle, and is the venue's `## Word budget` (JL 260803).
QBv1  A venue cuts across Delivery: its README maps to Claims, Display, Minimap, and Write/Edit at once, so it can be filed under no single concern. The packs are their own repository and this plugin reads them and never writes them. One page per TARGET, with no pack-head layer above it (JL 260802).
QC1 names the four-part Engine: Paper, Probe, Display, and the Board substrate. QC5 is where the Paper Board adds its manuscript-specific writing dialect above Board's generic page and sentence grammar.
QF1–QF3 prove or block a Delivery × Engine route; they never become a second authoring tree.
```

## Board Structure

This Board has one editable Board-Folder and one generated Board-Webpage site. The group letters now follow the Skill-Board shape; every live page id matches its current group. Historical ids that do not collide remain declared aliases in `## Links`. The old Engine `QB*`/`QC*` names collided with new Delivery/Engine ids, so their prose references are migrated to their current `QC*` names rather than ambiguously preserved.

**Board-Folder: source and generated output on disk**

```text
01-haipipe-paper-260725/
├── board.md                         Board-level source and page registry
├── QA-design/                        Design pages and paper-boundary records
├── QB-delivery/                      reader-facing paper delivery pages
├── QBe-delivery-element/             the three series, smallest unit first: sentence · float · section
├── QBv-venue-packs/                  one page per venue target: 14 journals + grant + patent
├── QC-engine/                        skills and their contracts
├── QF-execute/                       bounded execution records
├── _fixture/                         inspectable Paper evidence used by this Board
├── fig/                              the Board canvas and image assets
├── _archive/                         retired source pages, never deleted
└── board/                            generated site, never hand-edited
```

**Board-Webpage: the generated routes a reader opens**

```text
board/
├── index.html                        Board-Webpage-Index
├── QA.html … QF.html                 one Board-Webpage-Group per live group
├── QB/QB1-opening.html               one focused Board-Webpage-Page
└── _assets/                          one shared stylesheet and script bundle
```

## Related Folders

Open the shipping Paper skills, the Board engine that renders them, or this Board's own source without leaving the Index.
@ ../../paper/ | Paper skill family
- README.md
- PHILOSOPHY.md
@ ../../board/haipipe-board/ | Board engine and canonical contract
- SKILL.md
- ref/board-form.md
@ . | This Paper design Board
- board.md

## Pages

### QA · Design
What the Paper system is before a delivery is produced: folder law, boundaries, ownership, and where a ruling may land.

```text
⚙️ ENGINE                      📋 PAGES · the working record          📂 FOLDER
─────────────────────────      ───────────────────────────────────    ────────────────────────
?                          ◀── QA0–QA9  system map, boundaries, and  ──▶  Paper/Board/Probe law
?                          ◀── QA6      paper scaffold and folder law ──▶  paper folder
?                          ◀── QA10     the prose verb, argued here    ──▶  writing/ · the only
                                        because it has no board          shared family whose
                                        of its own                       board is this board
```
QA0-the-board-map.md
QA1-the-folder-map.md
QA2-the-skill-set.md
QA3-the-skill-board.md
QA4-the-board-tool.md
QA5-the-probe-layer.md
QA6-paper-scaffold.md
QA7-the-paper-board.md
QA8-owning-the-shared-page.md
QA9-driving-work-from-a-page.md
QA10-the-writing-layer.md

### QB · Delivery
What one paper must give its reader or collaborator, in reader order and uninterrupted. QB1 through QB10 are the ten concerns, and reading them top to bottom is the paper.
QB0 sits before all of them and draws the whole paper board at once, which is the one thing no single concern can show.
A concern says what the reader GETS, and that is the only thing this group holds. What a rule APPLIES TO is `QBe`, and what a desk REWARDS is `QBv`; both are read while a concern is being worked and neither is a concern itself.

```text
⚙️ ENGINE                      📋 PAGES · the working record          📂 FOLDER
─────────────────────────      ───────────────────────────────────    ────────────────────────
skill routes                ◀── QB1–QB10   the ten concerns, in order ──▶  paper artifacts
the whole board at once     ◀── QB0        the layout every group is ──▶  <paper>/0-lifecycle/
                                           a slice of
```
QB0-paper-board-layout.md
QB1-opening.md
QB2-work.md
QB3-literature.md
QB4-value.md
QB5-display.md
QB6-main.md
QB7-appendix.md
QB8-present.md
QB9-build.md
QB10-round.md

### QBe · Delivery Element
One series per UNIT a delivery rule can apply to, numbered from the smallest unit up: one sentence, then one float, then a whole section. Split out of `QB` on 260803, after that group's own copy had spent a round telling readers it was "read in two passes" while thirteen of its twenty-four pages sat in the second one.
The order is the ruling (JL 260803). A float is the unit that sits between the other two, larger than the sentence that points at it and smaller than the section it lands in, and the numbers now say so: `QBe1` sentence, `QBe2` float, `QBe3` section.
A concern is entered by reading it through; a series is entered by dropping in, because you arrive already holding a unit and needing the rule that governs it. The question that files a rule is what you must hold in your hand to check it: one sentence alone, one float as an object, or the whole `## Content` in order.
Each series reads from the paper's own stage folder, which is where the evidence is produced: `QBe1`'s three types from `S03-literature`, `S04-value` and `S05-display`, `QBe2` from `S05-display`, and `QBe3` from `S06-main` and `S07-appendix` (JL 260803, after the MISQ paper regrouped its lifecycle into `S01` to `S10`).
This group is not an eleventh Delivery concern, for the same reason `QBv` is not: it gives the reader nothing directly, and every rule in it is spent on something `QB1`–`QB10` deliver.

Each series is ONE page, and its filename names what it holds (JL 260803). The ten faces became numbered divisions of their series on 260803, following `QB5-overview` on the boardform board; they are archived rather than deleted and every retired id still resolves through `## Links`.

```text
⚙️ ENGINE                      📋 PAGES · the working record          📂 FOLDER
─────────────────────────      ───────────────────────────────────    ────────────────────────
probe + evidence            ◀── QBe1  cite · value · display        ──▶  markers and chips
                                      unit = one sentence · §4–§7
Display layer               ◀── QBe2  folder · render · caption      ──▶  displays/<unit>/
                                      unit = one float · §4–§6
adapters                    ◀── QBe3  content · latex · word ·       ──▶  sections/*.tex · docx
                                      display · unit = one ## Content · §3–§5

🔑 each name is UNIT then PARTS, and `display` appears in all three: a sentence
   POINTS at one, QBe2 IS one, a section PLACES one (JL 260803)
```
QBe1-sentence-cite-value-display.md
QBe2-display-folder-render-caption.md
QBe3-content-latex-word-display.md

### QBv · Delivery Venue
One page per VENUE TARGET, and nothing above it. A page is a specific journal, agency, or patent office: what that desk accepts, what it desk-rejects, and what it requires of every section and of the appendix. `QB1` ruled on 260729 that the venue DECISION lives inside Opening and that ruling stands: this group is not an eleventh Delivery concern, it is the catalog Opening reads to make that decision and that four other concerns read afterwards.
A venue cuts across Delivery, which is why it cannot be filed under any single concern. Every `playbook-*/README.md` carries four stage maps: rewards land on QB4 Value, display conventions on QB5 Display, the section arc on QB6 Main, and the language profile on QBe3 §3.

**The law this group runs on**, absorbed from the retired `QBv0` on 260802: a venue pack is READ and never written by this plugin. The packs are their own repository, `jluo41/Venue-Paper`, pinned as a submodule at `paper/venue/`, so every paper stage is a reader by construction. A pack answers at two levels, family and outlet, and a file missing from either level is a missing answer rather than a missing folder. Two files sit at different levels depending on the pack: `taste.md` and `examples/` are per-outlet for the eleven multi-outlet journals and per-family for PNAS, grant, and patent, and that split is declared nowhere. `../../paper/1-lifecycle/haipipe-paper-stage/stages/section-kinds.yml` is the reader-side resolver: it maps outlet to section kinds, aliases `theory-model` to `theory`, rules that a pack path is reached by GLOB and never by concatenation, and declares grant and patent blueprint-only by design.

```text
⚙️ ENGINE                      📋 PAGES · the working record          📂 FOLDER
─────────────────────────      ───────────────────────────────────    ────────────────────────
2a-venue reads packs:       ◀── QBv1–QBv4   the UTD-IS desks         ──▶  playbook-utd-is/
QB1 owns the DECISION       ◀── QBv5–QBv7   the JAMA portfolio       ──▶  playbook-jama-portfolio/
QB4·QB5·QB6·QBe3 §3 read it   ◀── QBv8–QBv12  the Nature portfolio     ──▶  playbook-nature-portfolio/
section-kinds.yml resolves  ◀── QBv13–QBv14 PNAS · Diabetes Care     ──▶  playbook-pnas · -medical-journals
  outlet ▶ section kinds    ◀── QBv15–QBv16 grant · patent, the two  ──▶  README delta tables
                                            non-journal targets
```
QBv1-misq.md
QBv2-isr.md
QBv3-ms-is.md
QBv4-ms-marketing.md
QBv5-jama.md
QBv6-jama-im.md
QBv7-jama-network-open.md
QBv8-npj-digital-medicine.md
QBv9-nature-medicine.md
QBv10-nature-communications.md
QBv11-nature-human-behaviour.md
QBv12-nature-machine-intelligence.md
QBv13-pnas.md
QBv14-diabetes-care.md
QBv15-grant.md
QBv16-patent.md

### QC · Engine
How reusable Paper, Probe, and Display routes serve Delivery on a shared Board substrate. The Engine map, mirrored skill pages, stage/page contracts, and Paper-specific sentence/evidence dialect stay here; Board supplies generic structure but never manuscript truth.

```text
⚙️ ENGINE                      📋 PAGES · the working record          📂 FOLDER
─────────────────────────      ───────────────────────────────────    ────────────────────────
Paper / Probe / Display     ◀── QC1–QC5  delivery and writing routes  ──▶  skill + page handoffs
Board substrate             ◀── Skill-6–10 page/index/sentence/routing ──▶ shared Board grammar
```
QC1-delivery-skill-map.md
QC1a-skill-card-admission.md
Skill-0-haipipe-paper.md
Skill-1-haipipe-paper-lifecycle.md
Skill-2-haipipe-paper-stage.md
Skill-3-haipipe-paper-draft.md
Skill-4-haipipe-paper-probe.md
Skill-5-haipipe-paper-revise.md
Skill-6-haipipe-board.md
Skill-8-haipipe-board-page.md
Skill-9-haipipe-board-sentence.md
Skill-10-haipipe-board-routing.md
QC2-stage-contract.md
QC3-page-contract.md
QC3a-page-template.md
QC3b-page-name.md
QC3c-second-run.md
QC3d-page-output.md
QC4-phase-flow.md
QC4a-draft.md
QC4b-probe.md
QC4c-revise.md
QC4d-check.md
QC5-sentence-evidence-contract.md
QC6-paper-skill-folder.md
Skill-11-haipipe-writing.md

### QF · Execute
What actually ran. Each record names its Delivery target, Engine route, fixture, observable gate, non-write boundary, receipt, and failure-to-reopen path.

```text
⚙️ ENGINE                      📋 PAGES · the working record          📂 FOLDER
─────────────────────────      ───────────────────────────────────    ────────────────────────
check + fresh agent         ◀── QF1–QF3  bounded execution evidence  ──▶  pass / failure receipt
```
QF1-execution-map.md
QF2-contract-run.md
QF3-fresh-agent-run.md

## Links
QG0                QB-delivery/QB1-opening.md
QH0                QB-delivery/QB2-work.md
QI0                QB-delivery/QB3-literature.md
QJ0                QB-delivery/QB4-value.md
QK0                QB-delivery/QB5-display.md
QL0                QB-delivery/QB6-main.md
QM0                QB-delivery/QB7-appendix.md
QN0                QB-delivery/QB8-present.md
QO0                QB-delivery/QB9-build.md
QP0                QB-delivery/QB10-round.md
QS0                QC-engine/QC1-delivery-skill-map.md
QS4                QC-engine/QC1a-skill-card-admission.md
QC0                QC-engine/QC5-sentence-evidence-contract.md
QD1                _archive/QBe2a-display-folder.md
QD2                _archive/QBe2b-requested-display.md
QD3                _archive/QBe2c-display-caption.md
QD4                _archive/QBe3c-display-placement.md
QE0                QF-execute/QF1-execution-map.md
QE1                QF-execute/QF2-contract-run.md
QE2                QF-execute/QF3-fresh-agent-run.md
Q-Skill-haipipe-paper          QC-engine/Skill-0-haipipe-paper.md
Q-Skill-haipipe-paper-lifecycle QC-engine/Skill-1-haipipe-paper-lifecycle.md
Q-Skill-haipipe-paper-stage    QC-engine/Skill-2-haipipe-paper-stage.md
Q-Skill-haipipe-paper-draft    QC-engine/Skill-3-haipipe-paper-draft.md
Q-Skill-haipipe-paper-probe    QC-engine/Skill-4-haipipe-paper-probe.md
Q-Skill-haipipe-paper-revise   QC-engine/Skill-5-haipipe-paper-revise.md
Q-Skill-haipipe-board          QC-engine/Skill-6-haipipe-board.md
Q-Skill-haipipe-board-index    _archive/Skill-7-haipipe-board-index.md
Skill-7              _archive/Skill-7-haipipe-board-index.md
Q-Skill-haipipe-board-page     QC-engine/Skill-8-haipipe-board-page.md
Q-Skill-haipipe-board-sentence QC-engine/Skill-9-haipipe-board-sentence.md
Q-Skill-haipipe-board-routing  QC-engine/Skill-10-haipipe-board-routing.md
Q-Skill-haipipe-writing        QC-engine/Skill-11-haipipe-writing.md
Legacy-QB1          QC-engine/QC2-stage-contract.md
Legacy-QB2          QC-engine/QC3-page-contract.md
Legacy-QB2a         QC-engine/QC3a-page-template.md
Legacy-QB2b         QC-engine/QC3b-page-name.md
Legacy-QB2c         QC-engine/QC3c-second-run.md
Legacy-QB2d         QC-engine/QC3d-page-output.md
Legacy-QB3          QC-engine/QC4-phase-flow.md
Legacy-QB3a         QC-engine/QC4a-draft.md
Legacy-QB3b         QC-engine/QC4b-probe.md
Legacy-QB3c         QC-engine/QC4c-revise.md
Legacy-QB3d         QC-engine/QC4d-check.md
Legacy-QC1          _archive/QBe1a-sentence-citation.md
Legacy-QC2          _archive/QBe1b-sentence-value.md
Legacy-QC3          _archive/QBe1c-sentence-display-table.md
Legacy-QC4          _archive/QBe1d-sentence-display-figure.md
Legacy-QC5          _archive/QBe3a-section-to-latex.md
Legacy-QC6          _archive/QBe3b-section-to-word.md
QV0                 ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/S04-value/QV0-value-delivery.md
QP0                 ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/S08-present/QP0-present-delivery.md
QR0                 ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/S10-round/QR0-round-delivery.md
QB3a                _archive/QBe1a-sentence-citation.md
QB4a                _archive/QBe1b-sentence-value.md
QB5a                _archive/QBe1c-sentence-display-table.md
QB5b                _archive/QBe1d-sentence-display-figure.md
QB5c                _archive/QBe2a-display-folder.md
QB5d                _archive/QBe2b-requested-display.md
QB5e                _archive/QBe2c-display-caption.md
QB5f                _archive/QBe3c-display-placement.md
QB9a                _archive/QBe3a-section-to-latex.md
QB9b                _archive/QBe3b-section-to-word.md
QBe1a               _archive/QBe1a-sentence-citation.md
QBe1b               _archive/QBe1b-sentence-value.md
QBe1c               _archive/QBe1c-sentence-display-table.md
QBe1d               _archive/QBe1d-sentence-display-figure.md
QBe2a               _archive/QBe2a-display-folder.md
QBe2b               _archive/QBe2b-requested-display.md
QBe2c               _archive/QBe2c-display-caption.md
QBe3a               _archive/QBe3a-section-to-latex.md
QBe3b               _archive/QBe3b-section-to-word.md
QBe3c               _archive/QBe3c-display-placement.md
QB11                QBe-delivery-element/QBe3-content-latex-word-display.md
QB11a               _archive/QBe3a-section-to-latex.md
QB11b               _archive/QBe3b-section-to-word.md
QB11c               _archive/QBe3c-display-placement.md
QB12                QBe-delivery-element/QBe1-sentence-cite-value-display.md
QB12a               _archive/QBe1a-sentence-citation.md
QB12b               _archive/QBe1b-sentence-value.md
QB12c               _archive/QBe1c-sentence-display-table.md
QB12d               _archive/QBe1d-sentence-display-figure.md
QB13                QBe-delivery-element/QBe2-display-folder-render-caption.md
QB13a               _archive/QBe2a-display-folder.md
QB13b               _archive/QBe2b-requested-display.md
QB13c               _archive/QBe2c-display-caption.md
PHILOSOPHY.md      ../../paper/PHILOSOPHY.md
README.md          ../../paper/README.md
stages/            ../../paper/1-lifecycle/haipipe-paper-stage/stages/
index.yml          ../../paper/1-lifecycle/haipipe-paper-stage/stages/index.yml
CONTRACT.md        ../../paper/1-lifecycle/haipipe-paper-stage/stages/CONTRACT.md
venue/             ../../paper/venue/
haipipe-probe/     ../../probe/haipipe-probe/
haipipe-writing/   ../../writing/haipipe-writing/
writing/           ../../writing/
haipipe-display/   ../../display/
haipipe-board/     ../../board/haipipe-board/
haipipe-board-routing/ ../../board/haipipe-board-routing/
haipipe-board-page/ ../../board/haipipe-board-page/
haipipe-board-sentence/ ../../board/haipipe-board-sentence/
haipipe-board-routing/ ../../board/haipipe-board-routing/
dialect_paper.py   ../../board/haipipe-board/src/dialect_paper.py
haipipe-paper-probe          ../../paper/2-phase/1-probe/haipipe-paper-probe/
haipipe-paper                ../../paper/haipipe-paper/
haipipe-paper-lifecycle      ../../paper/1-lifecycle/haipipe-paper-lifecycle/
haipipe-paper-stage          ../../paper/1-lifecycle/haipipe-paper-stage/
haipipe-paper-draft          ../../paper/2-phase/0-draft/haipipe-paper-draft/
haipipe-paper-revise         ../../paper/2-phase/2-revise/haipipe-paper-revise/
haipipe-paper-revise-place   ../../paper/2-phase/2-revise/haipipe-paper-revise-place/
haipipe-paper-revise-results ../../paper/2-phase/2-revise/haipipe-paper-revise-results/
haipipe-paper-revise-content ../../paper/2-phase/2-revise/haipipe-paper-revise-content/
haipipe-paper-revise-humanizer ../../paper/2-phase/2-revise/haipipe-paper-revise-humanizer/
haipipe-paper-check          ../../paper/2-phase/3-check/haipipe-paper-check/
haipipe-paper-check-evidence ../../paper/2-phase/3-check/haipipe-paper-check-evidence/
haipipe-paper-project        ../../paper/3-deliver/1-build/haipipe-paper-project/
paper-folder/      ../../paper/3-deliver/1-build/haipipe-paper-folder/
paper-conform/     ../../paper/3-deliver/1-build/haipipe-paper-conform/
paper-compile/     ../../paper/3-deliver/4-ship/haipipe-paper-compile/
5-section-edit/    ../../paper/1-lifecycle/haipipe-paper-stage/stages/5-section-edit/
4-display/         ../../paper/1-lifecycle/haipipe-paper-stage/stages/4-display/
boardform-board/   ../01-boardform-260722/
probe-board/       ../01-probe-qa-260726/
display-board/     ../01-haipipe-display-260727/
QB1@probe          ../01-probe-qa-260726/QB-the-verbs-one-page-each/QB1-the-order.md
QB3@probe          ../01-probe-qa-260726/QB-the-verbs-one-page-each/QB3-match.md
QC1@probe          ../01-probe-qa-260726/QC-the-contract/QC1-qa-state-line.md
QB6@probe          ../01-probe-qa-260726/QB-the-verbs-one-page-each/QB6-interpret.md
QB4@boardform      ../01-boardform-260722/QB-delivery/QB4-overall.md
QA8@boardform      ../01-boardform-260722/QB-delivery/_archive/QB5a-evidence-card.md
QA1@display        ../01-haipipe-display-260727/QA-where-display-lives/QA1-display-map.md
QA3@display        ../01-haipipe-display-260727/QA-where-display-lives/QA3-unit-page-and-unit-folder.md
QB1@display        ../01-haipipe-display-260727/QB-one-display-unit/QB1-unit-contract.md
QB2@display        ../01-haipipe-display-260727/QB-one-display-unit/QB2-display-intake.md
QB3@display        ../01-haipipe-display-260727/QB-one-display-unit/QB3-recipe-and-render.md
QB4@display        ../01-haipipe-display-260727/QB-one-display-unit/QB4-candidates-and-promotion.md
QB5@display        ../01-haipipe-display-260727/QB-one-display-unit/QB5-wrapper-and-placement.md
QC1@display        ../01-haipipe-display-260727/QC-renderers-and-projections/QC1-renderer-taxonomy.md
QC3@display        ../01-haipipe-display-260727/QC-renderers-and-projections/QC3-many-consumers.md
QD1@display        ../01-haipipe-display-260727/QD-bridges-to-other-layers/QD1-task-to-intake.md
QD2@display        ../01-haipipe-display-260727/QD-bridges-to-other-layers/QD2-paper-display-bridge.md
QD3@display        ../01-haipipe-display-260727/QD-bridges-to-other-layers/QD3-sentence-and-projection.md
QC1@boardform      ../01-boardform-260722/_archive/QC1-where.md
QA2@boardform      ../01-boardform-260722/_archive/QA2-qtemplate.md
QE4                ../01-boardform-260722/QE-sharing/QE4-editlock.md
QX5                _fixture/1-probes/PP03_results-values/QX5_binary-exposure-flags.md
QD1-display-ownership       _archive/QD1-display-ownership.md
QD2-render-contract         _archive/QD2-render-contract.md
QD3-renderer-taxonomy       _archive/QD3-renderer-taxonomy.md
QD4-format-adapters         _archive/QD4-format-adapters.md
QD6                         _archive/QD6-provenance-chain.md
QD7                         _archive/QD7-one-content-many-formats.md
QD8                         _archive/QD8-display-intake.md
