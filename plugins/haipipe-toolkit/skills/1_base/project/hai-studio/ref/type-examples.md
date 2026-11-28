# Examples beside type requirements

A Studio Type keeps its Top views and Left items. Its Right content shows the
requirement followed by an expandable Example. This example explains that element;
it does not certify that the example meets every requirement. Examples belong with
their corresponding right-content requirements, not in a separate Examples top view.

Use `examples.json` beside `elements.md` to bind each rendered requirement to an
existing instance's `studio-views.json` item:

```json
{
  "Page-Job / job-overview": {
    "topic": "examples/Project-Example/blueprint/b01_theme/s11-preview",
    "view": "Page-Job",
    "item": "job-overview"
  }
}
```

The key is `Top / Left`, or `Top` when there is no left item. Bindings select by
name, never by array position. Once a type opts in, every rendered requirement
needs a binding; a missing source or selector is an error, not an empty success.
The instance manifest owns its URL or file. Do not copy that target into the type.

`scripts/requirement_examples.py` resolves those bindings. It reuses the shared
open-dot and file/drawing routes; a page URL stays origin-relative. Child Job/Task
page bindings become selections inside their owning Block. An iframe reads its
target when opened; a generated HTML target is still a generated example, not a
claim that its source folders are read live. Simulated layouts must be identified
as proposals by their owning content, not presented as executed work.

`type_requirements.py` renders examples for standard type sources. A specialized
generator must call the same element reader, example renderer and Check builder.
Check criteria remain in `elements.md`, as specified by [check-view.md](check-view.md).

Validate missing selectors, missing files/fragments, external URLs and canonical
Block selection. Open the owning Block and inspect the matching requirement,
example and Check on desktop and phone. Generating an example is not verification
of its content.
