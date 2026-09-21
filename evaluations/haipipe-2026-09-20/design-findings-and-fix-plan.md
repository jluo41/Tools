# Design 家族：复核发现与修复计划

## 1. 结论、快照与边界

审阅日期：2026-09-20。原评估为 [design.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/design.md)。当前 HEAD 仍为 `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`；本次核对使用当前工作树，而非只看提交中的文件。

**结论：Design 的当前指令仍未统一，原报告的主要完成边界问题成立。** 核心 Workflow 已采用 Commission、Generate、Verify，独立 Verify 通过后 ready for Delivery；venue、Unit 合约、Board 插件及共享 Run 入口却仍有要求 Adopt 的当前指令。需先解决这组冲突，再处理展示、计数和恢复说明。

这是一份补充评估和实施计划。本轮只新增本报告；不修改原报告、技能、实现、测试或其他家族的文件，也不创建实现任务。没有调用 Design 技能、启动网页、运行生成/审核流程或执行测试。下面的代码判断来自静态阅读，验收条目均是后续工作。

工作树已有大量其他会话的修改，包括 Insight、Page、共享 Board、STRUCTURE 和 references 子模块。核对时 Design 主目录、指定两个 Design 插件，以及 `live/design.py`、`live/design_actions.py`、`live/designboard.py` 相对 HEAD 无修改。原评估的 Design 证据仍可使用；跨家族结论必须按当前文件更新。

### 对原报告的修正

| 原报告发现 | 当前判定 | 本报告对应项 |
|---|---|---|
| Venue 的 Phase/Adopt 生命周期 | 仍成立，P1 | F01 |
| Board 当前要求 Adopt | 文档问题成立，P1；实现已有 ready 投影，不能说实际 UI 仍必然有 Adopt 队列 | F02 |
| Unit 合约的 Adopt/调用方边界 | 仍成立，P1；共享 Run 入口也有同样残留 | F03 |
| Page 把 Delivery 放进 Run 链 | 示例和命名问题成立，P2；当前代码遍历真实 Runs，没有证据表明会为新数据自动追加第四个 Delivery Run | F04 |
| Phase/graph 与列表模型 | 收紧判断：活动的 Phase 指令要改；否定 Phase 的句子不等于保留 Phase 权限。路由图可与 Runs 列表共存 | F01、F04 |
| Venue 路径及 Card/DU/grant 样例 | 仍成立，P2 | F05 |
| blocked 与人为 hold 混合 | 状态解释和恢复指引问题成立，P2；已有 Release 保护，撤回“可能直接提供错误 Release 按钮”的强推断 | F06 |
| Unit 标题的 Commission/Result 基数 | 仍有阅读歧义，降为 P3；正文已按 Ticket 限定工作 | F07 |
| 范围外 Insight 旧物理路径、Application 父级 | 当前工作树已修正文案；不再列作未修复缺陷 | 第 5 节 |

复核另确认 F08–F12：渲染写入范围冲突、历史 Run id 展示改写、Commission 计数矛盾、Verify 重试措辞和冻结配置措辞。

优先级：P1 表示当前指令会给出互不兼容的写入范围、操作或完成边界；P2 表示路径、身份、计数、状态或契约解释有明确偏差；P3 表示正文已有正确约束但标题或局部措辞容易误读。没有发现足以定为 P0 的证据。

## 2. 全家族覆盖

以原报告的完整阅读为基础，本轮复读报告并核对当前入口、支持材料和相关实现片段。当前技能清单仍为 Design 主目录 4 个，加指定 Page/Board 插件 2 个，共 6 个。

| 范围 | 当前核对结论 |
|---|---|
| [haipipe-design](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design/SKILL.md) | Item/Run、Page/Design 两套身份、Verify 后 ready 的主要边界可保留；Run 表、Phase 措辞及计数需校正。 |
| [haipipe-design-brief](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-brief/SKILL.md) | Brief 的 Page 工作流与 Design Commission 前置依赖清楚。未确认新的独立 P1/P2 缺陷；保留版本、签名和 Board 两类限定写入的约束。 |
| [haipipe-design-unit](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/SKILL.md) | 单 Ticket worker、独立 Verify、完整检查覆盖值得保留；Adopt、渲染写入范围、标题和参考路径需修。 |
| [haipipe-design-workflow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md) | 三种当前 Run Type 和 Route 已明确；列表、Projection 表、Commission 次数和重审限制需统一。 |
| [Page Design 插件](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-design/SKILL.md) | 当前 action 表主要正确；示例、Steps 标签、旧“双人工门”标题和若干边界措辞落后。 |
| [Board Design 插件](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/SKILL.md) | Adopt、队列、汇总和 CSV 说明仍是旧模型；需与已更新的投影实现对齐。 |
| 支持指令 | Designer agent、Brief agent 配置、Unit 两份 reference、Workflow run-profile、venue schema、8 个 README、8 个 style profile，以及两个插件的 space-mapping 均纳入修复范围核对。 |
| 历史资料 | 原评估读过的 7 份 field-test 文档及旧 changelog 作为历史材料；不充当当前运行成功证据，不纳入机械术语替换。 |
| 实现与测试 | 静态阅读 Design 相关状态折叠、action、Board 汇总、renderer 和 checker 片段，确认测试入口；没有完成这些实现的全面代码审计，也未执行测试。 |

