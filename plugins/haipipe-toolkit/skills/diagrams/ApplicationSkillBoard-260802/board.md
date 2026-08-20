# /haipipe-application: Brief → Insights → Design → Artifacts

spine: An Application first states the audience, outcome, and delivery boundary in one Brief; it then builds Application-local Insight Pages with Task-backed evidence authority; many Design Pages consume exact Insight Design Handoffs through PageX; concrete messages and interfaces remain Design projections unless one unit needs an independent acceptance or deployment lifecycle.
close: Brief, Insight, Design, and optional Artifact Page contracts ship from the Application skill set; the public Application door routes all four; Design Pages never Probe; one fresh-context run proves the route and Board checks expose any remaining migration debt.
session: 9bab8e87-20eb-4ebf-8e73-b23cec29ad11

## Topic

This is the Skill-Board for the Application family. It answers one question:
how do settled data and analysis become audience-facing messages, interfaces,
reports, or other designed artifacts without turning Design into another evidence
pipeline?

- **QA · Architecture** fixes the ownership wall, runtime folders, and cardinality.
- **QI · Insights** defines the Application-local DIKW layer and Design Handoff.
- **QBt · Page Types** specifies Brief, Design, and optional Artifact; QI owns the
  fourth Page Type specimen, Insight.
- **QB · Legacy Delivery** preserves the old ladder only as migration evidence.
- **QBv · Venue Packs** supplies channel constraints.
- **QC · Engine** maps public verbs to Page contracts.
- **QF · Execute** records mechanical and fresh-context validation.

## Pipeline

```text
Task folders · Discovery folders · accepted existing Pages
                    │
                    │ Probe only when an Insight Page needs new evidence
                    ▼
┌────────────┐   ┌──────────────────────┐   ┌─────────────────────────┐
│ 📌 Brief   │──▶│ 🔎 Insight Pages × N │──▶│ 🎨 Design Pages × N      │
│ one app    │   │ D → I → K → W        │   │ audience × job × venue  │
└────────────┘   │ + Design Handoff     │   │ message/unit divisions  │
                 └──────────────────────┘   └────────────┬────────────┘
                         ▲ PageX                         │ projection first
                         │                               ▼
                 accepted Pages               ┌───────────────────────┐
                                              │ 📦 Artifact Pages 0..N│
                                              │ only if independently │
                                              │ governed              │
                                              └───────────┬───────────┘
                                                          ▼
                                                   🚀 Deploy · 🔁 Rounds
```

The two authorities are deliberately split:

```text
placement / consumer authority       evidence authority
──────────────────────────────       ──────────────────────────────
Application owns 1-insights/         Task rules source/run/staleness
Brief/Design state the need           Probe reaches Task/Discovery
Insight publishes Design Handoff      human reads the run-bound result
```

## Board Map

```text
QA architecture ──▶ QI insights ──▶ QBt page contracts ──▶ QC routing ──▶ QF proof
       │                   │                 ▲
       │                   └──── PageX ──────┘
       └──── QB legacy migration      QBv venue constraints ─────────────┘
```

## Related Folders

@ ../../application/ | Shipping Application skill family
- README.md
- PHILOSOPHY.md
@ ../../application/haipipe-application/ | Public Application door
- SKILL.md
- CHANGELOG.md
- PREFERENCES.md
@ ../../application/page-types/ | Application-owned Page Types
- haipipe-page-for-brief/SKILL.md
- haipipe-page-for-insight/SKILL.md
- haipipe-page-for-intervention/SKILL.md
- haipipe-page-for-artifact/SKILL.md
@ . | This Application design Board
- board.md

## Board Structure

```text
ApplicationSkillBoard-260802/
├── board.md
├── 1-QA-design/              architecture and runtime shape
├── 2-QB-delivery/            legacy ladder migration record
├── 3-QBv-venue-packs/        channel constraints
├── 4-QC-engine/              public routing and compatibility
├── 5-QF-execute/             checks and fresh-context proof
├── 6-QBt-page-types/         Brief · Design · Artifact
├── 7-QI-insights/            local Insight layer and Page Type
├── _fixture/                 validation fixture
└── board/                    generated site
```

The logical pipeline places QI between QA and QBt. Its folder is numbered `7-`
because this revision preserves every existing group path; `## Pages` remains
the reading authority.

## Pages

### QA · Architecture
What Application owns, where its runtime files live, and how evidence work stays
separate from design work.

QA0-the-board-map.md
QA1-the-folder-map.md
QA2-the-skill-set.md
QA3-the-intervention-board.md
QA4-evidence-channel.md

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
How the public Application door and compatibility skills route to the four Page
contracts.

QC1-delivery-skill-map.md
QC2-stage-engine.md
Skill-0-haipipe-application.md
Skill-1-haipipe-application-enter.md
Skill-2-haipipe-application-lifecycle.md
Skill-3-haipipe-application-probe.md
Skill-4-haipipe-application-draft.md
Skill-5-haipipe-application-check.md

### QF · Execute
Mechanical checks, Board receipts, and fresh-context skill validation.

QF1-execution-map.md
QF2-fresh-agent-run.md

### QBt · Page Types this family owns
The remaining three Page Type specimens. The user-facing term **Design Page**
keeps the globally unique machine key `page-type: intervention`.

QBt1-for-brief.md
QBt2-for-intervention.md
QBt3-for-artifact.md

### QI · Insights
How one Application-local Page turns Task-backed evidence into a bounded Design
Handoff, including the missing-insight route.

QI0-the-local-insights-layer.md
QI1-the-insight-page.md
QI2-insight-to-design-handoff.md

## Links
QBv1@paper ../PaperSkillBoard-260725/3-QBv-venue-packs/QBv1-misq/QBv1-misq.md
README.md ../../application/README.md
PHILOSOPHY.md ../../application/PHILOSOPHY.md
haipipe-application/ ../../application/haipipe-application/
for-brief/ ../../application/page-types/haipipe-page-for-brief/
for-insight/ ../../application/page-types/haipipe-page-for-insight/
for-intervention/ ../../application/page-types/haipipe-page-for-intervention/
for-artifact/ ../../application/page-types/haipipe-page-for-artifact/
