# Run Catalogue

The catalogue defines reusable Run Types. It does not define Workflow rows,
Workspace rosters, Cells, or actual activity.

```text
Run Type ──referenced by──> Run Spec ──materializes──> Run Instance
Run Instance ──produces──> terminal outcome + Result/receipt
```

## Type grain

One row describes one independently closable kind of work. Do not create a
type for every Step, command, retry, API call, file, Workspace projection, or
human click.

```yaml
run_catalog:
  id: <catalogue-id>
  version: <version>
  owner: <Workspace/Workflow contract>
  run_types:
    - key: <stable key>
      family: <family>
      run_for: <independently closable purpose>
      allowed_actions: [<action or interaction>]
      actor_modes: [human | automatic | agent | hybrid]
      target: <target grammar>
      default_entry_gate: open | <assertion>
      default_exit_gate: <testable close rule>
      result_payload: <shape or none>
      receipt: <required durable shape/path>
      allowed_routes: [<Run Type/spec outcomes, CLOSE, HOLD>]
      owner_contract: <contract>
      not_a_run_when: [<boundary examples>]
```

## Canonical reference types

| Run Type | Actor | Run for | Typical target | Close semantics | Result/receipt |
|---|---|---|---|---|---|
| `acquisition.scrape` | agent/system | one bounded crawl | source + scope | requested scope covered or terminal error recorded | dataset + runtime receipt |
| `transformation.build-data` | agent/system | one reproducible build | named input/output dataset | output and manifest validate | dataset + manifest + receipt |
| `training.fit` | agent/system | one fitting attempt | model/config/data | artifact loads and fit metrics exist | model + metrics + receipt |
| `evaluation.validate` | agent | one bounded evaluation | artifact + evaluation set | verdict and required assertions settle | report + receipt |
| `authoring.write-file` | agent/hybrid | one bounded content change | named file/artifact | requested checks and acceptance settle | candidate/diff + receipt |
| `Page.interactive-writing` | hybrid | one fixed-scope writing goal | Structure, Section, or paragraph group | explicit scoped acceptance and evidence obligations settle | Version/Step journal + receipt |
| `Design.commission` | human | release one exact Design Commission | Commission/config version | release or hold decision is durably recorded | release decision + receipt |
| `Design.generate` | agent | generate one candidate target | released unit/set/sequence | integrity and self-check pass or terminal failure | immutable candidate + receipt |
| `Design.verify` | agent | independently verify candidate Results | named generation Results | fresh coverage settles pass/fail | immutable verdict + receipt |
| `Design.adopt` | human | adopt/decline exact verified candidates | verified hash set | adoption decision is durably recorded | decision + receipt |

The list is template vocabulary. A live Workflow references only resolved keys
and may declare additional types that satisfy the same contract.

## Run Spec use

```yaml
run_specs:
  - id: generate
    run_type: Design.generate
    target: released design unit
    actor: {mode: agent, owner: haipipe-design-unit}
    action: generate
    exit_gate: {mode: automatic, assertion: integrity and self-check pass}
    routes: {pass: verify, fail: HOLD}
    result: {payload: candidate, receipt: results/<run>/runtime.yaml}
    cardinality: N
```

The Workflow row, not a Cell, owns this profile. Cells bind it to Create,
Review, Runtime, or another member Workspace.

## Human decision boundary

A human decision gets a Run Type only when it has:

1. one bounded question/target;
2. explicit commission and actor;
3. independent close rule;
4. durable decision Result/receipt.

Otherwise it remains a Gate or Step inside the owning Run. The Human Queue
projects either case by pointing to that same Run Instance.

## Audit

- every Run Spec key resolves to one catalogue row;
- actor mode and action are allowed;
- target fits the type grammar;
- exit Gate and receipt are explicit or inherited without contradiction;
- routes are allowed and resolve in the Workflow;
- planned cardinality is not presented as actual inventory;
- every actual Run joins to exactly one Run Spec and one type;
- Runtime Workspace projections do not mint or recount.
