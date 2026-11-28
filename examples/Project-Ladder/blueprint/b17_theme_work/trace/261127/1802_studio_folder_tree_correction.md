---
title: Studio Structure uses Folder Tree
date: 2026-11-27 18:02
topic: s01-work-ladder
aim: Structure Studio displays the approved Bands and topic slots as a collapsible Folder Tree.
closed: false
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1802_studio_folder_tree_correction.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: Use existing Folder Tree for Studio bands and topic slots
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_studio_bands.py
  what: Reject mindmap Structure bindings and require semantic tree
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: Check Band tree content
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands-by-block-type.md
  what: Define Folder Tree presentation
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: Record correction and real acceptance
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
  what: Bind Structure Studio to folder tree; keep original Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/s01-work-ladder.md
  what: Link to Studio tree and clarify presentation
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
  what: Regenerate Studio rule tree; preserve actual Folder section
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/studio-views.json
  what: Bind Structure Studio to folder tree; keep original Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/s02-work-skills.md
  what: Link to Studio tree and clarify presentation
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
  what: Regenerate Studio rule tree; preserve actual Folder section
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/studio-views.json
  what: Bind Structure Studio to folder tree; keep original Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/s03-q01-work-ladder.md
  what: Link to Studio tree and clarify presentation
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
  what: Regenerate Studio rule tree; preserve actual Folder section
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/studio-views.json
  what: Bind Structure Studio to folder tree; keep original Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
  what: Link to Studio tree and clarify presentation
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
  what: Regenerate Studio rule tree; preserve actual Folder section
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1802_studio_folder_tree_correction.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_studio_bands.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands-by-block-type.md
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/s01-work-ladder.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/s02-work-skills.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/s03-q01-work-ladder.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
---

# Studio Structure uses Folder Tree

## Prompts

- **18:02** 你给我解释一下为什么我们的S01里面那个 Studio Structure它还是 Mind Map啊？它不是我不是说一直要用那个 Folder Tree吗？你给我解释清楚，到底是什么原因。
- 用户追问：“那为什么我们的S71并没有说把东西弄清楚？你为什么没有符合我们S71的要求呢？我一定要把这问题弄清楚。你搁这儿，妈的，你浪费我的时间，浪费我的token，赔钱。”

## Check

- check_studio_bands.py passes for S01–S04; a negative probe restoring the wrong mindmap binding is rejected.
- Browser opened the actual Block, selected S01 Structure → Studio, expanded Work Design and saw its two topic slots in a Folder Tree. At 390 × 844 the screenshot shows the expanded tree inside the content frame, with readable wrapped names.
- Four actual Folder sections match the pre-correction baseline byte for byte.
- Broader check_organization.py reaches its retained Folder hash check and fails on work. The current Folder was already different from that historical hash before this correction; no assertion was removed and no reference hash was rewritten. Its fixed Band count was replaced with registry-based presence.
- S71 elements.md lines 25–49: Job-Task explicitly requires Folder Tree; Studio does not repeat that requirement and requires emoji/name/numbers. The delivered tree does not yet satisfy the latter completely. Do not claim complete S71 conformity.
- The prior custom guard incorrectly required mindmap binding. This guard now rejects it; full S71 acceptance remains open.

## Summary

Corrected the S01–S04 Structure Studio representation using the existing Folder Tree; preserved Band content, actual Folder sections and original Draw canvases. S01 desktop expansion and phone-width appearance were personally verified. Overall S71 conformance remains open for explicit Studio tree requirements and Band emoji/number definitions; the historical Folder-hash discrepancy is recorded, not hidden.