## 3. 修复后的统一模型

用户要求的首要定义应直接落在所有入口：**A Workflow is a list of Runs. Run 不等同于 Phase。**

建议共享声明如下，随后再解释 Run Spec、Route 和实例化：

```text
A Workflow is a list of Runs. The Design Workflow contains Commission,
Generate and Verify Runs. Each allocated Run keeps its own identity,
bounded target, actor, gate and Result or receipt.

Routes describe dependencies and which Run may be created next. A route
graph is a view of those relationships. Delivery is a read-only projection
of the exact candidate whose independent Verify passed.

Comments, clicks, model calls and renders are internal Steps unless they
are separately commissioned and recorded as independently closable Runs.
```

三种 Run Type 不是“每个 Item 永远恰好三条 Run”。一个实际列表可以包含 Hold Commission、随后 Release Commission、多次 Generate 和 Verify。列表应能追溯每条真实记录；路线图可以解释分支，不另造执行单位。简化卡片可折叠历史记录，但完整 Run Space 的身份和计数必须来自同一组真实记录。

下列现有约束继续保留：

- Design 与 Insight 是独立家族；Brief 是设计输入，Page 有自己的 Run 和完成边界。
- 只有明确释放的 Commission 能授权下游工作；不回填已完成的决定，不原位改写完成的 Result。
- Commission 固定当前契约规定的配置与证据，不在这次修复中擅自增加“整个 Brief/venue pack 必须冻结”的新要求。
- Generate 自检不能替代独立 Verify；结构检查通过不能证明主观质量、真实独立性或人的授权有效。
- Verify 通过使确切目标 ready for Delivery；Delivery 不产生新的人工 Adopt 门、Run id 或设计 Result。
- 只保留已明示支持的历史 `rdNN_adopt_*` 读取。不得借此恢复 v1、DU、D0–D5、PageX 等已拒绝形状。

## 4. 逐项发现与具体修法

### F01 · P1 · Venue 支持指令仍规定另一套生命周期

**位置与证据：**[venue schema](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/_SCHEMA.md:26) 的 profile 要求 `terminal: adopted`，第 47 行要求 `Phase use`，第 53–61 行定义 Preview、Adopt 和 Application terminal；与第 12–14 行“venue 不创建生命周期”自相矛盾。[SMS README](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-sms/README.md:28) 更直接把 Commission → Generate → Verify → Adopt 称作唯一 Workflow。8 套 README 全部保留终态和 Phase 章节，逐文件位置见第 4.1 节。Unit 会加载选中的 pack，因此这些是可到达的现行指令。

**影响：**执行者可能在 Verify 通过后等待不存在的 Adopt 操作，或把 Preview 计为额外 Run；不同 venue 给出不同于核心 Workflow 的完成边界。

**修法：**schema 与 8 套 README 一起改。删除 venue 对终态的所有权，取消 `terminal: adopted`，把 `Phase use` 改成 `Run guidance`；只说明该 venue 对 Commission 输入、Generate 内容、Verify 标准的增量。Render/Preview 放进对应 Run 的内部操作说明，并引用 F08 的写入位置。将准备交付的状态写为 `ready for Delivery`。保留各 venue 的长度、内容、可视性和证据要求。

**验收：**任选一套 pack 与核心 Workflow 同读，都只得到三种当前 Run Type；所有 8 套不再指示执行 Adopt/decline；Visual pack 不能绕过独立 Verify；支持材料不再声明 Application 父级终态。

### F02 · P1 · Board 文档要求当前 controller 不接受的 Adopt，并错误解释 CSV

**位置与证据：**[Board SKILL](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/SKILL.md:48) 第 48–49、64–65、108、116–124、163、196、216 行分别涉及 Adopt 步骤、adopted 数量、`JL · adopt` 队列、稿件选择、CSV 过滤和动作。[Board mapping](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/ref/space-mapping.md:5) 第 5、9、12、68 行重复这些约定。

