# subjective-label

A human-grounded plugin for building one subjective label and then scanning a
corpus under that frozen meaning.

## Family architecture

```text
subjective-label                         one user-facing umbrella
├── label-building                      Building side LAW: authority, human gates, verbs
├── label-building-workflow             Building side ORDER: round steps, item resume, round receipts
├── label-scanning                      Scanning side LAW
├── label-scanning-workflow             Scanning side ORDER: test lock, runs, risk queue, audit loop
└── subjective-label-workflow           the CROSSING: phase numbers P0-P5, gates G0-G6, handoff, invalidation
```

The split follows one authority boundary:

```text
🏗 Building   asks "is this what the human means?"
              Contract → Round × N → Freeze → signed Label Handoff

🔍 Scanning   asks "was that frozen meaning executed reliably?"
              Test → Scan → Audit → D*
```

One identified human is the semantic authority. Models may retrieve, predict,
diagnose, draft, and execute; their consensus never creates human gold.

## Six journey phases

| phase | side | authority artifact | purpose |
|---|---|---|---|
| P0 Contract | Building | config + corpus manifest + test reservation | establish one valid job |
| P1 Round | Building | closed checkpoint | refine `D_t` and `G_t` |
| P2 Freeze | Building | `handoff/label-v1.yaml` | sign `G*` and `D_cal*` |
| P3 Test | Scanning | blind `T*` gold + frozen scorecards | qualify an executor route |
| P4 Scan | Scanning | production run | create one terminal candidate per item |
| P5 Audit | Scanning | final audit receipt | support a bounded `D*` claim |

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

| skill | responsibility |
|---|---|
| `/subjective-label` | auto-route the job through the family |
| `/label-building` | the Building law: Contract, Round, Freeze |
| `/label-building-workflow` | the Building order: card, prepare, prospect, judge, learn, close |
| `/label-scanning` | the Scanning law: Test, Scan, Audit |
| `/label-scanning-workflow` | the Scanning order: gold, score, manifest, attempts, queue, audit, repair |
| `/subjective-label-workflow` | phase numbers, gates, the crossing |

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
│   └── page-plugins/haipipe-plugin-labeling/  🏷 receipt workbench + Page Chat
├── agents/                              bounded execution roles
├── engine/                                 partial technical primitives
├── ref/                                 authority, artifact, and handoff contracts
├── fixtures/                            job-mini (mock job) + its rendered board
└── diagram/                             design history and rendered board
```

The `engine/` folder still contains partial legacy-era primitives. A skill must
return `HOLD` when the current seal, keeper, writer, reconciler, or audit
contract is not implemented; it must not fall back to panel-majority gold,
public-dataset convergence, or unvalidated nearest-neighbor inheritance.

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
