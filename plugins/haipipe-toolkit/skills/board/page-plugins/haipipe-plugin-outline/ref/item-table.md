# The Evidence Item table · `<stem>-evidence-items.md`

The Evidence Item table is the authored contract between planning and work. It
answers, for every thing the approved outline needs:

1. **What ready evidence is expected?** SHAPE specifies this.
2. **Which upstream Results support it?** SURVEY maps and classifies zero or
   more Supporting Run routes.
3. **Which one local Run makes it ready for this Page?** SURVEY declares
   exactly one Page · Evidence Item route; LAND allocates it when needed and
   executes it.

SHAPE and SURVEY are planning cycles. Neither scaffolds or executes a Level-4
Run. SURVEY reserves a complete Paper-local P/J/T/R address for each proposed
local Run; LAND is the first cycle that creates its Ticket/runtime receipt,
executes it, or materializes a Result.

```text
<stem>-evidence-items.md  AUTHORED   item identity + expectation + audited candidate Run graph
<stem>-evidence.md        GENERATED  the same items joined to Run receipts and Results
```

## The unit · one typed item with a readable name

Every item has one immutable id:

```text
E<NN>-<TYPE>-<slug>
```

The initial type vocabulary is closed:

| Type | Ready evidence | Typical local Result |
|---|---|---|
| `VALUE` | a checked scalar, interval, count, or comparison | structured value + units + provenance |
| `CITE` | a source claim ready to cite | verified citation record + supported claim |
| `DISPLAY` | a figure, table, diagram, or illustration ready to place | preview/build artifact + caption claim + provenance |

Examples: `E01-VALUE-adjusted-effect`, `E02-DISPLAY-effect-forest`,
`E03-CITE-prior-work`. Never use a bare `E01`: the type and human-readable
name must be visible before SURVEY can plan Runs.

The item id is stable across outline versions. If its evidence type, target,
or acceptance meaning changes materially, create a new item id and retire the
old one; do not silently redefine it.

## The authored grammar

```text
# <stem> · evidence items
page: <stem>
kind: evidence-items · authored · SHAPE specifies; SURVEY classifies; LAND allocates/binds
plan: v<N>
surveyed: YYMMDD HHMM · <who>

### E01-VALUE-adjusted-effect · C2.P3.B1 · adjusted treatment effect
- **Target**: C2.P3.B1
- **Label**: AdjustedFx
- **Need**: the adjusted effect estimate used by this bullet
- **Expected**: VALUE · estimate, 95% interval, unit, population, and model label
- **Acceptance**: recomputes from named Results; aggregate only; no row-level data
- **Supporting Runs**: Execution · reuse · b01j02t03r04; Discovery · registered · b02j01t05r01
- **Local Input**: Supporting Results + page-local methods.yaml
- **Local Run**: Page · Evidence Item · new-run · pj01t01r01
- **Decide**: ☑ make · JL 260901
> Comment JL · local input freezes both Supporting Results before execution · 260901
```

The record head has three parts: item id, target bullet address, and a short
human-readable evidence name. `Target` repeats the address intentionally so
record renderers can show it as a column. The labels are fixed and ordered:

The Board wall projects that identity as
`E<n><kind>.<Label>`, where
`V = VALUE`, `C = CITE`, and `D = DISPLAY`; for example,
`E3V.AdjustedFx`. `Label` is authored by SHAPE, contains one or two concepts,
matches `[A-Za-z][A-Za-z0-9]{0,11}`, and stays stable unless the item's
meaning changes. It is never generated from the full readable name. Legacy
records without `Label` receive a bounded 12-character fallback until their
next SHAPE pass. This compact label is presentation only:
the immutable `E<NN>-<TYPE>-<slug>` remains the authored id and is exposed in
the item detail. A wall must never show only `E01 · VALUE`, because that hides
what the evidence contains. It must also present `Supporting Runs` and `Local
Run` as separate columns; they are different graph layers, not one folded
`Route` field. A real global Supporting Run is shown in readable dotted form, such as
`b01.j02.t03.r04`, links to its owning card in the Outline Evidence Workspace,
and carries a short next-action label (`run`, `rerun`, or `reuse`). A real
Ticket that has never produced an attempt receipt is `registered`; a prior
failed, smoke-only, invalid, or explicitly stale attempt is `rerun`. `Ticket
only` is a derived Result-availability state, not a competing action token. An
absent external Ticket is displayed as `needs … Run` and never assigned an invented
address. A Paper-local proposed Run instead reserves its own non-colliding
`pjNNtNNrNN` plan identity and displays `P jNN.tNN.rNN plan`. An unregistered
`new-*` route is an honest SURVEY finding and may
close SURVEY when its parent route and bounded design are explicit; LAND later
allocates the `rNN`. The Page Outline grid has no
separate item `Status` column: colour is only the compact signal. A Run
popover separates its Purpose/Plan, Availability, and Next action; it never
uses `new`, `rerun`, `run only`, or `ready` as one mixed status. `CITE`
items share the Evidence column with VALUE and DISPLAY;
several citation items may support one bullet.

