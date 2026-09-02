# The Evidence Item table · `<stem>-evidence-items.md`

The Evidence Item table is the authored contract between planning and work. It
answers, for every thing the approved outline needs:

1. **What ready evidence is expected?** SHAPE specifies this.
2. **Which accepted cross-Folder sources does it bind?** SURVEY records zero
   or more exact PageX bindings.
3. **Which upstream Results support it?** SURVEY registers zero or more
   Supporting Runs.
4. **Which one local Run makes it ready for this Page?** SURVEY registers
   exactly one Page · Evidence Item Run; LAND executes it.

SHAPE and SURVEY are planning cycles. Neither executes a Level-4 Run. SURVEY
may allocate and scaffold Tickets with planned runtime receipts; LAND is the
first cycle that executes a Run or materializes a Result.

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
kind: evidence-items · authored · SHAPE specifies; SURVEY registers; LAND binds
plan: v<N>
surveyed: YYMMDD HHMM · <who>

### E01-VALUE-adjusted-effect · C2.P3.B1 · adjusted treatment effect
- **Target**: C2.P3.B1
- **Need**: the adjusted effect estimate used by this bullet
- **Expected**: VALUE · estimate, 95% interval, unit, population, and model label
- **Acceptance**: recomputes from named Results; aggregate only; no row-level data
- **Supporting Runs**: Execution · reuse · b01j02t03r04; Discovery · registered · b02j01t05r01
- **PageX Bindings**: other/page/results/r04/result.yaml · authority b01j02t03r04
- **Local Input**: Supporting Results + PageX bindings
- **Local Run**: Page · Evidence Item · registered · b03j01t02r01
- **Decide**: ☑ make · JL 260901
> Comment JL · local input freezes both Supporting Results before execution · 260901
```

The record head has three parts: item id, target bullet address, and a short
human-readable evidence name. `Target` repeats the address intentionally so
record renderers can show it as a column. The labels are fixed and ordered:

The Board wall projects that identity as
`E<n><kind>.<ShortNameNoSpaces>`, where
`V = VALUE`, `C = CITE`, and `D = DISPLAY`; for example,
`E3V.TotalMME`. This compact label is presentation only:
the immutable `E<NN>-<TYPE>-<slug>` remains the authored id and is exposed in
the item detail. A wall must never show only `E01 · VALUE`, because that hides
what the evidence contains. It must also present `Supporting Runs` and `Local
Run` as separate columns; they are different graph layers, not one folded
`Route` field. A real global Run is shown in readable dotted form, such as
`b01.j02.t03.r04`, links to the Run Index, and carries its short lifecycle
label (for example `Ready` or `Rerun`). A current Task ticket with no validated
Result is `Rerun`, even if a smoke receipt exists; an absent ticket is displayed
as `needs … Run` and never assigned an invented address. An unregistered `new-*` route is only a
pre-registration note and cannot close SURVEY. The Page Outline grid has no
separate item `Status` column: colour is the compact state
signal, and the evidence-item popover names the exact derived state. `CITE`
items share the Evidence column with VALUE and DISPLAY;
several citation items may support one bullet.

| Label | Written by | Contract |
|---|---|---|
| `Target` | SHAPE | exactly one `C<n>.P<m>.B<k>` address |
| `Need` | SHAPE | why the outline needs this item, in one line |
| `Expected` | SHAPE | `<TYPE> · <ready-to-use payload>` |
| `Acceptance` | SHAPE | observable checks for the ready Evidence Result |
| `Supporting Runs` | SURVEY | `[]` or a semicolon-separated list of `Family · reuse/rerun/registered · full global Run id` |
| `PageX Bindings` | SURVEY; LAND validates | `[]` or exact cross-Folder file/Result paths, each with its source authority; never a whole Folder |
| `Local Input` | SURVEY; LAND freezes | one envelope plan: Supporting Results plus PageX bindings and/or named pre-existing local paths; LAND appends `→ <packet>#<sha256>` |
| `Local Run` | SURVEY; LAND binds | exactly one `Page · Evidence Item · reuse/rerun/registered · full global Run id [→ Result]` |
| `Decide` | human gate | `☐ make` or signed `☑ make/defer/drop` |

Comments hold rationale; they never replace an expected payload, acceptance
test, or Run address. A typed `Status` label is a defect because status is
derived from receipts and Results.

## The Run graph · zero-to-many supports, exactly one local Run

```text
Supporting Runs  0..N  Execution | Discovery
PageX Bindings   0..N  exact accepted cross-Folder files/Results; not Runs
                         ↓ validated upstream authorities
Local Input       1     one frozen envelope containing those Results/bindings
                         ↓
Local Run         1     Page · Evidence Item
                         ↓
Ready Result      1     VALUE | CITE | DISPLAY, accepted by this item's contract
```

