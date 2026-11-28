---
title: Studio Type examples and element checks
date: 2026-11-27
topic: s72-studio-type-block-job-ui-preview
aim: Connect right-content requirements to examples and element-scoped Check.
closed: true
plan:
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/requirement_examples.py
  what: "NEW: resolve instance manifest examples, validate sources and keep Job/Task selection in its Block; reuse preview components."
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
  what: "Attach examples to corresponding requirements, without changing types that have no example bindings."
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/check_views.py
  what: "Add an opt-in Top / Left element layout; retain every criterion, method and source without claiming execution."
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_requirement_examples.py
  what: "NEW: source binding, missing examples, invalid paths and canonical Block navigation tests."
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_check_views.py
  what: "Cover criteria completeness, element navigation and no fabricated pass results."
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/check-view.md
  what: "Document element-scoped criteria, verification methods and evidence boundaries."
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/type-examples.md
  what: "NEW: document inline example bindings and distinguish examples from implemented behavior."
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: "Extend A06 with examples beside requirements and element-scoped Check."
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: "Link the example and Check contracts so fresh sessions can discover them."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: "Make Structure / Studio Folder Tree requirement explicit; retain other requirements."
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/examples.json
  what: "NEW: map Top / Left requirements to existing S01 content."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
  what: "Use element-scoped Check while retaining content views."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/draw.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--example-1.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--folder.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--job-task.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--studio.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-group-type-1.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-group-type-2.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-type-1.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-type-2.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/skills.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--folder.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--job-task.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--studio.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-group-type-1.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-group-type-2.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-type-1.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-type-2.html
  what: "Regenerate requirement and its expandable example from source bindings."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/check.html
  what: "Regenerate element-scoped criteria."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/elements.md
  what: "Normalize to shared Top / Left / must syntax; retain requirements and add specific verification methods."
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/examples.json
  what: "NEW: map Top / Left requirements to existing S11 content."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
  what: "Reuse shared criteria, example and Check readers; add type-only generation to avoid rewriting S11-S14."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/studio-views.json
  what: "Add final Check view while retaining existing content views."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/delivery.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/draw.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-findings.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-group-type.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-overview.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-rows.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-tasks.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-type.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/quickhtml.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-findings.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-group-type.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-overview.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-rows.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-runs.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-type.html
  what: "Regenerate this element requirement with its corresponding expandable example."
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/check.html
  what: "NEW: generate S72 element-scoped criteria from its source requirements."
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: "Record exact request, findings, implementation, guards and remaining gaps."
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1900_type_examples_check.md
  what: "NEW: record approved file plan before edits; then checks, browser evidence and remaining gaps."
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/delivery/check.html
  what: Refresh inherited S71 criteria under the prior approved Check-pilot file scope.
changed:
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/requirement_examples.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/check_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_requirement_examples.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_check_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/check-view.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/type-examples.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/examples.json
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/draw.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--example-1.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--folder.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--job-task.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--studio.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-group-type-1.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-group-type-2.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-type-1.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/job-types--job-type-2.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/skills.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--folder.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--job-task.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--studio.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-group-type-1.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-group-type-2.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-type-1.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/task-types--task-type-2.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/check.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/examples.json
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/delivery.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/draw.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-findings.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-group-type.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-overview.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-rows.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-tasks.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/job-type.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/quickhtml.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-findings.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-group-type.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-overview.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-rows.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-runs.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/task-type.html
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/check.html
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1900_type_examples_check.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/delivery/check.html
---

# Studio Type examples and element checks

## Prompts

The user requested examples alongside right-content requirements and Check organized by Top / Left / Right. The exact file plan was approved before edits.

- “你像这些 Studio Type，S7，S7二，就是我们要加 Check，能不能也加一些，比如说那个 Example。你比如说我每次都是上边是上，对吧，Top，然后 left，right，right 现在是我们的 right 的一些路。那能不能把一些 right 的一些，比如说 Example 也列一下。然后再就是 Check。我觉得这个 Check 的话，你也可以用这种模式，Top，Left，Right，然后说一定要 Check 什么什么什么。嗯。但这东西，比如说我的 Mars 里面写都有啊，你这都是睁不开你的狗眼啊。”
- “现在是下步干嘛，为啥这么多人给你发消息啊？你不要看那个别人给你发的消息了，你先focus在你自己的任务上。”
- “你现在要做啥？你赶紧想想plan,然后去执行好吧。”
- File-plan approval: “好，赶紧吧，去干吧，赶紧干吧，我同意了。”

