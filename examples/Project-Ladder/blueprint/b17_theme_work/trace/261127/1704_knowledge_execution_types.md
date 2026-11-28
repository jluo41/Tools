---
title: Knowledge 四层执行类型
date: 2026-11-27 17:04
topic: s05-knowledge-structure
aim: 在 S05 定义 Job group type、Job type、Task group type、Task type，并显示 A2UI 模拟映射。
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1704_knowledge_execution_types.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/s05-knowledge-structure.md
  what: 更新四层定义与未决项
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/types.md
  what: 类型用途、内容要求及共享引用
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/s05-knowledge-structure.mindmap.md
  what: 四层组织及 A2UI 模拟对照
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/studio-views.json
  what: 四层类型条目绑定
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/build_structure.py
  what: 读取共享定义并生成四层内容
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/delivery/structure.html
  what: 重新生成结构内容
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/knowledge/hai-knowledge/SKILL.md
  what: 分组、类型、实例与执行门槛
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/knowledge/hai-knowledge/CONSTITUTION.md
  what: 记录用户纠正与检查
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1704_knowledge_execution_types.md
- examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/s05-knowledge-structure.md
- examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/types.md
- examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/s05-knowledge-structure.mindmap.md
- examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/build_structure.py
- examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/delivery/structure.html
- plugins/haipipe-toolkit/skills/2_work/knowledge/hai-knowledge/SKILL.md
- plugins/haipipe-toolkit/skills/2_work/knowledge/hai-knowledge/CONSTITUTION.md
---

# Knowledge 四层执行类型

## Prompts

- **17:04** 但是你这个 job task 这些东西就是说也没有说得很清楚啊，就是它不应该是一个，对吧？一个 job group呀，job group type，job type，task group type，task type，这些东西你都没有吗。
- **时间未提供** 然后你在对应的，你对应的是哪一个SNN呢？你怎么去在上面的SNN上去把它给就是说更新一下，实现一下。
- **时间未提供** 好，那你去执行吧，好吧，执行一下，我看看效果怎么样。
- **时间未提供** 批准范围：九文件计划。17:04 为计划标识时间；未收到各消息的原始发送时间。
- **协调消息（时间未提供）** Paper 协调通知要求对齐共享 Block Structure，复用 block_types_pages.py；本轮在九文件范围内调用其 page/members/VIEWS，生成同一已批准 HTML 的 fragments，不运行其额外文件写入入口。Work 协调通知提供 studio-bands-by-block-type.md；已核对 Knowledge 三组和 Sources 方向，实际 Sources UI 与窄屏共享体验仍不在本轮执行类型范围。

## Check

- host-venv build_structure.py --content-only 与 --check 通过；本轮只生成获批 HTML 和 manifest，未重绘 Excalidraw/PNG。
- 直接针对 S05 的 block_types_check.problems 通过：Job group / Job / Task group / Task 四层非空，条目分别 1/3/2/2；标题、占位符和文件长度检查通过。
- quick_validate.py 通过；README fresh-context validator 实际采用 Skill 推演 A2UI 与纯概念学习，并在内存增加类型、改变 Work 原定义，确认列表和内容动态生成、引用来源单份维护。
- Chrome 真实 Tailscale b17 页面：S05 Job types 显示 group 与 code/check/doc；Task types 显示 Make/Show 与 code/display。右侧读取 Work for/holds，显示 A2UI 用法和执行缺口。
- Structure > Job-Task 的四层关系及 A2UI 模拟映射可展开。调用共享 .drawing 容器保持横向滚动，实际滚动后已目视完整右侧层级；未另建 renderer 或修改共享服务。
- 实际 b18 仍无 Jobs；没有新建或执行 Task/Run。code 在 Work 结构定义存在，但 hai-task 执行路由缺失；display 专用合同不承担实时 A2UI 渲染。
- 修正前轮判断：实际实例可省略空组，不等于类型设计可以不解释分组。当前定义有真实组织目的，未修改共享 checker。

## Summary

完成获批九文件范围：S05 补齐四层类型、共享定义引用、动态顶部视图与左条目、可展开 A2UI 模拟对照，以及 Knowledge Skill 当前规则。正式入口仍为 Tailscale b17 Block 的 S05。实际 Sources 实例、code 执行路由和手机共享 mindmap 体验另有边界。

