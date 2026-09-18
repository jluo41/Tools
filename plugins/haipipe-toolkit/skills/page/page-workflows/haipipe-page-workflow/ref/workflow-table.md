# Page Workflow × Space table

This is the canonical Page Run Spec graph projected into Page Spaces. The
serialized controller labels `CONTEXT`, `OUTLINE`, `EVIDENCE`, `CONTENT`, and
`CHECK` remain routing/progress coordinates only; they are not Phase authority
or Run identities.

## Space roster

Page uses the Spaces exposed by its plugins:

| Space | Purpose |
|---|---|
| Draft | Structure, Bullets, candidate prose, and human Scratch capture |
| Evidence | Evidence Item routes and ready Results |
| Runtime (`Run` UI label) | read-only Run/Gate/Route/receipt projection |
| Delivery | Page artifacts, previews, adoption/build receipts |

Context is a generated off-stage record visible through Folder inspection, not
another reader Space.

## Directed Run graph

```text
Page.context
  └─▶ Page.structure (`rp-struct-01`)
         ├─ feedback ─▶ SELF / next Step
         ├─ reopen ───▶ NEW_VERSION
         └─ close ────▶ selected Page.writing and/or Page.evidence Runs

Page.scratch (`rp-scratch-NN_<target>`)
  ├─ Save ─────▶ SELF / update the open Scratch Run
  ├─ Finish ───▶ owning Structure/Section/Paragraph Run as human input
  └─ reopen ───▶ NEW_RUN (a closed Scratch Run is immutable)

Page.writing (`rp-sec-NN`, `rp-para-NN_Pxx[-Pyy]`)
  ├─ feedback ─▶ SELF / next Step
  ├─ reopen ───▶ NEW_VERSION
  ├─ changed target/goal ─▶ NEW_RUN
  └─ accepted + evidence ready ─▶ Page.delivery

Page.evidence (`re-value|cite|display-*` plus Supporting Runs)
  ├─ ready ─▶ Page.writing or Page.delivery
  └─ meaning changed ─▶ Page.structure or NEW_RUN

Page.delivery (`rdNN_<target>`)
  └─ current build ─▶ Page.check

Page.check
  ├─ pass ─▶ CLOSE
  └─ finding ─▶ owning Run Spec | HOLD
```

`SHAPE` and `SURVEY` are Steps inside `rp-struct-01`. `LAND` and `EMBED` are
actions inside Evidence Runs and their binding workflow. Human feedback is a
Step inside one fixed-scope Writing Run. A Page CHECK may be implemented as a
bounded Run when it has a Ticket/Result/receipt; the current controller's
whole-Page check remains a controller close Gate until that identity exists.

The table is not a Version or instance ledger. Reopening the same target adds a
Version inside the existing Run; changing the target adds a Run Instance under
the same parameterized writing Spec. Neither action duplicates the Spec row.
Runs Overview is where those concrete identities and Version/Step state appear.

## Run Spec table

| Run Spec | Run Type | Actor | Target/action | Exit Gate | Routes | Cardinality | Space Cells | Controller labels |
|---|---|---|---|---|---|---:|---|---|
| `context` | `Page.context` | agent/hybrid | freeze Page/Folder identity, policy, requirements, related context | Context is resolved/fresh or truthful HOLD | `structure`, `SELF`, `HOLD` | `1` when commissioned as a durable Run; otherwise controller input assembly | Folder inspection; Runtime if instantiated | `CONTEXT/PREPARE` |
| `structure` | `Page.interactive-writing.structure` | hybrid | whole-Page map, Mermaid, Bullets, paragraph jobs, Evidence Item decisions | accepted Shape + Survey contract | `SELF`, `NEW_VERSION`, selected writing/evidence Specs, `NEW_RUN`, `HOLD` | exactly initial `rp-struct-01`; later ids only for new goals | Draft + Evidence + Runtime | `OUTLINE/SHAPE+SURVEY` |
| `scratch` | `Page.interactive-writing.scratch` | human | rough thinking for one Section or whole paragraph group in the current Outline grammar; no B/symbol target | person manually triggers Finish; AI returns a non-empty Summary | `SELF`, `CLOSE`, `NEW_RUN` | `0..N` per target; closed Run immutable | Draft Scratch + Runtime | `OUTLINE/SCRATCH` |
| `section-writing` | `Page.interactive-writing.section` | hybrid | one named Section goal | explicit scoped acceptance + ready dependencies | `SELF`, `NEW_VERSION`, delivery/evidence, `NEW_RUN`, `HOLD` | `0..S` selected Runs | Draft + Runtime | `OUTLINE/SHAPE`, `CONTENT/WRITE` |
| `paragraph-writing` | `Page.interactive-writing.paragraph` | hybrid | one fixed paragraph/group | accepted text + settled Bullets + ready evidence | `SELF`, `NEW_VERSION`, delivery/evidence, `NEW_RUN`, `HOLD` | `0..K`, `1 <= K <= N` | Draft + Evidence + Runtime | `OUTLINE/SHAPE`, `CONTENT/WRITE` |
| `evidence-item` | `Page.evidence-item` | agent/system/hybrid | one VALUE, CITE, or DISPLAY Result | typed Acceptance and any human verification settle | `SELF`, writing/delivery, `NEW_RUN`, `HOLD` | one RE per make-item + `0..N` Supporting Runs | Evidence + Runtime | `EVIDENCE/LAND+EMBED` |
| `delivery` | `Page.delivery` | agent/system | one web/LaTeX/Word/render target | current artifact + build receipt | `SELF`, check, `NEW_RUN`, `HOLD` | one RD per target | Delivery + Runtime | `CONTENT/WRITE` |
| `check` | `Page.check` or controller Gate | fresh agent/hybrid | one immutable built Page version | pass or named finding route | `CLOSE`, owning Spec, `HOLD` | one Run only when independently ticketed; otherwise no L4 instance | read-only Draft/Evidence/Runtime/Delivery | `CHECK/CHECK` |