The Outline Evidence Workspace reuses this same `E<n><kind>.<Label>` identity.
Its `Evidences` lens renders one card per Evidence Item and explains what that
Evidence is about, what it must contain, and when it is ready. Its `Runs` lens
groups by Evidence and renders one card per mapped Supporting or Paper-local
Run inside that group. A shared Run may appear under several Evidences; the
surface reports both total Run mappings and unique Run identities so repetition
is explicit. Planned routes remain visible there but are not counted as
allocated Runs by the top-level `⚙️ Runs` plugin. Reader-facing paths are named `Run` and
`Result`; legacy Ticket/receipt fields may be parsed internally but never
appear as competing UI terms. Exact repository-relative paths live under the
collapsed `Run & Result paths` disclosure and must wrap within the card.

| Label | Written by | Contract |
|---|---|---|
| `Target` | SHAPE | exactly one `C<n>.P<m>.B<k>` address |
| `Label` | SHAPE | stable 1–12 character ASCII alphanumeric display name; one or two concepts |
| `Need` | SHAPE | why the outline needs this item, in one line |
| `Expected` | SHAPE | `<TYPE> · <ready-to-use payload>` |
| `Acceptance` | SHAPE | observable checks for the ready Evidence Result |
| `Supporting Runs` | SURVEY | `[]` or a semicolon-separated list of existing `Family · reuse/rerun/registered · full global Run id` and/or planned `Family · new-* · parent route` entries |
| `Local Input` | SURVEY; LAND freezes | one envelope plan: Supporting Results plus named governed page-local paths when needed; LAND appends `→ <packet>#<sha256>` |
| `Local Run` | SURVEY declares; LAND allocates/binds | exactly one Paper-local `Page · Evidence Item · new-run/reuse/rerun/registered · pjNNtNNrNN [→ Result]`; `new-run` has no Ticket |
| `Decide` | human gate | `☐ make` or signed `☑ make/defer/drop` |

Comments hold rationale; they never replace an expected payload, acceptance
test, or Run address. A typed `Status` label is a defect because status is
derived from receipts and Results.

## The Run graph · zero-to-many supports, exactly one local Run

```text
Supporting Runs  0..N  Execution | Discovery
                         ↓ validated upstream Results
Local Input       1     one frozen envelope containing those Results/local sources
                         ↓
Local Run         1     Page · Evidence Item
                         ↓
Ready Result      1     VALUE | CITE | DISPLAY, accepted by this item's contract
```

This is the precise meaning of “one input and one execution”: one Evidence
Item has one frozen input envelope and exactly one local execution. The input
envelope may contain zero, one, or many Supporting Results plus pre-existing
governed page-local artifacts named in `Local Input`. Cross-Folder evidence
must enter through a Supporting Run Result. Calls, retries,
scripts, render passes, and model turns inside that local execution remain
implementation details unless they independently satisfy the base Run tests.

The local Result is factual and reusable; it does not interpret the evidence
for the Page. EMBED owns that interpretation and writes it into the next
outline version.

Paper-local indexing is structural: `P` is the fixed Paper block, `jNN`
indexes the Page, `tNN` preserves the Evidence Item number, and `rNN` indexes
the attempt. Thus Abstract Page `j01`, item `E03`, first proposed attempt is
stored as `pj01t03r01` and shown as `P j01.t03.r01 plan`.

## Run detail · description, availability, and action are different facts

The Evidence Workspace presents every mapped Run with three independent
fields:

| Field | Meaning | Authority |
|---|---|---|
| `Purpose` / `Plan` | what the Run does; use `Plan` when no Run exists yet | allocated Ticket + Evidence Item, or the authored Expected/Acceptance/Local Input plan |
| `Availability` | `Planned`, `Run exists · Result missing`, `Run + Result`, or `Paths unresolved` | paths resolved from disk |
| `Next action` | `Allocate and run`, `Run`, `Rerun`, `Reuse Result`, or `Resolve path` | SURVEY action plus resolved availability |

Do not store a new Run-description or status file. For an existing Run, its
Ticket remains the purpose authority and the Evidence Item explains why it is
used here. For a proposed Page-local Run, the plan remains in
`<stem>-evidence-items.md`: Expected and Acceptance define the Result target,
and Local Input defines the future frozen envelope. LAND creates the authored
Run in `runs/`; the generated output and runtime receipt live under
`results/`. Raw paths are selectable text in the popover, never download
anchors.

## Families and actions are separate dimensions

Supporting Run families are only:

```text
Execution   computation · data · model · deterministic tooling
Discovery   search · papers · sources · external evidence
```

The action vocabulary is:

