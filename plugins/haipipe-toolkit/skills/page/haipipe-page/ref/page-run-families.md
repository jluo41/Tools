---
name: page-run-families
description: >-
  The canonical Page-local Run-family contract. It distinguishes RP writing
  Runs, typed RE Evidence Runs, RD Delivery Runs, workflow passes, and
  owner-native Supporting Runs, and defines how Evidence Items, Results,
  Cards, and Labels bind to one another.
metadata:
  version: "0.3.3"
  last_updated: "2026-09-20"
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
        ├── RE  Page Evidence Run  one Page Evidence Item's lineage
        └── RD  Page Delivery Run  one delivery target/version

owner-native rNN / bNN.jNN.tNN.rNN  Supporting Run; never renamed to RP/RE/RD
```

## The three Page-special families

| Family | Meaning | Canonical identity | Owns | Does not own |
|---|---|---|---|---|
| `RP` | Page Writing Run | `rp-struct-01`, `rp-scratch-01_C1.P1`, `rp-sec-01`, `rp-para-01_P03-P05`, `rp-revise-01_C1.P3` | bounded human/Page interaction, Scratch capture, feedback Steps, candidate structure/prose; `rp-struct-01` fuses SHAPE + SURVEY | final Page Content, evidence truth, delivery acceptance |
| `RE` | Page Evidence Run | `re-value-01_<slug>`, `re-display-01_<slug>`, `re-cite-01_<slug>` | one Evidence Item's frozen input, evidence work, and current Result lineage | upstream source truth, unrelated items, whole-Page acceptance |
| `RD` | Page Delivery Run | `rd01_web`, `rd02_latex`, `rd03_word` | one delivery target/version, artifact, and build receipt | Page prose authority, Evidence truth, human CHECK close |

`RP`, `RE`, and `RD` counters are independent. The typed RP and RE
sequences are also independent within their own kinds: `rp-struct-01` and
`rp-sec-01` may coexist, as may `re-value-01` and `re-display-01`. Never
renumber an allocated identity. Existing records using the retired compact
forms such as `rp00_mermaid-structure` or `re01_<slug>` are compatibility input
only during migration; active Page folders, packets, links, and new allocation
use the canonical forms above.

### RP · Page Writing Run

`RP` has five explicit kind tokens. The kind is part of the identity; there
are no hidden numeric bands:

| Identity | Scope | Required output and boundary |
|---|---|---|
| `rp-struct-NN` | Page Structure Run: SHAPE + SURVEY | Page direction, coverage/non-coverage, high-level section flow, ordered Bullets, Point roles, paragraph jobs, typed evidence decisions, and structure list |
| `rp-scratch-NN_<target>` | human Scratch capture | rough thinking for one Section (`C1`) or whole paragraph group (`C1.P1`) in the current Outline grammar; there is no separate subsection node and B/symbol rows are not Scratch targets; the person manually triggers Finish Scratch, which asks the AI for a Summary before closing; does not edit `Draft:` prose |
| `rp-sec-NN` | Section-level writing | one named Section drafting/revision session and its review loop |
| `rp-para-NN_Pxx[-Pyy]` | paragraph-level writing | one fixed paragraph or contiguous paragraph group |
| `rp-revise-NN_<target>` | Revise: before and after | two frozen texts of one target (two Versions of a writing Run, an accepted Version against a delegated paragraph Result, or two built Page versions) compared into one change ledger; every row decided; the accepted text returns to the owning writing Run as a Version; owns decisions, never prose (`haipipe-page-revise`) |

`NN` starts at `01` independently for each kind. `rp-struct-01` is the first
Structure Run and contains both SHAPE and SURVEY. It can have several human
participants; record one shared Run and one paired Result, with contributors
on each Step. `rp-struct-02` is a later independent structure/Bullet Run, not a
new Survey pass or a new participant.
Scratch may be commissioned at a Section or whole paragraph-group target as
soon as the selected Outline exists; it is a human thinking aid, not a replacement for
the Structure gate. After the structure contract is closed, Section Runs begin
at `rp-sec-01` and paragraph Runs begin at `rp-para-01_P01` (or the selected
exact target).
The paragraph target is mandatory and uses the Page-global `P01..PN` index.

```text
RP Run   = one independently commissioned writing session/round at a fixed scope
Step     = one complete draft → review/rating → diagnose → revise cycle
Version  = one append-only candidate snapshot/journal inside that Run
```

A complete Section cycle is one Step, not a new Run. A later independent
Section session receives the next `rp-sec-NN`. A revisit of the same fixed
paragraph target normally reopens its existing `rp-para-NN_Pxx[-Pyy]` in a
new Version; a materially different target or goal receives a new Run.

### RE · Page Evidence Run

`RE` is the Page-owned evidence lineage for one Evidence Item. Its kind token
names the focal Result, not every label that the Result may expose:

| Identity | Focal Result | Additional field |
|---|---|---|
| `re-value-NN_<slug>` | one value or coherent value set | `kind: value` |
| `re-display-NN_<slug>` | one display unit | `kind: display`; `display_kind: table\|figure\|algorithm` |
| `re-cite-NN_<slug>` | one citation/source bundle | `kind: cite` |

`DISPLAY` is the umbrella type. A table, figure, or algorithm block is a
display subtype and uses the same `D_` label namespace; there is no `re-table`
or `re-figure` family. Conceptual diagrams or AI illustrations, when used,
are delivered as ordinary figures and therefore use `\figure{D_<slug>}` rather
than introducing `\diagram{...}` or `\illustration{...}` Page labels.

```text
one Evidence Item obligation
        └── one current RE lineage
                └── one current accepted Result
                        └── one read-only Evidence Card
                                └── zero-to-many Evidence Labels
