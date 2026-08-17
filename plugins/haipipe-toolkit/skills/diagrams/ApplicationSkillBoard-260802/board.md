# /haipipe-application: Insight Pages → Brief → Intervention → Artifact

spine: Application is a composition system, not a second evidence pipeline. It reads settled consumer-neutral Insight Pages through PageX, fixes the opportunity and promise in a Brief, maps insights into mechanisms and components in an Intervention, and realizes each independently approvable delivery unit as an Artifact.
close: Brief, Intervention, and every Artifact have an owning Page Type, explicit PageX lineage, and a reviewable acceptance state; missing knowledge is routed back to the Task/Insights Board rather than probed inside Application.
session: 9bab8e87-20eb-4ebf-8e73-b23cec29ad11

## Topic

This is a **Skill-Board** for the Application family, organized like the Paper family's Skill-Board at `paper-board/` and citing it wherever a ruling is family-generic.
Cast: JL = the one who decides. CC = Claude Code, who does the work.

- **QA · Design** defines the Application system and the ownership wall: Task/Insight owns evidence; Application owns recomposition.
- **QB · Delivery** preserves the old ladder as migration history. New applications do not copy it.
- **QBt · Page Types** is the canonical Application roster: Brief, Intervention, Artifact.
- **QBv · Delivery Venue** holds channel knowledge used by Brief and downstream Artifact constraints.
- **QC · Engine** records the old engine proposal and the compatibility routes that must eventually fold into the Page-first door.
- **QF · Execute** records bounded runs, checks, receipts, and fresh-agent evidence against `_fixture/`.

`QD · Working` and `QE · Sharing` are intentionally absent: live Board interaction, hosting, and mounts are owned by `/haipipe-board`. DIKW work is also absent by design; it lives on the Task/Insights Board.

## Pipeline

```text
Task/Discovery folders
       │ Probe · owned by Task/Insight
       ▼
Task/Insights Board · D → I → K → W
       │ settled Insight Pages through PageX
       ▼
QBt · APPLICATION PAGE TYPES
       Brief → Intervention → Artifact unit(s)
         │         │              │
         │         │              └─ review → deploy → iterate
         │         └─ mechanism · components · variants · safety
         └─ opportunity · audience · outcome · venue · promise
       ▲
       └── QBv · venue pack constraints
```

An Application Page may ask for a missing insight, but it cannot answer that question locally. The door opens or reuses an Insight Page on the Task Board, waits for settlement, then refreshes the PageX binding.

## Board Map

```text
      evidence owner                 composition owner                 delivery tail
┌────────────────────────┐    ┌────────────────────────────┐    ┌────────────────────┐
│ Task/Insights Board    │    │ Application Board          │    │ review/deploy       │
│ Probe → Task/Discovery │    │ QBt1 Brief                 │    │ iterate              │
│ Insight D→I→K→W        │───▶│ QBt2 Intervention          │───▶│ runtime receipts     │
│ settled PageX export   │    │ QBt3 Artifact × n          │    │ reopen owning Page   │
└────────────────────────┘    └─────────────┬──────────────┘    └────────────────────┘
                                           ▲
                                  ┌────────┴────────┐
                                  │ QBv venue packs │
                                  └─────────────────┘

QB1-QB9 and QC1-QC2 remain migration evidence. They do not override the QBt contracts.
```

## Related Folders

Open the shipping Application skills, the Board engine that renders them, or this Board's own source without leaving the Index.
The Paper precedent board is cited per-page as the `@paper` token, not browsed here, because pointing Related Folders at a sibling board's generated tree emits cross-board links at the wrong depth.
@ ../../application/ | Application skill family
- README.md
- PHILOSOPHY.md
@ ../../board/haipipe-board/ | Board engine and canonical contract
- SKILL.md
@ . | This Application design Board
- board.md

## Board Structure

This Board has one editable Board-Folder and one generated Board-Webpage site.
`_fixture/` holds one inspectable intervention (seeded from `designs/Project-Application-SMSDesign/applications/01_sms_young_male`) used by Execute records; the leading underscore keeps it out of page discovery.