反证来自当前实现：[Page dispatcher](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py:1659) 拒绝 Adopt 等旧动作；[Board Delivery](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/designboard.py:417) 只展示 ready 对象，[CSV 构造](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/designboard.py:475) 同样使用 `i.get("ready")`。因此本项首先是现行文档与实现冲突，不能报告为“已观察到线上仍有 Adopt 队列”。

**影响：**人或 agent 会寻找 controller 拒绝的按钮；按文档使用 CSV 的消费者可能把 ready 行全部漏掉。文档中“没有 adopted 就用最新通过 records check 的 draft”还会使读者把生成自检当成足够的交付凭据。

**修法：**同时重写 SKILL 的示例、队列、汇总、Delivery、CSV、边界及 Reader contract，并同步 mapping。当前交付只依据通过独立 Verify 的确切候选；汇总统一用 ready，CSV 说明与实际字段一致。把历史 adopt/declined 解释集中在兼容章节。检查旧 query alias 是否仍被实际支持，分别记录 current 与 legacy，不能凭文字替换擅自删除 URL 兼容。

**验收：**同一组混合状态 fixture 中，Page ready、Board ready 数量、Delivery 列表和 CSV 行数一致；仅生成自检通过、Verify fail 或 Verify invalid 的候选不能出现在交付集合；当前说明不再让人执行 Adopt，也不声称当前发送条件是 `state=adopted`。

### F03 · P1 · Unit 合约和共享 Run 入口仍把 Adopt 作为当前职责

**位置与证据：**[unit-contract](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/references/unit-contract.md:35) 第 37 行 Commission/Adopt Tickets、第 46 行 Application callers、第 155 行 human adoption receipt、第 170–175 行 Adopt 审计说明，均未划出当前/历史边界。[Unit 边界](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/SKILL.md:120) 把 adopts results 留给 caller。范围外的 [共享 Run 分类](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:270) 第 270–271 行仍把 Adopt decision 列为 Design Run，第 286 行还列 `commission/generate/verify/adopt` gates。

**影响：**worker 从核心 Workflow 进入必读合约后，又得到第二个完成门；共享 Run 技能也可能把旧契约重新带回 Design。checker 接受历史配对并不能证明新写入应允许 Adopt。

**修法：**Unit 与 contract 统一描述当前 Commission/Generate/Verify 分工。caller 负责释放、排队、关闭和只读投影，移除当前 adoption 职责；`Application callers` 改成准确的 Design 调用方，并保留签名、Board reads 和输入范围校验。把 `rdNN_adopt_*` 的审计说明放在明确的 legacy 小节。同步共享 Run 的当前分类与引用文案。保留 checker 的必要历史读取，先区分 writer/reader 再决定任何代码清理。

**验收：**新上下文从共享 Run、Design Workflow、Unit 或合约任一入口进入，都不会新建 Adopt；历史支持范围没有扩大或缩小；完成标准仍是有效的独立 Verify pass。

### F04 · P2 · Runs 列表、Step 标签和 Delivery projection 混在同一组说明中

**位置与证据：**[Workflow Run Specs](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:48) 说每行是可独立关闭的 Run Spec，第 59 行却放入 Delivery projection，第 63–64 行又说它不是 Run。主入口 [Run Type 表](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design/SKILL.md:146) 也混入 Delivery。[Page 示例](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-design/SKILL.md:166) 把 Delivery 放在 STEPS 链；第 63–65、205–207 行用 Steps 指实际 Runs。实现 [卡片标签](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py:1129) 也叫 Steps，但第 1094 行实际遍历 `item["runs"]`。

[主入口](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design/SKILL.md:65) 第 65、248 行和 Page 第 300 行仍以 design phase 描述当前工作；这是可直接改成 Design Runs 的活措辞。相反，Brief 第 38 行、Workflow 第 48 行是否定 Phase，不能据此认定存在 Phase 执行层。

**影响：**读者无法从表格判断 Delivery 是否需要 id、receipt 和完成动作，也难区分 Run 内的 Step 与跨 Run 的列表。

**修法：**采用第 3 节的列表优先定义；三种 Run Type 和实际 Run 清单分别说明。Run Specs 表只含真正的 Run，Delivery 放在独立的投影表或表外状态。Page/Board 实际 Run 芯片改称 `Runs`；内部点击、工具调用仍叫 Step。补充路线图的用途，不删除有用的分支图。将 [Page Actions 标题](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-design/SKILL.md:398) 的“two human gates”同步改为当前动作说明。

**验收：**表格、示例与真实卡片都不把 Delivery 当作第四个 Run；读者可区分 Run Type、Run 实例与内部 Step；当前执行说明不使用 Phase 定义工作单位。历史路径名、退役说明不做全局替换。

