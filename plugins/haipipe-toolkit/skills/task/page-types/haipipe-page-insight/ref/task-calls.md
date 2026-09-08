# Shared Task recipes and instance execution

## Three identities

1. Recipe: reusable computation and parameter interface owned by the Task.
   Implementation stays in Task `scripts/`; shared Job code stays in `src/`.
2. Test execution: a frozen sample input used to verify the recipe. Its
   ticket/result/receipt remain evidence about that test.
3. Instance execution: an Insight call with its own data snapshot, parameters,
   output scope, receipt, and full execution identity.

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
execution: <instance>#<local-supporting-run>@<version>
receipt: <exact-upstream-runtime-receipt-path>
```

The adapter maps these fields to real worker flags/environment/config. Unknown
keys and unresolved dataset fields fail visibly. Validate the effective input
and output in the producing receipt; never fall back to test data. Freeze the
effective config and recipe/code hashes before work. Output location alone is
not execution identity.

## Execution sequence

1. Search for accepted support matching exact input/recipe/parameters; reuse
   it if available.
2. Otherwise allocate an instance-local supporting ticket/receipt calling the
   shared recipe. The recipe is a definition, not a second counted execution.
3. Pass a frozen manifest and isolated output root. Concurrent A/B calls use
   disjoint output, scratch, and notebook paths. Shared code and the existing
   test execution remain unchanged.
4. Run under the producing Task's execution and Result/report rules. Materialize
   the Supporting Result and provenance. One page-serving collection route
   binds numeric output for Page use.
5. Complete typed local Evidence Runs and freeze their Results into the
   Insight item's interpretation input.
6. Execute the independent DIKW work, check, and publish the item Result.

Computation and DIKW have distinct targets and Results. A forwarding caller
does not earn an extra umbrella Run; code alone is not citable evidence.

## Storage

The existing Task `RESULT_STORE`/`OUTPUT_ROOT` resolver can select an
instance-owned store. Use the adapter's declared resolver. A common mirror:

```text
<instance-store>/<block>/<job>/results/<task>/<local-run>/<version>/
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