This is the precise meaning of “one input and one execution”: one Evidence
Item has one frozen input envelope and exactly one local execution. The input
envelope may contain zero, one, or many Supporting Results, zero or more
validated PageX bindings, plus pre-existing governed local artifacts named in
`Local Input`. Calls, retries,
scripts, render passes, and model turns inside that local execution remain
implementation details unless they independently satisfy the base Run tests.

The local Result is factual and reusable; it does not interpret the evidence
for the Page. EMBED owns that interpretation and writes it into the next
outline version.

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
| `registered` | a new Run Ticket and planned runtime receipt are scaffolded; LAND will execute it | full global Run id required |
| `new-run` | pre-registration note only; SURVEY must allocate/scaffold before closing | parent `bNNjNNtNN` |
| `new-task` | pre-registration note only; SURVEY must scaffold before closing | parent `bNNjNN` |
| `new-job` | pre-registration note only; SURVEY must scaffold before closing | parent `bNN` |
| `new-block` | pre-registration note only; SURVEY must scaffold before closing | planned block name |

`reuse` and `rerun` always name a full global id such as `b01j02t03r04`.
`rerun` preserves the same target, frozen inputs, and acceptance contract. If
any of those change materially, register a new Run and record
`supersedes: b01j02t03r04` in the new Run receipt.

There is no `person`, `found`, or `none` action. A citation can use a Discovery
Supporting Run; existing work is `reuse`; and an impossible item routes back
to SHAPE. No supports is represented structurally as `Supporting Runs: []`.
That form is valid only when `Local Input` names sufficient pre-existing local
material or says `item contract only` for a genuinely source-free construction.

A sibling Evidence Item's future local Result is never an implicit local input.
If two items need the same upstream evidence, both list the same Execution or
Discovery Supporting Run (normally `reuse`). This keeps item graphs independently
closable and preserves LAND's item-level parallelism.

## PageX bindings are sources, never Results

PageX is the optional cross-Folder source-binding mechanism of the unified
`haipipe-plugin-evidence`. It is not an Evidence Item type, Run family, action,
or fourth Result kind. The authored value is either `[]` or a semicolon-separated
list:

```text
<repo-relative exact file-or-Result path> · authority <Run id, accepted artifact id, or accepted Page version>
```

Each path must identify the exact accepted material used by this item and must
not end `/`. A whole-Folder PageX relationship is valid navigation, but not an
evidence binding. When bindings are present, `Local Input` must explicitly say
that it freezes `PageX bindings`; LAND then resolves the path, verifies the
named authority and freshness, and records the frozen pointer/hash.

The PageX segment is derived from this item graph. It shows the selected source
beside the item's Supporting Runs, Local Run, and ready Result; it does not keep
a disconnected evidence list or count the link as another Run.

## What SHAPE, SURVEY, LAND, and EMBED write

| Cycle | Level-4 Runs? | Writes to this table |
|---|---:|---|
| SHAPE | none | item id/name/type, Target, Need, Expected, Acceptance |
| SURVEY | allocate + scaffold only | registered Supporting Runs, PageX bindings, one Local Input, exactly one registered Local Run, Decide gate |
| LAND | execute only | validated/frozen PageX bindings and `→ <Result>` on completed bindings |
| EMBED | none | nothing; it writes `Answered:` or `Drawn:` into outline v<N+1> |

SURVEY is complete when every approved item has registered Supporting Runs and
Local Run Tickets with planned runtime receipts, valid PageX bindings, one
explicit Local Input plan, and a signed decision. `Ready` on a Run means its
Ticket is ready to execute; evidence-item `ready` still requires a validated
local Result. LAND refuses an undecided or unregistered item. Item graphs may execute in parallel,
but within one item its local Run waits until every declared Supporting Result
and PageX binding is valid and frozen into the input envelope. LAND closes only
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
| `folded` | the next outline version binds the ready Result | SHAPE / DRAFT |
| `accepted` | the Page passed CHECK | closed |
| `stale` | a bound Result changed after the fold | LAND or EMBED |
| `deferred` | signed defer | human route |
| `dropped` | signed drop | SHAPE if the outline still asks for it |
| `blocked` | a commissioned Run truthfully cannot complete | LAND / SHAPE |

The overview stays compact: item id, type, target, support count, PageX binding
count, local Run, state, Result. Clicking the item or Run reveals the frozen
input, individual Supporting Runs, PageX authorities, receipts, acceptance
checks, and artifacts.
