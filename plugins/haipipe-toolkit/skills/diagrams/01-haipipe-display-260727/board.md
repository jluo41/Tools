# /haipipe-display: turn approved evidence into a reusable visual unit

spine: A Display is neither a task result nor a loose figure file. It binds a small, traceable Intake to a renderer, preserves a rebuild recipe and candidate history, and lets a consumer own the visual argument, caption, placement, and human gate. Pin down the unit, its sources, its renderer choices, and its bridges to Paper and other consumers so a fresh agent can make one display without reading raw data or inventing semantics.
close: Every Q here is RULED (✅) or PARKED (⏸️), with the decision on its own page and reflected in the Display contracts. The board stays open while the main Display entry door or the per-unit Display-stage migration remains undecided; a legacy paper is not silently migrated merely to close the board.

## Topic
`haipipe-display` is the reusable visual-production layer.
It accepts a bounded input package and produces an inspectable visual bundle.
It does not compute scientific evidence, decide a paper's claim, or choose where a paper cites a result.

The central object is a DISPLAY UNIT:

```text
intake/     what this unit was allowed to read
recipe/     how the visual can be rebuilt
candidates/ alternatives before a decision
assets/     the promoted visual
float.tex   a consumer-owned wrapper around the asset
```

Task retains the canonical evidence.
Paper retains the visual argument and wrapper semantics.
Display renders the approved unit without crossing either boundary.

This Board is the design/control plane for the reusable layer.
It is not a paper's live gallery.
Each concrete paper display instead receives an `S-Display-N` page in that paper's own lifecycle Board.

Words this board leans on.
An INTAKE is a provenance-bound, display-safe snapshot, not a second data store.
A RECIPE is code, a FigureSpec, or a prompt that transforms the Intake.
A CANDIDATE is a reversible render that cannot silently replace what a reader sees.
A WRAPPER is the consumer-owned caption, label, placement, and asset reference.
A PROJECTION is one consumer-specific use of a selected asset, such as Paper, slides, poster, or HTML.

## Pipeline
```text
QA · WHERE DISPLAY LIVES
   QA1 map and boundary ──► QA2 this design Board vs a paper Board
                        └─► QA3 one unit has a page AND a folder
                        └─► QA4 whether the family needs one main entry door

QB · ONE DISPLAY UNIT
   QB1 contract
       ├─► QB2 Intake      approved source snapshot
       ├─► QB3 Recipe      reproducible transform
       ├─► QB4 Candidates  reversible alternatives
       ├─► QB5 Wrapper     consumer-owned meaning
       └─► QB6 Legacy      no accidental migration

QC · RENDERERS AND PROJECTIONS
   QC1 choose table | figure | diagram | illustration
       └─► QC2 refuse incomplete or unsafe inputs
       └─► QC3 project one selected asset to several consumers

QD · BRIDGES TO OTHER LAYERS
   QD1 Task exports aggregate + provenance
   QD2 Paper Display accepts, binds, and gates a unit
   QD3 Section/sentence cites the selected wrapper

QE · ASSURANCE
   QE1 structural verification and provenance checks
   QE2 a fresh agent follows the whole route
```

The order is deliberate.
First locate ownership.
Then define the unit.
Then decide how it renders.
Only after that attach it to Task, Paper, and sentences.
Verification comes last because it tests the earlier decisions rather than replacing them.

## Pages
### QA · Where Display lives
Display is a reusable layer between evidence and presentation.
These pages distinguish its design Board from a paper's operational Board and distinguish the unit's human page from its on-disk bundle.
The fourth page keeps one real design question visible: whether non-paper consumers need a single public Display entry skill.
QA1-display-map.md
QA2-display-board.md
QA3-unit-page-and-unit-folder.md
QA4-main-entry-door.md

### QB · One Display unit
One unit is the atomic visual artifact.
The pages follow it from its contract, through approved inputs and reproducible rendering, to reversible candidates, Paper-owned wrapper semantics, and compatibility with legacy units.
QB1-unit-contract.md
QB2-display-intake.md
QB3-recipe-and-render.md
QB4-candidates-and-promotion.md
QB5-wrapper-and-placement.md
QB6-legacy-migration.md

### QC · Renderers and projections
The renderer is chosen by the form of the visual, not by whichever skill happens to be available.
Every renderer shares the same Intake and refusal contract.
One accepted asset can then be projected to Paper, slides, posters, or HTML without duplicating evidence.
QC1-renderer-taxonomy.md
QC2-refusal-and-safety.md
QC3-many-consumers.md

### QD · Bridges to other layers
Task owns verified values.
Paper Display owns the visual argument and gate.
Section Edit owns the reader-facing sentence.
These bridges make those handoffs explicit rather than making Display reach into another layer.
QD1-task-to-intake.md
QD2-paper-display-bridge.md
QD3-sentence-and-projection.md

### QE · Assurance and shipping
The final two pages define what can be checked mechanically and what a fresh agent must be able to do.
QE1-verification.md
QE2-fresh-agent.md

## Links
display-unit-contract   ../../display/ref/display-unit-output-contract.md
display-intake-contract ../../display/ref/display-intake-contract.md
intake-manifest         ../../display/ref/intake-manifest.template.yaml
paper-adapter           ../../paper/1-lifecycle/4-display/ref/paper-adapter.md
paper-display-stage     ../../paper/1-lifecycle/haipipe-paper-stage/stages/4-display/stage.md
display-task            ../../task/7_display/haipipe-task-for-display/SKILL.md
paper-board             ../01-haipipe-paper-260725/
QB2b@paper              ../01-haipipe-paper-260725/QB-engine-stage-contract/QB2b-its-name.md
task-board              ../01-haipipe-task-260726/
probe-board             ../01-probe-qa-260726/
boardform-board         ../01-boardform-260722/
haipipe-board           ../../board/haipipe-board/
display-table           ../../display/skills/haipipe-display-table/
display-figure          ../../display/skills/haipipe-display-figure/
display-diagram         ../../display/skills/haipipe-display-diagram/
display-illustration    ../../display/skills/haipipe-display-illustration/
