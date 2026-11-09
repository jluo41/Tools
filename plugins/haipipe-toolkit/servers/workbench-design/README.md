# Design workbench

This module depends on the shared host in `../_host` and the shared workbench frame in `../workbench`. The shared host can start without a Design page being present.

## Current Block frame

`design_context.py` adapts modern Design Board Blocks to the shared Report frame. It reuses `design_focus.block_view` for domain content and actions, retaining Summary, Goals, Jobs, Rounds, Methods and MindMap. Legacy Block Work links select the corresponding Report view.

Each view contains Review Content followed by the eight shared Around the Work sections. Explicit `view:` metadata takes precedence over linked Topic scope. Unassigned supporting records remain in the aggregate rail. Skills and Files use the same selected scope as the other supporting sections.

Job and Task pages retain their existing workflows and human release approval. Older six-Space and Design Folder pages are unchanged. Replacing the six business views, introducing a method-development Block, and adding a four-state Checklist approval workflow remain proposals.

The authored contract lives in [`b12_theme_design/ui/structure.md`](../../../../blueprints/Project-Ladder/work/b12_theme_design/ui/structure.md), with its Block matrix, source and skill explanations, and routed examples beside it. Earlier blueprint drawings remain historical and have not been redrawn.

## Validation

From the repository root, with Python, pytest and the host dependencies installed:

```sh
python -B -m pytest -q plugins/haipipe-toolkit/servers/workbench-design/tests plugins/haipipe-toolkit/servers/workbench/tests/test_work_frame.py
```

On 2026-11-08, this check passed with **73 tests and 298 subtests**. After removing a duplicated pending instruction in the merged Block content, the four `test_design_context.py` tests passed again. The tests cover explicit scope precedence, aggregate rail retention, consistent supporting sections, legacy routes, preserved Job approval wording, real matrix/example routes, and read-only rendering of the fixture.

An isolated loopback host also verified the desktop Design Block, the blueprint matrix explanation dialog, and its Goals example link. At 390px, the six view buttons wrapped and the Sections drawer opened correctly; DevTools was restored afterward. This was a focused visual check, not a complete mobile interaction audit of every Topic and file preview.

The shared running host was not restarted. A host that imported the earlier code needs a restart to load this adapter. No user acceptance, goal signature, release, commit or push is implied by these checks.

## Clickable use cases

The blueprint now has Block, Job and Task matrices with seven clickable use cases: SMS and checklist design at Block and Job level, plus input-bounded reasoning, individual design verification, and whole-set ranking at Task level. There is one Design Job contract; released and reasoning examples are state variants. The three Task roles come from `design_reader.kind_of` and `design_focus.TASK_STEPS`.

Public fixtures live in the adjacent `view-guide.json` and are labeled **Blueprint example**. Project mappings live only in the ignored `.server_config/workbench-examples.json`; the shared `use_case_examples` module resolves each SPACE's configured origin. Checklist examples have no synthetic public counterpart yet: without the local mapping their dialog says **No linked examples yet**. No project content or deployment origin is stored in the public guide.

Validation on 2026-11-08:

- `test_design_context.py` and `test_use_case_examples.py`: **8 passed**. Public example levels, Task roles, view routes, missing-instance behavior and shared path restrictions are covered.
- All seven dialogs opened in the isolated preview. Project and Blueprint examples were distinguishable; Job Tasks and Path expanded; closing and reopening worked.
- A configured checklist project's Block, Job and individual-design Task opened in its existing service. That service still displayed its earlier UI; this did not deploy the new frame there.
- The SMS project's source faces and hierarchy resolved, but its configured service could not be reached in Chrome. Its online destination is not verified as available; service recovery remains with the coordinating session.
- At 390px, the Task use-case dialog, expanded Tasks and long Path wrapped within the viewport. DevTools was restored and the verification tab closed.

No external SPACE service was restarted and no shared renderer was changed for this integration.
