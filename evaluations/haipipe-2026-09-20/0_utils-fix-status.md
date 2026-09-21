# Utility skill fixes and validation status

Date: 2026-09-20. Scope: all ten skills in `plugins/haipipe-toolkit/skills/0_utils`.

The locally actionable findings in the [fix plan](0_utils-findings-and-fix-plan.md)
have been addressed. Nine skills received further changes; `diagram-ascii`
retained its earlier fixes and was exercised by fresh-context validation.
Live integrations remain unverified. This report supersedes the plan's status
column, while preserving that earlier report as the record of the original findings.

## Status of each skill

| Skill | Current status | Changes and evidence | Remaining limits |
|---|---|---|---|
| `call-peer` | Local startup and read-only paths checked | Removed import-time Physician-SPACE discovery; delayed optional SDK loading; fixed Python 3.9 UTC imports; separated installed script paths from target cwd; clarified pair and native display names. All five help commands and isolated missing-pair paths work. | Provider execution, native session creation/resume, and a configured SDK success path were not exercised. |
| `diagram-ascii` | Earlier fixes retained; exercised | Fresh context produced a plain ASCII Design process diagram without mandatory emoji. | This checks the selected diagram scenario, not every gallery pattern. |
| `field-test` | Authorization guidance repaired; preparation checked | Replaced stale auto-charter guidance with the current Insight authorization reference; preserve covered grants, exact scope, owner gates, and FIELD isolation. Prepared a commission and expectations. | Synthetic target; no real standing grant supplied and no FIELD execution. No real-task convergence claimed. |
| `meal-cam-logger` | Controls passed isolated execution checks | Independent tool/output paths; restorable session controls; PID/start-time/script checks; paused stop uses TERM then CONT; delayed shutdown is reported accurately. All 27 control checks passed. | Real camera, MediaPipe model, real image encoding, Anthropic API, and other operating systems were not exercised. |
| `notebook-cell-python` | Execution and failure paths checked | Converter errors now fail the process; partial batches report actual counts. New helper preserves unique attempts, artifacts, logs, and execution receipts. Source runs once before conversion. Added cell IDs and removed an unverified Python version claim. | No browser rendering or nbconvert execution; those dependencies were absent in the fresh validation context. |
| `remote-error` | Generic interaction checked | CMS selection requires real project context; CMS-only statuses/gates moved into the profile. Reuses authorized scope, permits conditional reply sections, and distinguishes local changes from remote proof. Fixed language-specific comment markers. | Generic fixture was edited and syntax-checked; no remote rerun or real project gate. |
| `response-format` | Composition checked | Chat instructions no longer override artifact headings. Scope exceptions remain intact; final inventory placement now matches its example. | Representative text artifacts checked; viewport rendering not checked. |
| `table-task` / `task-table` | Renderer and drift checks passed | Installed renderer path independent of target cwd; Task-local receipts documented correctly; Job-level results marked legacy. Task `Not run` is distinguished from Run `Ready`. Target path contained spaces. | Other operating systems and arbitrary legacy project layouts were not exercised. |
| `table-workflow` / `workflow-table` | Declaration and owner consistency checked | Removed retired Adopt; corrected failure routes and Verify closure; Delivery projects the verified candidate. Three Specs and fifteen Cells. Counts are `C + N + J`, preserving held Commission decisions and allowing at most one release. | No live Design execution was dispatched. |
| `whoop-connect` | Missing-dependency preflight checked | Checks checkout, scripts, interpreter, credential loader, callback, and status interface before app setup. Redirect URI derives from the verified listener. | Configured external checkout absent; OAuth, token refresh, sync, and scheduling remain unverified. |

## Findings R1–R12

