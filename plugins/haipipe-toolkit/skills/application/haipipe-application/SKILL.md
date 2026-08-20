---
name: haipipe-application
description: >-
  One door for building an Application Board from an application Brief, Application-local Insight Pages, audience/job Design Pages, and optional independently accepted Artifact Pages. Insight Pages live inside the Application folder but use Task-backed Probe, source/run, DIKW, staleness, and human-reading rules; Design Pages consume only settled Insight handoffs through PageX and never inspect Task/Discovery sources. Use for application setup or status, application insight, DIKW for a design need, message/intervention design, SMS/email/dashboard/checklist/report design, artifact review, deploy, retarget, or iteration. Trigger: application, application board, application insights, insight need, design page, intervention, message design, artifact, SMS, email, dashboard, checklist, report, review, deploy, iterate, PageX insight, /haipipe-application.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.8.0"
  last_updated: "2026-08-20"
  summary: "Application-local Insights: Brief → Insight Pages → Design Pages → optional Artifact Pages, with Task-backed evidence and PageX-only design consumption."
---

# /haipipe-application · understand for this application, then design

Read `PREFERENCES.md` first. This skill is the only user-facing Application door. Resolve the Application root, select one owning Page, and hand it to `haipipe-page` with the matching Page Type and current Page phase.

## Architecture

```text
Task / Discovery evidence
          │ Probe · Task authority
          ▼
Application Board
Brief → Insight Page(s) → Design Page(s) → Artifact projection/Page → review → deploy
             D→I→K→W          │ PageX
```

Application owns the folder, the design need, the contextual Wisdom, and delivery. Task rules still own how an Insight Page crosses Task/Discovery evidence. Folder ownership does not transfer evidence authority.

## Four Page Types

```text
page-type: brief          exactly one · opportunity, audience set, outcome, venue scope, Insight Need Map
page-type: insight        one per application insight question · Task-backed D→I→K→W + Design Handoff
page-type: intervention   many · UI label Design Page · one audience × behavior job × primary venue
page-type: artifact       optional · only an independently accepted/deployed unit promoted from a Design Page
```

Keep `page-type: intervention` as the stable globally unique machine key; call it **Design Page** in user-facing prose. No generic `page-type: design` contract is live.

## Verbs

```text
enter | status | board         resolve the Application root and current frontier
brief | opportunity | venue    create/resume the one Brief Page through fn/brief.md
insight | understand | DIKW    create/resume an Application-local Insight Page through fn/insight.md
missing-insight | evidence-gap release one blocked need through fn/missing-insight.md
intervention | design | message
  | arc | components           create/resume one Design Page through fn/intervention.md
artifact | promote | unit      promote/resume an independently accepted Artifact through fn/artifact.md
review | audit | check         CHECK selected Design/Artifact versions and their trace
deploy | ship | go-live        ship accepted versions only
iterate | round | A/B          route measurements through Task work, refresh Insight, then reopen dependents
feedback | digest              run the existing family feedback procedures
```

No-argument behavior: inside an Application, run `enter .`; outside one, ask for a path or offer to create a Board-shaped Application folder. Never infer an audience, behavior, or venue when that choice changes the design.

## Runtime folder

```text
<application-root>/
├── board.md
├── STATUS.md                         compatibility projection; derive truth from Pages
├── 0-brief/
│   └── A00-brief/
│       ├── A00-brief.md
│       └── pagex/
├── 1-insights/
│   └── I<NN>-<slug>/
│       ├── I<NN>-<slug>.md           page-type: insight
│       ├── probe/                    Task/Discovery evidence cards
│       ├── pagex/                    accepted existing-Page inputs
│       └── display/                  optional evidence views
├── 2-design/
│   └── D<NN>-<audience>-<job>/
│       ├── D<NN>-<audience>-<job>.md page-type: intervention
│       ├── pagex/                    Brief + settled Insight handoffs
│       ├── outline/
│       └── display/                  message previews / interaction mockups
├── 3-artifacts/                      versioned projections and promoted Artifact Pages
├── 4-deploy/                         shipment records; no evidence edits
└── 5-rounds/vYYMMDD/                 feedback, decisions, applied changes
```

Do not create the legacy descriptions/themes/claims/advice ladder or a flat Application-wide `1-probes/`. Each Insight Page owns its own bounded `probe/`; Design Pages own none.

## The two authorities

