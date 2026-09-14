---
name: page-run-families
description: >-
  The canonical Page-local Run-family contract. It distinguishes RP writing
  Runs, RE Evidence Runs, RD Delivery Runs, workflow passes, and owner-native
  Supporting Runs, and defines how Evidence Items, Results, Cards, and Labels
  bind to one another.
metadata:
  version: "0.1.1"
  last_updated: "2026-09-14"
---

# Page Run families · RP, RE, and RD

This is the single naming and ownership contract for Page-special Runs. A
Page workflow pass is a controller record, not one of these Runs. A native
Task, Discovery, Execution, or Display Run keeps its owner's namespace and is
shown as a Supporting Run when it supplies a Page.

```text
Page workflow pass                 controller receipt; not a Level-4 Run
        │
        ├── RP  Page Writing Run   human/agent structure or prose iteration
        ├── RE  Page Evidence Run  one Page Evidence Item's execution lineage
        └── RD  Page Delivery Run  one target/version shipped from the Page

owner-native rNN / bNN.jNN.tNN.rNN  Supporting Run; never renamed to RP/RE/RD
```

## The three Page-special families

| Family | Meaning | Typical identity | Owns | Does not own |
|---|---|---|---|---|
| `RP` | Page Writing Run | `rp00_mermaid-structure`, `rp01_p01-p03` | bounded human/Page interaction, feedback Steps, candidate prose | final Page Content, evidence truth, delivery acceptance |
| `RE` | Page Evidence Run | `re01_e18-variable-operationalization` | one Page Evidence Item's frozen input, execution/normalization, and current Result lineage | upstream source truth, unrelated Evidence Items, whole-Page acceptance |
| `RD` | Page Delivery Run | `rd01_web`, `rd02_latex`, `rd03_word` | one delivery target/version, its artifact, and build receipt | Page prose authority, Evidence truth, human CHECK close |

The counters are independent. `rp03`, `re03`, and `rd03` are unrelated
identities. A family prefix is never rewritten into an owner-native Run id,
and an owner-native Run id is never made to look like an `RP`, `RE`, or `RD`.

### RP · Page Writing Run

`RP` is the persistent interaction unit for agreeing structure or wording.
`rp00_mermaid-structure` is reserved for the Page-global argument map and
paragraph index. Later `rpNN_pNN[-pNN]` Runs cover one independently closable
human question. A new chat window does not create a new RP; feedback advances
Steps and Versions inside the existing RP.

Closing an RP settles a candidate wording and its local decisions. CONTENT
adopts accepted wording into the Page source. RP never silently changes the
Page source, Evidence Result, or delivery artifact merely because a Step
closed.

### RE · Page Evidence Run

`RE` is the Page-owned identity for one Evidence Item's evidence-making work.
It may call, reuse, or normalize zero-to-many owner-native Supporting Runs and
freezes one Local Input. It emits one typed Page Evidence Result for the
target item. Ordinary retries are attempts within the same RE lineage; create
a new RE only when the evidence contract or lineage is materially replaced,
or when the old lineage must remain auditable as retired.

The Page contract is therefore:

```text
one Evidence Item obligation
        └── one current RE lineage
                └── one current accepted Result
                        └── one read-only Evidence Card
                                └── zero-to-many Evidence Labels
```

Supporting Runs may be many because they are upstream inputs. They do not
replace the Page's RE and they do not become the Page's Evidence Card.

### RD · Page Delivery Run

`RD` is commissioned after the content/evidence release barrier is open. One
RD targets one delivery lane and concrete source version: for example web,
LaTeX, Word, slides, or a rendered recipient preview. It records the output
artifact, source/version binding, build diagnostics, and the delivery receipt
(normally `delivery/<lane>/build-manifest.json`).

Different targets or materially different source versions use different RD
identities. A rebuild of the same target may be a new attempt in the same RD
lineage when the target contract is unchanged. RD can report a failed or
partial build; only Page CHECK decides whether the whole Page is closed.

## Evidence Item, Result, Card, and Label

These words name different layers and must not be used interchangeably:

