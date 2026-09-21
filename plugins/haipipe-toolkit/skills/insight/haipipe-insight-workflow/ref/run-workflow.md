# Insight Run Specs and Runtime

Load this contract when planning, dispatching, resuming, or reporting InsightBoard
work. The shared contracts are
[`haipipe-run`](../../../run/haipipe-run/SKILL.md) and
[`Workflow Runtime`](../../../task/haipipe-workflow/ref/workflow-runtime.md).
Task-side `riNN` work keeps its own item contract.

## Definition and materialization

A Workflow Definition is a list of bounded Run Specs with dependencies,
Spec-owned routes, and completion rules. A Workflow Runtime records the actual
Runs selected for one execution. Meta, Question, Data, Information, Knowledge,
and Wisdom are resource kinds. DIKW defines evidence/interpretation dependencies;
it does not prescribe six Runs or six execution positions.

Bind one Spec to each independently closable target. These templates reuse
existing owners and identity grammars:

| Spec template | Owner / native identity | Bounded target and inputs | Result / exit | Cardinality and routes |
|---|---|---|---|---|
| `support.<target>` | selected Task or Discovery owner; full `rNN`, paper-run, or other declared address | one missing computation/source Result, exact data/config and release | accepted native Result + native receipt | 0..N; ready Result → dependent evidence Spec, truthful failure → HOLD or declared retry |
| `evidence.<page>.<item>` | `haipipe-page-evidence`; Page RE lineage plus its native Ticket address | one decided VALUE/CITE/DISPLAY item and frozen Local Input | typed accepted Result + native receipt, required verification satisfied | one per commissioned make-item; ready → dependent writing/delivery, failure → HOLD or declared retry |
| `structure.<page>` | shared Page writing owner; `rp-struct-NN` | explicitly commissioned whole-Page map, Shape and Survey target | accepted structure Result + receipt | only when commissioned; close → selected writing targets/evidence obligations |
| `write.<page>.<scope>` | shared Page writing owner; `rp-sec-NN` or `rp-para-NN_<target>` | one selected section/paragraph goal, exact parent rows and ready evidence | accepted writing Result + receipt | 0..N selected scopes; owner-defined SELF/NEW_VERSION/CLOSE/NEW_RUN routes |
| `deliver.<page>.<target>` | shared Page delivery owner; RD lineage/native Ticket | one released Page delivery target | current artifact, hashes and build receipt | 0..N declared targets; close → Page CHECK control, failure → repair or HOLD |

The exact Run Type, actor, worker and storage dialect come from the selected
owner, never from a Folder-kind label. A derivation or robustness computation
uses `support.<target>` with an executable owner. It is not a second domain
Run wrapped around that same computation. A single producer may serve multiple
cells; its full native identity appears once and carries multiple consumers.
RE/RD lineage and its underlying native Ticket identify the same work, so use
one inventory row with aliases, never two Runs.

An existing accepted Result is a dependency reference. Index it with
`participation: reused` and its exact version/hash; do not allocate or execute
it again. An open matching Run resumes through its owner and is indexed with
`participation: managed`. Proposed work has a Spec and target, but no invented
Run id before the owner creates its Ticket and receipt.

Registration, partition registration, Page controller passes, Page CHECK,
GI evaluation, signature recording, and Queue settlement are control/resource
actions. They do not get Run ids. Page writing on Meta or a Question register
may have real RP/RD Runs when explicitly commissioned; routine register edits
do not. A control-only execution can truthfully contain `runs: []`.

## Dependency rules

The concrete graph may include these edges, only where work is actually owed:

```text
selected structure Run ── accepted plan ──▶ selected evidence/writing Specs
Supporting Run ── accepted Result ──▶ local Evidence Run
local Evidence Run ── ready typed Result ──▶ dependent writing/delivery Runs
accepted writing Runs ── Page release ──▶ delivery Run
delivery Result ── Page CHECK + GI predicates ──▶ downstream evidence/work
```

Page CHECK and GI annotations on an edge are predicates/control records, not
Run nodes. Scope inventory and question registration constrain Spec entry.
Semantic D→I→K→W dependencies pin exact parent rows; only the required
downstream work is instantiated. Existing current accepted parents satisfy an
edge without another Run. The X contrast consumes mirrored I rows; the pooling
verdict consumes K claims. Every partition-major W target depends on the current
verdict for the exact partition set. A verified Task Wisdom RF bridge supplies
an external parent to local W work under the five bridge assertions.

Freeze the selected Specs, entry predicates, routes, requested answer/control targets and
completion rules before dispatch. If a new need changes the graph, preserve
the frozen definition, append a new definition revision with its reason, and
bind new work to that revision. Do not change existing Tickets or historical
Results to fit the new graph. Independent ready Runs may execute concurrently
only when their owners permit it; shared register writes are serialized.

