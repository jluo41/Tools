# Studio Check view

A type defines requirements once in `elements.md`; its instance references that type with a
SPACE-relative `check_type` in `studio-views.json`. Check is the final top view, separate from
content views and skill buttons. Use the existing Studio top-view/left-tab/right-content framework.

```json
{"check_type": "examples/Project-Example/blueprint/b01_theme/s71-type", "views": []}
```

The left selects a content view; in a Skills instance it selects an actual skill. The right lists
that type's `must` requirements and its `check` verification method, with a source link under Verify.
Definitions use ◇; instances use □ with a Not verified tooltip. Neither mark claims execution.
Source requirements are not copied into an independently maintained instance checklist.

For element-level navigation, set `check_layout: "elements"` in the manifest.
The Check left items then read `Top › Left` (or `Top` for full-width content).
Each right card retains that element's requirements and inherits its Top view's
requirements. This checks the enclosing layout as well as the selected content;
no parent criteria may disappear when the element is selected. Verification
methods describe concrete source comparisons and interactions. Results require
actual execution evidence; the generated cards themselves supply no result.
Examples beside requirements follow [type-examples.md](type-examples.md).

Use `scripts/check_views.py <topic>` to generate `delivery/check.html` and the managed Check view.
`--check` compares generated content, including the requirements fingerprint, to its current source.
It checks that this UI is current; it does not certify the underlying Studio, skill or work product.
Missing criteria, missing types and paths outside the SPACE are errors, not successful empty checks.

`type_requirements.py` and `skills_views.py` include this generation when `check_type` is present.
A Skills topic's Check button is not a skill and does not replace any skill's file tabs.
No browser action runs shell commands. Automated execution, result receipts and evidence freshness
are separate capabilities; this pilot records no pass result or fabricated verification time.

Validate with `tests/test_check_views.py`, then open the owning Block, select Check, switch left items
and inspect Verify. Confirm both the inherited criterion and its type source, including phone width.