| Object | Layer | Definition | Authority |
|---|---|---|---|
| Evidence Item | authored plan | one immutable, typed obligation such as `E18-VALUE-...` | Outline SHAPE/SURVEY |
| Evidence Run (`RE`) | execution | the Page-local lineage that makes that item ready | Page EVIDENCE/LAND |
| Evidence Result | fact | the typed `result.yaml` plus payload emitted by the RE | Result path and its provenance |
| Evidence Card | UI projection | a read-only view of one current Result, with its item and run context | derived from Result |
| Evidence Label | inline reference | a stable token that points to one Result payload/claim/display/citation | label binding in the Result manifest |

An Evidence Item is not a Card and is not a Run. In the current Page state,
one item normally has one current RE and one current Result, so the UI may
make them look like one card. That is a convenient one-to-one projection,
not a definition of the objects.

One Result/Card may expose many labels. For example:

```text
RE → Result/Card
       ├── $V_adjusted_fx$
       ├── \figure{D_effect_forest}
       ├── \table{D_regression_main}
       ├── \algorithm{D_algorithm_block}
       └── \cite{C_prior_work}
```

`DISPLAY` is the umbrella type for a placed visual or structured presentation:
a table, figure, diagram, illustration, or algorithm block. `TABLE` is only a
compatibility alias/subtype of `DISPLAY`, not a fourth Page Run family or a
separate Card lane. A table, figure, or algorithm-block label therefore uses
the `D_` namespace. These are deliberately LaTeX-like placeholders. Their visible value or
display may be embedded now, while the hidden binding retains the label, the
Evidence Item, the RE, the Result path, and the provenance needed to resolve
it later. A label is not an independent Evidence Item merely because it is
used several times. If a label needs its own acceptance decision, provenance,
or execution lineage, split the obligation into another Evidence Item and RE.

The canonical binding shape is conceptual; implementations may serialize it
in YAML or JSON:

```yaml
item: E18-VALUE-variable-operationalization
page_run: re01_e18-variable-operationalization
result: results/re01_e18-variable-operationalization/result.yaml
labels:
  - token: "$V_adjusted_fx$"
    kind: VALUE
    target: payload.value.adjusted_fx
  - token: "\\cite{C_prior_work}"
    kind: CITE
    target: payload.sources.prior_work
```

The `item` and `page_run` fields are the stable joins. The `result` is the
fact source. The Card and inline labels are recomputed views and must not
become competing stores of evidence truth.

## Storage and routing

Page-special tickets use the Page-readable family identity:

```text
runs/rpNN_<slug>     Writing Run ticket
runs/reNN_<slug>     Evidence Run ticket
runs/rdNN_<slug>     Delivery Run ticket
results/reNN_<slug>/result.yaml
delivery/<lane>/     RD-produced delivery artifacts and receipts
```

An `RE` is the Page ticket/lineage identity. An owner-native Task may still
own the actual executable Ticket and canonical Result under the Folder/Task
dialect. The RE records that full owner-native id, Result path, and hash; it
never copies or renames the upstream Result just to make it appear Page-local.
When the Folder uses its own canonical output root, `results/<re-run>/` is the
Page-readable binding/projection and the owner-native resolved Result path is
the fact source.

The Run Space may present four logical groups—RP, RE, RD, and Supporting
Runs—even though the Page has one Run presenter. The Delivery plugin remains
one visible tab; its build actions and receipts are RD-backed rather than a
second delivery-quality system.

## Boundaries

- `RP`, `RE`, and `RD` are Page-local Run families, not new workflow phases.
- The workflow pass receipt is not an RP, RE, or RD and must not be counted as
  one.
- `RE` is item-scoped; there is no umbrella Page-wide “Evidence Run”.
- Supporting Runs remain accountable to their owner. The Page RE only binds
  their outputs into the Page's frozen Local Input and Result.
- `RD` does not reopen or rewrite evidence. A stale delivery routes to a new
  delivery attempt/RD, and a changed evidence obligation routes through the
  normal EVIDENCE/CONTENT rules first.
- Page CHECK remains the only human whole-Page close gate.
