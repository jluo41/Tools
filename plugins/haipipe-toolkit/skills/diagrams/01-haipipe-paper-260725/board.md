# /haipipe-paper: Delivery → Engine → Execute

spine: A paper is a delivery system. First name the reader-facing delivery and its authority; then trace the skill-first Engine route that may produce it; then inspect a bounded Execute run that proves or blocks that route.
dialect: paper
paper-root: _fixture
close: Every Delivery group has a named artifact, authority, Engine route, and Execute evidence or an explicit open gap; every design question is ruled or deliberately parked; fresh-agent evidence validates completed skill work.

## Topic
This Board has three reading jobs.

**DELIVERY** says what one paper must give its reader or collaborator. It owns the desired artifact,
the canonical content, and the human completion decision. Its accepted reading order is:

```text
Opening → Work → Literature → Value → Display → Main → Appendix → Present → Build → Round
   │         │
   Venue     └─ grows discovery + task banks
```

Venue is inside Opening. Build also owns diffusion/distribution. Present includes slides and
posters. Response is named Round, one batch per round.

**ENGINE** says how reusable, callable skills serve those deliveries. Its target contract is
skill-first: each skill page will list the Delivery content it serves, the authorities it reads, the
narrow places it may write, the handoff it produces, and what it refuses to own. Until those
backlinks are added, `QS0` is the explicit forward crosswalk and the missing reciprocals remain open.

**EXECUTE** records an actual bounded run of one Delivery through one Engine route. A test, gate,
compile, receipt, or fresh-agent observation is evidence inside Execute. Execute never becomes a
second authoring tree and never promotes a candidate without the existing human authorization.

Delivery order is a reader-facing concern order, not a replacement for the Engine's dependency
graph. A stage may revisit an earlier Delivery concern; execution order remains declared by stage
contracts rather than inferred from adjacent groups.

`state:` on this design Board records whether a decision is ruled, partial, open, or parked.
Implementation status belongs in each page's Items and Where-we-are sections.

## Pipeline
```text
DELIVERY · what one paper must give readers and collaborators
│
├─ QF  Delivery map and submission-cut law
├─ QG  Opening = Seed + Venue + Pitch + Narrative
├─ QH  Work = resources + claims + probes that grow both banks
├─ QI  Literature
├─ QJ  Value
├─ QK  Display
├─ QL  Main
├─ QM  Appendix
├─ QN  Present = slides + poster
├─ QO  Build = projection + diffusion/distribution + compile + promotion
└─ QP  Round = review/rebuttal/revision/resubmission batches

ENGINE · skill-first routes that serve Delivery
│
├─ QS  Delivery × Skill map and callable-skill pages
├─ QA  Ownership and Paper–Board–Probe boundaries
├─ QB  Stage and page execution contracts
└─ QC  Sentence and evidence contracts

EXECUTE · actual bounded runs and their evidence
│
└─ QE  Execution map, contract checks, fresh-agent runs, and reopen evidence
```

## Board Structure
The index is deliberately Delivery-first. Existing Q ids remain historical addresses; their order
does not declare lifecycle dependencies or move paper authority.

The target Delivery overview contract is:

```text
Reader result · Artifact · Authority · Completion gate · Consumes
Engine route · Execute evidence · Open gaps
```

The target Engine skill-card contract is:

```text
Trigger · Serves · Reads · May write · Produces · Hands off · Refuses · Execute evidence
```

The target Execute-record contract is:

```text
Delivery target · Engine route · Fixture · Observable gate · Non-write boundary
Receipt or observation · Failure → owning page to reopen
```

The current Delivery overview pages retain their existing seven-field wording while the crosswalk
is filled in. No page may claim the new contract is complete before its Engine route and Execute
evidence are actually linked.

## Pages
### QF · Delivery map
The paper-folder law, source/candidate/submission roles, and the map into every Delivery group.
QA6-paper-scaffold.md

### QG · Delivery: Opening
Opening includes Venue: Seed → Venue → Pitch → Narrative.
QG0-delivery-opening.md

