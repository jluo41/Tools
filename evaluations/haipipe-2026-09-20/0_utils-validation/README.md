# Utility validation evidence

These are snapshots from isolated checks conducted on 2026-09-20. The original
receipts preserve their timestamps, commands, temporary paths, and limits.
Relative links inside those original receipts may still refer to the temporary
workspace. Use this index for the durable evidence copies.

| Evidence | Location |
|---|---|
| Fresh call-peer and notebook checks | [execution receipt](execution/validation-receipt.md), [checks](execution/checks.json) |
| Meal session controls | [receipt](meal/validation-receipt.md), [27 checks and commands](meal/validation.json), [isolated harness](meal/validate.py) |
| Workflow, ASCII diagram, and Task renderer | [receipt and recheck](workflow/VALIDATION-RECEIPT.md), [commands](workflow/commands.json), [Design table](workflow/design-workflow.md), [declaration](workflow/design-workflow.json), [diagram](workflow/design-process.txt) |
| Task report fixture | [generated Task Table](workflow/Project%20with%20spaces/tasks/TASK-TABLE.md) |
| Generic debugging, reply formats, FIELD preparation, Whoop preflight | [receipt and recheck](interaction/validation-receipt.md), [frictions](interaction/friction-log.md), [authorization limits](interaction/authorization-evidence.md) |
| Default Python 3.9 checks | [17 local checks](local/checks.json) |
| Notebook SIGTERM finalization | [interruption check](interruption/checks.json) |
| Final Python syntax, skill frontmatter, and whitespace checks | [static checks](static-checks.json) |
| Original-to-snapshot paths | [snapshot manifest](snapshot-manifest.json) |

The Design declaration and diagram show the initial fresh-context output.
The workflow receipt's recheck and source excerpts record the later correction
from `1 + N + J` to `C + N + J`; the original output is retained as evidence of
the friction. The execution receipt similarly predates the local correction
of notebook cell IDs and metadata; the subsequent local checks cover those fixes.

These checks use synthetic fixtures or local read-only paths. They do not
establish live provider, camera, OAuth, Whoop, or real FIELD execution success.