### F05 · P2 · Venue 导航和 style profile 的对象名过时

**位置与证据：**[modes.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/references/modes.md:35) 指向不存在的当前家族路径 `application/venue/venue-<kind>/`，实际目录是 `design/venue/`。8 份 style profile 都要求 Card id/grant；[SMS profile](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-sms/style-profile.md:80) 第 83、87–93 行还用 DU、division-id、draft/judged 和 `card.md`。具体行号见第 4.1 节。

**影响：**新上下文会找错 pack 或按旧对象编写、自检，无法把检查项对应到当前 Item、Ticket、Result 和输入哈希。

**修法：**给 modes 一个按文件位置可解析的相对路径，例如从 `references/modes.md` 指向 `../../venue/venue-<kind>/`，并说明起点。把检查清单改为 Item id、释放的 Commission、明确角色的输入、Result/artifact hash，以及需要时的 render 记录。SMS 改为当前记录可表达的示例；不要只把 `DU` 字符串换成 `ITEM` 而保留不存在的 card 字段。UI wireframe 与最终 screen/render 区分，视觉验收不能仅凭 ASCII 示意完成。

**验收：**8 套 pack 均可从 Unit 指引定位；按任一 profile 自检不需要创建 `card.md` 或 DU 目录；修正后的示例能逐项映射到当前 contract。仍可保留原始语气、版式和渠道约束。

### F06 · P2 · 人为暂缓和运行阻塞共享 hold，恢复说明不足

**位置与证据：**[Page 状态 mapping](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-design/ref/space-mapping.md:45) 第 45 行是 Commission hold，第 57 行是任意 Run blocked。[状态折叠](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py:320) 把二者都显示为 hold。第 907–913 行 `_held_at` 检查最后的 Commission 是否真的 hold，第 931 行才开放 Release/Hold；其他阻塞可能落到第 947 行无按钮。

**影响：**列表虽然能显示 failure，统一的 hold 名称仍让人难以分辨这是等待决定，还是需要修复输入/记录；没有按钮时，下一步和负责人不够明确。现有保护使本项不能被当成已证实的越权 Release 漏洞。

**修法：**投影中区分 `commission held` 与 `blocked · reason`，保留底层 receipt 的真实状态。逐种阻塞指定责任方和恢复路径；只有已支持的动作才显示按钮，需人工修复时直接说明文件/原因。还应区分 worker 返回的 named hold 诊断与人类 Commission 的 HOLD Route，不能因同一英文词自动完成一次人类决定。

**验收：**Commission hold 可通过新的明确决定恢复；Generate/Verify blocked 显示自己的 Run、原因、等待对象，不凭状态名称获得 Release。没有可自动恢复动作时也能读懂该做什么。

### F07 · P3 · Unit 标题用 Commission 描述了 worker 的执行粒度

**位置与证据：**[Unit 标题](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/SKILL.md:13) 为“one commission, one inspectable result”；第 35–39 行 Entry 实际接收 Generate/Verify Ticket。正文已经正确约束单次操作，所以本项是标题歧义，不是已证实的 Result 基数错误。

**影响：**第一次进入技能的人可能误以为整个 Commission 只允许一个产物或一次 Unit 调用。

**修法与验收：**标题改为 `one Ticket, one inspectable Result`，正文继续解释 Commission 是上游授权；一个 Commission 下多次 Generate/Verify 的示例与标题不冲突。

### F08 · P1 · UI renderer 示例越出 Unit 被允许的写入目录

**位置与证据：**[Unit Generate](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/SKILL.md:57) 第 57、126 行要求只写当前 Result；第 74–77 行却令 renderer 写 `<folder>/delivery/render/*.png` 和共享 manifest。[Designer dispatcher](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design/agents/haipipe-designer-agent.md:25) 第 25–27 行更明确禁止修改 Delivery projection。[renderer 实现](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/render_screen.py:137) 第 137–139、159–171 行确实创建 PNG 并重写指定的 manifest，不只是返回一个建议路径。

**影响：**执行 UI Generate 的 agent 无法同时遵守渲染命令与写入边界；共享 Delivery 目录还可能出现尚未通过 Verify 的生成过程产物。这里确认的是指令和实际写入行为的矛盾，未证明当前 UI 会错误发布这些文件。

**修法：**建议保持 worker 只写 Result：Generate 的截图、计量和局部 manifest 放在其 Result 内；Verify 如需自行渲染，输出到自己的 Result。caller/presenter 从 hash-bound 产物投影或复制准备交付的图片到 Delivery，记录准确来源并保持派生过程可重建。Design Space 可读取草稿的 Result 预览，Delivery Space 仍只读 ready 对象。Render 不因此升级为额外 Run。

