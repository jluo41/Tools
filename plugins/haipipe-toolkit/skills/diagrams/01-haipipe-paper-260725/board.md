# /haipipe-paper: Design → Delivery → Engine → Execute

spine: A paper is a delivery system. Design first fixes what the Paper system is and who owns it; Delivery then names what readers receive; Engine supplies the callable skill routes; Execute records what actually ran and whether it reopens an owner.
dialect: paper
paper-root: _fixture
close: Every Delivery target has an owning Engine route and Execute evidence or an explicit open gap; every design question is ruled or deliberately parked; fresh-agent evidence validates completed skill work.

## Topic

This is a **Skill-Board** for the Paper family, organized like the `/haipipe-board` Skill-Board.

- **QA · Design** defines the Paper system, its folders, and ownership boundaries.
- **QB · Delivery** defines what the paper must give readers and collaborators, in the paper-facing order below.
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
          │ folders · ownership   │     │ Opening → … → Round    │ │ skill routes ·       │
          │ Paper / Board / Probe │     │ 20 working records     │ │ Paper/Probe/Display  │
          │ boundaries            │     │                        │ │ + Board substrate    │
          └───────────────────────┘     └───────────┬────────────┘ └──────────┬───────────┘
                                                      │                         │
                                                      └───────────┬─────────────┘
                                                                  ▼
                                                     ┌────────────────────────┐
                                                     │ QF · Execute           │
                                                     │ bounded run · evidence │
                                                     │ failure → reopen owner │
                                                     └────────────────────────┘

QB1   Opening includes Seed, Venue, Pitch, and Narrative.
QB2   Work grows the discovery and task banks through explicit probes.
QB9   Build includes projection, diffusion/distribution, compile, and promotion.
QB10  Round contains one review/rebuttal/revision/resubmission batch.
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
```
QA0-the-board-map.md
QA1-eight-folders.md
QA2-the-skill-set.md
QA3-the-skill-board.md
QA4-the-board-tool.md
QA5-the-probe-layer.md
QA6-paper-scaffold.md
QA7-the-paper-board.md
QA8-owning-the-shared-page.md
QA9-driving-work-from-a-page.md

### QB · Delivery
What one paper must give its reader or collaborator. The group page supplies the delivery overview; its pages carry the ten reader-facing concerns in order.

```text
⚙️ ENGINE                      📋 PAGES · the working record          📂 FOLDER
─────────────────────────      ───────────────────────────────────    ────────────────────────
skill routes                ◀── QB1–QB10  paper-facing delivery      ──▶  paper artifacts
```
QB1-opening.md
QB2-work.md
QB3-literature.md
QB3a-sentence-citation.md
QB4-value.md
QB4a-sentence-value.md
QB5-display.md
QB5a-sentence-display-table.md
QB5b-sentence-display-figure.md
QB5c-display-folder.md
QB5d-requested-display.md
QB5e-display-caption.md
QB5f-display-placement.md
QB6-main.md
QB7-appendix.md
QB8-present.md
QB9-build.md
QB9a-sentence-to-latex.md
QB9b-sentence-to-word.md
QB10-round.md

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
Skill-7-haipipe-board-index.md
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
QD1                QB-delivery/QB5c-display-folder.md
QD2                QB-delivery/QB5d-requested-display.md
QD3                QB-delivery/QB5e-display-caption.md
QD4                QB-delivery/QB5f-display-placement.md
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
Q-Skill-haipipe-board-index    QC-engine/Skill-7-haipipe-board-index.md
Q-Skill-haipipe-board-page     QC-engine/Skill-8-haipipe-board-page.md
Q-Skill-haipipe-board-sentence QC-engine/Skill-9-haipipe-board-sentence.md
Q-Skill-haipipe-board-routing  QC-engine/Skill-10-haipipe-board-routing.md
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
Legacy-QC1          QB-delivery/QB3a-sentence-citation.md
Legacy-QC2          QB-delivery/QB4a-sentence-value.md
Legacy-QC3          QB-delivery/QB5a-sentence-display-table.md
Legacy-QC4          QB-delivery/QB5b-sentence-display-figure.md
Legacy-QC5          QB-delivery/QB9a-sentence-to-latex.md
Legacy-QC6          QB-delivery/QB9b-sentence-to-word.md
PHILOSOPHY.md      ../../paper/PHILOSOPHY.md
README.md          ../../paper/README.md
stages/            ../../paper/1-lifecycle/haipipe-paper-stage/stages/
index.yml          ../../paper/1-lifecycle/haipipe-paper-stage/stages/index.yml
CONTRACT.md        ../../paper/1-lifecycle/haipipe-paper-stage/stages/CONTRACT.md
venue/             ../../paper/venue/
haipipe-probe/     ../../probe/haipipe-probe/
haipipe-board/     ../../board/haipipe-board/
haipipe-board-index/ ../../board/haipipe-board-index/
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
QA8@boardform      ../01-boardform-260722/QB-delivery/QB5a-evidence-card.md
QA8a@boardform     ../01-boardform-260722/QB-delivery/QB5d-agent-visibility.md
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