```

An RE may consume zero-to-many owner-native Supporting Runs and freezes one
Local Input. A single Result/Card may therefore expose all of these labels:

```text
RE → Result/Card
       ├── $V_adjusted_effect$
       ├── $V_ci_lower$
       ├── \figure{D_effect_forest}
       ├── \table{D_regression_main}
       ├── \algorithm{D_algorithm_block}
       └── \cite{C_prior_work}
```

The placeholder is deliberately LaTeX-like and may remain unresolved during
writing. Its hidden binding records the label, Evidence Item, RE, Result path,
Card projection, and provenance. The later resolver replaces or renders the
placeholder; it does not create a new Run.

Use one RE when the labels share the same focal target, frozen inputs, worker,
and acceptance gate. Split into another Evidence Item and RE when a value,
display, or citation needs an independent execution lineage, provenance,
acceptance decision, or lifecycle. A citation attached to a value is normally
just a `C_` Label on that value's Card, not a second `re-cite`.

The canonical conceptual binding is:

```yaml
item: E18
page_run: re-value-01_adjusted-effect
kind: value
result: results/re-value-01_adjusted-effect/result.yaml
labels:
  - token: "$V_adjusted_effect$"
    kind: VALUE
    target: payload.value.adjusted_effect
  - token: "\\cite{C_analysis_source}"
    kind: CITE
    target: payload.sources.analysis_source
```

### Result `labels:` manifest

The root-level `labels:` list is the machine-readable bridge between authored
tokens and the current Result/Card. It is optional while an RE is pending, but
each token emitted or resolved by a ready Result must have one entry:

```yaml
labels:
  - token: "$V_adjusted_effect$"
    kind: VALUE
    key: V_adjusted_effect
    target: payload.estimate
    status: resolved
    display: "100"
  - token: "\\figure{D_effect_forest}"
    kind: DISPLAY
    display_kind: figure
    target: payload.unit
    status: resolved
    display: "Effect forest"
  - token: "\\cite{C_analysis_source}"
    kind: CITE
    target: payload.sources.analysis_source
    status: unresolved
```

`token` is the authored identity and is never deleted when `display` is
available. `display` is the reader-facing value used by Draft Space and the
Evidence Card; `status: unresolved|pending|missing` keeps the token visible.
The renderer may place the display inline, but its disclosure must retain the
token, Item, current RE, Result path, target, and provenance. `labels` is a
one-to-many projection of one Result/Card; it does not create additional Items,
Runs, or Cards. Duplicate tokens within one Page are a contract error and are
not silently merged.

An RE is not the underlying computation or search. Those remain native
Supporting Runs; the RE binds their validated Results into one Page evidence
contract. An Evidence Result becomes Page evidence only at LAND, and Page
interpretation belongs to EMBED.

### RD · Page Delivery Run

`RD` is commissioned after the content/evidence release barrier is open. One
RD targets one delivery lane and concrete source version: web, LaTeX, Word,
slides, or a rendered recipient preview. A rebuild of the same target may be
another attempt in the same RD lineage when its contract is unchanged.
Different targets or materially different source versions use different RD
identities. RD does not reopen or rewrite an RE.

## Evidence Item, Result, Card, and Label

These words name different layers and must not be used interchangeably:

| Object | Layer | Definition | Authority |
|---|---|---|---|
| Evidence Item | authored plan | one typed obligation, such as `E18-VALUE-variable-operationalization` | Outline SHAPE/SURVEY |
| Evidence Run (`RE`) | execution/lineage | the Page-local typed lineage that makes that item ready | Page EVIDENCE/LAND |
| Evidence Result | fact | typed `result.yaml` plus payload emitted or bound by the RE | Result path and provenance |
| Evidence Card | UI projection | read-only view of one current Result with item and run context | derived from Result |
| Evidence Label | inline reference | stable token pointing to one Result payload, claim, display, or citation | Result manifest binding |

An Evidence Item is not a Card and is not a Run. One current item has one
current RE and one current Result/Card projection. One Result/Card may expose
many labels. A label can be referenced by many Bullets or paragraphs, but its
current authority is one Result/Card binding.

## Storage and routing

Page-special tickets use the Page-readable family identity:

```text
runs/rp-struct-NN.md
runs/rp-scratch-NN_<target>.md
runs/rp-sec-NN.md
runs/rp-para-NN_Pxx[-Pyy].md
runs/rp-revise-NN_<target>.md
runs/re-value-NN_<slug>.md
runs/re-display-NN_<slug>.md
runs/re-cite-NN_<slug>.md
runs/rdNN_<target>.md
results/<same-run>/
delivery/<lane>/
```

The Folder dialect may place the executable owner-native Ticket and canonical
Result elsewhere. The RE records that full owner-native id, Result path, and
hash; it never copies or renames an upstream Result to imitate Page-local
storage.

## Boundaries

- `RP`, `RE`, and `RD` are Page-local Run families, not Runs.
- RP kind tokens are `struct`, `scratch`, `sec`, and `para`; paragraph identities expose
  their exact `Pxx` target or contiguous range.
- RE kind tokens are `value`, `display`, and `cite`; `display_kind` distinguishes
  table, figure, and algorithm. Other renderer mechanisms remain internal and
  are cited as the resulting Page `figure` when they become a display.
- One Evidence Item has one current RE lineage and one current Result/Card;
  that Card may expose many `V_`, `D_`, and `C_` Labels.
- Supporting Runs remain accountable to their owner. The Page RE binds their
  outputs into the frozen Local Input and Result.
- A workflow pass is not an RP, RE, or RD and must not be counted as one.
- Page CHECK remains the only human whole-Page close gate.
