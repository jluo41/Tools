# Workflow × Workspace schema

## Normalized declaration

```yaml
workflow_table:
  id: <workflow-family-id>
  title: <human-readable title>
  owner: <domain Workflow>

  workspace_roster:
    id: <stable-roster-id>
    declared_by: <one Plugin/work object>
    workspaces:
      - id: <stable-workspace-id>
        label: <reader-facing label>
        purpose: <presentation/interaction purpose>

  run_specs:
    - id: <stable-run-spec-id>
      run_type: <Run Catalogue key>
      purpose: <why one instance independently closes>
      target: <bounded goal/target grammar>
      actor:
        mode: <human | automatic | agent | hybrid>
        owner: <literal owner>
      action: <action or interaction>
      input: []
      depends_on: []
      entry_gate:
        mode: <human | automatic | agent | hybrid>
        assertion: <testable condition>
        record: <record/path or none>
      exit_gate:
        mode: <human | automatic | agent | hybrid>
        assertion: <testable close condition>
        record: <record/path>
      routes:
        <outcome>: <run-spec-id | SELF | NEW_VERSION | NEW_RUN | CLOSE | HOLD>
      result:
        payload: <schema/pointer or none>
        receipt: <required durable receipt schema/path>
      cardinality: <1 | 0..N | symbolic formula>
      cells:
        - id: <run-spec-id>@<workspace-id>
          workspace_id: <one workspace_roster.workspaces id>
          mode: <own | action | review | decision | read-only | empty>
          owner_skill: <literal skill/contract or none>
          worker_skill_chain: [<ordered literal skills>]
          interaction: <what can be seen/done here or none>
          input_view: [<shown inputs or none>]
          output_view: [<shown outputs or none>]
          authority_change:
            kind: <create | revise | bind | promote | release | none>
            target: <authority or none>
            record: <path/field/receipt or none>
          gate_binding:
            role: <collect | evaluate | present | none>
            gate: <entry_gate | exit_gate | none>
          source_projection:
            kind: <source | projection | none>
            source_cell: <Cell coordinate or none>
            object: <Run/Result/authority or none>
            rule: <authority/projection rule>

  entry: [<run-spec-id>]
  terminal: [CLOSE, HOLD]

  run_catalog:
    mode: <declared | template-only | none>
    ref: <catalogue path or none>
    keys: [<used Run Type keys>]

  skill_coverage:
    - skill: <literal skill name>
      path: <literal SKILL.md path>
      role: <door | machine | contract | library | craft>
      used_by_cells: [<Cell coordinates>]
      provenance: {kind: <observed | user-declared | derived | unresolved>, source: <source>}
      status: <source-backed status>
      version: <version or "?">
      skill_md_lines: <integer or "?">
      quality: {class: <class or "?">, score_or_finding: <finding or "?">, source: <source or "?">}
      field_test: {status: <result or "?">, source: <receipt/path or "?">}
      gap: <smallest repair or none>
```

`input`, `depends_on`, and `entry_gate` may be empty. `exit_gate` may be
omitted only when the referenced Run Type supplies the same explicit close
semantics. `result.payload` may be `none`; `result.receipt` is required.

## Explicit empty Cell

Every Run Spec has one Cell for each member Workspace:

```yaml
id: <run-spec-id>@<workspace-id>
workspace_id: <workspace-id>
mode: empty
owner_skill: none
worker_skill_chain: []
interaction: none
input_view: []
output_view: []
authority_change: {kind: none, target: none, record: none}
gate_binding: {role: none, gate: none}
source_projection: {kind: none, source_cell: none, object: none, rule: none}
```

Compact renderings may hide validated empty Cells; source declarations may not
omit them.

## Ownership laws

### Workspace roster

The roster contains member Workspaces, not columns disguised as one Workspace.
Labels are presentation; ids are identity. Workspaces do not authorize Runs.

### Run Spec row

