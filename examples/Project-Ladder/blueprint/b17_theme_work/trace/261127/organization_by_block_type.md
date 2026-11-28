---
title: Organization follows the Block type
date: 2026-11-27
work:
- s01
- s02
- s03
- s04
closed: true
plan:
- path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/studio-views.json
  what: Route Structure/Draw to rules and Examples to preserved instance content.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/studio-views.json
  what: Route Structure/Draw to rules and Examples to preserved instance content.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/studio-views.json
  what: Route Structure/Draw to rules and Examples to preserved instance content.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
  what: Route Structure/Draw to rules and Examples to preserved instance content.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/s01-work-ladder.md
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/s02-work-skills.md
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/s03-q01-work-ladder.md
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: Align organization with Block type while preserving Folder.
  do: edit
- path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/organization_by_block_type.md
  what: Align organization with Block type while preserving Folder.
  do: edit
aim: Keep type-specific structure rules separate from source examples; preserve historical decisions.
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/s01-work-ladder.md
- examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/s02-work-skills.md
- examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/s03-q01-work-ladder.md
- examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/organization_by_block_type.md
---

## Requests

> For this, the topic type should be attached to the block type. Like for the blueprint work block, we should have block structure and the block UI, do you get it?

> The job topic and job name should be relevant to the block type as well! If it is general, then use the place holder of example 1 example 2

> Go ahead and make the plan and then update them

## Plan

Work uses Example 1 / Example 2 where no topic meaning is established. Blueprint shows structure, UI and skills work, with Block Structure and Block UI Studio types. CoWork uses requests, approvals and coordination; Discovery uses inquiry and evidence. These are illustrative organization patterns, not new canonical types or folders. Role labels distinguish a Job topic from a Job and a Task topic from a Task. Studio shows relevant topic types, never ownership levels. Keep the existing Folder inventory and shared renderer. Update faces, guard and topic record together.

## Folder section hashes before this change

```json
{
  "work": "633070064745239cb769b343732e34d94f7cfc0eb5e9b69d5dfa3ff9e1382498",
  "blueprint": "c3172b148e89f8ee5bd17169f41bee9ba246b547c464511dc1dcafab3aeffe59",
  "cowork": "97226a95ab4b4b61076014798fea5977b98ac178e6cbc89fcbf443ad2fc4225b",
  "discovery": "b1855a170a6c8dd21c30958ba27146a190deba883f6da2da2e1a984d0f4ffd19"
}
```

## Check

- `check_organization.py` passed. It checks type-specific roots and names, Blueprint’s exact Studio types, generic Example placeholders, removal of the ownership diagram, actual folder paths and unchanged Folder section hashes.
- Scoped `git diff --check` passed.
- Actual browser: Work Job organization shows Example 1 / Example 2 with role labels; Blueprint shows relevant structure/UI/skills Job names; CoWork shows request/approval/coordination Jobs; Discovery shows inquiry groups and evidence questions.
- Actual browser: Blueprint Studio Organization and Draw show Blueprint Work Block → Block Structure / Block UI. The final browser screenshot shows this diagram inside S02.
- Content reviewer `review_structure_content` found no material mismatch and confirmed the guard passes.
- No work directories, shared rendering code, or S11–S13 UI previews were changed.

## Result

The organization models now follow the Block type. Named organizations are examples rather than newly registered Job or Task types. Where meaning is unspecified, Work uses Example 1 / Example 2. Existing Folder content is byte-identical to the sections captured before this change.


## Explicit kinds and names correction

User: “每一个 block，之所以跟其他 block 不一样……job 种类是什么、job 的 name 是什么、task 的种类是什么、task name 是什么……重新更新 plan，然后执行。”

Plan: update the listed builder, guard, four generated files, four faces and topic record. Preserve Folder. Show meaningful Job Type / Job Name / Task Type / Task Name with names bound to existing records. Responsibility categories are design classifications, not new machine schema values. Record the CoWork contract/example discrepancy. This supersedes the generic placeholder plan.

## Verification of explicit kinds and names

- check_organization.py passed: four distinct models, four columns, source record existence and parentage, synchronized Draw, no placeholder names, existing Discovery manifest types, and unchanged Folder hashes.
- Chrome reloaded the actual b17 page on Tailscale port 5623. All four embedded Job / Task Organization tables displayed Job Type / Job Name / Task Type / Task Name. Verified Work Draw shows the corresponding typed tree.
- Job and Task names link to their source records. Responsibility categories are the structural design proposal, not silently added machine fields. CoWork contract/example mismatch remains explicitly shown; no contract was changed.
- Latest user correction and execution request sent to Paper, Labeling, Insight and Design. Design reported its revised definitions and browser acceptance complete; other outcomes not claimed here.

Concurrent-source note: Paper added content to its source tree during validation. The preserved Folder section stayed byte-identical; organization output stayed identical to regeneration. The guard now compares reproducibility outside Folder and keeps the independent Folder hash/path checks, rather than requiring unrelated source inventory to stop changing.

## Mind map correction

User: “不是，我意思是做一个mind map一样的炊，你懂吗。” The four columns are levels of one left-to-right branching tree, not a table or four selection lists. Plan: replace the organization renderer in build_organization.py, update check_organization.py, regenerate the four organization HTML files while preserving Folder verbatim, and update the topic record and this Trace. Keep names, sources and relationships. Add width-fit and actual-size viewing controls.

