# /haipipe-application: an InsightBoard and a DesignBoard

spine: An Application is two named boards. A `<DataSubject>-InsightBoard` is headed by one Meta Page saying what data exists plus four question registers saying what is asked of each rung, and holds one page per LEVEL, D then I then K then W, under Task-backed evidence authority; a `<DesignTopic>-DesignBoard` is headed by one Brief saying what is being built and for whom, and holds Design Pages that consume signed Design Handoffs through PageX, propose each message as a released BET before composing it, and carry each landed unit as a division with its own acceptance row.
close: Meta, Insight, Brief, and Design Page contracts ship from the Application skill set; the public Application door routes all four; Design Pages never Probe; the Application ends at ACCEPTED and hands shipping and measurement to the task layer; one fresh-context run proves the route and Board checks expose any remaining migration debt.
session: 9bab8e87-20eb-4ebf-8e73-b23cec29ad11

## Topic

This is the Skill-Board for the Application family. It answers one question:
how do settled data and analysis become audience-facing messages, interfaces,
reports, or other designed artifacts without turning Design into another evidence
pipeline, and without either half's reader having to read the other's queue?

- **QA · Architecture** fixes the ownership wall, runtime folders, board naming,
  and cardinality.
- **QI · Insights** defines the InsightBoard's DIKW layer and Design Handoff.
- **QD · Design** defines the DesignBoard's layer, its acceptance grain, and its
  projections, mirroring QI on the delivery side.
- **QBt · Page Types** specifies Meta, Brief, and Design, and records why Artifact
  was retired; QI owns the fourth live Page Type specimen, Insight.
- **QC3 · The Workflow** carries the RUN head: five journey phases named by their
  authority page, six gates, and the two loops the lanes turn in.
- **QB · Legacy Delivery** preserves the old ladder only as migration evidence.
- **QBv · Venue Packs** supplies channel constraints.
- **QC · Engine** maps public verbs to Page contracts, and its QC1 `skill/`
  plugin ranks the skills that stand behind them.
- **QF · Execute** records mechanical and fresh-context validation.

## Pipeline

```text
Task folders · Discovery folders · accepted existing Pages
                    │
                    │ Probe only when an Insight Page needs new evidence
                    ▼
🔎 <DataSubject>-InsightBoard          🎨 <DesignTopic>-DesignBoard
┌────────────────────────┐             ┌────────────────────────┐
│ 📊 MT00-meta           │             │ 📌 BR00-brief          │
│ sources · grain        │             │ audience · outcome     │
│ window · freshness     │             │ venue scope · kill     │
│ holds NO question      │             │ born-of: · needs OUT   │
│ 📋 MT01-MT04 registers │             └───────────┬────────────┘
│ one per rung · QD/QI/  │                         ▼
│ QK/QW ids              │             ┌────────────────────────┐
└───────────┬────────────┘   PageX     │ 🎨 DS<NN> Design Pages │
            ▼              ────────────▶│ audience × job × venue │
┌────────────────────────┐  a SIGNED   │ 📇 direction/ the BETS │
│ D → I → K → W          │  handoff    │ 🎨 design/    the UNITS│
│ one page per LEVEL     │             │ 📱 render/    what the │
│ four Page Types        │             │    recipient sees      │
│ + Design Handoff ✋    │             │ divisions, each with   │
└────────────────────────┘             │ accepted: ✋           │
            ▲ PageX                    └───────────┬────────────┘
            │                                      ▼
    accepted Pages                          ✅ ACCEPTED · STOP

shipping, the experiment, and data collection are TASK-LAYER work
```

The two authorities are deliberately split:

```text
placement / consumer authority       evidence authority
──────────────────────────────       ──────────────────────────────
Application owns the InsightBoard    Task rules source/run/staleness
Brief states the need                Probe reaches Task/Discovery
Meta rosters who took it             human reads the run-bound result
Insight publishes Design Handoff     Task owns shipping and measurement
```

## Board Map

```text
QA architecture ──▶ QI insights ──▶ QBt page contracts ──▶ QC routing ──▶ QF proof
       │                   │                 ▲              ▲
       │                   └──── PageX ─────▶ QD design ────┘
       └──── QB legacy migration      QBv venue constraints ─────────────┘
```

## Related Folders

@ ../../application/ | Shipping Application skill family
- README.md
@ ../../application/haipipe-application/ | Public Application door
- SKILL.md
- CHANGELOG.md
- PREFERENCES.md
@ ../../application/page-types/ | Application-owned Page Types
- haipipe-page-for-meta/SKILL.md
- haipipe-page-for-data/SKILL.md
- haipipe-page-for-information/SKILL.md
- haipipe-page-for-knowledge/SKILL.md
- haipipe-page-for-wisdom/SKILL.md
- haipipe-page-for-brief/SKILL.md
- haipipe-page-for-principle/SKILL.md
- haipipe-page-for-design/SKILL.md
@ . | This Application design Board
- board.md

