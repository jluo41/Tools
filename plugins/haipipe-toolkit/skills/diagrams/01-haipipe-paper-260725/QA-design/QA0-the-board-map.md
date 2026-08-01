# The Board map: Delivery → Engine → Execute
state: 🟡 PARTIAL
owner: JL
method: start from the required delivery, map it through skill-first Engine routes, then record bounded executions as evidence

## Opening
How should this Board let a fresh reader start from what a paper must deliver, trace the skills that may produce it, and inspect the concrete execution that proves or blocks the route?

Scope: This page covers The three-layer order, group roles, page contracts, and the migration plan. QA6 covers Submission-cut law and source/candidate/submission roles. QB9 covers The Build delivery contract. QC1 and QF1 covers The Delivery × Skill route map and the actual execution records.

## Diagram
```text
QA · DESIGN · folders, ownership, and Paper / Board / Probe boundaries
                                      │ shapes
                                      ▼
QB · DELIVERY · Opening → Work → Literature → Value → Display → Main → Appendix
                 → Present → Build → Round
                                      │ served by
                                      ▼
QC · ENGINE · Delivery × Skill map → stage / page / phase / sentence contracts
                                      │ demonstrated by
                                      ▼
QF · EXECUTE · bounded run → artifact / candidate → gate / receipt → reopen
```

## Content
### Board-Folder is source; Board-Webpage is the generated view
The editable Board-Folder is `board.md`, one descriptive source folder per group, and one Markdown file per page.
The generated Board-Webpage is `board/index.html`, one `board/<GROUP>.html` per group, one `board/<GROUP>/<page>.html` per page, and shared `board/_assets/`.
The generated tree is derived and never hand-edited; `build.py` reroots source-relative links, images, and PDF objects for each webpage depth.
`board.html` is retired for a Board-folder build, so Index, Group, and Page routes are the one webpage surface.

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
The `QB · Delivery` group is the overview. `QB1` through `QB10` carry the ten accepted delivery concerns; their letter now expresses their common enduring responsibility instead of creating one group per concern.

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

`QC1` holds the many-to-many Delivery × Skill crosswalk.
`QF1` holds run records and their failure-to-reopen link.
The old seven-field overview wording remains visible until each overview has been migrated deliberately.

### Identity survives regrouping
Live page ids now match their current group: `QA` Design, `QB` Delivery, `QC` Engine, and `QF` Execute.
Old ids without a collision remain aliases in `board.md`'s `## Links`.
The former Engine `QB*` and `QC*` names collided with the new Delivery/Engine series, so all live references have been migrated to their current `QC*` or `QB*` ids rather than leaving an ambiguous alias.

## Items to Finish
- [x] Adopt Delivery → Engine → Execute as the Board's three reading layers.
- [x] Put Venue inside Opening.
- [x] Order Opening → Work → Literature → Value → Display.
- [x] State that Work grows discovery and task banks.
- [x] Keep Present and include slides/posters.
- [x] Combine diffusion/distribution with Build.
- [x] Rename Response to Round.
- [x] Regroup and renumber live pages into the Skill-Board sequence.
- [x] Add the initial Delivery × Skill and Execute-map pages.
- [x] Align the Paper Board with the canonical Board-Folder → Board-Webpage structure.
      `board.md` declares the source and generated trees; the strict checker verifies the generated Index, Group, Page, assets, fragments, and local resources.
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
The registry now reads the Skill-Board core: Design, then Delivery, then skill-first Engine, then Execute evidence.
`QC1` and `QF1` establish the crosswalk and execution-record shapes; they do not assert that every Delivery route is implemented.
The existing MISQ Main-1 candidate is the first concrete Execute record: G0-G3 pass, G4 is baseline-blocked by one active Display input, and G5 was not run.
No paper authority, submission file, or promotion decision changed in this Board reorganization.
The current Board has 53 Page routes in four live groups; the active pages also use the Opening grammar.

## Files
- `board.md`
- `QB-delivery/`
- `QC-engine/QC1-delivery-skill-map.md`
- `QF-execute/QF1-execution-map.md`
- `../../board/haipipe-board/build.py`
- `../../board/haipipe-board/check.py`
- `board/`
  Generated output; do not hand-edit.

## Law
- Read Delivery first, then skill-first Engine, then Execute evidence.
- Delivery order is Opening, Work, Literature, Value, Display, Main, Appendix, Present, Build, Round.
- Delivery owns content authority; Engine only routes skills across it; Execute only records bounded runs.
- Tests, gates, receipts, compile checks, and fresh-agent observations are Execute evidence.
- QB1–QB10 carry the target Delivery contracts; the QB group page is their shared overview.
- Regrouping aligns every live page id with its current Skill-Board group and preserves non-conflicting historical ids as aliases.

## Glossary
- **Engine**: the reusable control model that makes paper work run consistently.
- **Delivery**: one concern or artifact a paper must author, consume, project, present, build, or revise.
- **Execute**: a bounded real or fixture run of one Delivery through one Engine route, with inspectable evidence.
- **Round**: one external-feedback batch and its applied revision/resubmission record.

## Log
260801 · Consolidated 16 historical groups into QA Design, QB Delivery, QC Engine, and QF Execute; migrated page ids to their live group, retained non-conflicting aliases, and reserved QD/QE for future Paper-specific Working/Sharing content.
260801 · Aligned the Paper Board with the canonical Board-Folder and Board-Webpage contract; rebuilt 53 pages, 16 groups, and one Index; strict structure and resource checks returned zero findings.
260730 · JL replaced the proposed Test layer with Execute: Delivery says what is wanted, Engine maps skill routes, and Execute records actual bounded runs and their evidence.
260730 · Reorganized the registry Delivery first, Engine second, Execute third; added QC1 and QF1 as the two non-authoritative maps.
260730 · Reconstructed the accepted 51-page regroup after workspace recovery and recorded the implemented Build trial on QB9.
260729 · JL placed Venue inside Opening; ordered Opening → Work → Literature → Value → Display; combined diffusion/distribution with Build; kept Present for slides/posters; renamed Response to Round.
260729 · Engine plus Delivery blueprint created, preserving existing ids and requiring one overview per Delivery group.
