# `render` · produce one unit as the recipient will see it

Renders live in the owning Folder's `delivery/render/` plugin lane, not in a
board-level folder. `page-type: artifact` and the `2-artifacts/` group are both
retired.

1. Resolve the owning `folder-kind: design` Folder and exact current DU
   Result/member hashes. Reject design-division, `page-type: design`, and old
   thread records.
2. Require a pinned venue: the venue picks the extension and the cap, and a page with no venue cannot render.
3. Render through the plugin route into `<page>/delivery/render/<stem>-<unit>-v<N>.<ext>`, stamping the DU/member hashes, Design Page version, every promoted-principle record version it cites (often none), the bound handoff versions, and this render's own version in `manifest.json`.
4. Show the render with its character count against the venue cap.
5. Do NOT require an adoption receipt before rendering. Adoption names a render
   version, so the preview must exist first. Distribution requires a downstream
   Task handoff; it is not authorized by rendering or by adoption alone.
6. If a rendered file was hand-edited, preserve it and return that feedback to
   the caller for a new generation Run. Never overwrite an immutable DU or
   re-render over the edit. Mark only the affected current adoption stale;
   retain the original person's decision and source versions.

Return the render path, exact source/version stamps, applicable venue checks,
and whether a current human adoption binds this preview and DU/member version.
Only the current native adoption receipt is valid.
