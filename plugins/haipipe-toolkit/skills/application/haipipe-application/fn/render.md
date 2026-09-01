# `render` · produce one unit as the recipient will see it

Renders live in the owning Folder's `delivery/render/` plugin lane, not in a
board-level folder. `page-type: artifact` and the `2-artifacts/` group are both
retired.

1. Resolve the owning D4 `folder-kind: design-division` Folder (or a legacy
   `page-type: design` Folder) and the requested unit division.
2. Require a pinned venue: the venue picks the extension and the cap, and a page with no venue cannot render.
3. Render through the plugin route into `<page>/delivery/render/<stem>-<unit>-v<N>.<ext>`, stamping the Design Page version, every promoted-principle record version it cites (often none), the bound handoff versions, and this render's own version in `manifest.json`.
4. Show the render with its character count against the venue cap.
5. Do NOT require an `accepted:` row. Acceptance names a render version, so the render must exist first; rendering is how a unit becomes reviewable. What requires acceptance is DISTRIBUTION, which is task-layer work and not this verb.
6. If a rendered file was hand-edited, reconcile it into the owning division before anything downstream uses it. That clears the division's `accepted:` row. Never re-render over an unreconciled edit: it silently deletes real feedback.

Return the render path, its three stamps, the character count against the cap, and whether the owning division carries an acceptance row.