## Board Structure

```text
ApplicationSkillBoard-260802/
├── board.md
├── 1-QA-design/              architecture and runtime shape
├── 2-QB-delivery/            legacy ladder migration record
├── 3-QBv-venue-packs/        channel constraints
├── 4-QC-engine/              public routing · QC1 carries the skill/ list
├── 5-QF-execute/             checks and fresh-context proof
├── 6-QBt-page-types/         Meta · Brief · Design · Artifact retirement
├── 7-QI-insights/            InsightBoard layer and Page Type
├── 8-QD-design/              DesignBoard layer, acceptance grain, projections,
│                             and the design-as-bets family (QD3)
├── _fixture/                 validation fixture
└── board/                    generated site
```

The logical pipeline places QI between QA and QBt. Its folder is numbered `7-`
because this revision preserves every existing group path; `## Pages` remains
the reading authority.

## Pages

### QA · Architecture
What Application owns, where its runtime files live, and how evidence work stays
separate from design work. QA6 adds the two InsightBoard layouts ruled 260823.

QA0-the-board-map.md
QA1-the-folder-map.md
QA2-the-skill-set.md
QA3-the-intervention-board.md
QA4-evidence-channel.md
QA5-board-naming.md
QA6-the-two-layouts.md

### QB · Legacy Delivery
The previous lifecycle ladder retained as migration evidence. These pages do not
override the four current Page Type contracts.

QB0-the-lifecycle-board.md
QB1-opening.md
QB2-data.md
QB3-insight.md
QB4-claims.md
QB5-design.md
QB6-display.md
QB7-artifact.md
QB8-deploy.md
QB9-iterate.md

### QBv · Delivery Venue
One page per delivery venue pack.

QBv1-sms.md
QBv2-email.md
QBv3-dashboard.md
QBv4-report.md
QBv5-push.md
QBv6-reminder.md
QBv7-checklist.md
QBv8-ui-card.md

### QC · Engine
How the public Application door routes to the Page contracts, and how the RUN head drives them. QC3 carries the five-phase machine; QC2 is kept as the record of the stage engine it replaced. The six
`Skill-<n>` pages were deleted on 260820: a Skill page COPIED a SKILL.md into
board prose, so five of the six documented skills that had been moved to `_old/`
hours earlier. QC1 now carries a `skill/` plugin list instead, which stores a
name rather than a copy and reads each skill's version and description live.

QC1-delivery-skill-map.md
QC2-stage-engine.md
QC3-the-workflow.md

### QF · Execute
Mechanical checks, Board receipts, and fresh-context skill validation.

QF1-execution-map.md
QF2-fresh-agent-run.md

### QBt · Page Types this family owns
The head pages of both boards, the Design Page, and the record of why Artifact
was retired. The machine key is `page-type: design`: the `intervention` key was
dropped on 260820 so one concept carries one word.

QBt1-for-brief.md
QBt2-for-design.md
QBt3-for-artifact.md
QBt4-for-meta.md

### QI · Insights
How one Application-local Page turns Task-backed evidence into a bounded Design
Handoff, including the missing-insight route.

QI0-the-local-insights-layer.md
QI1-the-insight-page.md
QI2-insight-to-design-handoff.md

### QD · Design
The delivery-side counterpart to QI. Where the DesignBoard stops, what one
signature covers, and why the rendered output is derived rather than a Page.
QBt2 keeps the Design Page's shape; these pages own its rules. QD3 adds the 260824 design family, where a design is a BET declared before the artifact exists.

QD0-the-design-layer.md
QD1-the-acceptance-grain.md
QD2-projections.md
QD3-design-as-bets.md

## Links
paper-board ../PaperSkillBoard-260725/board.md
README.md ../../application/README.md
PHILOSOPHY.md ../../application/_old/PHILOSOPHY.md
haipipe-application/ ../../application/haipipe-application/
for-brief/ ../../application/page-types/haipipe-page-for-brief/
for-insight/ ../../task/page-types/haipipe-page-for-insight/
for-design/ ../../application/page-types/haipipe-page-for-design/
for-meta/ ../../application/page-types/haipipe-page-for-meta/
for-principle/ ../../application/page-types/haipipe-page-for-principle/
for-wisdom/ ../../application/page-types/haipipe-page-for-wisdom/
for-question/ ../../application/page-types/haipipe-page-for-question/
haipipe-design/ ../../application/haipipe-design/
workflow/ ../../application/haipipe-application-workflow/
partition.md ../../application/haipipe-application/ref/partition.md
direction-plugin/ ../../board/page-plugins/haipipe-plugin-direction/
design-plugin/ ../../board/page-plugins/haipipe-plugin-design/
