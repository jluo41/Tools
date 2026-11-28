---
title: Independent Labeling Blocks and inline previews
date: 2026-11-27 08:52
aim: Three independent Block entry pages with embedded Jobs and Tasks, shown interactively in the conversation; no Task or Studio topic is presented as a Block.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/0852_independent_labeling_blocks.md
  what: this trace's own record, written first
- do: edit
  path: PRINCIPLE.md
  what: Make Block the only independently addressable UI level
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: Record the Block-only navigation rule
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
  what: Record the correction and its remaining implementation limits
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/board.md
  what: Register three independent Block examples
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/page-spec/block-types-proposal.md
  what: Replace Studio-as-Block and Task-page preview assumptions
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_focus.py
  what: Read explicit synthetic Block previews at the Block route
- do: add
  path: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_block_preview.py
  what: Render one synthetic preview from its owning Block
- do: add
  path: plugins/haipipe-toolkit/servers/workbench-labeling/tests/test_block_preview.py
  what: Check root ownership and no child page routes
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/block-preview.css
  what: Keep Workbench styling within each embedded Block
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/block-preview.js
  what: Keep Job Task and review interactions inside the Block
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/build_blocks.py
  what: Build Block pages and inline previews from the same sources
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/check_blocks.py
  what: Guard Block identity and embedded navigation
- do: add
  path: examples/Project-Ladder/labeling/b03_itemization/board.md
  what: Own the independent Block and its handoffs
- do: add
  path: examples/Project-Ladder/labeling/b03_itemization/delivery/ui/model.json
  what: Own synthetic Job Task and result records
- do: add
  path: examples/Project-Ladder/labeling/b03_itemization/delivery/ui/block.html
  what: Show the Block with inline Job and Task content
- do: add
  path: examples/Project-Ladder/labeling/b04_guideline_generation/board.md
  what: Own the independent Block and its handoffs
- do: add
  path: examples/Project-Ladder/labeling/b04_guideline_generation/delivery/ui/model.json
  what: Own synthetic Job Task and result records
- do: add
  path: examples/Project-Ladder/labeling/b04_guideline_generation/delivery/ui/block.html
  what: Show the Block with inline Job and Task content
- do: add
  path: examples/Project-Ladder/labeling/b05_labeling_at_scale/board.md
  what: Own the independent Block and its handoffs
- do: add
  path: examples/Project-Ladder/labeling/b05_labeling_at_scale/delivery/ui/model.json
  what: Own synthetic Job Task and result records
- do: add
  path: examples/Project-Ladder/labeling/b05_labeling_at_scale/delivery/ui/block.html
  what: Show the Block with inline Job and Task content
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/delivery/ui/job-preview.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s11-itemization-job-preview/delivery/ui/job-preview.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.excalidraw
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s11-itemization-job-preview/s11-itemization-job-preview.excalidraw
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s11-itemization-job-preview/s11-itemization-job-preview.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.md
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s11-itemization-job-preview/s11-itemization-job-preview.md
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.mindmap.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s11-itemization-job-preview/s11-itemization-job-preview.mindmap.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.mindmap.md
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s11-itemization-job-preview/s11-itemization-job-preview.mindmap.md
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.png
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s11-itemization-job-preview/s11-itemization-job-preview.png
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/delivery/ui/job-preview.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s12-guideline-job-preview/delivery/ui/job-preview.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.excalidraw
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s12-guideline-job-preview/s12-guideline-job-preview.excalidraw
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s12-guideline-job-preview/s12-guideline-job-preview.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.md
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s12-guideline-job-preview/s12-guideline-job-preview.md
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.mindmap.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s12-guideline-job-preview/s12-guideline-job-preview.mindmap.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.mindmap.md
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s12-guideline-job-preview/s12-guideline-job-preview.mindmap.md
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.png
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s12-guideline-job-preview/s12-guideline-job-preview.png
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/delivery/ui/job-preview.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s14-scale-job-preview/delivery/ui/job-preview.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.excalidraw
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s14-scale-job-preview/s14-scale-job-preview.excalidraw
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s14-scale-job-preview/s14-scale-job-preview.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.md
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s14-scale-job-preview/s14-scale-job-preview.md
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.mindmap.html
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s14-scale-job-preview/s14-scale-job-preview.mindmap.html
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.mindmap.md
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s14-scale-job-preview/s14-scale-job-preview.mindmap.md
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.png
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/s14-scale-job-preview/s14-scale-job-preview.png
- do: add
  path: /Users/jluo41/.codex/visualizations/2026/11/08/01a1bc86-f992-7212-b27b-97d9d801690c/itemization-block.html
  what: Conversation response preview of one independent Block
- do: add
  path: /Users/jluo41/.codex/visualizations/2026/11/08/01a1bc86-f992-7212-b27b-97d9d801690c/guideline-generation-block.html
  what: Conversation response preview of one independent Block
