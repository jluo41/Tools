# SURVEY · map the Run graph for each ready-evidence contract

> The second cycle of the Structure Run (`structure.md`); it runs after SHAPE is agreed.

SURVEY runs after SHAPE has named every item and passed its mechanical checks.
For `v0.*`, that checked state may advance in copilot or auto while approval
remains open; Content stays closed. For `G>=1`, the outline must have direct or
inherited human approval in either mode.
It inventories the current `task/` and `discovery/` libraries, classifies
each selected route as existing Result, Ticket only, rerun, or new design, and
writes the evidence-to-Run lineage. It does not scaffold a Ticket, execute a
worker, materialize a Result, or write prose. A new local route normally names
its real owner/parent and receives `rNN` only when LAND allocates the Ticket.
A full address may be reserved only when the Folder owner's current naming
contract permits it. Record that authority and keep the route labelled
`new-run`; a reservation is not a Run Ticket.

- **Preserve SHAPE's contract.** Item id, type, name, Target, Label, Need,
  Expected, and Acceptance are frozen inputs to SURVEY. If they are insufficient or
  impossible, route the item back to SHAPE; do not repair the meaning here.
- **Map Supporting Runs, zero to many.** Each existing Run is
  `Execution | Discovery · reuse | rerun | registered · bNNjNNtNNrNN`
  for Task-backed work. An accepted Insight instance/item execution may also
  supply a `reuse` route under `ref/item-table.md`; preserve its qualified
  instance/version identity and validate its owner's Result gate.
  Read the actual Ticket, receipt, and Result before choosing: an accepted
  Result is `reuse`; a real Ticket with no completed attempt is `registered`
  and has the derived availability state `Ticket only`; a failed, smoke-only,
  invalid, or explicitly stale attempt is `rerun`. When the task exists but no
  Ticket exists, write `new-run · bNNjNNtNN`; when the task is absent, write
  `new-task · bNNjNN`; when the job is absent, write `new-job · bNN`; use
  `new-block` only for a bounded block not yet placed in that hierarchy. Do not
  mint an `rNN` during inventory. Write `[]` when no upstream support is needed.
- **Use one global Run identity in two typographies.** Supporting records store the canonical
  compact id `bNNjNNtNNrNN`; the reader-facing table may display the same id as
  `bNN.jNN.tNN.rNN`. The dotted form is a hyperlink label, not a different
  identity. A planned parent `bNNjNNtNN` has no `rNN` until the owning workflow
  allocates a real Run.
- **Plan exactly one Local Input.** State whether its one future frozen
  envelope contains Supporting Results, named governed page-local static
  paths, or `item contract only`. Cross-Folder evidence must enter through a
  Supporting Run Result; Related Page links from Folder inspection are
  navigation/constraints only. A sibling item's future local Result is
  not a local source; both items must name the shared upstream
  Execution/Discovery Run instead.
- **Map exactly one Local Run declaration in the owner's namespace.** An
  existing route uses `registered`, `reuse`, or `rerun` plus its full Run id.
  A Task-local route with no Ticket is
  `Page · Evidence Item · new-run · bNNjNNtNN`; LAND allocates the next `rNN`
  and writes back `bNNjNNtNNrNN`. Another Folder-local owner names its stable
  Folder address and follows its Run Profile. If that owner permits a full
  reservation before allocation, preserve its exact address and cite the
  owner's current naming contract; Page does not prescribe that namespace.
  In every dialect, `new-run` means proposed, not allocated.
  Do not use a free-text dash placeholder as an action. Its future frozen input envelope may
  include every Supporting Result plus local source material. Its future Result
  must satisfy the item's typed Acceptance contract. Page interpretation is not
  part of this Run.
- **Keep family and action separate.** Discovery is a Supporting Run family,
  not an action. Existing accepted work is `reuse`; an existing Ticket that
  must be executed again is `rerun`; a real never-attempted Ticket is
  `registered`. Changed target/input/acceptance needs a new designed route.
  Supporting `new-run`, `new-task`, `new-job`, and `new-block` routes remain
  inventory findings and do not invent an external `rNN`. An owner-permitted
  reservation remains a plan; LAND is the first Run Spec allowed to create its Ticket.
  There is no `found`, `person`, or `none` action.
- **Citations use the same graph.** A `CITE` item may reuse or commission a
  Discovery Run, then its local Page Evidence Item Run produces the focal,
  verified citation claim and the accepted source set that entails it. It is
  not routed to a special `person` outcome, and its identity is not multiplied
  merely because CONTENT later places the same source more than once.
- **A SURVEY row is complete** when every declared Supporting and Local route
  is honestly classified (existing Result, Ticket only, rerun, or new design),
  one Local Input is explicit, the current `runs/` and `results/` references
  are resolved, and Decide is signed (`☑ make`, `☑ defer`,
  or `☑ drop`). A planned route is a plan, not `Ready` evidence. LAND refuses
  `☐`, an ambiguous route, or a fake/guessed Run identity.

The Outline workbench's Evidence Space joins the authored Item contract with
current Result manifests into one card per Evidence Item. Its identity is the same
compact `E<n><kind>.<Label>` used by the Outline Table; Supporting and Local
Runs are grouped Run items inside that card. The internal `Evidences` lens
explains each Evidence contract; the internal `Runs` lens groups by Evidence
and renders every mapped Supporting or local route as its own Run card.
It reports both mapping and unique-Run counts because shared Runs may appear in
several Evidence groups. This is SURVEY's source inventory, not proof that a
planned route has been allocated. Reader-facing paths are `Run` and
`Result`, with exact paths collapsed behind `Run & Result paths`. SURVEY does
not make the overview carry logs, commands, or output trees.

Each Run item must also answer “what is this for?” Existing Runs take their
Purpose from the real Ticket plus the owning Evidence Item. A proposed route
shows a Plan synthesized from Expected, Acceptance, and Local Input, which
remain authored in `<stem>-evidence-items.md`; SURVEY creates no second plan
file. Present `Availability` separately from `Next action`: existence is
`Planned | Run exists · Result missing | Run + Result | Paths unresolved`,
while action is `Allocate and run | Run | Rerun | Reuse Result | Resolve path`.
Do not present `new`, `rerun`, `run only`, and `ready` as one status scale.

### 🧑 The Decide ends the cycle

A person reads the table on the 🧭 tab (the Evidence Space lens, which renders
the table joined to the disk with a derived Status chip per row) and writes
one Decide per row. A machine may transcribe a chat decision with the quote;
it never ticks `☑` on its own. `cli/evidence-status.py` prints the classified
lineage and `cycle: SURVEY · decided n/n` until every row is signed and mapped,
then `cycle: LAND`.
