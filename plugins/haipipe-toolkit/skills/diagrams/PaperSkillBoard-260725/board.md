# Paper Page architecture: compose a paper from accepted Pages

spine: Seed fixes the venue-free paper identity; Venue records one desk; Narrative orders claims for that desk; Section executes one Narrative row; Round routes feedback; `/haipipe-paper status` reports the graph.
dialect: paper
paper-root: _fixture
close: The five Page Types, Paper composition boundary, venue catalog, and validation route agree; retired stage-era designs remain archived and are not registered as live Pages.
session: 8d4c966d-8db2-443b-9194-8dcb8a14b600

## Topic

This Board explains the current Paper architecture.
The useful design work now lives on typed Pages, so the Paper door stays small.
It selects Pages, runs their shared lifecycle, assembles accepted outputs, and does not maintain a second stage engine.

- **QA · Architecture** fixes the Page graph and ownership boundaries.
- **QBt · Page Types** carries one current specimen for each Paper Page Type.
- **QBv · Venues** keeps the reusable venue catalog, one Page per target.
- **QC · Composition and validation** explains the thin Paper door, Page-local plugins, and the tests that prove their route.

The old Delivery, Delivery Element, stage Engine, and engine-skill mirror groups are preserved under `_archive/`.
They are historical design evidence, not active Paper routes.

## Pipeline

```text
Probe
  ├── existing Board Pages ── PageX ─────────────────────┐
  └── Task / Discovery ────── QA Probe ──────────────────┤
                                                         ▼
                                               owning Page evidence

Seed + Venue + accepted Page evidence
                │
                ▼
        Narrative @ Venue
                │ one row per reader unit
                ▼
          Section Pages ──▶ assemble/build ──▶ Round
                ▲                                  │
                └──────── checked routed work ─────┘

`/haipipe-paper status [family]` = regenerated measurement over Pages and
plugin units, a command retired from being a sixth Page Type (dash) on 260820
```

Probe is the evidence-acquisition family with two typed lanes.
PageX reads bounded context from existing accepted Pages during OUTLINE.
QA Probe asks unresolved Task or Discovery questions during PROBE/EVIDENCE and lands the answer on the consuming Page.
The lanes remain physically separate as `pagex/` and `probe/`.

## Board Structure

```text
PaperSkillBoard-260725/
├── 1-QA-architecture/       current graph and boundaries
├── 2-QBt-page-types/        five live Paper Page Type specimens
├── 3-QBv-venue-packs/       sixteen venue targets
├── 4-QC-composition/        Paper composition and validation
├── _archive/                retired stage-era design, preserved
└── board/                   generated site, never hand-edited
```

The retained numeric prefixes preserve stable historical paths.
`## Pages` is the live registry.

## Related Folders

@ ../../paper/ | Current Paper family
- README.md
- haipipe-paper/SKILL.md
- page-types/
@ ../../board/haipipe-page/ | Shared Page contract
- SKILL.md
@ ../../board/page-plugins/ | Shared Page plugins
- haipipe-plugin-pagex/SKILL.md
- haipipe-plugin-probe/SKILL.md

## Pages

### QA · Architecture
The smallest graph that explains where paper decisions and evidence live.

```text
QA1  Page graph
QA2  ownership boundary
```
QA1-paper-page-graph.md
QA2-ownership-boundary.md

### QBt · Page Types
One live specimen for each Page Type owned by the Paper family.

```text
QBt1 Seed       stable identity
QBt2 Venue      external desk
QBt3 Narrative  venue-aligned claim and section map
QBt4 Section    one executable Narrative row
QBt5 Round      one feedback cycle
```
QBt1-for-seed.md
QBt2-for-venue.md
QBt3-for-narrative.md
QBt4-for-section.md
QBt5-for-round.md

### QBv · Venues
One evidence-backed Page per journal, funder, or patent target.
These Pages report desk rules and observed patterns; they do not choose the paper's target.

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

### QC · Composition and validation
How the thin Paper door composes typed Pages, delegates evidence/build work to Page-local plugins, and proves that route works.

```text
QC1  Paper routing and assembly
QC2  PageX, Probe, Bibex, Display, LaTeX, and Word boundaries
QC3  minimal paper graph fixture
QC4  fresh-context agent behavior
```
QC1-paper-door.md
QC2-page-local-plugins.md
QC3-minimal-fixture.md
QC4-fresh-agent-run.md

## Links

## Log

260820 · Replaced the stage-era Board registry with the six-type Page architecture.
260820 · Kept all sixteen Venue Pages live and archived the former QA, Delivery, QBt, Engine, and Execute groups intact.
260820 · Grouped PageX under Probe while preserving separate PageX and Task/Discovery QA records.
260820 · Merged validation into QC because the fixture and fresh-agent run prove the same composition contract.
260820 · Retired Dash (QBt6) as a sixth Page Type: JL proposed merging it into Narrative, but only one of its four families (section) was Narrative-shaped, so the merge was rejected in favor of dropping it outright. It survives as `/haipipe-paper status [family]`, a command, not a Page Type. QBt6 moved to `_archive/5-QBt6-dash-retired-260820/`.