### Mind map verification

- The four HTML outputs now use the same horizontal node-and-branch renderer in Structure and Draw. Parents are grouped once; Jobs without Tasks terminate at the Job node. Source links and meaningful names are retained.
- check_organization.py passed, including exact node/edge counts, four level headings, no table markup, fit/actual-size controls, source parentage and unchanged Folder hashes.
- Chrome verified the actual Work Studio iframe in Structure and Draw through Tailscale :5623. Actual-size enlarged readable nodes; fit-to-width showed all four levels at a 390 × 844 phone viewport. The temporary viewport override was reset.
- No server restart or shared server modification was needed. The remaining schema/contract discrepancies documented above were not changed by this presentation fix.


### Reusable renderer follow-up

Paper requested reuse for its own four-level trees. Plan: expose optional tree/source input and a standalone HTML wrapper in the existing builder, export the same zoom script, extend the existing guard, and record the interface in the topic. Existing generated HTML must stay byte-identical; no Paper content or shared server edits. This continues the authorized cross-theme visualization work.

Completed: organization_map(kind=None, *, tree=None, sources=None), organization_document(title, *, tree, sources=None) and MAP_SCRIPT are available. Full ancestry source keys disambiguate names reused across types. External-tree guard passes, including escaped text, no-Task branches, source links and invalid/deeper inputs. Existing output reproducibility and Folder preservation guards pass. No generated HTML was rewritten by this extraction; the browser-verified documents remain unchanged.


## Readable concrete examples

User: “你能不能把structure给我先给出来一些example出来？你现在做啥东西啊，我看都看不懂，看不清楚，不simple，太complicated了。你就不能就直接把那东西弄好吗？我操。”
Plan: in the existing builder, show one concrete Job example at a time with a named selector. Keep full type/name branches and sources. Narrow embedded views use a readable unscaled branching tree; wide views keep the horizontal map. Update the guard, four HTML files, topic and this Trace. Preserve Folder sections exactly and preserve the reusable map API for other themes.

Presentation refinement before acceptance: retain the requested horizontal four-level map on every viewport. Simplify through one named Job example at a time, larger 17px node text and actual-size default with scrolling; fit remains optional. Do not introduce a vertical-tree substitute. Source/contract notes move to the example selector hover.


## Simplify Structure reading

User: “你的structure就不能做简单一些吗？哎呀，我他妈看着我真的烦死了。”

Plan: continue within the listed builder, guard, four generated HTML files, topic record and this Trace. Show one named Job example and its horizontal four-level diagram, with readable text and optional fit. Remove the mobile substitute tree, repeated content headings, Studio role badges and explanatory paragraphs. Studio topics appear directly, with explanations on hover. Keep source/contract caveats in the example selector hover. Structure and Draw use the same content. Preserve Folder sections byte-for-byte. Retain the reusable map API.

Final readable-example result: one named Job selected at a time; 576px horizontal drawing with 132px nodes, 15px normal-word-wrapped text and minimum scale .9. Detailed notes remain in hover. CoWork starts with its Task-bearing example. Integrated concurrent owner changes: no Jobs repeated heading; Studio topic list with explanations on hover. Chrome checked actual Work Structure and switching First command line to First docs; guard checks source links, visibility, all options, scale floor and unchanged Folder. No contract or real source directory changes.


## Structure rules versus concrete examples · in progress

User: “那你想想怎么就是把这个东西表达得更清楚一些。 就是说要么就是说你有两个，一个是指example，另外一个version，就是有的时候我们这个block就是说它的job name就是说是 至于当下的具体的任务 的，有的时候它的job name或job group name它是固定的。我想说你怎么就是区分它们？”

User: “要不然你再重新再更新一下。”

User: “为什么我发现你的这个 Trace 没有更新啊？”

Cause: this follow-up began with contract reads before recording the request and plan. The previous Trace was still closed. Reopened it before implementation; prior results above remain historical.

Plan: separate the structure rule from a concrete Block instance. Structure/Draw show contract-backed fixed names and angle-bracket slots for names chosen for the current task. Examples retain the actual folder inventory, source-linked Job/Task diagrams and live Block entry. Fixed and variable naming is decided per level, not once for the whole Block. A sample name does not establish a rule. No source directory migration or topic folders.

Files: existing delivery/structure/build_organization.py and check_organization.py; four generated work/blueprint/cowork/discovery-organization.html; s01-work-ladder, s02-work-skills, s03-q01-work-ladder and s04-workbench-page-structure studio-views.json; existing workbench-work/ref/topics.md; this Trace.

Read so far: PRINCIPLE.md; hai-work, hai-cowork and hai-discovery skills. CoWork explicitly fixes j00_people and forbids a Task folder; the existing sample contains a Task, which must remain identified as a sample/contract discrepancy. Work Job names follow the agreed execution work, not the CSV demonstration roster.

Outstanding: complete grouping-contract reads; implement rule/example routing; update guard; verify live Structure and Examples and source destinations; then close this Trace. No page changes for this follow-up have been applied at the time of this entry.

Registered follow-up: `1150_structure_rules_and_examples.md`. This historical filename is not discovered by the Files Trace scanner; the registered trace carries the current plan, changes, checks and result.

## Summary

Historical organization work and follow-ups are preserved above. The current rule/example separation and its verification are registered in 1150_structure_rules_and_examples.md, which the Trace UI discovers. No source folders were moved.