```text
ApplicationSkillBoard-260802/
├── board.md                  Board-level source and page registry
├── 1-QA-design/              design pages: system map, folders, the intervention board
│   └── QA1-the-folder-map/   one page, one folder
│       └── QA1-the-folder-map.md    the page: the only .md discovery reads here
├── 2-QB-delivery/            consumer-facing delivery pages: the ladder + the tail
├── 3-QBv-venue-packs/        one page per venue pack target
├── 4-QC-engine/              skills, contracts, and the stage-engine port
├── 5-QF-execute/             bounded execution records
├── _fixture/                 inspectable intervention evidence used by this Board
├── fig/                      image assets
└── board/                    generated site, never hand-edited
```

Two shape rules landed on 260816, both from the Board family.
The leading number is the group's place in `## Pages`, so the folder listing reads in the order the board declares; `## Pages` stays the only authority on that order, and you change it by moving a `### ` block first and renaming the folder second.
Every page then owns a folder carrying its own name, with that name on it twice, once as the folder and once as the only `.md` inside; everything else beside that `.md` is one of the page's plugins.

## Pages

### QA · Design
What the Application system is before a delivery is produced: one Page-first delivery Board that
reads settled Task/Insight Pages through PageX. The 260802 stage-spine pages remain the migration
record; the 260817 target is Brief → Intervention → Artifact and owns no evidence Probe.

```text
⚙️ ENGINE                      📋 PAGES · the working record            📂 FOLDER
─────────────────────────      ─────────────────────────────────────    ────────────────────────
?                          ◀── QA0  the board map, four layers         ──▶  this board
?                          ◀── QA1  the folder map, family+intervention ──▶  application/ + designs/
?                          ◀── QA2  the skill set: what ships          ──▶  ~20 skills, versioned
?                          ◀── QA3  the INTERVENTION BOARD ruling      ──▶  0-lifecycle/ as a board
?                          ◀── QA4  the evidence wall, application cut ──▶  1-probes/ + the bank
```
QA0-the-board-map.md
QA1-the-folder-map.md
QA2-the-skill-set.md
QA3-the-intervention-board.md
QA4-evidence-channel.md

### QB · Delivery
The historical delivery concerns are kept here so the old Application ladder can be migrated
without losing its reasoning. The target no longer runs Data → Insight → Claims → Advice inside
each Application. Those DIKW concerns belong to the Task/Insights Board. Application selects
their settled Pages, then re-expresses them through Brief → Intervention → Artifact. QB1-QB9 are
therefore compatibility inputs, not the Page roster new applications copy; the live Page Type
contracts and specimens are in QBt below.

```text
⚙️ ENGINE                      📋 PAGES · the working record            📂 FOLDER
─────────────────────────      ─────────────────────────────────────    ────────────────────────
the S-spine, in miniature  ◀── QB0  the design lifecycle board       ──▶  0-lifecycle/ as a board
seed+venue+pitch stages    ◀── QB1  Opening: why + where + promise    ──▶  0-seed/ · 2-venue/
1a stage + task probes     ◀── QB2  Data: the anchored profile        ──▶  1a-descriptions/
1b stage + discovery       ◀── QB3  Insight: grounded themes          ──▶  1b-themes/
1c stage + probe loop      ◀── QB4  Claims: the adjudicated ledger    ──▶  1c-claims/
1d stage + narrative       ◀── QB5  Design: advice the tail adopts    ──▶  1d-advice/
display stage              ◀── QB6  Display: venue-gated units        ──▶  4-display/
artifact skill             ◀── QB7  Artifact: the shipped draft       ──▶  0-artifacts/
review+audit+deploy        ◀── QB8  Deploy: gate, audit, ship         ──▶  3-deliver routes
iterate skill              ◀── QB9  Iterate: A/B back into Data       ──▶  1-rounds/ + 1a refresh
```
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
One page per venue TARGET, and nothing above it: what that channel gates, rewards, and requires of claims settlement, tone, and shape.
The packs live at `application/venue/venue-<name>/`; this plugin reads them at pin time and each aligned stage consults them afterwards.

QBv1-sms.md
QBv2-email.md
QBv3-dashboard.md
QBv4-report.md
QBv5-push.md
QBv6-reminder.md
QBv7-checklist.md
QBv8-ui-card.md

