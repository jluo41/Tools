# Shared Task recipes and instance execution

## Execution identities

1. Base R: the normal reusable Task Run ticket/recipe and parameter interface.
   Implementation stays in Task `scripts/`; shared Job code stays in `src/`.
2. RI: the Insight Run Ticket that points to that R ticket and freezes a new
   dataset, question, DIKW target, and acceptance contract.
3. Test execution: a frozen sample input used to verify the recipe. Its
   ticket/result/receipt remain evidence about that test.
4. RI execution: the independent Insight Result with its own data snapshot,
   parameters, output scope, receipt, and full `instance#riNN@vNNN` identity.

A Task need not know all patients. It validates the supplied contract per
call. In this use case each patient has an independent complex dataset;
batching patients is an explicit choice, not an inferred redesign.

## Parameterized call packet

This is a new declared recipe protocol, not a claim that every old ticket
already accepts these parameters. Adapt a hardcoded launcher under its Task
owner first. Invoke a declared ticket; do not edit and restore the producer's
config or source arbitrary shell code into the calling process.

```yaml
recipe_id: <full-task-address>/description
owner: <task-folder-path>
entry: <declared-parameterized-task-ticket>
entry_sha256: <ticket-hash>
code_version: <git-sha-plus-dirty-diff-hash-or-code-content-hash>
parameters:
  input_manifest: <versioned-dataset-manifest>
  output_root: <instance-owned-supporting-result-store>
  options: {}
parameter_contract: <declared-interface-path-and-version>
producer_execution: <full-native-producing-Run-address>
consumer_insight_execution: <instance>#<riNN>@<version>
producer_ticket: <exact-native-producing-ticket-path>
producer_ticket_sha256: <ticket-sha256>
receipt: <exact-upstream-runtime-receipt-path>
receipt_sha256: <receipt-sha256>
```

The adapter maps these fields to real worker flags/environment/config. Unknown
keys and unresolved dataset fields fail visibly. Validate the effective input
and output in the producing receipt; never fall back to test data. Freeze the
effective config and recipe/code hashes before work. Output location alone is
not execution identity. The producing execution is distinct from the consumer
RI; its own Ticket and receipt name that producing identity. The frozen receipt
must report `execution`, `run_id`, or `run`, matching `producer_execution`, with
accepted terminal `status: complete | accepted | passed`. Adapt a native dialect
at its owner when needed; do not rewrite a completed receipt to impersonate RI.
The same producer must occur in `supporting_results`. Reused accepted support
needs no new recipe call, but the consumer still needs its own RI allocation.
Every support, reused or newly produced, binds its native `ticket`,
`ticket_sha256`, `receipt`, and `receipt_sha256` alongside the Result path/hash.
The same identity and terminal-receipt checks apply when `recipe_calls: []`.

## Execution sequence

1. Resolve the dataset and frozen question/target/acceptance, then allocate or
   resume the consumer RI through `insight_items.py bind`. This writes its
   immutable `binding.yaml` and planned receipt, not the final evidence input.
2. Search for accepted support matching the exact input/recipe/parameters.
   Reuse it if available. Otherwise commission the producer's native Ticket
   and distinct execution identity under that Task's authorization rules.
3. Pass a frozen manifest and isolated output root. Concurrent calls use
   disjoint output, scratch, and notebook paths. Freeze the effective producer
   config; the base recipe and original test execution remain unchanged.
4. Run under the producing Task's Result/report rules. Materialize the accepted
   Supporting Result and receipt. Bind numeric output through the Page's
   collection route and complete the required typed local Evidence Results.
5. Assemble a separate evidence packet containing `supporting_results`,
   `local_sources`, and completed `recipe_calls`. Finalize the interpretation
   input with `insight_items.py freeze <instance> --item <ri> --version v001
   --evidence <packet.yaml>`. It validates current hashes and copies the
   allocated binding into `input.yaml`, then records the frozen checkpoint.
6. Execute DIKW interpretation, obtain independent review, and publish the
   versioned RI Result. RI owns this interpretation; reusable numerical output
   retains its producing Run identity.

`freeze` refuses an existing input. A corrected input under the unchanged RI
binding uses the next explicit `vNNN`; changed dataset, base R, question, target,
or acceptance requires a new RI. Older prematurely frozen empty v001 packets
remain intact and can be superseded by v002 under the same binding.

Computation and DIKW have distinct targets and Results. A forwarding caller
does not earn an extra umbrella Run; code alone is not citable evidence.

## Storage

The existing Task `RESULT_STORE`/`OUTPUT_ROOT` resolver can select an
instance-owned store. Use the adapter's declared resolver. A common mirror:

```text
<instance-store>/<block>/<job>/<task>/results/<local-run>/<version>/
```

The version level belongs to the new Insight instance dialect, not all legacy
Task paths. Insight interpretation Results stay at
`<insight>/results/<item>/<version>/`. Preserve large data in its governed store.

## Adapter verification

Before claiming a shared entry is instance-ready, execute it on two small
synthetic independent datasets with distinguishable expected outputs. Verify
one unchanged recipe, disjoint outputs/scratch, actual input and code version
in receipts, rejection of unknown parameters, distinct identity after a data
version change, and an unchanged original test execution. These checks test
the adapter, not scientific findings.

This update defines the protocol. Adapting a project-specific launcher is
implementation work under its Task owner when commissioned; loading a Page
does not silently adapt or execute it.