```text
Application Insights layer
  may PROBE Task/Discovery under haipipe-page-for-insight
  owns D→I→K and application-contextual W

Application Design layer
  may use PageX only
  owns selection, design principles, message roles, concrete content, and acceptance
```

The old sentence “Application owns no Probe” is too broad. The current law is: **Application Design Pages own no Probe; Application Insight Pages may Probe under Task-backed evidence authority.**

## Page flow

```text
Brief
  defines the Application stake and Insight Need Map
    ↓
Insight Page(s)
  settle each load-bearing question as D→I→K→W and publish a Design Handoff
    ↓ PageX exact file/scope binding
Design Page(s)
  translate handoffs into principles, message architecture, repeated message divisions, and rails
    ↓
Artifact
  normally a versioned projection; promote to a Page only when it can pass/fail/deploy independently
    ↓
Review → Deploy → Iterate
```

## Phase behavior

- An Insight Page normally runs the full shared loop: `OUTLINE ⇄ PROBE ⇄ EVIDENCE → DRAFT → REVISE → CHECK`.
- Brief and Design Pages select exact accepted Page material through PageX during OUTLINE and normally skip local PROBE/EVIDENCE.
- A missing load-bearing premise creates/resumes a local Insight Page and holds only the dependent Brief/Design Aim.
- Design Page Content uses one repeated division per message role, touchpoint, panel, section, or other jointly reviewed unit.
- Artifact and projections use REVISE/COMPILE/CHECK for exact visible-version acceptance.
- CHECK remains the human authority for applicability, taste, venue fit, safety, and deployment acceptance.

## Insight-to-design handoff

An Insight Page keeps D/I/K evidence-led and lets W become Application-contextual only after K settles:

```text
Application Need → neutral Question → D → I → K → contextual W → Design Handoff
```

The Design Handoff names finding, strength, boundary, source versions, design consequence, forbidden overreach, and the Brief/Design need it serves. It does not write final message copy.

Design Pages borrow the exact handoff file/scope through PageX. PageX answers “which Page material”; the Design Page answers “which move follows here.” Never copy probe cards or inspect Task `results/` from a Design Page.

## Review and deployment gates

A Design or promoted Artifact is deployable only when all are true:

```text
trace       every substantive move reaches a settled Insight Design Handoff
applicability the borrowed K/W actually covers this audience, context, and outcome
venue       format, length, timing, interaction, and audience rules pass
safety      prohibited moves and uncertainty language pass
version     acceptance names design/handoff and visible render versions
human       the exact visible version is explicitly accepted
```

Deployment records external state but never edits evidence or design to make a failed gate appear green. A changed Insight handoff, Design division, venue constraint, or render reopens acceptance.

## Iteration

```text
deployment log → Task Folder P-B-E-R → Application Insight refresh
                                            │
                                            └─ changed handoff reopens PageX-dependent Design
```

Application may propose the measurement question. Task owns execution; the Application-local Insight Page owns the refreshed DIKW reading and source staleness; the Design Page owns the response.

## Legacy compatibility

Existing Applications remain readable. Do not delete or bulk-rewrite their folders without a separate migration request.

```text
legacy Seed + Venue + Pitch                    → Brief input
legacy Descriptions + Themes + Claims + Advice → candidate local Insight Pages
legacy Narrative + Display + Section-edit     → Design Page and Artifact input
legacy 1-probes/                               → historical bindings, read-only
external Task/Insights Board Pages             → valid PageX inputs; do not move them automatically
```

Compatibility means read-and-fold into the new target, not copy-and-continue the old stage spine.

## Status

Derive status from disk, not prose:

```text
frontier: brief | insight:<id> | design:<id> | artifact:<id> | review | deploy | iterate
maturity: scoped | understood | designed | authored | reviewed | deployed | iterating
```

Also report unresolved Insight needs, stale Probe/PageX bindings, Design Page/message counts, promoted Artifact units, and accepted render versions.

## Internal procedures

```text
fn/brief.md             Brief create/resume and Insight Need Map
fn/insight.md           Application-local Task-backed DIKW Page
fn/missing-insight.md   release a blocked need into fn/insight.md
fn/intervention.md      multi-Page audience/job Design and message divisions
fn/artifact.md          projection-first output; optional Page promotion
fn/feedback.md          family feedback
fn/digest.md            session feedback digestion
```

The old stage specialists remain compatibility readers during migration and are not the target architecture.
