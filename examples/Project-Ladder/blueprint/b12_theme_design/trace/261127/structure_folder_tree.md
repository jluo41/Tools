---
title: Design Structure as folder trees
date: '2026-11-27'
aim: Render every s01/s02 Structure model and embedded record tree as a shared expandable folder tree, retaining source navigation and Draw.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/structure_folder_tree.md
  what: Record confirmed scope, prompt, edits and actual-page acceptance.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/build_organization.py
  what: Reuse shared tree renderer and S71 colors for Structure; add regression checks.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-board.html
  what: Rebuild Design Board Structure content.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-methodbook.html
  what: Rebuild Method Book Structure content.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/CONSTITUTION.md
  what: Require folder trees for Structure, roles on hover and shared colors.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record requirement and validated outcome.
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/structure_folder_tree.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-board.html
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-methodbook.html
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
---

# Design Structure as folder trees

## Prompts

User: “现在是什么情况？要进行下一步了吗？然后你的这里的这个 的这block，S01，S02，你那个东西都要，那个 structure 都要变成 folder tree啊，不要用 mind map。”

The six-file plan was shown; the user then authorized execution: “你现在算已经修改好了吗？你现在开始去做任务吧。你别就是快快回复，你赶紧去干活啊，我操。”

## Findings

Folder already uses tree_html; Job/Task and Studio use organization_map. Structure and Draw share fragments, so separate mode bodies are needed to change Structure without changing the approved Draw binding. Shared S71 uses common hierarchy colors and hover explanations.

## Check

- b12 build_organization.py --check and workbench-design current_contract_check.py --structure pass. Structure content uses b17 tree_html; hierarchy colors are read from the shared S71 stylesheet, not a copied palette.
- Structure regression checks validate all three model trees, hover meanings, Job/Task parentage, four Board levels versus two Book levels, and every actual source URL. Negative mutations inserting a mind map, changing a level color or breaking a source URL are rejected.
- README fresh-context workbench-design invocation: PASS. Reviewer checked the final constitution, T21, S71 and generator, ran both guards and correctly distinguished Structure from Draw and Book versions from Tasks.
- Browser acceptance through the Tailscale b12 Block: both Folder trees show folders before files and expand through the Job. Both Job/Task trees and both Studio trees display as vertical folder trees. Expanded Board Job and Designs branches; checked all four computed colors and hover type names. Book stops at Job without an execution Task level.
- Expanded real example records. Book j02 opens DesignMethodBook-Example with Method / Steps / Versions / Used by in the existing preview. Board j01 opens Design-Example Main. The yes-first Task link opens t01 within Design-Example with the Task selector and Draft / Verify / Revise / State controls. No release action was submitted.
- Structure/Draw switching works. Browser left on b12 s01 Structure with its Job and Designs branch expanded. Actual source selection uses the owning Block URL and stays inside the preview.
- Hash comparison confirms manifests, type inventories and manual PNG/Excalidraw canvases unchanged. No shared code, registry or service was changed or restarted. Scoped diff whitespace check passes and all edited human-readable files are under 700 lines.

## Summary

The approved six-file folder-tree change is complete. Every s01/s02 Structure model and its expandable record outline uses the shared folder tree, with hierarchy colors, hover meanings and Block-owned source navigation. T21 is fixed with source checks and real-page acceptance. This does not close T20's inventory-generated type views or the distinct actual-Block Studio Band contract; the current Studio Band content is preserved in this presentation-only change.

## Verified entry

http://100.121.165.84:5623/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb12_theme_design&layout=focus&section=studio&group=Structure#s01-design

s02 is the Design Method Book fold on the same Block. Static HTML is embedded content, not the default entry.
