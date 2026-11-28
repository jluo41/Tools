---
title: Paper structure from existing examples
date: 2026-11-27 11:59
topic: s03-paper-block-structure
aim: Replace abstract speculative branches with source-grounded Paper work and the existing shared folded mind map.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1159_paper_examples_structure.md
  what: this trace's own record, written first
  outcome: done
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/build_organization_maps.py
  what: Render authored mind maps with the existing shared Workbench component.
  outcome: done
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py
  what: Guard source-backed names, Story boundaries, folded maps and shared bindings.
  outcome: done
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/jobs.mindmap.md
  what: Author the type/name hierarchy in the existing mind-map grammar.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/jobs.html
  what: Rebuild the embedded preview through the existing shared mind-map renderer.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/organization.json
  what: Retain the previous proposal and mark its replacement source.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/jobs.mindmap.md
  what: Author the type/name hierarchy in the existing mind-map grammar.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/jobs.html
  what: Rebuild the embedded preview through the existing shared mind-map renderer.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/organization.json
  what: Retain the previous proposal and mark its replacement source.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.mindmap.md
  what: Author the type/name hierarchy in the existing mind-map grammar.
  outcome: done
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.html
  what: Rebuild the embedded preview through the existing shared mind-map renderer.
  outcome: done
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/organization.json
  what: Retain the previous proposal and mark its replacement source.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.md
  what: Replace invented Story Tasks with evidence-based boundaries and name rules.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.md
  what: Describe the revised design and retain prior decisions.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.mindmap.md
  what: Link the current organization; retire the duplicated speculative tree.
  outcome: cancelled by user scope reduction
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/studio-views.json
  what: Add the two inspected Paper maps to Examples and a source reference to Skills.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/examples/sources.json
  what: Record exact source fields and hashes, using SPACE-relative paths.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/examples/sources.md
  what: Explain what the existing examples establish and what migration still needs.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/examples/scaling-glucose.mindmap.md
  what: Show the inspected Writing, Display, Value and Citation Jobs with actual Tasks.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/examples/scaling-glucose.html
  what: Render the example using the same shared folded mind map.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/examples/anchor-pk.mindmap.md
  what: Show the inspected Writing, Display, Value and Citation Jobs with actual Tasks.
  outcome: cancelled by user scope reduction
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/examples/anchor-pk.html
  what: Render the example using the same shared folded mind map.
  outcome: cancelled by user scope reduction
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/CONSTITUTION.md
  what: Require the existing renderer and keep content sections distinct from Tasks.
  outcome: cancelled by user scope reduction
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md
  what: Record the user complaint verbatim, findings, verification and remaining work.
  outcome: cancelled by user scope reduction
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/SKILL.md
  what: Route structure interpretation to the revised map and inspected examples.
  outcome: cancelled by user scope reduction
changed:
- examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1159_paper_examples_structure.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.mindmap.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.html
- examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/build_organization_maps.py
- examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py
---

# Paper structure from existing examples

## Prompts

- **11:59** 我觉得这也是一个不好。你能不能看一看，就比如说我们现在的这些paper的example，然后再想想这些东西该怎么去设计
- User correction: “你能别搞这么复杂吗？我就要一个简简单单的mind map。你能做那么长时间干嘛？”

## Check

- Paper map guard passed. Existing Workbench mindmap renderer used without custom layout.
- In-app browser: b16 → Studio → s03 opened the five folded branches. Open all revealed manuscript sections and nested Review/Submission; Close all restored the simple overview.
- No shared server restart. Manifest remains on jobs.html because the running process has not loaded native .mindmap binding yet; HTML is rendered by the existing shared component.

## Summary

User narrowed the task to a simple map. Replaced only the Paper primary map, retained five named groups, removed Unresolved type boxes and invented Story Tasks, and protected rebuilding with the shared renderer and a focused guard. The broader example inventory and three-Studio redesign were cancelled, not completed. Idea/Grant and research folders remain untouched. Prior organization.json and design documentation are historical proposals; runtime migration remains outside this change.

## Basis

The prior human instruction to revise each theme plan and execute remains the authorization. The exact file list was shown before these edits. Source research folders are read only. The latest shared direction retires custom SVG layouts in favor of hai-mindmap; no shared server or b17 files are in this plan.
