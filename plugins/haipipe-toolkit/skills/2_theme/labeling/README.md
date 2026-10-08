# haipipe-labeling · the labeling theme

A human-grounded package for building one subjective label and then scanning a
corpus under that frozen meaning.

For structured transcript inputs, define the labeling unit and prepare a
versioned, group-fenced item set before Contract; see
[corpus preparation](CORPUS-PREPARATION.md). Other raw formats need an explicit
normalizer before they can use this path.

## Family architecture

```text
haipipe-labeling                       the one user-facing door
├── haipipe-labeling-workflow          the Workflow: Run Specs, dependencies, gates, Routes, handoff
├── haipipe-labeling-building          Building side LAW: authority, human gates, verbs; its step
│                                      order, allocation and receipts in ref/step-order.md
├── haipipe-labeling-scanning          Scanning side LAW; its step order in ref/step-order.md
├── workbench-labeling                 the 🏷 Labeling workbench: four Spaces, one write door
└── one view skill per workbench View, grouped by Space:
    1_data/       haipipe-labeling-preparation · -contract · -embedding
    2_labeling/   haipipe-labeling-definition · -rounds · -guideline
    3_quality/    haipipe-labeling-test · -evaluation · -audit
    4_delivery/   haipipe-labeling-handoff · -scan · -final-labels
```

The split follows one authority boundary:

```text
🏗 Building   asks "is this what the human means?"
              contract Run → calibration Runs → handoff-freeze Run

🔍 Scanning   asks "was that frozen meaning executed reliably?"
              test Runs → production Runs → audit Runs → D*
```

**A Workflow declares Run Specs; its runtime is the concrete Runs.** Each Run Type declares its shared workflow,
domain, procedure, and View context Skills in the
[Run Type–Skill table](haipipe-labeling-building/ref/ref-space-mapping.md#run-type-skills).
P0-P5 remain compatibility capability tags
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
declared in `haipipe-labeling-workflow/SKILL.md`. Gate evidence belongs
to the Run Result/receipt it checks or to a named job control; a gate is not an
extra Run or independent lifecycle unit.

Pick, seal, judge, learn, measure, and decide are steps or verbs inside one
Round; GOLD and SCORE are the two steps inside Test. "Another round" is a route.

A Round is a UNIT on disk (`haipipe-labeling-building/ref/ref-assets.md` §3): `card.md` (the wager a
person releases), `README.md`, `manifest.yaml`, `evidence.md`, `prospect.md`,
the event files, `checkpoint.json`, and a rendered `view/`. Every policy version
carries a rendered `cheatsheet.md` and `gallery.md`; the project keeps a
`register.md` of the seven regions.

## The Label Handoff

`handoff/label-v1.yaml` is the only legal crossing. It binds corpus, schema,
`G*`, `D_cal*`, sealed-test manifest and its count, stopping evidence, lineage,
and human signature. It contains no protected test ids or text. Scanning binds
the exact handoff version (`label-v1` and its date) and cannot edit Building
artifacts.

## Skills

| skill | folder under `skills/2_theme/labeling/` | responsibility |
|---|---|---|
| `/haipipe-labeling` | `haipipe-labeling/` | auto-route the job through the family |
| `/haipipe-labeling-building` | `haipipe-labeling-building/` | the Building law: Contract, Round, Freeze; its step order (steps 1-13), allocation and receipts in `ref/step-order.md` |
| `/haipipe-labeling-scanning` | `haipipe-labeling-scanning/` | the Scanning law: Test, Scan, Audit; its step order (steps 14-26), allocation and receipts in `ref/step-order.md` |
| `/haipipe-labeling-workflow` | `haipipe-labeling-workflow/` | Run Specs, dependencies, gates, Routes, handoff and invalidation |
| `/haipipe-labeling-preparation` | `1_data/haipipe-labeling-preparation/` | transcript units, group reservation and the source-owned Data → Preparation Runs |
| `/haipipe-labeling-<view>` | `<N>_<space>/haipipe-labeling-<view>/` (11, grouped by Space) | one context Skill per workbench View; a Run Type also declares shared workflow, domain, and procedure Skills |
| `/haipipe-page-for-labeling` | `page-types/haipipe-page-for-labeling/` | the Job Page type: one Page per corpus and target |
| `/workbench-labeling` | `workbench-labeling/` | the 🏷 Labeling lane beside a Page: four Spaces, Runs panels and one write door |

Retired names route through the umbrella: `/label-init` and `/label-round` go
to `/haipipe-labeling-building`; `/label-evaluate` and `/label-complete` go to
`/haipipe-labeling-scanning`; `/label-status` is `/haipipe-labeling status`.

## Theme contents

The labeling theme is part of haipipe-toolkit (it was the separate `subjective-label`
plugin until 2026-10-07):

```text
plugins/haipipe-toolkit/
├── skills/2_theme/labeling/
│   ├── haipipe-labeling/
│   ├── haipipe-labeling-building/   (+ ref/step-order.md)
│   ├── haipipe-labeling-scanning/   (+ ref/step-order.md)
│   ├── haipipe-labeling-workflow/
│   ├── 1_data/      haipipe-labeling-{preparation,contract,embedding}/
│   ├── 2_labeling/  haipipe-labeling-{definition,rounds,guideline}/
│   ├── 3_quality/   haipipe-labeling-{test,evaluation,audit}/
│   ├── 4_delivery/  haipipe-labeling-{handoff,scan,final-labels}/
│   ├── haipipe-labeling-building/ref/            authority, artifact, Run, and Space contracts (ref-*.md)
│   ├── workbench-labeling/  🏷 Labeling contract: four Spaces + one write door
│   └── engine/                        P0/P1 writers + partial legacy-era primitives
├── servers/workbench-labeling/        the served 🏷 face (see its README.md); the annotator-only
│                                      host is `servers/_host/serve.py --only labeling`
└── agents/                            bounded execution roles (moderator-agent, sampler-agent, ...)
```

`engine/` now holds real writers for the start of Building:
`fence_source.py` (build a fenced source), `job.py` (P0 contract, status, and
meaning confirmation), `definition_discussion.py` (the human settles each
label's wording before G0; a change is one recorded meaning revision),
`calibration.py` (round_01 card, random draw, and judge
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