| Action | Meaning at SURVEY | Address rule |
|---|---|---|
| `reuse` | an accepted Result already satisfies this support or local target | full global Run id and registered Ticket/receipt required |
| `rerun` | the same frozen Run contract must execute again | full global Run id and registered Ticket/receipt required |
| `registered` | a real Ticket exists but has not produced a completed attempt; LAND will execute it | full global Run id required |
| `new-run` | no Run Ticket exists; LAND allocates/scaffolds | Supporting: parent `bNNjNNtNN`; Paper-local: reserved `pjNNtNNrNN` |
| `new-task` | task does not exist; LAND scaffolds task and Run | parent `bNNjNN` |
| `new-job` | job does not exist; LAND scaffolds job, task, and Run | parent `bNN` |
| `new-block` | only a bounded planned block exists; LAND routes it through the owning workflow | planned block name |

Supporting `reuse`, `rerun`, and `registered` name a full global id such as
`b01j02t03r04`; Paper-local actions name `pjNNtNNrNN`. `rerun` means an execution was attempted or the existing
historical Ticket is explicitly required to run fresh; a never-attempted real
Ticket is `registered`. The derived phrase `Ticket only` describes missing
Result availability and never replaces the action. `rerun` preserves the same
target, frozen inputs, and acceptance contract. If
any of those change materially, register a new Run and record
`supersedes: b01j02t03r04` in the new Run receipt.

There is no `person`, `found`, or `none` action. A citation can use a Discovery
Supporting Run; existing work is `reuse`; and an impossible item routes back
to SHAPE. No supports is represented structurally as `Supporting Runs: []`.
`Supporting Runs: []` is valid only when `Local Input` names sufficient
pre-existing page-local material or says `item contract only` for a genuinely
source-free construction.

A sibling Evidence Item's future local Result is never an implicit local input.
If two items need the same upstream evidence, both list the same Execution or
Discovery Supporting Run (normally `reuse`). This keeps item graphs independently
closable and preserves LAND's item-level parallelism.

## Cross-Folder evidence uses Supporting Results

There is no active `PageX Bindings` field. A Result owned by another Folder
enters this graph as a Supporting Run with a full Run id and validated Result
path. A related Page or Folder link belongs to Context Workspace and remains
navigation or a constraint until a Supporting Run makes an independently
auditable Result available.

A governed static source already owned by this Page may be named directly in
`Local Input` with its path and frozen hash. That exception does not authorize
copying an external Result into the Page or using a whole Folder as evidence.

Legacy rows containing `PageX Bindings` are migration input only. SURVEY must
convert each evidentiary binding to a Supporting Run Result or, when it is
truly page-local, to a governed Local Input path. New rows never write the
field.

## What SHAPE, SURVEY, LAND, and EMBED write

| Cycle | Level-4 Runs? | Writes to this table |
|---|---:|---|
| SHAPE | none | item id/name/type, Target, Label, Need, Expected, Acceptance |
| SURVEY | none; Paper address reservation only | classified existing/planned Supporting routes, one Local Input plan, exactly one indexed Paper-local Run, Decide gate |
| LAND | allocate/scaffold planned routes, then execute/reuse | full allocated Run ids, frozen Local Input, and `→ <Result>` on completed bindings |
| EMBED | none | nothing; it writes `Answered:` or `Drawn:` into outline v<N+1> |

SURVEY is complete when every approved item has every Supporting and Local
route honestly classified as existing Result, Ticket only, rerun, or bounded
new design; one explicit Local Input plan; and a signed
decision. Existing Supporting routes carry full ids; planned Supporting routes
carry only their real parent address or bounded block name. Every planned Local
Run carries its Paper-local `pjNNtNNrNN` address. `Ready` on a Run means its Ticket is
ready to execute; evidence-item `ready` still requires a validated local
Result. LAND refuses an undecided or ambiguous route, not an honestly planned
unallocated route. Item graphs may execute in parallel,
but within one item its local Run waits until every declared Supporting Result
is valid and frozen into the input envelope. LAND closes only
when both the Supporting and local Run layers are finished for every `make`
item.

## Derived status · simple in the overview, detailed on click

The generated `<stem>-evidence.md` and Runs surface derive one compact item
state; the authored table never stores it:

| State | Meaning | Next cycle |
|---|---|---|
| `specified` | SHAPE fields exist; Run graph or decision is incomplete | SURVEY |
| `planned` | Run graph is complete and `Decide = make`; local Result absent | LAND |
| `ready` | the local Page · Evidence Item Result exists and passes acceptance | EMBED |
| `folded` | the next outline version binds the ready Result | SHAPE / CONTENT |
| `accepted` | the Page passed CHECK | closed |
| `stale` | a bound Result changed after the fold | LAND or EMBED |
| `deferred` | signed defer | human route |
| `dropped` | signed drop | SHAPE if the outline still asks for it |
| `blocked` | a commissioned Run truthfully cannot complete | LAND / SHAPE |

The overview stays compact: canonical item identity, target, support count,
local Run, state, and Result. Clicking the item or Run reveals the frozen
input, individual Supporting Runs, governed local-source hashes, Run/Result
paths, acceptance checks, and artifacts.
