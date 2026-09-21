# haipipe-run implementation and validation

Date: 2026-09-20. Status: the approved source update is implemented.

The [revised plan](run-update-plan-v2.md) is now applied to the shared Run skill
and its direct consumers. Existing dirty worktree changes and concurrent
owner-contract updates were retained. No project Run was executed or migrated.

## What changed

| Area | Implemented result |
|---|---|
| Shared meaning | A Run is one bounded commission with one native identity; attempts and Steps remain its history. Workflow definitions list Specs and runtimes index actual instances, with dependencies and routes. |
| Skill structure | Compact entrypoint plus a shared catalogue, identity/history reference, and receipt/inventory reference. Version 0.27.0 and invocation metadata align with these decisions. |
| Catalogue | Current Task, Discovery, Page RP/RE/RD, delegated paragraph, optional post-run analysis, independent display, Insight, Design, Paper, and Labeling profiles point to their owners. Generic Execution templates and historical forms are labeled separately. |
| Consumers | Workflow and Task planning/reporting, Page families/workflow/glossary, Paper judgment closure, Ideation, Folder, table skills, STRUCTURE and package README use the same distinctions. The old Workflow catalogue forwards to the shared index. |
| Storage | Current Task output resolves as `$OUTPUT_ROOT/<task>/results/<run>`; readers retain historical `results/<task>/<run>` lookup and recognize declared mirrored stores. Relative stores use the SPACE marker or checkout ancestor, with explicit findings when unresolved. |
| Closure | Paper judgments require a saved named-human close; waiting is distinct from completion. Page/Task closure and promotion remain with their owners. Display references resolve governed units rather than forcing a second payload copy. |
| Inventory readers | Missing receipts are Held. Duplicate locations join into one recovery row. Orphan Results remain visible. Attempt archives add no Runs. Task tables retain recovery rows in the default report and preserve Waiting. |
| Task launcher | New shell Tickets verify declared input files/hashes, fingerprint the contract, preserve previous attempt receipts, increment attempt numbers, exclude simultaneous writers, and refuse to overwrite closed Results. |

Current Paper compile/response and Design Commission/Generate/Verify contracts
were already being developed in the worktree. The index follows those owner
contracts; this update does not claim authorship of their entire implementations.
Likewise, Task Workflow `run_specs` conversions already present were preserved.

## Who uses it

| Consumer | Use |
|---|---|
| Workflow, Paper and Ideation planners | Decide what deserves a Run Spec and which profile applies. |
| Native domain owners | Allocate, reuse, resume and close work under native schemas and authority. |
| Selected workers | Execute the commissioned work and produce its declared outputs. |
| Page Run Space and Task/Workflow tables | Resolve records, show truthful state and count identities once. |
| People requesting an inventory or explanation | Receive understandable targets, Results, findings and next actions. |

The primary consumer is the agent handling a domain request. A person can ask
to continue writing, analyze a source or inspect unfinished work without
supplying schema keys or Workspace matrices.

## Validation observed

| Check | Result |
|---|---|
| Skill-creator `quick_validate.py` on `haipipe-run` | Passed. |
| Main skill and new references: relative Markdown links | All file targets resolved. |
| Changed reader Python syntax and shell Ticket syntax | Passed. |
| Existing `test_runs_plugin.py` suite | 32 tests passed. |
| Isolated runtime/reader scenarios | 17 behavior checks passed; see the reproducible fixture below. |
| Fresh-context skill invocation, first pass | Correct ownership, counting and next actions; found retry-history and consumer-document contradictions. |
| Fresh-context invocation, final pass | Correctly distinguished 10 described existing identities (including one incomplete allocation), three planned commissions and two RI versions under one binding. Rechecked the corrected consumer sections. |

The fresh evaluators received a realistic request and skill path without the
planning report or expected answer. Their source-based findings prompted the
launcher/history fix, storage and Workspace clarification, and the remaining
consumer wording fixes. Their static review is separate from the runtime tests.

The isolated fixture exercises failed retry and byte-identical archived receipt,
attempt numbering, completed-Result immutability, changed config and input
rejection, missing inputs, explicit input hash checks, archive exclusion from
inventory, Paper closure, Design Commission, missing/orphan/duplicate records,
mirrored and relative Task stores, Waiting, and default-table recovery visibility.
One added report assertion initially failed because the fixture had removed its
store declaration; restoring that declaration made the duplicate-store scenario
valid. No production change was made to bypass that assertion.

### Reproduce the behavior checks

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 evaluations/haipipe-2026-09-20/run-validation/validate-runtime.py
```

This creates an isolated temporary workspace and prints its path. Its workers
are small synthetic fixtures with notebook mode off. It does not run research
jobs or modify project Tickets.

Evidence:

- [Behavior checks and subprocess outcomes](run-validation/runtime-checks.json)
- [Reproducible fixture](run-validation/validate-runtime.py)
- [Initial fresh-context answer](run-validation/fresh-initial-answer.md)
- [Initial sources](run-validation/fresh-initial-sources.md)
- [Final fresh-context answer](run-validation/fresh-final-answer.md)
- [Final evaluator sources](run-validation/fresh-final-sources.txt)
- [Final evaluator source hashes](run-validation/fresh-final-source-hashes.json)
- [Touched source paths](run-validation/changed-source-files.txt)
- [Source hashes at final local check](run-validation/source-hashes.json)

## Compatibility and limits

- These are repository source changes. Installed skill copies and existing
  project Tickets are not automatically replaced. A legacy failed receipt
  without a provable frozen fingerprint requires owner recovery before retry.
- The native attempt archive preserves receipts automatically. The owner must
  preserve partial payloads needed for recovery before retry. Declared inputs
  must include the dependencies needed to establish the frozen commission;
  the fingerprint does not discover undeclared environment dependencies.
- A dispatcher-only external `RESULT_STORE` needs a durable resolved pointer.
  Job-local readers cannot discover an unrecorded one-off destination. An
  inventory must disclose this coverage gap.
- Presenter checks establish structural availability. They do not grant human
  approval or replace domain acceptance and independent review.
- No Windows/PowerShell execution, browser UI interaction, real data workflow,
  installed-skill rollout, or historical runtime migration was performed.
- Labeling's optional-P0 planning formula was not changed. Its 25 operations
  are linked from the shared catalogue; planned cardinality remains domain-owned.

The source update implements all six batches of the approved plan within these
stated boundaries. Future allocation uses native owners; existing published
Results and their identities remain historical evidence.
