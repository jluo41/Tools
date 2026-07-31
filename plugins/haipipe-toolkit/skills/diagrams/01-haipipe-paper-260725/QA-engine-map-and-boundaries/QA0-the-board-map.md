# The Board map: Delivery → Engine → Execute
state: 🟡 PARTIAL
owner: JL
method: start from the required delivery, map it through skill-first Engine routes, then record bounded executions as evidence

## Question
How should this Board let a fresh reader start from what a paper must deliver, trace the skills that may produce it, and inspect the concrete execution that proves or blocks the route?

## Boundary
- ✅ Covered here
  The three-layer order, group roles, page contracts, and the migration plan.
- ↪ Covered by QA6
  Submission-cut law and source/candidate/submission roles.
- ↪ Covered by QO0
  The Build delivery contract.
- ↪ Covered by QS0 and QE0
  The Delivery × Skill route map and the actual execution records.

## Diagram
```text
DELIVERY · the desired reader-facing result and its authority
QF → QG Opening → QH Work → QI Literature → QJ Value → QK Display
                   → QL Main → QM Appendix → QN Present → QO Build → QP Round
                                      │
                                      │ target: every Delivery group names one Engine route
                                      ▼
ENGINE · skill-first reusable routes
QS skill map → paper → lifecycle → stage → draft / probe / revise → deliver / project
                │                  │
                └──── QA / QB / QC shared ownership, stage, and evidence contracts
                                      │
                                      │ an actual bounded run supplies evidence
                                      ▼
EXECUTE · observed runs, not a second authoring system
QE execution map → fixture or real paper → artifact / candidate → gate / receipt → reopen
```

## Content
### Delivery answers what the paper must give
Delivery is the reader-facing specification.
It owns the desired artifact, its canonical content, and the human decision that it is fit to hand off.
The Delivery reading order is not an execution graph and never renumbers lifecycle stages.

### Engine answers which skills serve that delivery
Engine is skill-first rather than stage-first.
One skill may serve several Delivery groups, and one Delivery group may need several skills in sequence.
The Engine map may link to authority but never copies or replaces it.
Every skill card must state its trigger, the Delivery content it serves, what it reads, what it may write, its handoff, its refusal boundary, and its Execute evidence.

### Execute answers what actually happened
Execute is one bounded attempt to turn one Delivery target through one Engine route on a named fixture or paper.
It produces an artifact, candidate, observation, gate result, or receipt.
Tests, compile checks, gates, and fresh-agent observations are ways to gather Execute evidence, not a separate authoring layer.
Failure reopens the owning Delivery or Engine page; it never turns a failed candidate into an implicit promotion.

### Accepted Delivery order
JL ruled the sequence:

```text
Opening → Work → Literature → Value → Display → Main → Appendix → Present → Build → Round
```

- Venue belongs inside Opening.
- Work comes immediately after Opening and grows the discovery and task banks through probes.
- Present includes slides and posters.
- Build also owns diffusion/distribution.
- Response is named Round, because the unit is a batch/iteration.
- This sequence is the Board's Delivery reading order. Engine dependencies and
  stage revisits remain explicit and are never inferred from group adjacency.

### The page contracts
Each of the ten accepted sequence groups QG through QP begins with a `0` overview, even if no detailed page exists yet.
QF is the Delivery meta-map that precedes those ten groups; it preserves the historical QA6 id rather than pretending to be an eleventh lifecycle step.

| Field | What it says |
|---|---|
| Reader result | What a reader or collaborator receives |
| Artifact | The concrete deliverable |
| Authority | Which page or path is canonical |
| Completion gate | What the human must verify |
| Consumes | Which accepted evidence or contract it may use |
| Engine route | The ordered skill links that serve it |
| Execute evidence | The run, receipt, or observed result that proves or blocks it |
| Open gaps | What remains absent or contradictory |

`QS0` holds the many-to-many Delivery × Skill crosswalk.
`QE0` holds run records and their failure-to-reopen link.
The old seven-field overview wording remains visible until each overview has been migrated deliberately.

### Identity survives regrouping
Existing page ids remain historical addresses.
Their folders and Board order changed; their ids did not.
Only the ten new Delivery overview pages received new ids QG0 through QP0.

## Items to Finish
- [x] Adopt Delivery → Engine → Execute as the Board's three reading layers.
- [x] Put Venue inside Opening.
- [x] Order Opening → Work → Literature → Value → Display.
- [x] State that Work grows discovery and task banks.
- [x] Keep Present and include slides/posters.
- [x] Combine diffusion/distribution with Build.
- [x] Rename Response to Round.
- [x] Preserve existing ids while putting Delivery first in the registry.
- [x] Add the initial Delivery × Skill and Execute-map pages.
- [ ] 🔗 Give every Delivery overview an Engine route and Execute-evidence link.
      Do this one group at a time so no page claims a route or run that does not exist.
- [ ] 🧩 Add `Serves` and `Execute evidence` to every existing Q-Skill page.
      The six initial authoring/control cards become the first Engine route, not a new authority layer.
- [ ] 🧱 Audit `haipipe-paper-deliver` and `haipipe-paper-project` for independent Q-Skill cards.
      Add a page only if its responsibility cannot remain an explicit leaf of an existing skill route.
- [ ] 🧪 Add Execute records only for runnable routes.
      Present and Round stay visible as delivery gaps until they have a callable route and a bounded execution.
- [ ] 🧭 Cold-read the reorganized Board with a fresh agent.

## Where we are
The registry now reads Delivery first, then skill-first Engine, then Execute evidence.
`QS0` and `QE0` establish the crosswalk and execution-record shapes; they do not assert that every Delivery route is implemented.
The existing MISQ Main-1 candidate is the first concrete Execute record: G0-G3 pass, G4 is baseline-blocked by one active Display input, and G5 was not run.
No paper authority, submission file, or promotion decision changed in this Board reorganization.

## Files
- `board.md`
- `QF-delivery-map/` through `QP-delivery-round/`
- `QS-engine-skill-set/QS0-delivery-engine-map.md`
- `QE-engine-acceptance/QE0-execution-map.md`

## Law
- Read Delivery first, then skill-first Engine, then Execute evidence.
- Delivery order is Opening, Work, Literature, Value, Display, Main, Appendix, Present, Build, Round.
- Delivery owns content authority; Engine only routes skills across it; Execute only records bounded runs.
- Tests, gates, receipts, compile checks, and fresh-agent observations are Execute evidence.
- Each Delivery sequence group QG-QP begins with the target overview contract; QF is the preceding meta-map.
- Regrouping preserves existing page ids.

## Glossary
- **Engine**: the reusable control model that makes paper work run consistently.
- **Delivery**: one concern or artifact a paper must author, consume, project, present, build, or revise.
- **Execute**: a bounded real or fixture run of one Delivery through one Engine route, with inspectable evidence.
- **Round**: one external-feedback batch and its applied revision/resubmission record.

## Log
260730 · JL replaced the proposed Test layer with Execute: Delivery says what is wanted, Engine maps skill routes, and Execute records actual bounded runs and their evidence.
260730 · Reorganized the registry Delivery first, Engine second, Execute third; added QS0 and QE0 as the two non-authoritative maps.
260730 · Reconstructed the accepted 51-page regroup after workspace recovery and recorded the implemented Build trial on QO0.
260729 · JL placed Venue inside Opening; ordered Opening → Work → Literature → Value → Display; combined diffusion/distribution with Build; kept Present for slides/posters; renamed Response to Round.
260729 · Engine plus Delivery blueprint created, preserving existing ids and requiring one overview per Delivery group.