The S01 inherited Check refresh uses the earlier approved Check-pilot file scope;
its additional path was recorded in this plan before the refresh. No S01 layout,
actual Folder tree, canvas or other instance manifest was rewritten.

## Check

- Twenty tests pass: eight example-binding tests, eight Check-view tests and four existing Skills-view tests.
- Both S71 type_requirements --check and S72 build_type_pages --type-only --check pass.
- check_views --check passes on S71, S72 and S01 after the inherited source refresh.
- Fresh-context skill review started from SKILL.md, discovered both new references, and independently exercised
  named bindings, canonical child-to-Block selection, parent/child criteria and unverified marks in temp fixtures.
  It caught a full-Block example bound to Folder; that selector was corrected to Example 1 and a regression test added.
- Actual Tailscale b17 Block: S71 Structure/Studio opens the corresponding collapsible Work Studio tree;
  S72 Page-Job/job-overview expands the live example, and its Requirements control changes the shown content.
  Clicking its open dot opens the same Block and Job in a full tab. S72 Page-Task/task-runs loads the example Block
  with group=j11 and task=t02. Check/Task Runs contains both Page-Task criteria and its own Run criterion;
  Verify opens the method and the correct elements.md source link.
- At 390px, the right-content Task Runs page measures clientWidth=390 and scrollWidth=390, with a 64px label column;
  its screenshot shows readable wrapping. The browser viewport override was reset after inspection.
- The broader check_organization.py still fails its historical work Folder hash at line 194. This batch did not
  change the actual Folder output or suppress that assertion; this is not reported as a pass.

## Summary

S71 and S72 show an expandable Example beside every rendered requirement. Shared bindings read existing instance
manifests and use the existing file/drawing/open-dot components. S72 now reads the shared Markdown syntax.
Check's element layout names Top / Left and preserves its parent-view requirements. Skill references and the
Constitution explain the same workflow. No shared server file was changed and no service was restarted.

This closes the example/Check presentation work, not full acceptance of every source example. In particular,
S01 Studio Band emoji/number completeness and the historical Folder-hash failure remain open. Generated source
examples are not called live filesystem readers; no automatic result receipt or fabricated passing mark was added.


## Correction: remove the separate Examples top view

The user pointed to S71 Examples and confirmed it was already supposed to be removed.
This corrects the completed implementation within the approved source/generated-file scope.
Keep examples beside their own right-content requirements; remove the separate top view and its Check entries.

Files before edits:
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md`: synchronize source, generation, guard or correction record
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/examples.json`: synchronize source, generation, guard or correction record
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json`: synchronize source, generation, guard or correction record
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/check.html`: synchronize source, generation, guard or correction record
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--example-1.html`: remove obsolete generated requirement page
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--folder.html`: remove obsolete generated requirement page
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--job-task.html`: remove obsolete generated requirement page
- `examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/examples--studio.html`: remove obsolete generated requirement page
- `plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_requirement_examples.py`: synchronize source, generation, guard or correction record
- `plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/type-examples.md`: synchronize source, generation, guard or correction record
- `plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md`: synchronize source, generation, guard or correction record
- `plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md`: synchronize source, generation, guard or correction record
- `examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/delivery/check.html`: synchronize source, generation, guard or correction record
- `examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1900_type_examples_check.md`: synchronize source, generation, guard or correction record

User correction: remove the standalone S71 Examples top view; keep inline examples only.

Correction validation: 8 tests pass, type generation freshness passes, and independent fresh-context skill
validation confirms the rule. The actual refreshed Block shows Structure / Job types / Task types / Draw / Skills / Check
with no Examples top view; the Folder requirement retains its inline Example fold. S01 inherited Check and its
managed manifest were refreshed under the prior Check-pilot approval. No server restart.
