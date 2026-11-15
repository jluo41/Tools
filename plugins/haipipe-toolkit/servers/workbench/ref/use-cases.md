# Linked use cases and UI walkthroughs

Part of the [Workbench base README](../README.md).

## Linked use cases

A matrix's `Use Cases` cells open related Block/Job/Task links. Public examples
are declared in the adjacent `view-guide.json` under
`use_cases[level][type][case]`, as a list of `{ "path": "relative/page", "label": "Blueprint example" }`.
The optional label distinguishes demonstration records from active work.

Cross-SPACE examples stay in the served root's ignored
`.server_config/workbench-examples.json`: `spaces` maps an alias to an absolute
`root`; `matrices` maps a root-relative matrix file to the same level/type/case
mapping. An entry may add `"space": "alias"`. Only this private allowlist can
refer outside the served root. The destination uses its own configured `DOMAIN`;
no proxy or extra file-serving route is added. Missing pages are omitted, and a
SPACE without an address is shown without an Open link. Related Tasks are read
from the selected Job's immediate existing Task faces. Runs stay within Tasks.

Work-shaped Job pages show their Job type below the title. The type follows the
existing Work, CoWork, Discovery, or People presentation; application purposes do
not create new types. An optional `use-case:` header on the Job's own face names
its application case. It is not inferred from folder names, inherited from the
Block, or copied from the example index. Missing use cases are omitted.

## UI walkthroughs

Block UI, Job UI and Task UI each have one **Walkthroughs** section. Its left tabs match the live examples; the right panel plays the recording or shows **Not recorded**. Recording requirements appear in that view's **Checklist**, derived from the same file lookup as the player. The right-rail Checklist includes all three UI views, grouped by view. Do not add a separate **Walks to record** section. Recorded means a recording file exists, not that the UI passed review.

Use-case mappings must be checked against source faces and, when ambiguous, their implementation. A Job-level example is labeled as related work at Job level; it does not count as Task coverage. `use_case_notes[level][type][case]` can explain a verified coverage gap. A private mapping with `preview_available: false` retains its verified source path but does not offer a broken preview link. Recheck the preview before removing that flag.
