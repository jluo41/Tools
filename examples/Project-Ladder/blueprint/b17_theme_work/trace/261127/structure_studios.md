---
title: General Block structure Studios
date: 2026-11-27
work: [s01, s02, s03, s04]
aim: Replace b17's four structure topics with generic Jobs and Tasks, Studio, and embedded Skills views.
closed: true
plan:
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/s01-work-ladder.md
    what: 更新为对应 Block Structure，保留历史入口
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
    what: 定义 Structure、Draw、Examples、Skills 顶部视图
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/result/structure-replaced-261127.md
    what: 原主题正文的完整备份
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/s02-work-skills.md
    what: 更新为对应 Block Structure，保留历史入口
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/studio-views.json
    what: 定义 Structure、Draw、Examples、Skills 顶部视图
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/result/structure-replaced-261127.md
    what: 原主题正文的完整备份
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/s03-q01-work-ladder.md
    what: 更新为对应 Block Structure，保留历史入口
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/studio-views.json
    what: 定义 Structure、Draw、Examples、Skills 顶部视图
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/result/structure-replaced-261127.md
    what: 原主题正文的完整备份
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
    what: 更新为对应 Block Structure，保留历史入口
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/studio-views.json
    what: 定义 Structure、Draw、Examples、Skills 顶部视图
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/result/structure-replaced-261127.md
    what: 原主题正文的完整备份
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/jobs.html
    what: 通用 Job topic → Job → Task topic → Task 图
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/studio.html
    what: 普通 Block 的通用 Studio 组织图
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/theme-studio.html
    what: Theme Block 的结构/UI/Guide Studio 组织图
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
    what: 同步 s01–s04 的当前入口与用途
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/_studio_groups.txt
    what: 增加 Structure 分组，保留其他分组
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: 读取可选的顶部视图定义；其他主题沿用现有路径
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
    what: 校验并解析现有文件到共享 Studio 视图
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_structure_views.py
    what: 验证视图隔离、路径边界与现有预览兼容
  - do: edit
    path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
    what: 记录用户规则与验证依据
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/structure_studios.md
    what: 记录覆盖授权、逐文件计划和验证
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/s01-work-ladder.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
  - examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/result/structure-replaced-261127.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/s02-work-skills.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/studio-views.json
  - examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/result/structure-replaced-261127.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/s03-q01-work-ladder.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/studio-views.json
  - examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/result/structure-replaced-261127.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/studio-views.json
  - examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/result/structure-replaced-261127.md
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/jobs.html
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/studio.html
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/theme-studio.html
  - examples/Project-Ladder/blueprint/b17_theme_work/board.md
  - examples/Project-Ladder/blueprint/b17_theme_work/_studio_groups.txt
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_structure_views.py
  - plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/structure_studios.md
---

## Prompts

> I think skill might still be into one item in the top view list. No need to have a new studio for it.

> And for the work block structure. It should just be general. What are the job topic job name task topic and task name. 他们可以先general一下。 不需要给具体的名字,你知道吗?你直接就是 example 1，example 2，或 job 1，job 2，这样就行了。

> 然后你继续工作自己的这个 BO7的话你能覆盖就覆盖吧。我们现在就是说不要搞 scale 了，就是说 scale的话我们是放到 S0、0、2、0、3里面的 view 里面，你懂我意思吗。

## Plan and authorization

BO7 is interpreted in context as b17; scale as Skills. The latest user instruction authorizes replacing the existing b17 topic content. The exact file list was shown before changes. Existing paths and decision history are preserved; old faces are backed up byte-for-byte. No new skill Studio is allocated.

## Check

- 11 Studio tests passed (authored views plus existing Effect/reset behavior).
- All four manifests retain every declared item; 17 distinct view source URLs returned HTTP 200 on existing Tailscale port 5623.
- Chrome verified Work Structure, interactive Draw, hai-work source preview, live Work example, and independent Theme Studio organization.
- Scoped git diff --check passed. Existing server picked up the change without restart.

## Summary

Implemented s01 Work, s02 CoWork, s03 Discovery and s04 Theme structure Studios with Structure / Draw / Examples / Skills. Current faces replaced with original bytes preserved in result backups. Shared renderer supports validated file and Block items. No skill-only Studio created. Existing historical s05/UI topics and canvas annotations are retained. T06 in workbench-work/ref/topics.md records the rule and regression guard.


## Format alignment

Design theme session relayed the user’s shared Structure / Draw / Examples / Skills format. Structure and Draw each contain Jobs & Tasks and Studio. Examples use validated Block directories; no Job/Task standalone routes. The implementation uses the same planned files.

## Shared Draw follow-up

Design reported raw Excalidraw JSON and clipped PNGs through authored views. Continued within the same authorized shared implementation files: studio_views.py routes Excalidraw through the canvas viewer; studio_tabs.py renders image files responsively through open_dot; test_structure_views.py guards single/multiple items. All 13 Studio tests pass. T07 records the report and pending real Design-page verification; existing stage-word cleanup remains open.

## Shared Draw service reload

Design reported its restored Excalidraw bindings still returned raw JSON. Verified PID 21093 and restarted only port 5623 with identical interpreter, root, host, port, no-terminal and daemon arguments; new PID 16969. Design Studio and both s01/s02 canvas viewer endpoints returned HTTP 200; rendered iframe sources now use /_excalidraw/?board=. Design files unchanged. Browser acceptance delegated back to the reporting Design session. The unchanged interpreter emits an existing missing claude_agent_sdk warning; no runtime replacement performed.

## Shared Draw acceptance

Design confirmed real-browser s01/s02 canvases display at automatic 53% zoom, with direct Excalidraw bindings and the Markdown workaround removed. Its four views passed; receipt: b12_theme_design/trace/261127/1009_design_structure_studios.md. T07 is fixed with regression tests plus real-page verification. The independent row-stage words remain open as T08.
