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
| `support.<target>` | `haipipe-task`; the answering page's ticket `run_bNNjNNtNNrNN_<partition>_<task>` (or a Discovery paper-run) | one page ticket in `<page>/runs/`: it sets `RESULT_DIR` to `<page>/results/<ticket>/` and `RUN_TICKET` to itself, then runs the task's own ticket in the DIKW Block, whose config names the board's ONE extract, the cut and `answers:` (a cross-check); the page's `answers.yaml` binds the evidence needs it serves to its files | `<page>/results/<ticket>/` (tables, `metrics.json`, `fig_*.png`) + `runtime.yaml` | 0..N per page; one task run may feed several pages, each through its own ticket and result; ready → `report` Specs, truthful failure → HOLD or declared retry |
| `report.<QID>.<partition>` | the level's folder skill (`haipipe-insight-data` · `-information` · `-knowledge`, which also writes the pooling verdict); `run-report-<MMDD>-<qid>-<cut>` | one answering page: its own current results its `runs:` header names (and, for Knowledge, the Information pages it cites) | the answering page's `.md` written or refreshed, citing each need and passing `haipipe-insight-check` (`haipipe-insight` `ref/report.md`, `ref/evidence-needs.md`) | 0..1 per page; every answering page states what its results show (Data: what was observed, briefly); close → GI2/GI3/GI4 predicate, then SETTLE |
| `evidence.<page>.<item>` | Wisdom pages (and boards made before page tickets) only · `haipipe-page-evidence`; Page RE lineage plus its native Ticket address | one decided VALUE/CITE/DISPLAY item and frozen Local Input | typed accepted Result + native receipt, required verification satisfied | one per commissioned make-item; ready → dependent writing/delivery, failure → HOLD or declared retry |
| `structure.<page>` | shared Page writing owner; `run-structure-<MMDD>-<slug>` | explicitly commissioned whole-Page map, Shape and Survey target | accepted structure Result + receipt | only when commissioned; close → selected writing targets/evidence obligations |
| `write.<page>.<scope>` | shared Page writing owner; `run-section-<MMDD>-<slug>` or `run-paragraph-<MMDD>-<slug>` | one selected section/paragraph goal, exact parent rows and ready evidence | accepted writing Result + receipt | 0..N selected scopes; owner-defined SELF/NEW_VERSION/CLOSE/NEW_RUN routes |
| `deliver.<page>.<target>` | shared Page delivery owner; fixed `run-delivery-<lane>` | one Page delivery lane | the lane's files at least as new as the Page | 0..N declared targets; close → Page CHECK control, failure → repair or HOLD |

The exact Run Type, actor, worker and storage dialect come from the selected
owner, never from a Folder-kind label. A derivation or robustness computation
uses `support.<target>` with an executable owner. It is not a second domain
Run wrapped around that same computation. A single producer may serve multiple
cells; its full native identity appears once and carries multiple consumers.
RE lineage and its underlying native Ticket identify the same work, so use
one inventory row with aliases, never two Runs.

An existing accepted Result is a dependency reference. Index it with
`participation: reused` and its exact version; do not allocate or execute
it again. An open matching Run resumes through its owner and is indexed with
`participation: managed`. Proposed work has a Spec and target, but no invented
Run id before the owner creates its Ticket and receipt.

`structure`, `write` and `deliver` apply to Wisdom pages (and to legacy
answer pages being repaired); a Data, Information or Knowledge answer is its
page's `support` tickets plus a `report` (JL 261001). A page whose evidence
needs are only cite and judge (every Wisdom page) has no `support` Spec; a
Knowledge compute need always has one.

Registration, evidence planning (need lines and their agreement), binding
(`answers.yaml`), the evidence check, partition registration, Page controller
passes, Page CHECK, GI evaluation, signature recording, and Queue settlement
are control/resource actions. They do not get Run ids. Page writing on Meta or a Question register
may have real RP/RD Runs when explicitly commissioned; routine register edits
do not. A control-only execution can truthfully contain `runs: []`.

## Dependency rules

The concrete graph may include these edges, only where work is actually owed:

```text
question needs (agreed) ── answers.yaml binding ──▶ support (page ticket → task run)
support (page ticket → task run) ── current result ──▶ report.<QI>.<cut>
report.<QI>.<cut> ── checked page ──▶ report.<QK>.<cut> (Knowledge cites it)
report.<QK>.<cut> ── checked page ──▶ Wisdom page writing (structure/write)
Wisdom page ── Page CHECK + GI5 signature ──▶ Design Handoff · GI6 SETTLE
```

Page CHECK and GI annotations on an edge are predicates/control records, not
Run nodes. Scope inventory and question registration constrain Spec entry.
Semantic D→I→K→W dependencies pin exact results and pages; only the required
downstream work is instantiated. A current result or checked page satisfies
an edge without another Run. The cross contrast consumes the mirrored Information
results of each partition; the pooling verdict consumes Knowledge pages. Every partition-major W target depends on the current
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
node. For example, answering Information question 3 on partition `alpha`: one page
ticket in `I03-alpha-<slug>/runs/` calling one task run (whose config also lists
other questions) and one report pass writing `I03-alpha-<slug>.md`. All
placeholders must resolve from actual owner records:

