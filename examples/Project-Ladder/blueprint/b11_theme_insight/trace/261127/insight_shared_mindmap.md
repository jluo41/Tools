---
title: Insight uses the existing mindmap inside its Work Block
date: '2026-11-27'
aim: Use hai-mindmap unchanged and default to the owning Work Block instead of
  standalone preview files.
closed: false
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_shared_mindmap.md
  what: requests, plan, validation and acceptance
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: reuse hai-mindmap and its grammar
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.js
  what: remove private drawing and zoom
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css
  what: shared map container and theme colors only
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
  what: shared-renderer and source guards
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
  what: generated shared Board map
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
  what: generated shared Book map
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
  what: generated shared Prep map
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
  what: canonical shared mindmap source
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
  what: canonical shared mindmap source
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
  what: canonical shared mindmap source
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md
  what: default owning Block entry and shared renderer door
- do: add
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/CONSTITUTION.md
  what: record shared implementation and Block entry rules
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
  what: replace private map presentation rule
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
  what: record correction and regression guard
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_shared_mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.js
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
---

# Shared mind map and owning Block

## Prompts

User, verbatim:

> 为什么不在 block里面打开？你每一次都要记住默认打开自己的对应的 work的这个 block。

> 然后这个也睡得不好，你为啥不用我们现有的这个mind map跟 schedule来设计呢？你为什么要设计一个自己新的呢？我操。 记得我们是有 mind map skill的呀。

The attached screenshot shows the private map's very small labels and clipped branches.
The file plan was shown before edits, within the authorized structure revision. Read the
explicitly named hai-mindmap skill, grammar and existing renderer before implementing.

## Design

Remove local map layout and scaling. Use the existing shared map renderer with default folds,
normal-size labels and native open/close controls. Preserve full paths and reference membership.
The .mindmap.md file uses the shared grammar and stable generated IDs; preserve authored edits.
Default user entry is the b11 Work Block Studio, with the actual map embedded inside it.
No separately identified Schedule component was found in the relevant map/Studio code; this
change introduces no new timeline or scheduling implementation.

## Check

- Scoped `check_structure.py` passes: canonical grammar, existing renderer, default folds,
  generated identities/parents, pinned questions, retained references and fresh output.
- `node --check delivery/structure/structure.js` and scoped `git diff --check` pass.
- Fresh-context skill validation found the initial guard rejected authored branches. The
  corrected guard preserves authored words, notes, children and grandchildren, and still
  rejects missing generated nodes or changed source ownership. The validator repeated
  both positive and negative cases successfully without editing repository content.
- Real in-app browser: opened the b11 Work Block, selected s01/s02/s03 Job / Task
  Organization, expanded Job Type -> Job -> Task Type -> Task and used Close all. The
  Block title and route remained b11. Source chips point to the original files. Book v2
  explicitly shows the retained v1 source in a question's detail. DataPrep Draw uses the
  same map and contains only the actual preparation-step ownership.
- Desktop screenshot: closed root and type fit, labels are 14px, transform is none.
  The private scale-to-fit code is gone. At 390 x 844 the map remains readable but its
  horizontal content needs panning; even the closed root and type do not fit together.
  Recorded as remaining shared-layout work, not a mobile acceptance pass. Viewport reset.
- Final browser tab is the owning b11 Block, marked as a deliverable. The static HTML is
  embedded content, never the default delivery link. No shared server was restarted.

## Remaining

Schedule was not identified in the relevant map/Studio/Workbench code. The matches named
schedule were chat polling and autosave functions. An asynchronous question asks the user
for the existing component's name or entry. Do not substitute a new timeline/Gantt.
The narrow-screen shared layout also remains open; changes belong to its shared owner.
No outbound report was sent to the coordinating session, per its latest instruction.

## Summary

Shared mindmap reuse and owning-Block entry are implemented and checked. Schedule identification
and narrow-screen shared-layout work remain open. No shared server, example source folder,
actual storage hierarchy or authored canvas was changed.

## Requirement clarification · 2026-11-27

The user clarified through Work coordination that Schedule was a misunderstanding and is not part of this task. No Schedule lookup or implementation is owed. The source record above is retained as written. The shared phone-layout issue remains open; readable font size and source ownership must be preserved. Current Studio alignment is tracked in insight_studio_bands.md.

## Phone acceptance in the Studio alignment batch

From the owning b11 Block, native rule/example expansion passes on desktop. At 390 × 844, horizontal nodes remain clipped by the shared container while text stays at normal size. The viewport override was reset. T36 remains open. Full source and browser evidence: [Studio alignment](insight_studio_bands.md).