## Cell binding law

The row owns target, actor, Gate, Route, Result/receipt contract, and planned
cardinality. A Space Cell binds the owner/worker skill and interaction:

For the corresponding file/folder placement, use the canonical **Workflow ×
Space Specification** in
`page-plugins/haipipe-plugin-outline/ref/space-mapping.md`. It is the physical
projection of this normalized table: each cell records `mode · schema · path`.
In the Page plugin, the user-facing word is `Space`; the normalized schema
continues to use `workspace_id` and `Workspace Cell` as stable internal terms.
The two documents have different jobs and must not become competing
authorities—this file defines Run Specs and their lifecycle contract; the
space-mapping file defines the UI projection and Page-relative storage paths.

```yaml
id: paragraph-writing@draft
workspace_id: draft
mode: action
owner_skill: haipipe-page-workflow
worker_skill_chain: [haipipe-page-outline, haipipe-writing]
interaction: review and revise the fixed paragraph target
gate_binding: {role: collect, gate: exit_gate}
source_projection: {kind: source, source_cell: none, object: Writing Result}
```

The Runtime Cell projects the same `rp-*` id and receipt. It never mints,
renames, copies, or recounts.

## Interactive writing

| Event | Identity consequence |
|---|---|
| ordinary feedback | append next Step in same Version/Run |
| reopen same target and goal | `NEW_VERSION` in same Run |
| explicit scoped acceptance | exit Gate; close or route to next Run |
| changed goal or target | `NEW_RUN` |
| model/tool call or review window | internal operation, no identity |

Use `interactive-writing-run.md` and `writing-step-template.md`. Draft Space
is read-only; human feedback and acceptance enter through the owning Page
Writing Run and its recorded Steps/Versions.

## Evidence layers

```text
0..N Supporting Runs → frozen Local Input → exactly one Page RE make-item Run
                     → VALUE | CITE | DISPLAY Result → bind to target Bullet
```

A planned Evidence Item or route is not an allocated Run. LAND allocates the
owner-native Ticket/Result. EMBED interprets a ready Result and does not create
another Run.

## Cardinality

Let `C` be durable Context Runs actually commissioned, `W` selected Structure/
Section/paragraph Writing Runs, `S` newly commissioned Supporting Runs, `I`
make-item Page RE Runs, `D` Delivery Runs, and `Q` independently ticketed Check
Runs:

```text
Actual Page Runs = C + W + S + I + D + Q
```

Count allocated identities and receipts, not controller labels, Steps,
Versions, paragraphs, tool calls, result files, or Space cards.

## Exact skill chains

```text
haipipe-page → haipipe-page-workflow → Run Spec owner
             → Folder owner → Page Face owner → exact policy/reference
             → haipipe-run + selected worker, when a Run is materialized
```

Worker mapping:

| Work | Primary skill |
|---|---|
| context resolution | `haipipe-page-context` |
| Structure/Bullet/evidence-route planning | `haipipe-page-outline` |
| interactive prose | `haipipe-writing` |
| evidence execution/binding | `haipipe-page-evidence` |
| adoption/delivery | `haipipe-page-content` |
| immutable whole-Page judgment | `haipipe-page-check` |

## Route by broken authority

| Finding | Route |
|---|---|
| stale identity/policy/context | context Run/dispatch |
| wrong map/Bullet/item contract | Structure Run `SELF`, `NEW_VERSION`, or `NEW_RUN` |
| missing/invalid evidence | owning Evidence/Supporting Run |
| prose feedback | current Writing Run Step |
| changed writing target/goal | new Writing Run |
| stale adoption/build | Delivery Run |
| whole-Page defect | the Run Spec that owns the finding |
| unresolved required authority | `HOLD` |

Only a fresh whole-Page check may route the Workflow Runtime to `CLOSE`.

## Audit

- no controller label is counted as a Run;
- every real Run joins one Run Spec and one receipt;
- Gate/Route live on the Run Spec/Instance, not the Space Cell;
- all `rp-*` feedback cycles stay Steps/Versions until target/goal changes;
- every Runtime card projects the same source identity;
- planned and actual cardinality remain separate;
- Page and Supporting Run identities are never renamed across families.
