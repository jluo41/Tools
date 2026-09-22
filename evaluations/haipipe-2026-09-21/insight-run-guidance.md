# Insight Run guidance update

Date: 2026-09-21. Scope: the Insight plugin family in the existing local checkout.

## Changed files

- `plugins/haipipe-toolkit/servers/workbench-insight/insight_run_specs.py` — new read-side selection and request model.
- `plugins/haipipe-toolkit/servers/workbench-insight/insightboard.py` — Insight surfaces, native inventory metadata and local clipboard action.
- `plugins/haipipe-toolkit/skills/board/haipipe-board/ref/insight-space-mapping.md` — surface, selection, metadata and copy contracts.
- This report.

No shared UI helper, style, central Run catalogue, native allocator, Skill
manifest or existing business Board was edited. Existing work in other families
and dirty submodules was preserved. No test-file changes remain.

## Selection and workflow

The selected question × partition is joined to an open Insight Runtime's
hash-pinned frozen definition. Only commissioned support, evidence, structure,
scoped writing and delivery Specs belonging to that answer target are shown.
Explicit cell consumers take precedence over Page matching; definitions with
multiple answer targets need an exact cell or Page binding. A definition with
one answer target can scope its bounded Specs to that target. Declared Spec or
native Run dependencies are followed without allocating anything.

Completed work is omitted from the offers. A reused label alone cannot hide an
incomplete Run; that inconsistency stays visible and held. Settled, refused,
unasked and partial-final cells have no answering offers. Unpinned, changed or
unreadable definitions, ambiguous bindings, and conflicting owner/type records
produce visible notes. Unsupported Spec families are identified as “Not built”.

The `chain` command remains the execution entry. Native owners retain their
entry/exit rules, acceptance, release, copilot and person-reserved gates.
DIKW/Folder kinds, registration, Page passes, checks, GI decisions, signatures
and settlement remain resources or controls. No Phase execution model or
wrapper Run was introduced.

## Surfaces and capability

| Surface | Work displayed | Capability |
|---|---|---|
| Insight / Answer | Owed structure and scoped writing Specs | Copy request → paste and send |
| Evidence | Owed support and local evidence Specs | Copy request → paste and send |
| Delivery | Owed commissioned delivery Specs | Copy request → paste and send |
| Page Insight / This page | Owed Specs with that exact target Page | Copy request → paste and send |
| Run / Runs | Actual native Run inventory and recorded statuses | Shown here · read-only |
| Run / Workflow map | Selected owed Specs, separate from instances | Shown here · read-only |
| Scope and Check | Registers and resource/GI controls | No Run launcher |

Each Spec exposes a reader-facing name, canonical recorded Run Type, bounded
purpose/target, owner Skill, worker Skills, actor, prerequisites and matching
native Run/status. Missing metadata is shown as unresolved; workers or Run Types
are never inferred from Folder kinds. The Run inventory preserves external
reused dependencies that do not have a newly allocated Spec or Ticket.

## Copy request behavior

The prompt includes the exact Board path, question and partition, answer Page,
Runtime and definition hash, selected Spec and target, canonical Run Type,
owner/workers/actor, frontier state, inputs, dependencies, entry requirements,
matching native Runs and next permitted action. It requires reuse of accepted
Results and resumption of compatible existing work, with native receipt/input
checks before allocation. It asks for the actual Run id, status, exact Result
and receipt paths, and any blocker. When no Run was allocated or resumed, the
answer must say so without inventing an identity or receipt.

Copying only accesses the clipboard. It does not send, start, allocate, update
a Runtime or persist a file. A visible read-only textarea is the fallback for
missing, denied or throwing clipboard access. Canonical identifiers are kept
intact when the display formatter expands Page names.

## Shared interfaces and remaining gaps

Native owners should publish `run_type`, `owner`, `actor`, `target`, `inputs`,
`depends_on`, `entry` and `worker_skills` (existing worker field variants are
also read). Definitions with multiple targets need precise `{question,
partition}` consumers or target Page paths. Absent fields remain unresolved
and the request tells the owner to hold and resolve them.

There is no native “Start here” launcher on these Insight surfaces. The existing
chain/owner route is used. Standalone Insight pages do not load the shared
clipboard helper, so the callback is local and namespaced. A future shared
clipboard interface would need to preserve exact prompt text, perform no
dispatch, and offer a visible copy fallback; no shared edit is required here.

Historical Page-referenced source receipts remain a separate read-only
provenance view. Their missing type, worker, actor and prerequisite metadata is
identified rather than fabricated. Aggregate statuses are recorded projections;
the copy request requires current native receipts to be read before execution.

## Validation record

- Python `ast.parse` passed for both changed Python files.
- `node --check` passed for the inline JavaScript. This was a syntax check;
  clipboard behavior was not executed in a browser.
- Scoped `git diff --check` passed.
- No test edits remain and no new tests were retained.

Before the coordinating task reiterated its no-tests constraint, the existing
suite was run once in response to the visible direct request to test:

```text
python3 -m unittest discover -s tests -p 'test_insight*.py' -q
56 tests run; 54 passed; 2 failed.
```

The failures were `test_render_every_space_and_short_link`, which expects the
old “Run Spec templates” heading, and
`test_register_question_appends_a_grid_row_and_a_log_line`, which expects the
old “give Claude Code” wording. The new UI uses selected “Owed Run Specs” and
an explicit execution-entry/copy action. After the correction, the test edits
and an unexecuted draft regression file were removed; no further tests were
run. These assertion updates remain for a separately authorized test change.
The implementation is not reported as having a passing test suite or browser
validation.