该修改必须连带检查 [Page 的图片映射说明](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-design/SKILL.md:261)、[manifest 读取器](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py:650)、renderer CLI 帮助/示例及 artifact 清单约定；不能只改命令路径后留下失效的预览。禁止覆盖已固定的图像，也不能在已完成 Result 中补写验证产物。

**验收：**UI Generate/Verify 的写入差集只落在各自 Result；producer Result、共享 Delivery 和 runtime 不由 worker 改动；caller 的投影绑定确切 Generate/artifact hash；新稿不显示旧图；未通过 Verify 的预览不会进入交付集合。

### F09 · P2 · 历史 Adopt Run 的显示 id 被改成虚构的 Delivery Run id

**位置与证据：**[Page Run 表](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py:897) 和第 1104 行 tooltip 对 id 执行 `.replace("_adopt_", "_delivery_")`；[Board Run 表](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/designboard.py:397) 同样如此。但 [Workflow identity 约束](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:81) 禁止 Run Space rename/copy/recount。

**影响：**显示名称与真实 Ticket/receipt 不同，复制 id 后找不到对应记录；也会误导读者认为存在 Delivery Run。链接仍指原 Ticket，不能把本项说成文件已被重命名。

**修法：**所有 Run id、tooltip 和链接显示原值；另外增加 `legacy Adopt record` 或中文历史标签。状态可解释为历史交付证据，但不得更改身份。更新 `_step_chain` 的旧 Adopt 流程 docstring。保留历史文件字节及真实链接，不创建 `_delivery_` 别名记录。

**验收：**一个合法历史 Adopt fixture 在 Page、Board、Run 表、tooltip 和打开的记录中 id 完全一致；新记录仍没有 Adopt/Delivery Run；旧数据不发生磁盘迁移或重写。

### F10 · P2 · “一个 Commission”计数与 Hold 后新决定的记录方式矛盾

**位置与证据：**[Workflow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:25) 第 25、41 行及 [run-profile](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/references/run-profile.md:11) 第 11–14 行使用 `1 Commission + N Generate + J Verify`；Workflow 第 94–95 行又允许 held Commission 通过新的 Commission decision 释放。[commission 实现](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design_actions.py:297) 只拒绝已有 release 的 Item，第 301–325 行每次合法决定都分配新的 `rdNN_commission_*` 和 receipt。

**影响：**Hold → Release 至少留下两条 Commission Run，按现行“actual Runs”公式计数会漏掉历史决定，也可能诱导实现者覆盖已完成 hold 记录。

**修法：**明确约束是“每个 Item 至多一次有效 release”，不等于“一生只有一条 Commission Run”。一般实际计数写为 `C Commission + N Generate + J Verify`；没有之前 hold 的常见释放路径才是 C=1。C/N/J 都按真实已分配记录统计，失败、阻塞、superseded 的显示/汇总口径明示；同 Run 内 attempt 不再计数。同步主入口、Workflow、run-profile 和 Page action 描述。

**验收：**Hold → Release → Generate → Verify 产生 4 条可追溯记录，其中 2 条 Commission；第二次 release 被拒绝；所有旧决定不变；简化卡片的折叠不改变完整审计数量。

### F11 · P3 · “已有 review 不可再审”遗漏 completed 条件

**位置与证据：**[Workflow Verify](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:125) 第 125–126 行禁止已 review 的 draft 再审，而第 130–132 行允许无效 review 重试。[Page action 表](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-design/SKILL.md:410) 同一行给 verify invalid 提供 Queue Verify，又说已有 review 就拒绝。实际 [queue_verify](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design_actions.py:426) 只用 `status == "complete"` 的目标 review 阻止重复审核。

**影响：**按说明恢复 unresolved/invalid 的执行者可能停住；当前代码已经区分，故不据此认定重试实现损坏。

**修法与验收：**说明改为“已有完成且有效的独立 review，不重复审核同一候选”；invalid/failed records-check review 可走新 Verify，已完成 verdict fail 则走新 Generate。三个路径分别能从文字和 action 表得到同一答案。

### F12 · P2 · “配置原样复制”没有说明 Run 专属字段的派生

**位置与证据：**[unit-contract 配置说明](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/references/unit-contract.md:77) 第 77–79 行写 Generate/Verify `copy it unchanged`，第 97 行又要求 self/independent 两种 review_mode。[配置构造](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design_actions.py:330) 第 344–347 行确实派生 review_mode，必要时改变 mode。

**影响：**接手者无法判断“冻结”要求逐字节相同，还是只要求设计目标和规则不漂移；机械落实原样复制会把 Verify 的独立模式写错。