### QH · Delivery: Work
After Opening, Work grows the discovery and task banks through explicit probes.
QH0-delivery-work.md

### QI · Delivery: Literature
Verified literature becomes sentence citations and format-specific references.
QI0-delivery-literature.md
QC1-sentence-citation.md

### QJ · Delivery: Value
Task-produced quantitative evidence remains bound to its producing run.
QJ0-delivery-value.md
QC2-sentence-value.md

### QK · Delivery: Display
Paper owns visual argument, caption, placement, and gate; `/haipipe-display` makes the render.
QK0-delivery-display.md
QC3-sentence-display-table.md
QC4-sentence-display-figure.md
QD1-the-display-folder.md
QD2-a-display-someone-asked-for.md
QD3-a-display-with-a-caption.md
QD4-a-display-placed-in-a-section.md

### QL · Delivery: Main
Authoritative Main S pages project into the journal's main manuscript.
QL0-delivery-main.md

### QM · Delivery: Appendix
Appendix source regions, gates, wrappers, and leaves remain explicit.
QM0-delivery-appendix.md

### QN · Delivery: Present
Present contains slides and posters as audience-facing projections.
QN0-delivery-present.md

### QO · Delivery: Build
Build includes diffusion/distribution: manifest wiring, candidates, handoffs, and explicit promotion. Concrete runs and their receipts are indexed under Execute.
QO0-delivery-build.md
QC5-sentence-to-latex.md
QC6-sentence-to-word.md

### QP · Delivery: Round
One external-feedback batch is one Round: review, rebuttal, revision, and resubmission.
QP0-delivery-round.md

### QS · Engine: skill-first routes
Each skill page states which Delivery content it serves. The existing six pages are the initial authoring/control cohort; delivery and project pages are added only after their independent contracts are audited.
QS0-delivery-engine-map.md
QS4-paper-skill-map.md
Q-Skill-haipipe-paper.md
Q-Skill-haipipe-paper-lifecycle.md
Q-Skill-haipipe-paper-stage.md
Q-Skill-haipipe-paper-draft.md
Q-Skill-haipipe-paper-probe.md
Q-Skill-haipipe-paper-revise.md

### QA · Engine foundations: ownership and boundaries
Where Paper, Board, Probe, and their records live; which layer owns each crossing.
QA0-the-board-map.md
QA1-eight-folders.md
QA2-the-skill-set.md
QA3-the-skill-board.md
QA4-the-board-tool.md
QA5-the-probe-layer.md
QA7-the-paper-board.md
QA8-owning-the-shared-page.md
QA9-driving-work-from-a-page.md

### QB · Engine foundations: stage and page contracts
What one stage declares, receives, runs, and provides.
QB1-what-a-stage-declares.md
QB2-the-page.md
QB2a-its-template.md
QB2b-its-name.md
QB2c-the-second-run.md
QB2d-what-comes-out.md
QB3-the-flow.md
QB3a-draft.md
QB3b-probe.md
QB3c-revise.md
QB3d-check.md

### QC · Engine foundations: sentence and evidence contracts
The sentence is the smallest authored manuscript unit; its evidence is attached and inspectable.
QC0-sentence-unit.md

### QE · Execute: bounded runs and evidence
Execute turns one Delivery target through one Engine route on a named fixture or paper. Tests, gates, receipts, and fresh-agent observations are evidence within that run.
QE0-execution-map.md
QE1-contract-form.md
QE2-fresh-agent.md

## Links
PHILOSOPHY.md      ../../paper/PHILOSOPHY.md
README.md          ../../paper/README.md
stages/            ../../paper/1-lifecycle/haipipe-paper-stage/stages/
index.yml          ../../paper/1-lifecycle/haipipe-paper-stage/stages/index.yml
CONTRACT.md        ../../paper/1-lifecycle/haipipe-paper-stage/stages/CONTRACT.md
venue/             ../../paper/venue/
haipipe-probe/     ../../probe/haipipe-probe/
haipipe-board/     ../../board/haipipe-board/
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