### QC · Engine
How reusable Application, Probe, and Display routes serve Delivery on the shared Board substrate, and the stage engine that round 3 ports from paper.

```text
⚙️ ENGINE                      📋 PAGES · the working record            📂 FOLDER
─────────────────────────      ─────────────────────────────────────    ────────────────────────
Application/Probe/Display  ◀── QC1  the delivery-skill route map      ──▶  skill + page handoffs
stages/<dir>/stage.md      ◀── QC2  the stage engine port             ──▶  index.yml · CONTRACT.md
skillpage.py sync          ◀── Skill-0..5  one mirror per shipped unit ──▶  SKILL.md snapshots
```
QC1-delivery-skill-map.md
QC2-stage-engine.md
Skill-0-haipipe-application.md
Skill-1-haipipe-application-enter.md
Skill-2-haipipe-application-lifecycle.md
Skill-3-haipipe-application-probe.md
Skill-4-haipipe-application-draft.md
Skill-5-haipipe-application-check.md

### QF · Execute
What actually ran against `_fixture/`, with evidence and a reopen path: the layer that keeps "skill written, delivery defined" from passing as done.

```text
⚙️ ENGINE                      📋 PAGES · the working record            📂 FOLDER
─────────────────────────      ─────────────────────────────────────    ────────────────────────
check + receipts           ◀── QF1  execution map: run · gate · reopen ──▶  pass / failure receipt
fresh application agent    ◀── QF2  fresh-agent run on the fixture    ──▶  acceptance verdict
```
QF1-execution-map.md
QF2-fresh-agent-run.md

### QBt · Page types this family owns
Three globally unique Page Types define the target Application Board. Brief is the Application
opening concern without colliding with Paper Opening. Intervention is the delivery architecture
without colliding with Board's generic Design type. Artifact is one independently approvable
delivery unit. All evidence arrives from settled Task/Insight Pages through PageX; missing
knowledge routes back to that Board.

```text
⚙️ ENGINE                      📋 PAGES · the working record            📂 FOLDER
─────────────────────────      ─────────────────────────────────────    ────────────────────────
Page + PageX                ◀── QBt1  Brief: why, who, venue, promise ──▶ pagex/
Page + PageX + outline      ◀── QBt2  Intervention: insight→component ──▶ pagex/ · outline/
Page + output plugins       ◀── QBt3  Artifact: one accepted unit     ──▶ display/ · word/
```
QBt1-for-brief.md
QBt2-for-intervention.md
QBt3-for-artifact.md