## Runtime storage and identity

A frozen definition resolves each selected template into a concrete bounded
node. For example, resuming one existing Information paragraph goal can use
this shape; all placeholders must resolve from actual owner records:

```yaml
schema: haipipe.insight-definition/v1
workflow_id: haipipe-insight-workflow
revision: v001
requested_answer_targets: [{question: QI3, partition: B}]
requested_controls: []
run_specs:
  - id: write.BI01.P01
    owner: haipipe-page-workflow
    run_type: page.interactive-writing.paragraph
    target: {page: <exact-Page-path>, paragraph: P01, goal: <frozen-existing-goal>}
    actor: hybrid
    action: resume-selected-writing
    inputs: [{path: <exact-local-Evidence-Result>, hash: <sha256>}]
    depends_on: [<full-reused-Evidence-Run-address>]
    entry: {mode: automatic, predicate: exact-required-evidence-current}
    exit: {mode: hybrid, predicate: native-writing-acceptance-and-dependencies}
    routes:
      - {when: feedback-within-goal, to: SELF}
      - {when: reopen-same-goal, to: NEW_VERSION}
      - {when: missing-input-or-decision, to: HOLD}
      - {when: accepted, to: CLOSE}
    cardinality: one-compatible-open-Run
completion:
  required_runs: accepted-writing-targets-or-licensed-non-answers
  required_controls: current-Page-CHECK-CLOSE-and-applicable-GI-settlement
  unresolved_decisions: none
  frontier: empty
```

`SELF`, `NEW_VERSION`, `HOLD` and `CLOSE` follow the native owner's rules.
`NEW_RUN` for a changed target requires a new bounded Spec or definition
revision, plus the owner's commission; it never mutates this frozen goal.
Result/receipt locations and any existing instance id are resolved from the
owner and indexed in the runtime below. Register-only definitions instead
declare an accepted registration control and have no answering Specs.

Use `<InsightBoard>/_runs/insight/<workflow_runtime_id>/runtime.yaml` for the
aggregate envelope and `definition-vNNN.yaml` beside it for each frozen
definition revision. The runtime id must be unique within the board and must
not look like a native Run id. These are controller records, not a new Folder
kind, flat Run bank, or Result store. Tickets, Results and receipts remain in
their owners' declared stores.

Use the shared envelope with these Insight bindings. Angle-bracket values
below are placeholders to resolve before dispatch, not allocated identities:

```yaml
schema: haipipe.workflow-runtime/v1
workflow_id: haipipe-insight-workflow
workflow_version: "1.3.2"
workflow_runtime_id: <board-unique-execution-id>
status: running
definition_ref: definition-v001.yaml
definition_hash: <sha256>
requested_answer_targets:
  - {question: QI3, partition: B, page: <board-relative-Page-path>}
requested_controls: []
runs:
  - run_id: <full-reused-Evidence-Run-address>
    owner: haipipe-page-evidence
    run_type: <native-Evidence-type>
    participation: reused
    target: <accepted-Evidence-item>
    status: complete
    result: <exact-local-Evidence-Result>
    result_hash: <sha256>
    receipt: <exact-native-Evidence-receipt>
  - run_id: <full-existing-Writing-Run-address>
    run_spec_id: write.BI01.P01
    run_type: page.interactive-writing.paragraph
    owner: haipipe-page-workflow
    participation: managed
    target: {page: <exact-Page-path>, paragraph: P01, goal: <frozen-existing-goal>}
    consumers: [{question: QI3, partition: B}]
    inputs: [{path: <exact-local-Evidence-Result>, hash: <sha256>}]
    depends_on: [<full-reused-Evidence-Run-address>]
    status: running
    ticket: <existing-native-Writing-Ticket>
    result: <native-Writing-Result-path>
    receipt: <native-Writing-runtime-receipt>

control:
  gates: []
  routes: []
resource_controls: []
frontier:
  - run_spec_id: write.BI01.P01
    target: {page: <exact-Page-path>, paragraph: P01, goal: <frozen-existing-goal>}
    state: ready
    waiting_on: []
output:
  path: <requested-answer-or-signed-handoff-path>
  acceptance: pending
```

Every managed `run_spec_id` and frontier Spec must resolve in the frozen
definition. In this example `write.BI01.P01` is the only managed Spec. The
accepted Evidence row is an external dependency with `participation: reused`;
it has no new Spec, Ticket allocation, or frontier entry in this execution.
Its id and Result/hash resolve the Writing Spec's exact dependency and input.