```yaml
schema: haipipe.insight-definition/v1
workflow_id: haipipe-insight-workflow
revision: v001
requested_answer_targets: [{question: QI3, partition: alpha}]
requested_controls: []
run_specs:
  - id: support.rates.alpha
    owner: haipipe-task
    run_type: task.run
    target: {ticket: 2-alpha/I03-alpha-<slug>/runs/run_b5Nj21t01r02_alpha_rates.sh,
             calls: tasks/<b5N_topic_dikw>/j21_information_<topic>/t01_rates/runs/r02_<dataset>_alpha.sh,
             answers: [QI1, QI2, QI3]}
    actor: person-presses-run
    inputs: [{path: <the board's ONE extract>, version: <manifest end date>}]
    env: {RESULT_DIR: 2-alpha/I03-alpha-<slug>/results/run_b5Nj21t01r02_alpha_rates/,
          RUN_TICKET: 2-alpha/I03-alpha-<slug>/runs/run_b5Nj21t01r02_alpha_rates.sh}
    exit: {mode: automatic, predicate: runtime-yaml-ok-and-result-gate}
    routes:
      - {when: failed, to: HOLD}
      - {when: ok, to: CLOSE}
  - id: report.QI3.alpha
    owner: haipipe-insight-information
    run_type: insight.report
    target: {page: 2-alpha/I03-alpha-<slug>/I03-alpha-<slug>.md}
    actor: agent
    depends_on: [support.rates.alpha]
    exit: {mode: hybrid, predicate: every-number-traces-to-a-named-current-result}
    routes:
      - {when: missing-input-or-decision, to: HOLD}
      - {when: checked, to: CLOSE}
completion:
  required_runs: page-tickets-ok-and-pages-checked
  required_controls: applicable-GI-settlement
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
workflow_version: "2.1.0"
workflow_runtime_id: <board-unique-execution-id>
status: running
definition_ref: definition-v001.yaml
requested_answer_targets:
  - {question: QI3, partition: alpha}
requested_controls: []
runs:
  - run_id: run_b5Nj21t01r02_alpha_rates
    run_spec_id: support.rates.alpha
    run_type: task.run
    owner: haipipe-task
    participation: reused
    target: {calls: <tasks/b5N_topic_dikw/j21_information_<topic>/t01_rates>/runs/r02_<dataset>_alpha.sh, answers: [QI1, QI2, QI3]}
    consumers: [{question: QI3, partition: alpha}]
    status: complete
    ticket: 2-alpha/I03-alpha-<slug>/runs/run_b5Nj21t01r02_alpha_rates.sh
    result: 2-alpha/I03-alpha-<slug>/results/run_b5Nj21t01r02_alpha_rates/
    receipt: 2-alpha/I03-alpha-<slug>/results/run_b5Nj21t01r02_alpha_rates/runtime.yaml
  - run_id: run-report-<MMDD>-qi3-alpha
    run_spec_id: report.QI3.alpha
    run_type: insight.report
    owner: haipipe-insight-information
    participation: managed
    target: {page: 2-alpha/I03-alpha-<slug>/I03-alpha-<slug>.md}
    consumers: [{question: QI3, partition: alpha}]
    depends_on: [run_b5Nj21t01r02_alpha_rates]
    status: running
    result: 2-alpha/I03-alpha-<slug>/I03-alpha-<slug>.md

control:
  gates: []
  routes: []
resource_controls: []
frontier:
  - run_spec_id: report.QI3.alpha
    target: {page: 2-alpha/I03-alpha-<slug>/I03-alpha-<slug>.md}
    state: running
    waiting_on: []
output:
  path: <requested-answer-or-signed-handoff-path>
  acceptance: pending
```

Every managed `run_spec_id` and frontier Spec must resolve in the frozen
definition. In this example `report.QI3.alpha` is the only managed Spec.
The page ticket already has a current `ok` result, so it is a dependency with
`participation: reused`: no new Ticket allocation or frontier entry. Its id and
result path resolve the report pass's exact dependency and input.

Native receipts own Run state; the runtime projects them and stores their
addresses. Run-owned gate/route entries use the shared `control` shape and
point back to the native receipt. Do not assign a Run id to a Page/GI/control
action just to fit that shape. Index such actions separately in
`resource_controls`, pointing to their authoritative Page or Folder log:

```yaml
key: GI6
target: {question: QW2, partition: full}
status: passed
authority: haipipe-insight-question
evidence: [<exact-Page-path-and-version>, <person-signature-source>]
receipt: <register>/draft/records/<register-stem>-log.md#<record-id>
```

Each dated control receipt records `workflow_runtime_id`, target, assertion,
outcome, actor, exact supporting paths/versions, and resulting action.
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
4. Dispatch the owner through the Ticket. A task run is dispatched through
   the answering page's own ticket (`bash <page>/runs/<ticket>.sh`), which sets
   `RESULT_DIR` to `<page>/results/<ticket>/`; the task config stays unchanged
   and never names a board or a result folder. A Page controller pass coordinates
   its own RP/RE/RD children; index their actual identities without wrapping
   the pass in another Run. Keep `mode: copilot` for Insight Page work.
5. Read the actual Result and receipt; apply the owner's exit predicates.
   Process exit alone never means success. Project Run state and routes into
   the runtime and evaluate dependent Page/GI controls at their named owners.
6. Settle a Queue cell only after its answering page passes its check (for
   Wisdom, its Page CHECK/CLOSE) and
   applicable GI conditions pass. For an exported W handoff, verify the person's signature
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
partition, reopen cross and all verdict-conditioned W bindings, preserve unrelated
D/I/K Results, and require a new person signature when any signed handoff payload changes,
including source/verdict versions even when counsel wording is unchanged.
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
