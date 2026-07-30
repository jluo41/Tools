# The Board map: Engine first, Delivery second
state: 🟡 PARTIAL
owner: JL
method: make the Board's reading order mirror the system that runs a paper and the artifacts a paper delivers

## Question
What should this Board look like so a fresh reader can see both how `/haipipe-paper` works and what it delivers?

The current QA through QE groups preserve the history of the design, but they mix system machinery, paper-folder structure, reader-facing artifacts, and acceptance tests in one sequence.
The Board needs a stable top-level map before its pages are regrouped, otherwise moving files will only replace one difficult index with another.

## Boundary
- ✅ Covered here
  The Board's top-level reading order, group names, group contracts, and the first-pass destination of existing pages.
- ↪ Covered by QA6
  The paper folder's submission-cut boundary, whether `3-dist/` is the fourth numbered work area, and how a candidate projection is promoted into the unnumbered submission projection.
- ↪ Covered by the regrouping implementation
  Creating the new group folders, moving pages, rewriting the Board pipeline, repairing links, and validating the result.
- ↪ Covered by the individual pages
  The substantive decisions about stages, sentences, evidence, Displays, delivery formats, and acceptance.

## Diagram
```text
/haipipe-paper skill-design Board
│
├── ENGINE · how the paper system works
│   ├── Map & boundaries
│   ├── Stage contract
│   ├── Page & sentence contract
│   ├── Skill set
│   └── Acceptance
│
└── DELIVERY · what a paper must produce and ship
    ├── Delivery map
    ├── Opening · Literature · Work · Venue · Value
    ├── Display · Main · Appendix
    └── Present · Build · Distribute · Respond
```

## Content
### §1 The two reading jobs
- **ENGINE answers how the system works**
  It holds the shared control model: boundaries, stage execution, page and sentence semantics, the skill call graph, and the acceptance test.
- **DELIVERY answers what the paper produces**
  It follows the paper from its premise and evidence through manuscript units, presentation forms, builds, exports, and response rounds.
- **The order is Engine then Delivery**
  A new agent first learns the rules of the machine, then sees every artifact family that the machine must own, consume, project, or ship.

### §2 Engine groups
| Group | The question it answers | Existing pages in the first pass |
|---|---|---|
| Map & boundaries | Where do Paper, Board, Probe, and their records live, and which layer owns each crossing? | `QA1` through `QA5`, `QA7` through `QA9` |
| Stage contract | What does one stage declare, receive, run, and provide? | `QB1` through `QB3d` |
| Page & sentence contract | What does a stage page mean, and how does a sentence bind to inspectable evidence? | `QC0` plus the page-shape faces that belong here after a cold read |
| Skill set | Which skills exist, who calls whom, and where does each responsibility stop? | The six `Q-Skill-*` pages plus `QS4` |
| Acceptance | What proves that a fresh agent can discover and run the design? | `QE1` and `QE2` |

### §3 Delivery groups
| Group | Lifecycle or working authority | Delivered or projected artifact |
|---|---|---|
| Delivery map | `QA6` and the paper-folder law | The complete map from working authority to shipped form |
| Opening | `0-lifecycle/0-seed/` | The paper premise and entry contract, not the Introduction section |
| Literature | Seed and Main pages plus `1-probes/` | Literature section, bibliography entries, and sentence citations |
| Work | `0-lifecycle/1-work/` | Questions, probe bindings, accepted claims, and evidence |
| Venue | `0-lifecycle/2-venue/` | Venue contract, class, bibliography style, and formatting constraints |
| Value | Probe results and sentence evidence cards | Inline quantitative claims with their producing runs |
| Display | `0-lifecycle/3-display/` | `displays/<unit>/`, its caption, label, placement, and human gate |
| Main | `0-lifecycle/4-main/` | Authoritative main-text pages and their manuscript projections |
| Appendix | `0-lifecycle/5-appendix/` | Authoritative appendix pages and their manuscript projections |
| Present | `5-present/paper-slides/` and `5-present/paper-poster/` | Slides and posters |
| Build | `2-src/` and Submission build pages | Rebuildable recipes, drivers, and compilation machinery |
| Distribute | Export and conversion skills | `3-dist/tex/`, `3-dist/word/`, PDFs, and `.media/` projections |
| Respond | `0-lifecycle/6-submission/` and `0-lifecycle/7-round/` | Rebuttal, revision, resubmission, and later-round records |

### §4 One contract at the front of every Delivery group
Every Delivery group starts with a `0` overview page, including a group whose implementation is still empty.

| Field | What the overview must say |
|---|---|
| Lifecycle | Where this concern enters the paper lifecycle |
| Authority | Which page or path is canonical |
| Projects to | Which reader-facing or shipped artifacts are generated from that authority |
| Skills | Which skills enter, transform, check, or ship it |
| Consumes | Which upstream evidence, contract, or artifact it is allowed to use |
| Gate | What a human must verify before this concern may close |
| Open gaps | What is absent, contradictory, or not yet implemented |

An empty group therefore remains visible as a red overview page instead of disappearing from the architecture.

### §5 Regroup without destroying identity
- **Keep every existing page id**
  Page ids are historical addresses used by discussions, logs, and cross-Board links, so regrouping changes paths and index order but does not rename ids.
- **Give new ids only to new overview pages**
  The overview family can establish the new structure without pretending that old decisions were made under a new numbering scheme.
- **Keep Delivery groups flat**
  `DELIVERY` is a visible story and `Delivery map` is its overview group; it is not a nested folder containing every other group because the Board group index is flat.
- **Move only after the map is accepted**
  Create the overview pages first, then use `git mv`, repair real-path links, rebuild, and run strict checks.