- do: add
  path: /Users/jluo41/.codex/visualizations/2026/11/08/01a1bc86-f992-7212-b27b-97d9d801690c/labeling-at-scale-block.html
  what: Conversation response preview of one independent Block
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/block-template.html
  what: Literal shared fragment template for Block and conversation rendering
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/preview.css
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/preview.css
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/preview.js
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/preview.js
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/build_drawings.py
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/build_drawings.py
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/check_previews.py
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/check_previews.py
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/0852_independent_labeling_blocks.md
- PRINCIPLE.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/board.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/page-spec/block-types-proposal.md
- plugins/haipipe-toolkit/servers/workbench-labeling/labeling_focus.py
- plugins/haipipe-toolkit/servers/workbench-labeling/labeling_block_preview.py
- plugins/haipipe-toolkit/servers/workbench-labeling/tests/test_block_preview.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/block-preview.css
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/block-preview.js
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/build_blocks.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/check_blocks.py
- examples/Project-Ladder/labeling/b03_itemization/board.md
- examples/Project-Ladder/labeling/b03_itemization/delivery/ui/model.json
- examples/Project-Ladder/labeling/b03_itemization/delivery/ui/block.html
- examples/Project-Ladder/labeling/b04_guideline_generation/board.md
- examples/Project-Ladder/labeling/b04_guideline_generation/delivery/ui/model.json
- examples/Project-Ladder/labeling/b04_guideline_generation/delivery/ui/block.html
- examples/Project-Ladder/labeling/b05_labeling_at_scale/board.md
- examples/Project-Ladder/labeling/b05_labeling_at_scale/delivery/ui/model.json
- examples/Project-Ladder/labeling/b05_labeling_at_scale/delivery/ui/block.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/delivery/ui/job-preview.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.excalidraw
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.mindmap.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.mindmap.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s11-itemization-job-preview/s11-itemization-job-preview.png
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/delivery/ui/job-preview.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.excalidraw
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.mindmap.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.mindmap.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s12-guideline-job-preview/s12-guideline-job-preview.png
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/delivery/ui/job-preview.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.excalidraw
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.mindmap.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.mindmap.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/s14-scale-job-preview/s14-scale-job-preview.png
- /Users/jluo41/.codex/visualizations/2026/11/08/01a1bc86-f992-7212-b27b-97d9d801690c/itemization-block.html
- /Users/jluo41/.codex/visualizations/2026/11/08/01a1bc86-f992-7212-b27b-97d9d801690c/guideline-generation-block.html
- /Users/jluo41/.codex/visualizations/2026/11/08/01a1bc86-f992-7212-b27b-97d9d801690c/labeling-at-scale-block.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/block-template.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/preview.css
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/preview.js
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/build_drawings.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/history/261127-studio-prototypes/shared/check_previews.py
---

# Independent Labeling Blocks and inline previews

## Prompts

- **08:52** 你可以把这些生成的东西，就是说交互的东西变成，就是说嵌入到对话的 HTML 吗？这样的话我不用点开看了。然后我觉得我们最重要的一个 rule，就是你要写到 agents 或者 principal 里面。就是说我们只有一个 level，就是 block。然后呢，像 job呀，task呀，它们就没有自己独立的，就是说链接了，它们都内嵌到这个 block level 里面了，你懂我意思吗？所以你现在，我看你生成的，我点开之后生成的，就是说你把它变成了 T03。就我们现在就没有所谓的以 T开头的东西了，都是只有一个 block，明白吗？然后你这三个它也不是 S，就是它也不是说是，就是说我是想把它变成三个独立的 block，你懂我意思吗？你这做的都不对。

## Check

- Block structure guard passed: 3 independent Block owners; generated fragments match their own models; no anchors, child-page routes, iframe dependencies, navigation calls, title replacement or remaining active s11/s12/s14 directories.
- JavaScript syntax check passed. New reader tests: 6 passed. Existing Labeling focus regression suite: 15 passed and 14 subtests passed. All 3 real Block routes also rendered through labeling_focus.render.
- Tools-SPACE Workbench restarted through the normal wb restart command. The first sandbox attempt could not inspect processes; the approved escalation succeeded on the existing port 5623. No additional server was started.
- Chrome opened each real Block route. Itemization Job and Task selection kept title Itemization and the exact Block URL; there were 0 links. Main hid the Task row. Whole conversations showed its own recipe and accepted it in place.
- Chrome: Guideline judgments, generation, validation and confirmation remained inside the Guideline Generation Block. Confirmation was disabled before validation; changing a judgment invalidated validation; regenerating, validating and confirming produced the preview release without changing the Block URL or title.
- Chrome: an unqualified executor disabled Run all. A qualified Job marked only the pending batch running, retained the completed batch, and disabled repeat queueing. The page stayed Labeling at Scale at the Block URL.
- Visual and layout review: inspected Itemization desktop and Guideline at 736px. Guideline and Scale documents fitted 320px without horizontal overflow. Temporary viewport override was reset and the test tab closed. Browser console contained only unrelated Zotero extension connection messages; no preview-script errors were observed.
- Inline response copies: 3 self-contained fragments, each under 26 KB, exactly matching its Block fragment; no external resources or API calls. The host visualization renderer itself is presented in the final response; live browser checks used the same fragment in the Workbench wrapper.
- File audit: all 51 planned files exist; all moves have their original paths removed; authored current files remain under 700 lines; scoped git diff --check passed. Existing unrelated dirty work was preserved.
- Scope remains explicit: three synthetic design Blocks and an enduring Block-only UI rule. Production execution and global migration of legacy Job/Task readers are still open under T02 and UI A10.

## Summary

Corrected the earlier Studio-as-Block interpretation. Itemization, Guideline Generation and Labeling at Scale now have independent Block owners and live Block entry pages. Job, Task, review and delivery interactions remain embedded under each Block title, with no child navigation. Added the permanent rule to PRINCIPLE.md and UI constitution A10; updated the blueprint and topic record; archived the old Studio prototypes and their builders. The same sources generate the three inline conversation previews. Design-example checks pass; production worker integration and legacy-route migration remain explicitly open.

## Scope

The user corrected the previously authorized design pass. The three independent Blocks are synthetic design examples. The rule concerns UI addressability; Job and Task remain internal work records. No production worker, migration of legacy work or blanket removal of stored Job/Task data is part of this correction. Existing dirty files are changed only at the named integration points. This Trace records the first available time for this correction.
