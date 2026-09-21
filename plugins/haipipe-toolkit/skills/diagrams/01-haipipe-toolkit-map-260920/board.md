# HAI-Pipe Toolkit capability map
spine: Give maintainers and new users one navigable model of the toolkit's skill families, ownership boundaries, Run/Result flows, and human-AI collaboration.
close: Each skill family is assigned to one Job Page with canonical entry links, inputs and outputs, owner-native Workflow Runs, and cross-family handoffs; human decisions and shared human-AI work are explicit; the Board builds and passes its structural check.

## Topic
This generic skill-design Board covers `plugins/haipipe-toolkit/skills/`. It maps reusable capabilities; the canonical instructions remain in each skill's `SKILL.md`. The checkout contained 141 `SKILL.md` files on 2026-09-20. The nine Job Pages below account for the skill families without copying their full instructions. Sibling plugins and upstream projects in `references/` are outside this Board.

The toolkit is the conceptual Block. Each Job is a capability family, each Task/Page is a concise family map, and Runs stay with the skill that owns their execution. This is an architecture view, not a `task-block` execution tree.

## Pipeline
Task and Discovery skills produce owner-native Run Results. Insight and Ideation consume accepted evidence for interpretation and research direction. Page and Paper compose reviewed content, while Design and Display produce visual artifacts. Board and Page provide shared navigation and human-AI work surfaces; Project and utility skills support the other families. These links are a dependency graph with feedback and parallel work, not one mandatory sequence.

Every Workflow is a list of bounded Run Specs and actual Run instances with dependencies and routes. Each Job Page points to its owner's Run contract. A Run is never inferred from a skill folder, a controller pass, or a historical phase label.

## Links
haipipe-board ../../board/haipipe-board/SKILL.md
haipipe-page ../../page/haipipe-page/SKILL.md
page-writing-run ../../page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md
haipipe-run ../../run/haipipe-run/SKILL.md
skill-structure ../../STRUCTURE.md
task-family ../../task/
haipipe-task ../../task/haipipe-task/SKILL.md
run-catalog ../../run/haipipe-run/ref/run-catalog.md
task-hierarchy ../../task/haipipe-task/ref/hierarchy.md
discovery-family ../../discovery/
haipipe-discovery ../../discovery/haipipe-discovery/SKILL.md
insight-family ../../insight/
haipipe-insight ../../insight/haipipe-insight/SKILL.md
insight-workflow ../../insight/haipipe-insight-workflow/SKILL.md
insight-run-workflow ../../insight/haipipe-insight-workflow/ref/run-workflow.md
ideation-family ../../ideation/
haipipe-ideation ../../ideation/haipipe-ideation/SKILL.md
design-family ../../design/
haipipe-design ../../design/haipipe-design/SKILL.md
design-workflow ../../design/haipipe-design-workflow/SKILL.md
paper-family ../../paper/
haipipe-paper ../../paper/haipipe-paper/SKILL.md
haipipe-writing ../../writing/haipipe-writing/SKILL.md
display-family ../../display/
project-family ../../project/
utility-family ../../0_utils/

## Board Map
```text
                         ┌── QB · Task and engineering ──┐
QA · shared contracts ───┤                                ├── owner-native Runs/Results ──▶ QD · Insight ──▶ QE · Ideation ──▶ QG · Paper and writing
                         └── QC · Discovery ─────────────┘                                         └──────────▶ QF · Design ──▶ QH · Display
                              QI · Project and utilities support all Jobs
                              QA · Board and Page coordinate navigation, records, and human-AI work
```

## Pages
### QA · J01 Shared contracts
Board, Page, and Run ownership and the human-AI collaboration model.
QA1-shared-contracts.md

### QB · J02 Task and engineering
Internal execution and the data, model, endpoint, and individual-work skill families.
QB1-task-engineering.md

### QC · J03 Discovery
External evidence acquisition, source review, and synthesis.
QC1-discovery.md

### QD · J04 Insight
Evidence-led interpretation, questions, dependencies, and signed handoffs.
QD1-insight.md

### QE · J05 Ideation
Accepted evidence into research directions and Paper handoffs.
QE1-ideation.md

### QF · J06 Design
An independent creative family that consumes signed Insight and produces verified design artifacts.
QF1-design.md

### QG · J07 Paper and writing
Paper composition and the shared writing capability, including human-AI co-work.
QG1-paper-writing.md

### QH · J08 Display
Figures, tables, diagrams, slides, posters, and other visual outputs.
QH1-display.md

### QI · J09 Project and utilities
Project scaffolding and cross-cutting utility skills.
QI1-project-utilities.md
