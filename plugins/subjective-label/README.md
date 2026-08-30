# subjective-label

A human-grounded plugin for building one subjective label and then scanning a
corpus under that frozen meaning.

## Family architecture

```text
subjective-label                         one user-facing umbrella
├── label-building                      semantic calibration side
├── label-scanning                      execution and reliability side
└── subjective-label-workflow           phases, gates, routes, receipts only
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

## The Label Handoff

`handoff/label-v1.yaml` is the only legal crossing. It binds corpus, schema,
`G*`, `D_cal*`, sealed-test manifest checksum, stopping evidence, lineage, and
human signature. It contains no protected test ids or text. Scanning binds the
exact handoff checksum and cannot edit Building artifacts.

## Skills

| skill | responsibility |
|---|---|
| `/subjective-label` | auto-route the job through the family |
| `/label-building` | Contract, calibration Round, Freeze |
| `/label-scanning` | Test, production Scan, final Audit |
| `/subjective-label-workflow` | derive frontier and test gates |

Retired names route through the umbrella: `/label-init` and `/label-round` go
to `/label-building`; `/label-evaluate` and `/label-complete` go to
`/label-scanning`; `/label-status` is `/subjective-label status`.

## Plugin contents

```text
subjective-label/
├── .claude-plugin/plugin.json
├── skills/
│   ├── subjective-label/
│   ├── label-building/
│   ├── label-scanning/
│   ├── subjective-label-workflow/
│   └── page-types/haipipe-page-for-labeling/
├── agents/                              bounded execution roles
├── engine/                                 partial technical primitives
├── ref/                                 authority, artifact, and handoff contracts
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

Version 0.4.0 introduces the Application-style umbrella + sibling-door +
workflow organization, the Building / Scanning names, and the signed Label
Handoff boundary.
