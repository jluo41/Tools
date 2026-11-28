---
title: Design uses the existing mindmap skill
date: 2026-11-27 11:56
topic: s01-design
aim: Replace custom SVG presentation with native folded mindmaps inside the owning Block; separate naming rules and actual examples.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1156_native_design_mindmaps.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
  what: Use existing mindmap renderer and validate content bindings
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/organization.mindmap.md
  what: Author native mindmap content with stable IDs
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/example.mindmap.md
  what: Author native mindmap content with stable IDs
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/studio.mindmap.md
  what: Author native mindmap content with stable IDs
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
  what: Bind native mindmaps and separate rules from examples
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
  what: Bind native mindmaps and separate rules from examples
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/organization.mindmap.md
  what: Author native mindmap content with stable IDs
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/example.mindmap.md
  what: Author native mindmap content with stable IDs
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/studio.mindmap.md
  what: Author native mindmap content with stable IDs
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
  what: Bind native mindmaps and separate rules from examples
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
  what: Bind native mindmaps and separate rules from examples
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record shared-mindmap correction and unresolved schedule
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/mindmap.html
  what: Thin in-frame redirect to the existing focus-map endpoint; no renderer or layout
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/mindmap.html
  what: Thin in-frame redirect to the existing focus-map endpoint; no renderer or layout
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1156_native_design_mindmaps.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/organization.mindmap.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/example.mindmap.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/studio.mindmap.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/organization.mindmap.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/example.mindmap.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/studio.mindmap.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/mindmap.html
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/mindmap.html
---

# Design uses the existing mindmap skill

## Prompts

- **11:56** Work coordinator relayed: reuse hai-mindmap mapview/mmmap through mindmap_module; default to owning Block, distinguish Structure naming rules from Examples, preserve folders and human edits; verify existing schedule rather than inventing one.
- User supplied a screenshot of raw mindmap Markdown and said: “你自己不解释拿你干啥东西吗？” Repair the actual current Block page, not just describe the missing runtime reload.

## Check

- All six native maps pass the skill grammar check. Existing focus_page.mindmap_document renders all six with fold controls and verified source files.
- Scoped git diff --check passes.
- Shared manifest routing and browser acceptance are pending the owning Work session. Schedule component remains unidentified; no speculative implementation.
- Automatic approval review rejected a supplemental message to Work, citing the coordinator no-incoming-reports instruction. No retry or alternate delivery was attempted.
- Shared native manifest integration is now on disk and the full Design checker passes.
- Browser opened the owning Design Block on 5623 and refreshed: iframe still routes through /_board/page and displays Markdown. The running service has not loaded the new binding; native fold/source-link acceptance remains pending. No restart performed by Design.
- Final acceptance: user in-app browser at Tailscale Design Block shows native folded graph, no raw root/node marks; type → Job → Task expansion works; Draw uses same map; Examples shows verified names and opens actual Job Markdown in the existing pop-out; Method Book ends at Job Name.
- Thin entry files redirect only their iframe to the existing focus-map endpoint; no custom map markup or styles. No shared process restart performed by Design.
- Final builder --check and scoped git diff --check pass.

## Summary

Reused the existing mindmap skill for both Design Studios, separated naming rules from real examples and verified the actual Block page. The raw-Markdown failure shown by the user was fixed with small in-frame native-route entry files, compatible with the running service. T11 is fixed. T12 (identifying the requested schedule component) remains open as a separate unresolved topic.