**修法：**列出字段级继承规则：设计意图、依据、目标、单位及验收规则来自已 release 配置；review_mode 随操作派生，revise 的 mode 按现行规则派生，challenge 的约束继续保留。每个 Run 固定其派生配置的 hash。不要为修正文案而取消冻结，也不要声称现有 checker 已证明所有字段继承正确。

**验收：**Generate=self、Verify=independent；普通 revise 与 challenge revise 各自符合模式约束；release 后修改 register 不改变已授权的目标、意图和验收规则；派生字段有明确白名单及对应证据。

### 4.1 八套 venue 的修改清单

下表列出当前行号，实施时按小节复核，避免其他会话改动后依赖旧行号。每行的 README 都纳入 F01，style profile 都纳入 F05。

| Venue | README：terminal / Phase use / Adopt 附近 | Style profile：Card/grant 检查 |
|---|---|---|
| checklist | [23 / 43 / 58](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-checklist/README.md:23) | [46](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-checklist/style-profile.md:46) |
| dashboard | [23 / 26 / 53](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-dashboard/README.md:23) | [39](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-dashboard/style-profile.md:39) |
| email | [24 / 27 / 49](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-email/README.md:24) | [67](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-email/style-profile.md:67) |
| push | [23 / 42 / 52](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-push/README.md:23) | [42](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-push/style-profile.md:42) |
| reminder | [23 / 46 / 57](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-reminder/README.md:23) | [37](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-reminder/style-profile.md:37) |
| report | [24 / 27 / 62](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-report/README.md:24) | [73](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-report/style-profile.md:73) |
| sms | [25 / 57 / 72–76](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-sms/README.md:25) | [75；80–93 另有旧输出语法](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-sms/style-profile.md:75) |
| ui-card | [23 / 26 / 52](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-ui-card/README.md:23) | [64；43 行 wireframe 说明同时核对](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/venue/venue-ui-card/style-profile.md:43) |

## 5. 共享问题、依赖与已修复项

| 编号 / 优先级 | 当前证据与影响 | 协同修法和验收 |
|---|---|---|
| X01 / P2：家族目录说明仍保留 Application | [Board README 第 19–21 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/README.md:19) 仍把 Application Pages 归 Application family；[STRUCTURE 第 148 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/STRUCTURE.md:148) 仍把 application 列为 Insight/Design join。会把已独立家族重新解释为子树。 | 由 Board/目录 owner 对齐 Design、Insight 直接所有权和实际路径。使用 Application 表示产品对象的正文不需一律删除。验收是目录表、入口和导航一致，无虚构的当前 `skills/application/` 目标。 |
| X02 / P2：共享 Workflow 的首要定义 | [Task Workflow 第 19–26 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-workflow/SKILL.md:19) 已有 `Process[Run₁ … Runₙ]`，但首句偏重 directed composition；[Run 第 193–205 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:193) 偏重 graph。不能说这些文件完全没有列表或把 Phase 当权限层。 | 共享 owner 把用户要求的列表定义置于首位，保留 Route 图作为依赖视图；同步 F03 的旧 Adopt 分类。验收是共享与 Design 对 Run、Spec、实例、内部 Step 的解释一致。 |
| 已修正文案：Insight 家族和旧路径 | [Insight 第 32–43 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:32) 已写真实 `skills/insight/` 路径，并明确 Insight/Design 是 peers；第 59 行把 application 标为 legacy scope token。 | 原报告的对应批评在当前工作树中关闭；不要再恢复或重复修改。这里只证明文本已改，未验证运行时路由。 |
| Page 与 Board 共用实现 | F04、F06、F08、F09 的可见行为由共享 Board 的 Design 模块承载；同目录有其他会话修改。 | 以最新工作树协调精确改动，只改 Design 相关函数；不覆盖 Insight、通用 folder contract 或并行修改。 |

Design 的修复不必等待所有家族完成。用户已给定列表模型，Design 可先落实；共享入口的 F03/X02 应在整体验收前合入，防止旧指令再次进入调用链。X01 可并行由目录 owner 修正，不应阻止 venue 和 Unit 的本地纠错。

## 6. 可实施的修改顺序

以下是工作包顺序，不是 Design 的运行生命周期，也不引入新的 Phase 或执行对象。