| Finding | Resolution |
|---|---|
| R1: call-peer startup depends on another repository | Removed that dependency from ordinary CLI startup and registry reads; optional SDK preflight is separate. |
| R2: retired Design Adopt and incorrect routes/counts | Main skill, schema, catalog, and coverage aligned with the current Design owner. Owner clarification requires `C + N + J`; the old `1 + N + J` is only the no-prior-hold case. |
| R3: converter reports success on errors | Entry point propagates `main()`'s status; partial batch failures return nonzero. |
| R4: same-day outputs overwrite and execution lacks receipts | Added unique preserved attempts and atomic execution receipts. Helper records a Step; optional `--run-id` links an existing owner identity without minting or closing a canonical Run. |
| R5: paused meal session cannot stop | Documented and exercised TERM followed by CONT, with session identity checks and bounded shutdown observation. |
| R6: installation paths and target roots conflated | Commands resolve the loaded skill directory separately and use a verified interpreter; target paths can contain spaces. |
| R7: generic debugging retains CMS rules | Profile-specific rules isolated, generic reporting corrected, and repeated authorization prompts removed where scope is already granted. |
| R8: field-test authorization reference stale | Current authorization contract linked and bounded standing grants preserved. |
| R9: Whoop preflight late and callback assumed | Dependency check moved before setup; callback now comes from the actual listener configuration. External dependency still unavailable. |
| R10: pair name contradicts native display name | Documentation distinguishes shared pair identity from the callee display-name suffix; session IDs and cwd remain authoritative. |
| R11: chat format overrides files | Artifact format follows the document's own template or directory rules. |
| R12: validation gap | Four fresh-context validation passes plus local checks completed. Live services, real FIELD execution, and other operating systems remain outside the validated scope. |

## Validation evidence

Evidence snapshots are stored in [0_utils-validation](0_utils-validation/README.md).
Receipts retain their original temporary paths and timestamps; the snapshot
manifest maps them to durable copies here.

- **Meal controls:** 27/27 checks across four sessions, with real process
  signals and deterministic camera/detector/API substitutes. Pause, resume,
  paused stop, empty receipts, episode removal, concurrent session isolation,
  and cleanup checked. [Receipt](0_utils-validation/meal/validation-receipt.md).
- **Local call-peer and notebook checks:** 17/17 passed on the default Python
  3.9, including all help commands, missing pair and SDK paths, two same-second
  attempts, failed-source receipts, converter errors, and notebook cell IDs.
  [Results](0_utils-validation/local/checks.json).
- **Notebook interruption:** one additional check passed: SIGTERM produces an
  interrupted receipt with end time, interrupted Step state, and no claimed notebook.
  [Result](0_utils-validation/interruption/checks.json).
- **Fresh execution context:** checked read-only pair behavior, notebook
  reruns, source preservation, missing input, failed data access, and mixed
  conversion failures. [Receipt](0_utils-validation/execution/validation-receipt.md).
- **Workflow and Task tables:** three Specs, fifteen Cells, Task-local receipt
  rendering, and clean/drift/expected-failure gates checked. Three documentation
  frictions were repaired and rechecked. [Receipt](0_utils-validation/workflow/VALIDATION-RECEIPT.md).
- **Interaction:** generic debugging, chat/artifact separation, commission
  preparation, and missing Whoop checkout checked. Both minor documentation
  frictions were repaired and rechecked.
  [Receipt](0_utils-validation/interaction/validation-receipt.md).
- **Static checks:** all 13 Python files parsed; utility `git diff --check`
  passed. Eight skills pass the stock Codex skill validator directly. The
  remaining two pass when their existing Claude `argument-hint` extension is
  omitted from temporary validation copies; that field remains in source.
  This is a validator compatibility exception, not an unconditional ten-skill
  stock-validator pass. [Results](0_utils-validation/static-checks.json).

Fresh validation also caught Python 3.9 import compatibility, missing notebook
cell IDs, stale receipt-path descriptions, and reply example conflicts. Those
were corrected before this report was finalized.

## Change boundaries

Pre-existing changes and dirty upstream submodules were preserved. This pass
changed 29 utility files relative to its saved starting snapshot, including
the new notebook helper and updates to eight existing version histories.
The related Insight agent description was also corrected from Application
Insight to InsightBoard; its other instructions were preserved.
Evaluation reports and evidence snapshots are additional files.

No provider call, camera capture, OAuth flow, real user-data access, deployment,
commit, or push was performed. Native camera-backend diagnostics may contain
source details; the skill now tells the operator to keep those logs local.

The remaining work requires actual integration environments: a configured
Whoop project, camera/model/API access, provider sessions/SDK, a real FIELD
target and grant, and platform-specific checks. The local fixes are ready for
those checks; this report does not claim those integrations already work.
