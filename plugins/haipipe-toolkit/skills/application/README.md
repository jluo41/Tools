# Application skill family

Application turns settled Insight Pages into an audience-facing intervention.
It is a delivery family like Paper, not a second evidence pipeline.

```text
Task / Insights Board                Delivery Boards
Data → Information → Knowledge → Wisdom
                    │ PageX          ├── Paper: Opening → Narrative → Section
                    └───────────────▶ └── Application: Brief → Intervention → Artifact
```

## Canonical boundary

| Family | Owns | Does not own |
|---|---|---|
| Task/Insights | execution, Probe, DIKW settlement, reusable Insight handoff | paper/message framing |
| Paper | academic selection, argument order, manuscript units | Task/Discovery evidence execution |
| Application | audience/venue promise, intervention architecture, delivery units | DIKW, raw evidence Probe |

Application reads evidence only as settled `page-type: insight` Pages through
PageX. A missing premise is routed back to `/haipipe-task insight`; it is never
answered in an Application-local `probe/`.

## Globally unique Page Types

```text
application/page-types/
├── haipipe-page-for-brief/          page-type: brief
├── haipipe-page-for-intervention/   page-type: intervention
└── haipipe-page-for-artifact/       page-type: artifact
```

The names avoid two resolver collisions:

- Paper owns `page-type: opening`; Application's opening concern is named Brief.
- Board owns generic `page-type: design`; Application's delivery architecture is
  named Intervention.

### Brief

Exactly one per application. It owns opportunity, audience and behavior,
observable outcome and kill criteria, selected Insight Pages, venue, promise,
and the bounded handoff to Intervention.

### Intervention

Exactly one per application. It maps selected Insight K/W rows into theory of
change, intervention principles, message/interaction strategy, components,
variants, safety rails, and one handoff row per Artifact unit. Narrative is a
conditional division here, not an Application Page Type.

### Artifact

One per independently approvable delivery unit: message set, email, checklist
block, dashboard card, UI panel, report section, or audience segment. Variants
reviewed together remain divisions inside one Page. Acceptance binds both the
Intervention handoff version and the visible render version.

## Target runtime

```text
<application-root>/
├── board.md
├── STATUS.md
├── 0-lifecycle/
│   ├── S-Brief-0-brief/
│   │   ├── S-Brief-0-brief.md
│   │   └── pagex/
│   ├── S-Intervention-0-intervention/
│   │   ├── S-Intervention-0-intervention.md
│   │   ├── pagex/
│   │   ├── outline/
│   │   └── display/
│   ├── S-Artifact-Dash/
│   └── S-Artifact-<unit>-<slug>/
│       ├── S-Artifact-<unit>-<slug>.md
│       └── display/ · word/ · pagex/ as required
├── 0-artifacts/              versioned deployable projections
└── 1-rounds/vYYMMDD/         decisions and applied iteration work
```

New applications do not create a local evidence ladder, `1-probes/`, or
separate Narrative/Display/Section-edit stages.

## Skill-tree target

```text
application/
├── haipipe-application/      THE one user-facing door
│   ├── SKILL.md
│   ├── PREFERENCES.md
│   └── fn/
│       ├── brief.md
│       ├── intervention.md
│       ├── artifact.md
│       ├── missing-insight.md
│       ├── feedback.md
│       └── digest.md
├── page-types/               three Page Type contracts
├── venue/                    channel knowledge packs, not lifecycle stages
├── 0-enter/                  legacy console/round compatibility during migration
├── 1-lifecycle/              legacy stage readers during migration
├── 2-phase/                  legacy Application-specific phase workers
├── 3-deliver/                legacy artifact/review/deploy specialists
└── 4-iterate/                legacy iteration specialist
```

The last four numbered groups remain readable until existing interventions are
migrated. They are compatibility surfaces, not the shape new work should copy.

## User-facing Skill Bar

```text
🧭 Outline   Brief → Intervention → Artifact map
📄 Page      current Page and Page lifecycle
🔗 PageX     settled Insight inputs and bounded cross-Page reads
🖼 Display   message mockups, dashboard panels, diagrams, report visuals
📂 Folder    application files and projections
📦 Artifact  current deployable preview/version
🚀 Deploy    acceptance gate and external delivery
💬 Chat      current Page conversation
```

Probe is deliberately absent. The Task/Insights Board owns Probe.

## Router

```text
/haipipe-application enter|status      resolve Board and frontier
/haipipe-application brief            one Brief Page
/haipipe-application intervention     one Intervention Page
/haipipe-application artifact [unit]  one Artifact Page
/haipipe-application review           Artifact CHECK and cross-unit audit
/haipipe-application deploy           accepted versions only
/haipipe-application iterate          product round; measurements route to Task
/haipipe-application missing-insight  Task/Insights Board request
```

Legacy verb routing:

| Legacy verb | Target |
|---|---|
| seed, venue, pitch | Brief |
| descriptions, themes, claims, advice | migrate/request Task Insight |
| narrative, display | Intervention |
| section-edit, draft | Artifact |

## Lifecycle and evidence return

```text
Brief
  ↓ accepted handoff
Intervention
  ↓ one component row per independently approvable unit
Artifact Page(s)
  ↓ trace + venue + safety + version + human acceptance
Deploy
  ↓ measurement question
Task P-B-E-R
  ↓
Insight Page refresh
  ↓ PageX staleness/revision signal
Intervention / Artifact revision
```

All Pages inherit the shared Page phases. Brief and Intervention normally skip
PROBE/EVIDENCE because their evidence is already settled behind PageX. Artifact
uses REVISE, COMPILE, and CHECK for concrete content and render acceptance.

## Missing Insight contract

A missing insight record carries:

```text
application stake   which Brief/Intervention decision is blocked
neutral question    what Task/Insights can answer without consumer vocabulary
target level        Data | Information | Knowledge | Wisdom
destination         Task/Insights Board
returned page       Page path, state, refresh/version
```

The Task/Insight Page owns source selection, Probe, DIKW trace, and settlement.
Application binds the settled result through PageX and resumes its own decision.

## Compatibility migration

Migration is explicit and non-destructive:

```text
Seed + Venue + Pitch                    → Brief
Descriptions + Themes + Claims + Advice → Task/Insight candidates
Narrative + Display                     → Intervention
Section-edit + drafted outputs          → Artifact Pages and projections
legacy 1-probes/                        → read-only provenance during migration
```

Do not delete legacy files or pretend they are settled Insight Pages. First
create/identify the Task Board, construct consumer-neutral Insight Pages with
source trace, then bind those Pages from Brief/Intervention.

## Status vocabulary

```text
frontier: brief | intervention | artifact:<unit> | review | deploy | iterate
maturity: briefed | designed | authored | reviewed | deployed | iterating
```

Status also reports missing Insight requests, stale PageX bindings, Artifact
unit count, and accepted handoff/render versions.