One row is one independently closable planned Run. It owns target, actor,
action/interaction, Gate, Route, Result/receipt contract, and planned
cardinality. A loop is a Route, not a duplicate row. A Step, Version, file,
tool call, human tick, or display card is not a row.

### Cell

A Cell binds one row to one member Workspace. It may present or collect the
row's Gate but cannot define a second Gate/Route. A source Cell owns the
Workspace-facing authority; a projection Cell points back to it and preserves
the same logical Run/Result identity.

### Runtime

Planned `cardinality` does not prove any Run exists. Runtime status and count
come only from allocated Run Instance ids and valid receipts. The Runtime
Workspace (`id: runtime`, label commonly `Run`) is read-only.

## Cell modes

| Mode | Contract |
|---|---|
| `own` | present/edit the authoritative Run Spec or owned work object |
| `action` | perform the row's declared action through bound skill(s) |
| `review` | inspect evidence and evaluate the row's declared Gate |
| `decision` | collect the human input/decision required by the row |
| `read-only` | project the same Run/Result; no mutation, mint, rename, copy, or recount |
| `empty` | explicit no binding |

## Worked Design declaration

```yaml
workflow_table:
  id: design-workflow
  owner: haipipe-design-workflow
  workspace_roster:
    id: design-workspaces
    declared_by: haipipe-design
    workspaces:
      - {id: goal, label: Goal, purpose: brief and objective context}
      - {id: design, label: Design, purpose: author Commissions; inspect candidates and verification evidence}
      - {id: insight, label: Insight, purpose: source and present the Insights referenced by a Commission}
      - {id: runtime, label: Run, purpose: read-only runtime presentation}
      - {id: delivery, label: Delivery, purpose: present exact Verify-passed candidate Results}
  entry: [commission]
  terminal: [CLOSE, HOLD]
  run_specs:
    - id: commission
      run_type: Design.commission
      purpose: release one exact Design Commission
      target: one Commission/config version
      actor: {mode: human, owner: design-owner}
      action: release-decision
      input: []
      depends_on: []
      entry_gate: {mode: automatic, assertion: open, record: none}
      exit_gate: {mode: human, assertion: exact Commission is released or held, record: results/<run>/decision.yaml}
      routes: {release: generate, hold: HOLD}
      result: {payload: released Commission fingerprint, receipt: results/<run>/runtime.yaml}
      cardinality: C
      cells:
        - {id: commission@goal, workspace_id: goal, mode: read-only, owner_skill: haipipe-design-workflow, worker_skill_chain: [], interaction: view the Brief and Insight board, input_view: [Brief, Insight board], output_view: [], authority_change: {kind: none, target: none, record: none}, gate_binding: {role: none, gate: none}, source_projection: {kind: source, source_cell: none, object: Brief and linked Insight board, rule: input context only}}
        - {id: commission@design, workspace_id: design, mode: decision, owner_skill: haipipe-design-workflow, worker_skill_chain: [], interaction: release or hold the exact Commission, input_view: [Brief, Commission scope, pinned Insight hashes], output_view: [decision receipt], authority_change: {kind: release, target: Commission, record: decision receipt}, gate_binding: {role: collect, gate: exit_gate}, source_projection: {kind: source, source_cell: none, object: Commission decision, rule: human authority}}
        - {id: commission@insight, workspace_id: insight, mode: read-only, owner_skill: haipipe-insight, worker_skill_chain: [], interaction: present Insights pinned by the Commission hash, input_view: [], output_view: [pinned Insight hashes and references], authority_change: {kind: none, target: none, record: none}, gate_binding: {role: none, gate: none}, source_projection: {kind: projection, source_cell: commission@design, object: same pinned Insights, rule: preserve source identities}}
        - {id: commission@runtime, workspace_id: runtime, mode: read-only, owner_skill: haipipe-run, worker_skill_chain: [], interaction: present the same decision Run, input_view: [], output_view: [same receipt], authority_change: {kind: none, target: none, record: none}, gate_binding: {role: present, gate: exit_gate}, source_projection: {kind: projection, source_cell: commission@design, object: same Run, rule: no mint or recount}}
        - {id: commission@delivery, workspace_id: delivery, mode: empty, owner_skill: none, worker_skill_chain: [], interaction: none, input_view: [], output_view: [], authority_change: {kind: none, target: none, record: none}, gate_binding: {role: none, gate: none}, source_projection: {kind: none, source_cell: none, object: none, rule: none}}

    - id: generate
      run_type: Design.generate
      purpose: generate one independently closable candidate target
      target: released unit/set/sequence
      actor: {mode: agent, owner: haipipe-design-unit}
      action: generate
      input: [released Commission]
      depends_on: [commission]
      exit_gate: {mode: automatic, assertion: Result integrity and self-check pass, record: results/<run>/checks.yaml}
      routes: {pass: verify, fail: generate}
      result: {payload: immutable candidate Result, receipt: results/<run>/runtime.yaml}
      cardinality: N
      cells: <one explicit Cell for each member Workspace>

    - id: verify
      run_type: Design.verify
      purpose: independently verify named candidate Results
      target: named generation Result set
      actor: {mode: agent, owner: fresh haipipe-design-unit context}
      action: verify
      input: [immutable generation Results]
      depends_on: [generate]
      exit_gate: {mode: agent, assertion: independent coverage settles pass/fail, record: results/<run>/checks.yaml}
      routes: {pass: CLOSE, fail: generate, invalid: verify}
      result: {payload: immutable verification Result, receipt: results/<run>/runtime.yaml}
      cardinality: J
      cells: <one explicit Cell for each member Workspace>

```