Native receipts own Run state; the runtime projects them and stores their
addresses. Run-owned gate/route entries use the shared `control` shape and
point back to the native receipt. Do not assign a Run id to a Page/GI/control
action just to fit that shape. Index such actions separately in
`resource_controls`, pointing to their authoritative Page or Folder log:

```yaml
key: GI6
target: {question: QW2, partition: F}
status: passed
authority: haipipe-insight-question
evidence: [<exact-Page-version-and-hash>, <person-signature-source>]
receipt: <register>/outline/<register-stem>-log.md#<record-id>
```

Each dated control receipt records `workflow_runtime_id`, target, assertion,
outcome, actor, exact supporting paths/versions/hashes, and resulting action.
If it consumed a Run, include that native id and receipt. A GI receipt does
not replace the Run receipt; the runtime is only an index of both. For 🟡 final,
preserve the two reciprocal register/answering-Page receipts and quote the
licensing sentence.

## Dispatch and closure

Record answering scope in `requested_answer_targets` and control-only scope in
`requested_controls`. For a registration-only request, the first is empty,
`runs: []`, and completion requires the requested neutral row, its eligible
open cells and registration receipt. It does not require answering that question
or GI6 settlement. Status/inspection and other resource-only requests likewise
close under their declared control outcome. Never expand a registration request
into an answering workflow.

1. Resolve the board, current inventory, question records, exact accepted
   parents, and existing native Runs. Determine the requested target set.
2. Reuse accepted Results; resume compatible open Runs. Declare only missing
   work as bounded Specs. Pin the frozen definition revision.
3. Select a ready Spec/Run from dependencies, not from a Folder number or
   Question Group position. Resolve its owner, Ticket, release and input pins.
   A missing input or person decision sets the affected target to waiting.
4. Dispatch the owner through the Ticket. A Page controller pass coordinates
   its own RP/RE/RD children; index their actual identities without wrapping
   the pass in another Run. Keep `mode: copilot` for Insight Page work.
5. Read the actual Result and receipt; apply the owner's exit predicates.
   Process exit alone never means success. Project Run state and routes into
   the runtime and evaluate dependent Page/GI controls at their named owners.
6. Settle a Queue cell only after its answering Page CHECK/CLOSE and applicable
   GI conditions pass. For an exported W handoff, verify the person's signature
   before GI6. A permitted POOL deferral exports no handoff and requires no new
   signature. Under `UNDETERMINED`, a licensed `🟡 <page> final` W non-answer
   has no GI5 pass, signature, or Design binding; Question may record its
   partial exit at GI6 with both required receipts. If the frozen Workflow can
   still obtain the missing evidence, keep the target waiting instead.
7. Continue other independent ready work within the request. If all remaining
   required work is blocked, write `held`, state exact blockers, and return.
   Close as `complete` only when requested answer cells are terminal, requested
   controls meet their own acceptance rules, required managed
   work is terminal with accepted outputs or licensed non-answers, no required
   decision is unresolved, final acceptance passes, and frontier is empty.

Status reports name `workflow_runtime_id`, definition revision, and one row per
actual native Run: Spec, owner, target, participation, status, exact Result,
receipt, dependency and next action. Show unallocated Specs and control-only
work separately with no Run id. Question Group/CELL summaries derive from the
same records and never substitute for the Run inventory.

## Reopening

Changed source/version/target marks dependent bindings stale and holds only
affected downstream work. Preserve completed Results and receipts; commission
replacement work through the owner's new-Run/new-version rules. Fixed-goal
interactive writing retains its native Version/Step semantics. For a late
partition, reopen X and all verdict-conditioned W bindings, preserve unrelated
D/I/K Results, and require a new person signature when any signed handoff payload changes,
including source/verdict versions or hashes even when counsel wording is unchanged.
A signature is reusable only for the exact unchanged signed payload whose
dependencies remain current; old signatures remain historical. A Run
retry under the same frozen contract follows the owner and is not counted twice.

## Registration writer

The Board Ask command writes a Question row, a canonical Outline log receipt,
and a control-only Runtime with `runs: []` and no answer targets. An empty
regular grid is valid; its first row is QD1/QI1/QK1/QW1 as appropriate.
Use `--workflow-runtime-id <id>` to index an exact already-declared registration
inside an open Runtime, and `--actor <actor>` for attribution. This does not
close the enclosing answering Runtime or claim GI1 answerability. Concurrent
register writes are refused by the board registration lock; recover an
interrupted writer from its planned Runtime before removing a stale lock.
Transposed legacy grids require a Question-owner edit and the same receipt
contract. No answer Run is implied by registration.
