# `render` · produce one unit as the recipient will see it

Renders live in the owning Folder's `delivery/render/` plugin lane, not in a
board-level folder. `page-type: artifact` and the `2-artifacts/` group are both
retired.

1. Resolve the owning `folder-kind: design` Folder and exact DU Result/member
   hashes. Legacy design-division/page-type: design records remain readable.
2. Require a pinned venue: the venue picks the extension and the cap, and a page with no venue cannot render.
3. Render through the plugin route into `<page>/delivery/render/<stem>-<unit>-v<N>.<ext>`, stamping the DU/member hashes, Design Page version, every promoted-principle record version it cites (often none), the bound handoff versions, and this render's own version in `manifest.json`.
4. Show the render with its character count against the venue cap.
5. Do NOT require an `accepted:` row. Acceptance names a render version, so the render must exist first; rendering is how a unit becomes reviewable. What requires acceptance is DISTRIBUTION, which is task-layer work and not this verb.
6. If a rendered file was hand-edited, preserve it and return that feedback to
   the caller for a new generation Run. Never overwrite an immutable DU or
   re-render over the edit. Mark only the affected current adoption stale;
   retain the original person's decision and source versions.

Return the render path, exact source/version stamps, applicable venue checks,
and whether a current human adoption binds this preview and DU/member version.
Historical acceptance rows remain readable; new work uses the native receipt.