The abbreviated `cells:` values for Generate and Verify must be fully
materialized in a live declaration. The matrix view is:

| Run Spec | Goal | Design | Insight | Run | Delivery |
|---|---|---|---|---|---|
| Commission | read-only | decision | read-only | read-only | empty |
| Generate | empty | read-only | empty | read-only | read-only |
| Verify | empty | read-only | empty | read-only | empty |

Expected actual Design Runs: `C + N + J`. C counts Commission decisions,
including holds; at most one may release the Item. Count allocated Runs with
receipts, including held, failed, blocked, and superseded Runs. The special
case `1 + N + J` applies when no hold preceded the release.

`pass`, `fail`, and `invalid` name the corresponding verdict/records-check
outcomes in the Design owner contract. A route back to Generate or Verify
names the next Spec; the person must queue its new instance. Only Commission
has a human HOLD decision. Verify pass closes the work and makes the exact
candidate ready in Delivery. Delivery is a projection, never a Run. The
Generate delivery Cell is visible only once independent Verify has passed.

## Runtime projections

### Runs Overview

```text
Run · Run Spec · Run Type · Target · Actor · Status · Gate outcome ·
Route taken · Result · Receipt · Projected-in Cells
```

### Human Queue

```text
Run · Run Spec · Human role · Question · State · Decision receipt
```

Rows are derived from actual Runs. A human decision Run appears in both views
without becoming two Runs. A pending Gate points to its owning Run.

### Skill Coverage

One row per literal skill, keyed to `used_by_cells`. A skill can serve many
Cells without becoming a Workflow axis.

## Audit checklist

```text
[ ] one Plugin/work object declares plural member Workspaces
[ ] one Run Spec row per independently closable Workflow node
[ ] every row has type, target, actor, action, close rule, receipt, cardinality
[ ] every route resolves; entry and terminal sets exist
[ ] every row has one Cell per member Workspace
[ ] every Cell id equals <run-spec-id>@<workspace-id>
[ ] Cells reference but never redefine row Gate/Route
[ ] Runtime projections preserve one source Run identity
[ ] human decision Runs pass the bounded independent-close test
[ ] feedback/clicks/Steps/Versions are not extra Runs
[ ] planned cardinality is separate from actual receipt-backed count
[ ] Skill Coverage resolves every literal owner/worker binding
[ ] all four projections agree with the declaration
```

Missing evidence yields `HOLD` with the exact field and source; never a guess.
