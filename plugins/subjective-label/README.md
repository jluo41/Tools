# subjective-label

A human-grounded plugin for building one subjective label and then scanning a
corpus under that frozen meaning.

## Family architecture

```text
subjective-label                         one user-facing umbrella
├── label-building                      Building side LAW: authority, human gates, verbs
├── label-building-workflow             Building Run Spec guide: order, item resume, Run receipts
├── label-scanning                      Scanning side LAW
├── label-scanning-workflow             Scanning Run Spec guide: test lock, risk queue, audit loop
└── subjective-label-workflow           the Workflow: Run Specs, dependencies, gates, Routes, handoff
```

The split follows one authority boundary:

```text
🏗 Building   asks "is this what the human means?"
              contract Run → calibration Runs → handoff-freeze Run

🔍 Scanning   asks "was that frozen meaning executed reliably?"
              test Runs → production Runs → audit Runs → D*
```

**A Workflow is a list of Runs.** P0-P5 remain compatibility capability tags
on existing records and views; they do not own work or determine routing. Each
Run Spec's dependencies, gates, and Routes define the executable graph.

One identified human is the semantic authority. Models may retrieve, predict,
diagnose, draft, and execute; their consensus never creates human gold.
The current local CLI and Board record that authority as a caller attestation;
they do not authenticate the person's identity. Treat G0 receipts as
single-user workflow evidence, not identity proof or a production security
boundary.

## Capability groups (P0-P5 compatibility tags)

| compatibility tag | side | Run Spec grouping |
|---|---|---|
| P0 Contract | Building | establish one valid job |
| P1 Round | Building | refine `D_t` and `G_t` |
| P2 Freeze | Building | sign `G*` and `D_cal*` |
| P3 Test | Scanning | qualify an executor route |
| P4 Scan | Scanning | create one terminal candidate per item |
| P5 Audit | Scanning | support a bounded `D*` claim |

The Run Spec graph, its route predicates, and the Label Handoff crossing are
declared in `skills/subjective-label-workflow/SKILL.md`. Gate evidence belongs
to the Run Result/receipt it checks or to a named job control; a gate is not an
extra Run or independent lifecycle unit.

Pick, seal, judge, learn, measure, and decide are steps or verbs inside one
Round; GOLD and SCORE are the two steps inside Test. "Another round" is a route.

A Round is a UNIT on disk (`ref/ref-assets.md` §3): `card.md` (the wager a
person releases), `README.md`, `manifest.yaml`, `evidence.md`, `prospect.md`,
the event files, `checkpoint.json`, and a rendered `view/`. Every policy version
carries a rendered `cheatsheet.md` and `gallery.md`; the project keeps a
`register.md` of the seven regions.

## The Label Handoff

`handoff/label-v1.yaml` is the only legal crossing. It binds corpus, schema,
`G*`, `D_cal*`, sealed-test manifest checksum, stopping evidence, lineage, and
human signature. It contains no protected test ids or text. Scanning binds the
exact handoff checksum and cannot edit Building artifacts.

## Skills

| skill | folder under `skills/` | responsibility |
|---|---|---|
| `/subjective-label` | `subjective-label/` | auto-route the job through the family |
| `/label-building` | `label-building/` | the Building law: Contract, Round, Freeze |
| `/label-building-workflow` | `label-building-workflow/` | the Building order: fence, contract, card, prepare, judge, learn, close |
| `/label-scanning` | `label-scanning/` | the Scanning law: Test, Scan, Audit |
| `/label-scanning-workflow` | `label-scanning-workflow/` | the Scanning order: gold, score, manifest, attempts, queue, audit, repair |
| `/subjective-label-workflow` | `subjective-label-workflow/` | Run Specs, dependencies, gates, Routes, handoff and invalidation |
| `/haipipe-page-for-labeling` | `page-types/haipipe-page-for-labeling/` | the Job Page type: one Page per corpus and target |
| `/haipipe-plugin-labeling` | `page-plugins/haipipe-plugin-labeling/` | the 🏷 Labeling lane beside a Page: five Spaces and one write door |

Retired names route through the umbrella: `/label-init` and `/label-round` go
to `/label-building`; `/label-evaluate` and `/label-complete` go to
`/label-scanning`; `/label-status` is `/subjective-label status`.

## Plugin contents

```text
subjective-label/
├── .claude-plugin/plugin.json
├── skills/
│   ├── subjective-label/
│   ├── label-building/ · label-building-workflow/
│   ├── label-scanning/ · label-scanning-workflow/
│   ├── subjective-label-workflow/
│   ├── page-types/haipipe-page-for-labeling/
│   └── page-plugins/haipipe-plugin-labeling/  🏷 Labeling surface: five Spaces + one write door
├── agents/                              bounded execution roles
├── engine/                              P0/P1 writers + partial legacy-era primitives
├── ref/                                 authority, artifact, and handoff contracts
├── pages/                               S-Label-1-labeling-lab, a standalone trial Page
├── fixtures/                            job-mini (mock job) + its rendered board
├── field-tests/                         field-test expectations and settlements
├── personas/                            reader lenses (skeptic, close reader, ...)
└── diagram/                             design history and rendered board
```

`engine/` now holds real writers for the start of Building:
`fence_source.py` (build a fenced source), `job.py` (P0 contract, status, and
meaning confirmation), `calibration.py` (round_01 card, random draw, and judge
events), and `gates.py` (`label.py`, `embed.py`, `sample.py`, and
`classify.py` refuse a v2 job before G0). The rest are partial legacy-era
primitives. A skill must return `HOLD` when the current seal, keeper, writer,
reconciler, or audit contract is not implemented (today: LEARN, MEASURE,
CLOSE, later rounds, and all of P2-P5); it must not fall back to
panel-majority gold, public-dataset convergence, or unvalidated
nearest-neighbor inheritance.

## Final deliverables

- `G*`: frozen human-and-machine-readable label policy;
- `D_cal*`: cumulative human-confirmed calibration gold;
- `T*`: sealed, blind human-gold test;
- scorecards: executor quality, uplift, transfer, stability, cost, and errors;
- `D*`: completed corpus with one terminal disposition per item;
- final audit and full provenance.

Version 0.4.0 introduced the Application-style umbrella + sibling-door +
workflow organization, the Building / Scanning names, and the signed Label
Handoff boundary. Version 0.5.0 split each side into a LAW door and an ORDER
workflow, defined the round unit, register, and rendered views, and shipped the
`fixtures/job-mini/` job with its rendered board as the family's acceptance
fixture.