### §6 First-pass migration
| Existing pages | Destination |
|---|---|
| `QA1` through `QA5`, `QA7` through `QA9` | Engine: Map & boundaries |
| `QB1` through `QB3d` | Engine: Stage contract |
| `QC0` | Engine: Page & sentence contract |
| The six `Q-Skill-*` pages plus `QS4` | Engine: Skill set |
| `QE1` and `QE2` | Engine: Acceptance |
| `QA6` | Delivery: Delivery map |
| `QC1` | Delivery: Literature |
| `QC2` | Delivery: Value |
| `QC3`, `QC4`, and `QD1` through `QD4` | Delivery: Display |
| `QC5` and `QC6` | Delivery: Distribute |

Groups without an existing destination page receive only their overview page in the first pass.
Their later pages should be opened from concrete gaps rather than invented to make the groups look equally full.

### §7 The rule that must be settled before the move
QA6's accepted 260726 rule that a paper has "three numbered folders and only three" is now stale because the working paper already has `3-dist/`.

The proposed replacement is a submission-cut rule rather than a fixed count:

```text
numbered path = excluded from the journal submission package

0-lifecycle  authoritative Board and S-page source
1-probes     evidence bindings
2-src        build recipes
3-dist       candidate and handoff projections
```

Under this rule, `3-dist/` is not part of the journal submission projection.
The S page is the source authority, `3-dist/tex/` is the candidate projection, and the unnumbered LaTeX tree is the submission projection.
QA6 now specifies the contract rather than merely naming it: a pure wiring manifest at `2-src/projection.yaml`, followed by coverage, source, candidate, evidence, compile, and human-promotion refusal gates.
The proposed `haipipe-paper-project` runtime belongs to Delivery: Build; QC5 and `md2tex.py` remain the LaTeX adapter under Delivery: Distribute.
The remaining decision is whether JL accepts that submission-cut and three-role model.
Implementation then starts with a candidate-only trial, not with regrouping or a submission overwrite.

## Items to Finish
- [x] 🧭 Separate the Board into Engine and Delivery
      The top-level reading order now distinguishes how the paper system works from what a paper produces and ships.
- [x] 🗂 Name the Engine and Delivery groups
      The blueprint records five Engine groups and thirteen Delivery groups, including Present, Distribute, and Respond.
- [x] 📋 Give every Delivery group the same overview contract
      Lifecycle, Authority, Projects to, Skills, Consumes, Gate, and Open gaps are the required scan fields.
- [x] 🧷 Preserve existing page ids during regrouping
      Existing ids remain stable historical and cross-Board addresses; only new overview pages receive new ids.
- [ ] ⚖️ Settle the submission-cut rule and promotion contract
      QA6 has designed the manifest and six-gate path.
      JL still must replace the fixed three-folder count, admit or reject `3-dist/`, and accept or revise the proposed source, candidate, and submission roles.
- [ ] 🚚 Create the overview pages and regroup the existing pages
      No file moves belong to this recording step; regrouping begins only after the remaining rule is accepted.
- [ ] 🧪 Rebuild, check, and cold-read the regrouped Board
      A fresh agent must be able to answer where a concern lives, who owns it, what ships to the journal, and which projection may be regenerated.

## Where we are
JL approved the Engine plus Delivery direction in the earlier Paper skill-set discussion and asked on 2026-07-29 for that design to be recorded in QA0.
JL then confirmed that the active work is this Paper skill Board and asked for the projection design to continue.
QA6 now carries an implementable manifest and refusal-gate proposal grounded in the live MISQ master reachability.
No existing page has been moved or renamed, and acceptance of QA6's submission-cut and three-role model remains the blocking structural decision.

## Files
- `board.md`
  Registers QA0 and will later carry the Engine to Delivery reading order.
- `QA-where-things-live/QA0-the-board-map.md`
  Owns the Board-level structure proposed here.
- `QA-where-things-live/QA6-paper-scaffold.md`
  Owns the submission-cut and candidate-to-submission promotion decisions that must precede regrouping.
- `QC-the-sentence-with-evidence-card/QC5-sentence-to-latex.md`
  Owns candidate conversion semantics; QA6 owns only path wiring and promotion.
- `3-deliver/1-build/haipipe-paper-project/`
  Proposed Build-group runtime; not created yet.
- `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/`
  Supplies the current paper tree against which this map was checked.
- `Tools/plugins/haipipe-toolkit/skills/paper/`
  Supplies the current Paper skill-set and the Present, Build, Distribute, and Respond responsibilities.

## Law
- This Board tells two stories in order: Engine first, Delivery second.
- Engine groups explain the reusable paper system; Delivery groups mirror the concerns and artifacts of an actual paper.
- Every Delivery group begins with the same seven-field overview contract, even when the group contains no implemented page yet.
- Regrouping preserves every existing page id.

## Glossary
- **Engine**
  The reusable control model that makes paper work run consistently across papers.
- **Delivery**
  A concern or artifact that one paper must author, project, present, build, distribute, or respond through.
- **Projection**
  A rebuildable format-specific rendering of an authoritative page or artifact.

## Log
260729 2124 · Cold review separated target-root ownership from external compile dependencies and named `haipipe-paper-project` as the proposed Build runtime. This sharpens the future grouping: Build owns manifest checking and promotion; Distribute owns the LaTeX adapter.
260729 2104 · QA6 developed the open projection blocker into a pure manifest plus six refusal gates and measured the live reachable target set. QA0 still does not authorize regrouping: acceptance, one candidate-only trial, and the Appendix source gap come first.
260729 2020 · Refined QA6's blocker from a false `sections/` versus `3-dist/tex/` authority choice into a three-role model: S-page source, candidate projection, and submission projection, joined by an explicit promotion contract.
260729 1840 · Created QA0 to record the approved Engine plus Delivery Board blueprint before any regrouping.
