# Design workbench rules

These articles govern Design skill instructions and blueprint content. The shared UI constitution owns the
frame and page wording. The Design folder owner and specialist skills own their execution records.

## A01 · Current contracts in skill entry points

State the current rule, its source, its writer and its check. Keep conversation provenance and superseded
instructions in the blueprint's Trace or Git. Preserve valid executable responsibilities and source links.
A skill's metadata is the single version declaration; changing it requires explicit user approval.

The checked scope is the seven Design entry points, `hai-design/ref/design-ladder.md`, this constitution
and `ref/topics.md`. A passing scoped check does not certify every referenced document or the running service.

**Check:** `python scripts/current_contract_check.py`; README's fresh-context skill invocation validation.

## A02 · Block owns the page; types and groups have distinct meanings

Open Design through its owning Block. Job, Main, Task and Run content stays inside that Block. Main hides the
Task row; selected Tasks preserve their own Run identities. A Board execution Job pins goal × method version ×
inputs version. A Method Book Job holds one method identity and its signed versions, with no execution Tasks.

Board Task types are `design-reason`, `design-item` and `design-whole`; their groups are Ideas, Designs and Review.
Method family groups Jobs without creating new Job types. Fixed names stay fixed; variable rule names use
〈brackets〉. Report missing serialized Job types as a contract question; do not invent fields on real examples.

**Check:** `scripts/current_contract_check.py` reads actual Task faces and the Book's directories;
`servers/workbench-design/tests/test_design_jobs.py` checks grouping, embedded Main and original Runs.

## A03 · Shared Bands and topic definitions

Band classification and Studio Type definitions are separate. Read Band names and order from the Work blueprint's
`delivery/page-spec/studio-bands.json` through shared `studio_types.py` / `studio_tabs.py` and its structure adapter.
Studio Type requirements are authored in their own topics. Do not copy a classification list
into Design. Theme-specific definitions exist only when a distinct content contract needs them. Empty groups
are omitted; an actual Work Block shows its Studio instances without a mandatory type catalogue.

Task procedures stay with the Task type and skill; theme guidance belongs to Theme Guide. Changing a type
catalogue does not delete actual topic content, renumber directories or overwrite a person's canvas.

**Check:** `scripts/current_contract_check.py` validates shared sourcing; the shared Studio type tests own Band
rendering. Browser checks must establish what the current service actually displays.

## A04 · Structure, drawings and live previews

A Block Structure topic uses Structure / Draw / Skills. Structure pairs naming rules with real examples and
embeds the real Block. Every Structure model and embedded record outline uses the shared expandable folder
style tree: Folder, Job/Task and Studio. Job group, Job name, Task group and Task name use the common S71
level colors; meanings and types belong on hover. Preserve parentage and Block-owned source navigation.
Structure does not render a mind map. Draw remains a separate view and preserves authored drawings.
Draw reuses the shared drawing code. Skills opens the actual owning files. Change the
generator before rebuilding pages. Preserve source links and actual ownership.

A Block Job UI Preview uses live Page content and Effect for a proposal when needed. It has no independent
Delivery or Instances top view; keep outputs in the appropriate preview or Files and comparisons in Checklist.
Do not apply that restriction to unrelated Studio types. Do not claim planned Main consolidation is implemented.

**Check:** `scripts/current_contract_check.py`, the b12 structure builder's `--check`, and browser verification
of each changed view, expansion and actual Block/source links.

## A05 · Reading is not signing

Preview checks are read-only. Opening content, copying a Run prompt or changing documentation never signs a
goal, a method version, predictions, a release or closure. Keep the existing human gate and independent reviewer
context. A released Job, frozen input version or closed hard Result is immutable.

**Check:** the existing Design release, projection and embedded Job tests; fresh-context validation must respect
these boundaries and identify the correct owner rather than write a result on its behalf.
