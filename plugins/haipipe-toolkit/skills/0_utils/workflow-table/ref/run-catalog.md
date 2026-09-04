# Run Catalogue schema and workspace reference

The Run Catalogue is the workspace's reference table for what a Run can be.
This file, shipped beside `/workflow-table`, is the schema/example reference;
it is **not automatically the live catalogue for every workspace**. A live
workspace catalogue must be explicitly declared at a resolved path and contain
its own `run_catalog.runs` rows. It is not a log of current activity. A
catalogue row names a stable Run type; an actual instance belongs in a
workflow's Runs Overview with an allocated Run ID, Ticket, Result, acceptance,
and receipt.

## 1. Row grain

One row represents one independently closable Run type. The key answers “Run
for what?” and the close gate answers “when is that work done?”

```text
Run Catalogue type ──permits──> concrete Run ID
concrete Run ──produces──> Result + receipt
Result ──passes phase gate──> L3 promotion or route
```

Do not make a new catalogue type for every script, API request, retry, or
substep. If several calls share one Ticket, target, Result, and acceptance
gate, they are operations inside one Run. A call or file edit becomes a Run
only when it has its own independent close boundary and receipt.

## 2. Canonical reference table

| Run key | Family | Run for | Common operations | Typical target | Inputs | Result | Close gate | Owner contract | Not a Run when |
|---|---|---|---|---|---|---|---|---|---|
| `acquisition.scrape` | Acquisition | one bounded crawl/extraction attempt | fetch, parse, checkpoint, resume | source/site + scope | URL/config/browser profile | raw dataset + receipt | requested scope is covered or an explicit terminal error is recorded | `haipipe-run` + source contract | a single page request is one step in a larger crawl |
| `acquisition.api-fetch` | Acquisition | one bounded API retrieval | authenticate, call, paginate, validate | endpoint + query/snapshot | endpoint/version/parameters | response artifact + validation receipt | response is stored and schema/status checks pass | `haipipe-run` + source contract | each HTTP call shares the same Ticket and close gate |
| `transformation.build-data` | Transformation | one reproducible data build | transform, join, validate, export | named input/output dataset | frozen inputs + config | derived dataset + manifest | output and manifest pass validation | data-pipeline contract | a helper function or temporary file has no independent receipt |
| `training.fit` | Modeling | one model-fitting attempt | fit, checkpoint, save | dataset/config/model family | train split + config + seed | model artifact + metrics | artifact loads and required fit metrics are recorded | model/Run contract | each epoch or hyperparameter call shares the Run gate |
| `evaluation.validate` | Evaluation | one bounded validation/evaluation | score, compare, summarize | model + evaluation set | frozen model/data/version | metrics/report + receipt | predefined evaluation assertions pass or are signed as failed | evaluation contract | a metric calculation is only a step in the evaluation |
| `inference.batch-predict` | Inference | one bounded prediction batch | load, predict, write, check | model + input batch | model/version + batch | prediction artifact + manifest | all rows are accounted for and artifact is readable | endpoint/inference contract | one prediction row or API call has no separate close gate |
| `discovery.paper-analysis` | Discovery | one bounded source-analysis attempt | retrieve, read, extract, cite | paper/source set | query + source policy | evidence record + provenance | claims and source pointers pass the discovery gate | discovery contract | a browser search or note fragment is not independently closable |
| `authoring.write-file` | Authoring | one bounded file/content change | edit, render, lint, diff | named file or artifact | brief + current version + policy | candidate file + diff/receipt | requested checks pass and the change is accepted or routed back | owning artifact contract | an editor keystroke or generated temp file is a step |
| `packaging.smoke-test` | Packaging | one bounded package/release check | assemble, install, invoke, inspect | package/version | source tree + lock/config | test report + receipt | smoke assertions pass or a terminal failure is recorded | packaging contract | each shell command is part of the same smoke test |

The examples are workspace vocabulary, not a mandatory roster. A workflow
declares only the keys it uses. If no existing key fits, define a new key with
the same columns in the live workspace catalogue before commissioning a
concrete Run. Until that happens, the bundled examples are `template-only`.

## 3. Normalized catalogue

```yaml
run_catalog:
  id: <workspace-run-catalog-id>
  version: <catalogue version>
  owner: <workspace contract or skill>
  runs:
    - key: <stable run key>
      family: <family>
      run_for: <independently closable purpose>
      operations:
        - <operation>
      typical_target: <target grammar>
      inputs:
        - <frozen input or policy>
      result: <result shape/pointer>
      close_gate: <testable close condition>
      owner_contract: <contract path/name>
      not_a_run_when:
        - <boundary condition>
```

In a workflow declaration, reference the catalogue without confusing type
keys with instances:

```yaml
workflow_table:
  run_catalog:
    mode: <declared | template-only | none>
    ref: <workspace path to run-catalog declaration>
    keys:
      - acquisition.scrape
      - evaluation.validate
  rows:
    - id: source.collect
      l4_run_profile:
        families: [Acquisition]
        operations: [scrape]
        target: <bounded source scope>
        cardinality: 0..N
        owner_contract: haipipe-run
```

When `mode: template-only`, the `ref` points only to this skill reference and
the key is guidance, not a workspace resolution. When `mode: declared`, `ref`
must resolve to the live workspace catalogue. `acquisition.scrape` is a type
reference. A concrete Runs Overview might instead contain `b01j02t01r03`, its
Ticket, status, Result pointer, and receipt.
The catalogue never claims that the Run happened, succeeded, or has a current
status.

## 4. Boundaries and audit checks

| Question | Catalogue answer | If false |
|---|---|---|
| Can the work close independently? | define a Run type | keep it as a phase step or operation |
| Does it have one Ticket, target, Result, and close gate? | one Run may contain many calls/commands | do not split calls into fake Runs |
| Is it a human approval or signature? | Human Actions gate | not a Run |
| Is it a planned cardinality such as `0..N`? | a workflow demand | not actual inventory |
| Is it an allocated identity with receipt? | concrete Runs Overview instance | not merely a catalogue row |
| Does the type have a named owner contract? | catalogue row is usable | `HOLD` before commissioning |

Every Run profile named by a workflow should resolve to a catalogue key when a
catalogue is declared. Every concrete Runs Overview row should resolve to one
catalogue key, but its status and Result must come from the instance receipt,
not from this reference table.