| 顺序 | 工作包与文件组 | 依赖 | 完成条件 |
|---:|---|---|---|
| 0 | 重新核对 git status、当前改动和 scoped guidance；冻结本次拟改文件清单 | 无 | 不覆盖其他会话和脏子模块；确认原报告留存。 |
| 1 | 定义和基数：主入口、Workflow、run-profile；协调共享 Run/Workflow（F03/F04/F10、X02） | 0 | 列表优先；Delivery 表外；C/N/J 与一次 release 约束一致；明确 current/legacy。 |
| 2 | 完成边界：Unit/contract、venue schema、全部 8 README、Board SKILL/mapping（F01–F03） | 1 | 所有可到达的现行指令都在独立 Verify pass 后 ready；当前无 Adopt gate。应作为一组一致修改交付。 |
| 3 | Worker 细节：modes、8 profiles、Unit 标题、配置字段和重试措辞（F05/F07/F11/F12） | 1–2 | pack 可定位；示例可映射当前契约；冻结字段和运行字段区分明确。 |
| 4 | UI 渲染所有权：Unit/agent、renderer 示例/必要实现、Page manifest 说明与消费者（F08） | 1–3 | 写入范围、草稿预览、ready 交付和 hash 对应关系一致。先确定 Result 附件形状，再改读取器。 |
| 5 | Page/Board 展示：Runs 标签、hold/blocked 恢复、历史 id（F04/F06/F09） | 1–2；图片展示依赖 4 | id 不改写；状态和下一步明确；Delivery 不冒充 Run。 |
| 6 | 共享目录与文档收尾：X01、当前修订说明、交叉引用 | 可与 2–5 并行 | 所有入口引用新契约；没有重复 family owner；没有破坏旧链接或历史说明。 |
| 7 | 静态一致性、针对性测试、新上下文技能验证、人类界面走查 | 1–6 | 第 7 节的关键场景通过，记录实际证据与仍未验证项。 |

### 修改策略

- 不对 `Phase`、`Adopt`、`Application` 做仓库级搜索替换：活动指令、历史身份、旧 URL token、产品名和否定旧模型的句子需要分别判断。
- 先使说明与已正确的实现一致。F02/F11 不因文档落后就回退 ready 或重复审核保护。
- F08、F09、必要的 F06 属于行为/展示修复，需要独立的实现差异和验收证据；不能把它们包装为纯文案修改。
- 旧 changelog 和 field-test 记录保留历史事实；在当前修订说明中补记修复及兼容边界，不重写历史结果以制造一致。
- 四个 Design 技能当前版本锁定 `0.4.0`，不在此计划中升级到 1.x 或擅改版本；两个插件各有自己的版本，保持各自约束。没有新增/退休 package 的计划，通常无需改 marketplace 或安装器。
- 不借此次修复新增投放、发送、测量成效或外部授权流程。Design 的交付边界保持为可审计的设计产物。

## 7. 验收计划（本轮未执行）

### 7.1 静态一致性

逐条核对 6 个入口、所有当前支持指令、8 套 venue、两份 mapping 和共享引用；搜索结果按语境分类，不能以某个词零命中代替语义验收。

必达条件：

1. 所有入口明白表达 Workflow 是 Runs 列表；Run 与内部 Step 分开，Route 图不增加身份。
2. 当前新写入只有 Commission/Generate/Verify；Verify pass 的确切候选 ready，Delivery 是投影。
3. 所有文档中的目录和示例可解析；没有要求创建旧 DU/card 数据才能完成当前流程。
4. 所有真实 Run 的 id、Result、receipt 可对应；历史身份不经显示层改名。
5. 计数、Review 重试、配置继承与实际写入一致；失败与完成 verdict fail 不混为一谈。
6. 新旧边界明确；现有支持的 Adopt 历史可读，明确拒绝的旧形状不被重新接受。

### 7.2 关键场景矩阵

全部使用临时合成 fixture；记录实际路径、Run id、状态、输出 hash 与写入差集。表中的预期不是本轮测试结果。

