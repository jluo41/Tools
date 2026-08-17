---
name: haipipe-application
description: >-
  One door for composing settled Task/Insight Pages into an intervention. New applications use three globally unique Page Types: Brief (opportunity, audience, outcome, venue, promise), Intervention (insight-to-mechanism/component architecture), and Artifact (one independently reviewable delivery unit). Application never rebuilds evidence: PageX reads settled Insight Pages; missing knowledge routes to `/haipipe-task insight`, where Probe reads Task/Discovery sources. Use for application status, SMS/email/dashboard/checklist/report design, Brief, Intervention, Artifact, review, deploy, retarget, or iteration. Legacy Seed/Descriptions/Themes/Claims/Advice/Venue/Pitch/Narrative/Display/Section commands remain compatibility aliases folded into the three Page contracts. Trigger: application, intervention, application board, brief, message design, component map, artifact, SMS, email, dashboard, checklist, report, review, deploy, iterate, PageX insight, /haipipe-application.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.7.0"
  last_updated: "2026-08-17"
  summary: "Page-first Application architecture: Brief → Intervention → Artifact, consuming settled Task/Insight Pages through PageX and owning no evidence Probe."
---

# /haipipe-application · compose settled insights into an intervention

Read `PREFERENCES.md` first. This skill is the only user-facing Application door. It resolves the application root, selects one Page, and hands that Page to the shared `haipipe-page` lifecycle with the matching Application Page Type.

## Architecture

```text
Task / Discovery evidence
          │ Probe
          ▼
Task / Insights Board: D → I → K → W
          │ settled Insight Page through PageX
          ▼
Application Board
Brief → Intervention → Artifact unit(s) → review → deploy
```

Application owns composition and delivery. It does not own DIKW, Task execution, Discovery search, or evidence settlement.

## Globally unique Page Types

```text
page-type: brief          exactly one · identity, audience, outcome, venue, promise
page-type: intervention   exactly one · mechanisms, strategy, components, variants
page-type: artifact       one per independently approvable delivery unit
```

Application does not use `page-type: opening`; Paper owns Opening. It does not use `page-type: design`; Board's generic Design Page compares candidates and closes on selection. The distinct names let `haipipe-page` resolve every type without family context.

## Verbs

```text
enter | status | board        resolve the application root and show Page frontier
brief | opportunity | venue   create/resume the one Brief Page through fn/brief.md
intervention | strategy |
  design | arc | components   create/resume the one Intervention Page through fn/intervention.md
artifact | draft | write |
  message | unit              create/resume an Artifact Page through fn/artifact.md
review | audit | check        CHECK the selected Artifact(s) and their trace
deploy | ship | go-live       ship accepted Artifact versions only
iterate | round | A/B         record delivery feedback; measurement routes to Task/Insights
missing-insight | evidence-gap route one consumer-neutral question through fn/missing-insight.md
feedback | digest             run the existing family feedback procedures
```

No-argument behavior: inside an application, run `enter .`; outside one, ask for a path or offer to create a Board-shaped application folder. Never infer a venue when the choice changes the deliverable.

## Runtime folder

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
├── 0-artifacts/              deployable projections, versioned
└── 1-rounds/vYYMMDD/         decisions, deployment feedback, applied changes
```

New applications do not create `1-probes/`, descriptions/themes/claims/advice stage folders, or a separate narrative/display/section-edit spine. Page plugins and Page phases carry those concerns where they belong.

## Page flow

```text
Brief
  selects settled Insight Pages and pins audience, outcome, venue, promise
    ↓
Intervention
  maps Insight K/W rows to mechanism, principles, components, variants, rails
    ↓
Artifact
  executes one component handoff as concrete, reviewable content
    ↓
Review
  checks venue fit, trace, safety, handoff/render versions
    ↓
Deploy
  ships accepted versions only
    ↓
Iterate
  delivery data → Task execution → refreshed Insight Page → PageX → revise
```

All three Pages use the shared Page phases `OUTLINE → DRAFT → PROBE → EVIDENCE → REVISE → COMPILE → CHECK`, but Application narrows their meaning:

- Brief and Intervention normally skip PROBE/EVIDENCE because their evidence arrives as settled PageX inputs.
- A missing insight routes to Task/Insights Board and places the current Page on HOLD where load-bearing.
- Artifact uses REVISE/COMPILE/CHECK for concrete content and render acceptance.
- CHECK remains the human authority for taste, venue fit, safety, and deployment acceptance.

## PageX and missing insights

PageX is Application's only evidence input surface:

```text
existing settled Insight Page ──▶ pagex/ ──▶ Brief or Intervention
missing knowledge ──▶ missing-insight request ──▶ /haipipe-task insight
                   ──▶ Insight Page Probe ──▶ settled Page ──▶ PageX return
```

Never inspect Task `results/`, call Task/Discovery as an Application evidence worker, copy another Page's probe cards, or settle a claim inside Application. The application-specific stake stays on Brief/Intervention; the question sent to Task is rewritten in consumer-neutral language.

## Review and deployment gates

An Artifact is deployable only when all are true:

```text
trace       every substantive move reaches an Intervention principle and Insight Page
handoff     the Artifact executes the current component row
venue       format, length, interaction, and audience rules pass
safety      prohibited moves and uncertainty language pass
version     acceptance names handoff version and render version
human       the visible version is explicitly accepted
```

Deployment records external state but never edits evidence or design to make a failed gate appear green. A changed handoff or render reopens Artifact acceptance.

## Iteration

Keep application rounds for product decisions and applied changes. Treat deployment measurements as Task data:

```text
deployment log → Task Folder P-B-E-R → Task/Insight refresh → PageX
                                                │
                                                └─ source change reopens dependent design
```

Application may propose the measurement question and create the Task/Insight request, but Task owns execution and DIKW interpretation.

## Legacy compatibility

Existing applications remain readable. Do not delete or bulk-rewrite their folders without a separate migration request.

```text
legacy Seed + Venue + Pitch                    → Brief input
legacy Descriptions + Themes + Claims + Advice → candidate Insight material;
                                                   migrate to Task/Insights before reuse
legacy Narrative + Display + Section-edit     → Intervention and Artifact input
legacy 1-probes/                              → historical evidence bindings, read-only
```

Legacy aliases route to the owning new Page:

```text
seed | venue | pitch                         → brief
descriptions | themes | claims | advice      → missing-insight / Task Board migration
narrative | display                          → intervention
section-edit | draft                         → artifact
```

Compatibility means read-and-fold, not copy-and-continue. New work lands on the three target Page Types.

## Status

Derive status from disk, not prose:

```text
frontier: brief | intervention | artifact:<unit> | review | deploy | iterate
maturity: briefed | designed | authored | reviewed | deployed | iterating
```

Also report unresolved PageX bindings, missing Insight requests, Artifact units, and accepted render versions. The Gate Ledger may remain during migration, but new completion authority is the Page's own Aim/State and acceptance record.

## Internal procedures

```text
fn/brief.md             Brief create/resume and legacy fold
fn/intervention.md      Intervention create/resume and component mapping
fn/artifact.md          Artifact grain, creation, version, projection
fn/missing-insight.md   consumer-neutral request to Task/Insights Board
fn/feedback.md          family feedback
fn/digest.md            session feedback digestion
```

The old stage specialists remain compatibility readers during migration and are not the target architecture.