## Links
QA0@paper           ../PaperSkillBoard-260725/1-QA-design/QA0-the-board-map/QA0-the-board-map.md
QA1@paper           ../PaperSkillBoard-260725/1-QA-design/QA1-the-folder-map/QA1-the-folder-map.md
QA2@paper           ../PaperSkillBoard-260725/1-QA-design/QA2-the-skill-set/QA2-the-skill-set.md
QA3@paper           ../PaperSkillBoard-260725/1-QA-design/QA3-the-skill-board/QA3-the-skill-board.md
QA5@paper           ../PaperSkillBoard-260725/1-QA-design/QA5-the-probe-layer/QA5-the-probe-layer.md
QA6@paper           ../PaperSkillBoard-260725/1-QA-design/QA6-paper-scaffold/QA6-paper-scaffold.md
QA7@paper           ../PaperSkillBoard-260725/1-QA-design/QA7-the-paper-board/QA7-the-paper-board.md
QA8@paper           ../PaperSkillBoard-260725/1-QA-design/QA8-owning-the-shared-page/QA8-owning-the-shared-page.md
QA9@paper           ../PaperSkillBoard-260725/1-QA-design/QA9-driving-work-from-a-page/QA9-driving-work-from-a-page.md
QB1@paper           ../PaperSkillBoard-260725/2-QB-delivery/QB1-opening/QB1-opening.md
QB2@paper           ../PaperSkillBoard-260725/2-QB-delivery/QB2-work/QB2-work.md
QB4@paper           ../PaperSkillBoard-260725/2-QB-delivery/QB4-value/QB4-value.md
QB5@paper           ../PaperSkillBoard-260725/2-QB-delivery/QB5-display/QB5-display.md
QB6@paper           ../PaperSkillBoard-260725/2-QB-delivery/QB6-main/QB6-main.md
QB9@paper           ../PaperSkillBoard-260725/2-QB-delivery/QB9-build/QB9-build.md
QB10@paper          ../PaperSkillBoard-260725/2-QB-delivery/QB10-round/QB10-round.md
QBv1@paper          ../PaperSkillBoard-260725/5-QBv-venue-packs/QBv1-misq/QBv1-misq.md
QC1@paper           ../PaperSkillBoard-260725/6-QC-engine/QC1-delivery-skill-map/QC1-delivery-skill-map.md
QC2@paper           ../PaperSkillBoard-260725/6-QC-engine/QC2-stage-contract/QC2-stage-contract.md
QC4@paper           ../PaperSkillBoard-260725/6-QC-engine/QC4-phase-flow/QC4-phase-flow.md
QF1@paper           ../PaperSkillBoard-260725/8-QF-execute/QF1-execution-map/QF1-execution-map.md
QF3@paper           ../PaperSkillBoard-260725/8-QF-execute/QF3-fresh-agent-run/QF3-fresh-agent-run.md
paper-board/        ../PaperSkillBoard-260725/
boardform-board/    ../BoardSkillBoard-260722/
README.md           ../../application/README.md
PHILOSOPHY.md       ../../application/PHILOSOPHY.md
SOP-paper-alignment.md ../../application/SOP-paper-alignment.md
SOP-ladder-restage.md  ../../application/SOP-ladder-restage.md
haipipe-application/   ../../application/haipipe-application/
haipipe-application-enter/     ../../application/0-enter/haipipe-application-enter/
haipipe-application-round/     ../../application/0-enter/haipipe-application-round/
haipipe-application-lifecycle/ ../../application/1-lifecycle/haipipe-application-lifecycle/
haipipe-application-seed/      ../../application/1-lifecycle/0-seed/haipipe-application-seed/
haipipe-application-descriptions/ ../../application/1-lifecycle/1a-descriptions/haipipe-application-descriptions/
haipipe-application-themes/    ../../application/1-lifecycle/1b-themes/haipipe-application-themes/
haipipe-application-claims/    ../../application/1-lifecycle/1c-claims/haipipe-application-claims/
haipipe-application-advice/    ../../application/1-lifecycle/1d-advice/haipipe-application-advice/
haipipe-application-venue/     ../../application/1-lifecycle/haipipe-application-venue/
haipipe-application-pitch/     ../../application/1-lifecycle/2-pitch/haipipe-application-pitch/
haipipe-application-narrative/ ../../application/1-lifecycle/3-narrative/haipipe-application-narrative/
haipipe-application-display/   ../../application/1-lifecycle/4-display/haipipe-application-display/
haipipe-application-section-edit/ ../../application/1-lifecycle/5-section-edit/haipipe-application-section-edit/
haipipe-application-evidence/  ../../application/2-phase/1-evidence/haipipe-application-evidence/
haipipe-application-draft/     ../../application/2-phase/0-draft/haipipe-application-draft/
haipipe-application-revise/    ../../application/2-phase/2-revise/haipipe-application-revise/
haipipe-application-check/     ../../application/2-phase/3-check/haipipe-application-check/
haipipe-application-artifact/  ../../application/3-deliver/haipipe-application-artifact/
haipipe-application-review/    ../../application/3-deliver/haipipe-application-review/
haipipe-application-claim-audit/ ../../application/3-deliver/haipipe-application-claim-audit/
haipipe-application-deploy/    ../../application/3-deliver/haipipe-application-deploy/
haipipe-application-iterate/   ../../application/4-iterate/haipipe-application-iterate/
venue-packs/        ../../application/venue/
haipipe-paper-stage/ ../../paper/_old/haipipe-paper-stage/
stages-index.yml    ../../paper/haipipe-paper/stages/index.yml
stages-CONTRACT.md  ../../paper/haipipe-paper/stages/CONTRACT.md
haipipe-board/      ../../board/haipipe-board/
_fixture/           _fixture/
fixture-intervention/ ../../../../../../designs/Project-Application-SMSDesign/applications/01_sms_young_male/