| 场景 | 必须观察到的结果 | 对应发现 |
|---|---|---|
| 普通 SMS：Release → Generate → Verify pass | 3 条真实 Runs；无 Adopt/Delivery Run；Page/Board/CSV 同一候选 ready | F01–F04 |
| Commission Hold → Release | 2 条不同 Commission 记录，旧记录不变；完成 Generate/Verify 后总计 4；第二次 release 拒绝 | F06/F10 |
| Verify completed + verdict fail | 候选保留；给 feedback 后新 Generate，再独立 Verify；不在同一已审候选上刷 review | F11 |
| Verify unresolved / records check invalid | 无 ready；可建立有效的后续 Verify；不被“已有 review”字样阻止 | F11 |
| Generate/Verify blocked | 清楚显示阻塞 Run、原因和责任方；不会因 hold 标签获得不属于它的 Release | F06 |
| queued 输入变动 / worker 未产 Result 中断 | 按现有契约区分 superseded+新 Run 与同 Run 的恢复 attempt；不遗漏或重复计数 | F04/F10 |
| release 后改 register；普通 revise 与 challenge revise | 冻结的目标/规则不漂移；只派生允许字段；challenge 约束保持；self/independent 正确 | F12 |
| UI card 的 Generate 和独立 Verify | worker 只写各自 Result；实际检查图片与计量；结果可在正确 Space 展示，旧图不冒充新稿 | F05/F08 |
| 仅生成自检通过、审核失败、审核通过混合的 Board | Delivery/CSV 只含独立 Verify pass 的候选，数量与 Page 一致 | F02 |
| 合法历史 rdNN_adopt_* | 可读且标历史；所有显示 id 与文件一致；不生成新 Adopt/Delivery 记录 | F03/F09 |
| v1 / DU / D0–D5 / PageX 输入 | 仍按当前 clean-break 规则拒绝，不作兼容迁移 | F03/F09 |
| 五个群组各十条 SMS 的 Brief/Board 入口 | 5 条设计任务与每条数量 10 分清；开 Folder、登记 Item、释放 Commission 的职责分清，不能把按钮数当 Run 数 | 全入口交互 |
| brief-only 与 signed W evidence-informed 两种输入 | brief-only 不伪造证据；evidence-informed 验签与适用范围；不能把结构检查当签名授权证明 | Brief/Unit/Insight 边界 |

每个 venue 至少进行一次新上下文的指令读取与输出契约核对；SMS 和 ui-card 作为完整主路径，其他 6 套补足各自的特定约束检查。候选集/sequence 要确认 artifact×criterion 完整覆盖，不能只验证第一条内容。

### 7.3 已有测试入口与新增覆盖

现有测试可作为实施后的回归起点，而非“已经覆盖了所有问题”的证据：

| 运行工作目录 | 后续可用命令 | 用途 |
|---|---|---|
| [Design Unit](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit) | `python3 -m unittest discover -s tests -p 'test_unit.py'` | Ticket、Result 和 records-check 契约 |
| [Board engine](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board) | `python3 -m unittest discover -s tests -p 'test_design*.py'` | Design family、Page/Board 插件与 Run gate |

实施时先审阅现有断言，再为 F06/F08/F09/F10 和必要的 F12 增补针对性覆盖。不能仅删除仍期待 Adopt 的断言来获得绿色结果；需说明哪些是当前 writer 断言、哪些必须保留为历史 reader 断言。以上命令本轮均未运行，依赖环境和浏览器可用性也未验证。

[根 README 第 133–136 行](/Users/jluo41/Desktop/Tools-SPACE/README.md:133) 要求技能变更使用新上下文 subagent 在现实任务中调用并验证。后续实际修改技能时按此执行，记录技能是否被正确选择、指令是否遵守、输出是否符合预期。本轮未改技能，因此不以当前熟悉代码的上下文假装完成这项验证，也未启动此验证。

独立 Verify 的测试必须真的使用不同于 producer 的新上下文；改 actor 名称不能算通过。人类界面走查至少应让读者回答：现在有哪些真实 Runs、当前等谁、为什么阻塞、哪一个确切版本已可交付。若只做了静态 HTML 检查，应如实标注，没有真人测试不能称为真人验证。

## 8. 不确定性与交付条件

- 本报告证明的是现行说明和部分实现的矛盾；没有证明真实用户已因此误操作，也没有证明所有受影响 runtime 路径都不可用。
- F08 的推荐方案需要实施者核对附件/manifest 与 renderer 消费者后落实。当前不足以承诺仅改路径就能兼容全部屏幕预览。
- 旧 `design_actions.adopt` 辅助函数和 checker 的历史接受路径仍存在；Page dispatcher 已拒绝相应 live action。是否还有其他直接调用点，需要在任何删除前检索确认，本报告不据存在函数就判定存在可达新 Adopt 流程。
- Brief 与 venue pack 不被 Commission 整体固定是当前明确选择；是否要加强长期可复现性属于另一个契约决定，本次不把它自动升级为缺陷或新增门槛。
- 共享文件仍在变化。实施前应重新确认 X01/X02 与 Insight 修正文案，已修复的内容不重复覆盖；这里的行号属于此次快照。

**关闭本次发现的标准：**F01/F02/F03/F08 的 P1 冲突全部消除；F04–F06、F09–F10、F12 的身份、状态、计数和契约解释一致；F07/F11 的局部误导修正；共享入口不再引入旧模型；关键场景有真实验收记录。仅核心 Workflow 改成三行、或仅搜索不到 Adopt，不足以关闭整家族评估。

本轮交付只有本补充报告，原始评估保留，源码修复与运行验收尚未实施。
