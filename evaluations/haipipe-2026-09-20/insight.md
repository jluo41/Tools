# Insight 技能族评估报告

**实施状态（2026-09-20）：** 用户已授权落实更新。第 1–9 节保留修改前评估与设计讨论；实际修订及验证结果见第 10 节。旧路径和源码行号属于评估快照，不代表更新后的目录。

**目录归属更新（2026-09-21）：** Task-side `haipipe-page-insight` 已从
`skills/task/page-types/` 移到 `skills/insight/haipipe-page-insight/`。它仍
服务 Task Insight route，公开 Skill 名称不变；当前 inventory 将它计入
Insight family。下文旧路径只用于说明当日评估证据。

**总体结论：** Insight 路由、证据来源和 signed Design Handoff 边界写得细；Task 侧的 riNN、Application-context InsightBoard 与签名手递大体可区分。但 Application Board 控制器仍把 I0–I5 分类当作工作流骨架，以 CELL 而不是 Run 身份推进。按“Workflow 由 Runs 构成”这一强制标准，Insight 工作流整体**不通过**。Task 侧已有真实 riNN Runs，且正确地没有把 checkpoint、LLM 调用或工具执行另算成 Run。目标模型不再有 Phase 概念：本报告提到的 live Phase 词汇、字段和路径，是当前文档/持久化格式里的待迁移遗留项，不是建议保留的目标抽象。

## 1. 快照与审阅边界

- 审阅日期：2026-09-20。
- 基线提交：f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217，与评估 Brief 记录一致。
- 当前树有 8 个已修改的 references/ 子模块指针；evaluations/ 是未跟踪目录，现有 BRIEF.md、inventory.json、sessions.json 属于共享评估资料。本报告原始评估阶段仅写入 evaluations/haipipe-2026-09-20/insight.md，没有修改技能、代码或其他报告；后续目录归属更新见上方说明。
- 初始八项 Insight 清单与磁盘一致：八个当前 SKILL.md 均存在，未发现新增的 Insight SKILL.md。另按 Brief 要求审阅 Task 侧 haipipe-page-insight/SKILL.md 和 haipipe-task/fn/insight.md。
- 没有执行被审阅的技能、脚本、测试或外部服务；下文走查都是桌面推演，不是现场用户测试或运行时验证。

## 2. 完整覆盖清单

| 类别 | 当前文件 | 覆盖 | Workflow/Run 结果 |
|---|---|---|---|
| Insight 入口 | plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md | 全文 393 行；另读 agents/openai.yaml、三个 ref 文件 | 部分符合：路由和 Run 边界清楚，入口仍继承 RunType 骨架 |
| Insight 控制器 | plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md | 全文 486 行；另读共享 workflow-runtime.md | **不符合**：定义列 RunType，运行时按 cell/RunType 推进，未把 Workflow 定义为 Run 列表 |
| I0 Meta | plugins/haipipe-toolkit/skills/insight/workflow-phases/haipipe-insight-meta/SKILL.md | 全文 93 行 | 部分符合：仍称 workflow phase，metadata.phase 未标为兼容字段 |
| I1 Question | plugins/haipipe-toolkit/skills/insight/workflow-phases/haipipe-insight-question/SKILL.md | 全文 125 行 | **不符合**：称 I1 为工作流阶段，同时明令 runs 禁用；未说明其在 Workflow Run 列表中的身份 |
| I2 Data | plugins/haipipe-toolkit/skills/insight/workflow-phases/haipipe-insight-data/SKILL.md | 全文 102 行 | 部分符合：Run/Result 溯源边界明确，I2 仍使用 live phase 名称和字段 |
| I3 Information | plugins/haipipe-toolkit/skills/insight/workflow-phases/haipipe-insight-information/SKILL.md | 全文 87 行 | 部分符合：推导 Run 与 Page closure 分得清，仍使用 live phase 标签 |
| I4 Knowledge | plugins/haipipe-toolkit/skills/insight/workflow-phases/haipipe-insight-knowledge/SKILL.md | 全文 85 行 | 部分符合：可选稳健性 Run 有独立目的，I4 的实际 Run 身份未定义 |
| I5 Wisdom | plugins/haipipe-toolkit/skills/insight/workflow-phases/haipipe-insight-wisdom/SKILL.md | 全文 104 行 | 部分符合：签名与外部 RF 边界清楚，I5 仍以 Phase/Folder 表达流程位置 |
| Task 侧边界 | plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/SKILL.md | 全文 237 行；另读四个 ref 文件和 agents/openai.yaml | 部分符合：riNN 是真实 Run，checkpoint 与 Run 有区别；仍有 Phase × Run 标题 |
| Task 侧入口过程 | plugins/haipipe-toolkit/skills/task/haipipe-task/fn/insight.md | 全文 68 行 | 过程文件，不另计 Skill；返回值仍写 Page phase |

完整阅读的 Insight 支持文件：haipipe-insight/ref/page-v2-adapter.md、ref/partition.md、ref/question-groups.md。Task Insight 支持文件：haipipe-page-insight/ref/instance-items.md、ref/workflow-table.md、ref/task-calls.md、ref/migration.md。另为核实共享模型与跨族交接，全文阅读了 task/haipipe-workflow/ref/workflow-runtime.md，并检查了 page/haipipe-page-workflow、page/haipipe-page、board/haipipe-folder、design/haipipe-design-workflow 和 design/haipipe-design 的相关契约段落。

**排除及缺口：** CHANGELOG.md 属版本史，多个文件明言运行时不加载；它们未作为当前操作契约逐份全文审阅，只检索了 Phase/Run 迁移的历史线索。Task Insight 的 scripts/insight_items.py 与 scripts/test_insight_items.py 已确认存在，但未阅读或执行；本报告评价文档承诺，不背书实现行为。没有打开第三方参考子模块、真实 Board 数据或媒体资产。共享 Workflow Runtime 在 workflow-runtime.md:3 链接的根文件 WORKFLOW-DESIGN-PRINCIPLE.md 当前树中不存在；该文件未能阅读，但下方 Runtime 契约本身已全文阅读。

## 3. 总体判断与应保留的写法

这组说明并非缺少术语，而是术语定义重叠：Run Spec 是可复用执行合同，Run 是有 Ticket、Input/Target、Execution、Result、Receipt 的具体工作单元；Workflow Runtime 又保存多个 Run 的状态。Insight 再以问题—分区 CELL 作为前沿，并把 Page workflow pass 嵌套在 Run 里。文档对局部差异写得认真，但顶层仍把六个 I# 分类写成 Workflow 主体，读者不易判断“下一项”是 Run、Folder Page、Gate，还是一个队列 cell。

值得保留的部分：

- 入口用显式路由表列出 Task 与 Application-context 两条路径，并规定路径/上下文有歧义时停下来问，不猜测也不创建重复项：haipipe-insight/SKILL.md:65、:73。
- Task Insight 区分 rNN（可复用方法）和 riNN（新数据绑定），且明确不把每个工具调用、数据行或 finding 算成 Run：haipipe-page-insight/SKILL.md:64、:74、:117、:121。
- 证据图与语义父行分开：Supporting Run Result → frozen Local Input → local Evidence Run → typed Result；PARENTS 只说明 finding 如何解释已授权父行：ref/page-v2-adapter.md:32、:51、:65。
- RF 与 Design Handoff 没混为一谈。Task RF 只是 consumer-neutral evidence；Application I1/I5 还需注册问题、做本地适用性判断并由人签名：haipipe-page-insight/SKILL.md:210、:212；haipipe-insight-wisdom/SKILL.md:82。
- Task 侧区分 supported null 与 insufficient evidence，并要求独立检查准确的 frozen Result：ref/instance-items.md:148、:199。这是可复用的证据质量边界。

### 可读性与人机互动评语（非单列缺陷）

入口先给出 “one public door, two Insight scopes” 和可操作的 route table，信息顺序有效：先决定 Task 或 Application-context，再加载 owner（haipipe-insight/SKILL.md:20、:65、:73）。六个 I# 合同也遵循一致的 Position / Input / Page Face / Task Face / Gate / Handoff 骨架，便于 agent 按同一顺序执行。

主要认知负担来自 Run、RunType、Workflow Runtime、Page Run、CELL、Question Group、GI、RI、Supporting Run 等词集中出现，并在入口和控制器中反复交叉引用；这与 P1 模型问题相连，不另算一项已证实的语义缺陷。适合在唯一的规范词汇表定义这些对象，再让路由入口只显示当前用户的下一步。人机互动方面，SURVEY Decide、逐 Run release、mode: copilot、本人签名和 blocked gate 的停止回应都有明确边界；这些规则应保留。auto charter 缺模板的问题见 P2。

## 4. 优先问题

### P1 — Application Insight Workflow 还不是 Run 清单/依赖图

**证据。** 控制器写道：

> Workflow Definition = I0..I5 RunTypes + Run Specs + GI policies + Routes

见 haipipe-insight-workflow/SKILL.md:51。该 Skill 特别说明 RunType 是 “RunType vocabulary, not a runtime instance”（:38、:40）。运行时先选 Question Group/CELL，只有 “when work is needed” 才 materialize 一个 owner-native Run（:58、:60）；dispatcher 的步骤是选 cell、加载 RunType skill、对一个 Page 做 Page workflow PASS（:373、:377、:378）。因此，定义列表、当前运行位置与实际 Run 身份不是同一个单位。

共享 Runtime 契约把 Workflow Definition 定义为 Run Specs、从其 Routes 编成的图及 completion policy；Runtime 才包含 concrete Run instances；run_type_id 是可复用行为契约，run_id 是具体执行：task/haipipe-workflow/ref/workflow-runtime.md:10、:15、:21、:130、:132。设计族也提供对照：每个独立 Run Spec 是工作流一行，运行时物化 Run Instances；Steps 不另建 Run：design/haipipe-design-workflow/SKILL.md:48、:54、:61。

**影响。** Agent 可能把 I2 当成一次运行，即使它只是选了 Folder 类型并启动 Page pass；也可能把 CELL、GI gate 或整个 Insight RunType 误报成 Run。状态回应要求报告 current RunType 和最高 GI，而不是明确 owner-native Run id（haipipe-insight-workflow/SKILL.md:404）；这会让人误以为 Board 有一个“当前阶段”，尽管文档正确指出不同 cell 可以同时处于不同位置（:110、:112）。这不只是术语问题，还关系到运行记录、复用、统计和待办决策。

**建议。** 先定真实 Run 粒度。Workflow Definition 应由可复用 Run Specs、依赖/Route 图和完成条件组成；Workflow Runtime 持有本次具体 Run instances、状态和 Gate/Route receipts。每个 Run 必须有 bounded target、owner-native Run Spec/Ticket、输入、Result、receipt 和退出条件。Question Group/CELL 可保留作调度/状态投影，但不是执行身份。不要把 I0–I5 序号继续当阶段或默认映射成 RunType；逐项按真实所有者和产物，决定它是完整 Run、Run 依赖，还是不生成 Run 的控制记录。没有独立 Ticket→Result→Receipt 的 Page pass、register edit、GI 检查、Step 或工具调用，不得因换了名字就变成 Run。Workflow 的进度由 Run 状态及依赖条件表达，不设当前 Phase。

### P1 — 六个 I0–I5 合同仍以 Phase 作一等身份；I1 还明令不建 Run

**证据。** 六个 Skill 都位于 skills/insight/workflow-phases/，description 仍分别说 “workflow phase I0…I5”，frontmatter 有 phase: I0…I5。例子：Meta 的 haipipe-insight-meta/SKILL.md:4、:13、:36；Question 的 haipipe-insight-question/SKILL.md:4、:13、:37；Wisdom 的 haipipe-insight-wisdom/SKILL.md:4、:12、:32。Data 还写 “This phase may commission…”（haipipe-insight-data/SKILL.md:65）；Information、Knowledge、Wisdom 把 PARENTS 称作 phase-owned；Question Task Face 使用 “phase receipts”（haipipe-insight-question/SKILL.md:84）。其中最难与要求并存的是 Question 合同：I1 被定义为 Workflow 位置（:37），又规定 runs 和 code forbidden（:99）。

haipipe-insight-workflow/SKILL.md:64、:68 确实把既有 phase 字段称为 compatibility/display labels；这足以保留那些明确标成兼容的持久字段，但没有把六个 Skill 自身的 phase 元数据、workflow-phases 目录或 “workflow phase I#” 描述宣布为兼容。page-v2-adapter.md:13、:53 也仍称 Folder kind / PARENTS 为 phase-owned。partition.md:59 以 “Folder phases” 介绍布局。这些是当前指导语，不只是历史记录。

**影响。** Agent 在编辑 Skill 或 Page 模板时会收到多套 authority：外层规定 I0–I5 RunType，内层规定 I# workflow phase，共享 Folder 契约又把 phase 视为 Folder identity。目标模型没有 Phase 这一层；这些冲突不能靠挑一套 Phase 权威解决。把六个目录机械改成 runs/ 也不正确：这些合同中的 Folder/Page、证据、注册表、Gate 与支持性计算生命周期不同；例如 I1 禁止 Run。应逐项按其真实 owner、持久产物和执行结果重组，并为确实执行了工作的项定义 Run 合同；没有独立执行结果的动作就明确是控制记录或状态更新，不虚构 Run。

**建议。** 对六个合同逐一按 owner 与结果建模：真实的独立执行工作定义 Run Spec 并生成 Run；Folder kind、Question 注册、Gate 判断等按各自资源/控制记录建模，不套在 I# 生命周期里。移除 live 文案中的 Phase 概念、phase frontmatter 和 workflow-phases 的组织语义。持久数据或旧 reader 若短期仍依赖 `phase` 字段/路径，只能作为明确标注、无业务 authority 的兼容映射，给出版本、读写限制和迁移期限；不能把它保留为当前状态、Folder 身份或运行进度。

### P1 — 控制器称“它签署”手递，同时把 Handoff 叫作 Design 的 Brief

**证据。** haipipe-insight-workflow/SKILL.md:18 说此 Workflow 是 I0–I5 与 GI0–GI6 的 authority；:19 接着说 “it signs the W handoff”；:20 又说 Design Workflow 把它 “takes as its Brief”。但同一控制器明确规定 signed: 必须是 ✅ <initials> <YYMMDD> 且不能由机器写入（:321）；Wisdom 合同要求签名未完成时停止（haipipe-insight-wisdom/SKILL.md:82、:85）。

**影响。** 控制器段落的语法主语是 “it”，新上下文 agent 可能以为 Workflow/agent 会给 W 写签名。这直接越过明确的人类权力边界。Brief 一词也可能让人误以为 W Handoff 取代 Design Brief。Design 族的实际契约把 Goal/Brief 与 Insight 支持分开；Design Item 的 evidence 文件使用 handoff role，界面显示为 “signed insight”（design/haipipe-design/SKILL.md:58、:62），Commission 冻结 exact evidence file hash（design/haipipe-design-workflow/SKILL.md:86、:92）。

**建议。** 改成 “the workflow verifies and records a person-signed W handoff; Design consumes its exact signed version as Insight input.” 由人提供签名；Insight controller 只验证签名与 GI 条件、记录 receipt。把 “Brief” 改成 “Insight input” 或 “handoff evidence”，Design 的 Brief/Goal 仍归 Design 管理。

### P2 — 当前入口指向磁盘上不存在的 procedure 与 Application owner

**证据。** 入口动词表写着 “the umbrella's fn/meta.md”、“the umbrella's fn/question.md”、“the umbrella's fn/chain.md” 和 “the umbrella's fn/verdict.md”：haipipe-insight/SKILL.md:247、:249、:251、:255。当前 haipipe-insight/ 目录只有 SKILL、refs、agent descriptor 和 changelog，没有这些 fn/ 文件。相同 Skill 还说物理路径在 skills/application/（:35），但当前 Skill 实际在 skills/insight/，当前树没有 skills/application/；ownership map 另有未定义的 application-wf（:348），当前树也没有 haipipe-application-workflow/SKILL.md。

**影响。** Agent 按 entry 动词表继续加载 procedure 会遇到磁盘缺口；更重要的是，不知道 cross-board receipts/handoffs 归 Insight、Design 还是所谓 Application workflow。这与 Insight 和 Design 为独立一等技能族、没有 Application 父族相冲突。Application 作为应用上下文仍可保留，但不应看起来是父技能族。

**建议。** 逐项检查这些动词的当前 inline procedure / owner Skill；把链接更新到真实文件，或恢复对应 procedure 后再保留引用。物理路径改为真实 skills/insight/。用明确的 Insight 与 Design owner 替换 application-wf；如它实际是通用控制器，写出真实 Skill 名与责任，不创建虚构 Application 父族。

### P2 — Task Insight 的“Phase × Run Map”标题与工作内容模型相反

**证据。** Task Insight 说 checkpoint/workflow 位于 ref/workflow-table.md，页面作者仍用共享 Page workflow，DIKW 在 item Result 内、不是四个 phase-owned Folder（haipipe-page-insight/SKILL.md:149、:152）。但同文件把表称作 “Phase × Run Map”（:150、:231），参考文件列头是 Phase / Folder / episode / Allowed Run operations / Cardinality（ref/workflow-table.md:25、:27）。Task route 最后返回 “next item checkpoint/Page phase”（haipipe-task/fn/insight.md:66、:67）。

表本身区分得很好：Scope/Plan 的 Run cardinality 为 0，Bind/Evidence 列依赖 Runs，Reason/Publish 才有 riNN Insight Run；也明确 checkpoint、LLM call 与 rendering pass 不是额外 item/Run：ref/workflow-table.md:29、:31、:37、:38。因此这里不应把每个表格行改称 Run。问题是 “Phase” 仍把读者导向阶段式 Workflow。

**影响。** 严格的 Workflow-as-Runs 说法和这个表名并列时，使用者难以判断每行是 Run、Run 内步骤，还是 Run 前后的控制活动。Task 侧的主要优势——checkpoint 不是 Run、dependency Run 有自身身份、RI 只是 DIKW 工作——会被标题削弱。

**建议。** 改表名为 “Workflow activities × Run ownership” 或 “Run inventory by workflow activity”；将列头 Phase 改为 Workflow activity。说明这些行是操作/检查点映射，不是 Runs；实际 Workflow Run 清单列准确的 riNN、Supporting Runs 与 local Evidence Runs。Task 返回词改为 “next item checkpoint or Page workflow action”。共享 Page controller 的 `phase(...)` 若暂时受旧调用方依赖，只能作为待移除的兼容 API，不能在新文档、新记录或状态回应中呈现为领域概念。

### P2 — per-run auto charter 有权限范围，但缺少可执行的签发与核验格式

**证据。** charter 段落写道：“A charter names the run, the classes, and the expiry (the run's close); its receipt quotes it” （haipipe-insight/SKILL.md:365）；可预授权类别及不可 charter 的动作见 :358、:361。这里没有 charter 样例、receipt 路径、固定字段或核验步骤，也未说明如何绑定 workflow_runtime_id、Run ids 和 Board。

**影响。** Agent 知道哪些类别“原则上可授权”，却不能稳定判断现有文本是否覆盖当前修改、何时过期、应把什么写入哪条 receipt。过窄会反复打断；过宽会把含糊同意延伸到后续 cell。

**建议。** 给出由人填写、机器只能核对的简短模板：授权者、Insight Board、Workflow Runtime、精确允许类别、禁止类别、目标 Run/cell 范围、截止条件、签署时间与 receipt 地址；每次引用时记录对应授权条款。若共享运行时没有稳定记录/核验路径，应暂时移除 charter 路径，保留逐次 SURVEY Decide 与人签名。

## 5. Workflow/Run 指标汇总

下表逐项给出八个初始 Insight Skill 的判定；Task-side haipipe-page-insight 作为补充边界 Skill 另列。

| Skill | 判定 | 依据 |
|---|---|---|
| haipipe-insight | 部分 | 路由 Task riNN、Application RunType、非 Run 的 Question Group；没有 Application Workflow 的 Run 清单 |
| haipipe-insight-workflow | **不通过** | 定义列 RunTypes 和控制策略，Runtime 以 cell/RunType 定位；仅按需生成具体 Run |
| haipipe-insight-meta | 部分 | I0 仍是 workflow phase/metadata.phase；Meta 是 Folder/Page，不承诺独立 Run |
| haipipe-insight-question | **不通过** | I1 被当作阶段，却禁止 runs；未说明它是 Workflow 外控制记录还是应有 Run |
| haipipe-insight-data | 部分 | 来源与计算 Run/Result 边界清楚；I2 的 live phase 身份未迁移 |
| haipipe-insight-information | 部分 | 可选推导 Run 与 Page closure 分得清；I3 仍是 phase-owned Folder 合同 |
| haipipe-insight-knowledge | 部分 | 可选稳健性 Run 有独立目的；I4 的实际 Run 身份未定义 |
| haipipe-insight-wisdom | 部分 | 人签手递与 RF 边界清楚；I5 仍用 Phase/Folder 表达流程位置 |
| 补充 Skill haipipe-page-insight | 部分 | riNN 有 ticket、Result、receipt；checkpoint 与 Run 分开，但保留 Phase 标题 |

**整体 Workflow/Run 判定：不通过。** Task 路线在 Insight Item 的具体 Run 身份上符合得较好；Application Board 路线的核心控制器不符合。因为 I0/I1 等具体合同仍将无 Run 的工作描述成 Workflow Phase，不能通过全局字符串替换修复。Design 族可作为“Workflow 直接由 Runs 与依赖关系表达”的对照；Insight 与共享 Folder owner 需逐项决定哪些工作具备 Ticket/Result/Receipt Run contract，哪些是独立资源变更或控制记录。目标模型中不保留 Phase 层。

### Compatibility 与历史用语的划分

不要把以下明确兼容/历史内容误作 live 概念：

- haipipe-insight-workflow/SKILL.md:68 明说既有 phase 字段是 compatibility/display labels；共享 Page controller 也说 phase(...) 是进度组调用，不是 Run identity（page/page-workflows/haipipe-page-workflow/SKILL.md:57、:61）。若迁移期间仍需这些低层字段/API，它们只能是有期限、无业务 authority 的兼容机制；目标文档与新记录不再使用 Phase 概念。
- page-type: 在 Insight contracts 中是旧键；page-v2-adapter.md:97、:98、:99 将其写成 read-only compatibility。9-X-cross/、旧 probe/、items-v1 与旧 #rNN@vNNN 地址也明确定义为可读历史，不能盲改。
- 相反，workflow-phases/、六个 frontmatter phase: I#、各 description 中的 “workflow phase”、Task 表的 “Phase × Run”，以及 page-v2-adapter.md 对新页面的 workflow/phase.yaml 说明都未一致标成 compatibility。它们目前仍是当前契约/schema 入口，所以是必须迁移的 live 遗留；迁移完成前应显式收窄其 authority，最终从领域模型中移除。

共享 Folder contract 把 workflow/phase.yaml current.folder-kind 说成 authoritative in-place identity，且记录 current.phase 与转换历史：board/haipipe-folder/SKILL.md:58、:61、:264、:272；共享 Page Workflow 却说文件名不创建 Phase authority，phase 只是 controller label：page/page-workflows/haipipe-page-workflow/SKILL.md:57、:59、:111、:113。这是共享 Folder/Page owner 的模型冲突。目标上应把 Folder kind 与 Run/控制记录分开；旧文件名、字段和调用只能通过无 authority 的兼容映射迁移，不应由 Insight 单族自行改 schema。

## 6. 代表性桌面走查

以下均为基于文档的假设请求，**不是**现场用户行为观察，也没有运行实际技能。

### A. 用户提出 dataset-first 的观察问题

**假设请求：**“在 cohort-v3 这个数据集里看看响应模式和限制。”

**文档应导出的路径：**路由表将 dataset-first topic 送往 Task-side Insight Page；搜索同 topic/data context 后复用或创建 Page，新增一个 riNN intent，绑定快照与目标。执行者先在 SURVEY 选 Supporting Run Results，再走本地 Evidence Run；不会因为提到 topic 就执行整项 Task（haipipe-insight/SKILL.md:69、:95；haipipe-task/fn/insight.md:38、:40）。

**更清楚的预期回应：**“这听起来是 Task-side Insight。我会先查找同一数据上下文的 Insight Page；如果有唯一匹配，就在那页新增或续接 item。‘响应模式和限制’可作为一个 Wisdom-targeted riNN。当前还需确认 cohort-v3 的不可变快照版本；确定后我会先列出支持数据的来源和执行身份，再请你决定是否释放新的 Supporting computation。”

**检查点：**source rerun 会让依赖的 Insight rows 与 Synthesis stale，不自动改写结论；riNN Ticket/receipt 才证明 Run 已分配。若 Board 上有两个同名 context，应询问而非猜测。

### B. Application-context InsightBoard 要比较一个新分区

**假设请求：**“在这个 InsightBoard 上判断 A/B 两组能否共用同一条建议，然后更新 handoff。”

**文档应导出的路径：**定位 Application-context InsightBoard，读取问题注册表、已有 Run 实例及其依赖/待决项。若尚无对应问题记录，先执行 owner 定义的注册表更新；这项更新只有在有独立 Ticket→Result→Receipt 合同的情况下才算 Run。问题需要比较多个分区时，建立明确的比较目标与所需输入依赖。输入缺失时先说明缺口并等待 SURVEY Decide 对新 computation 的决定。每次 dispatch 应指向一个具体 Run id/目标；Page CHECK/CLOSE 本身不推进 GI。

**更清楚的预期回应：**“当前没有可完成的比较 Run：目标需要 A、B 两边已接受的 Information rows，目前缺 B 侧本地 Evidence Result。我会列出精确缺失输入和依赖它的 Run；是否授权创建这项 Supporting Run？现有 Run 的状态与结果不会因这个缺口而被覆盖。”

**检查点：**文档有足够的 gate、stop 与返回要求。状态报告应以 Run id、状态、目标和阻塞依赖为主；Question Group/CELL 可作为辅助定位视图，不能代替 Run identity。现有文档主要写 current RunType，故此例仍受 P1 模型缺口影响。

### C. Task RF 请求直接用于 Design

**假设请求：**“把 patient-study 的 RF1 用于这次 SMS。”

**文档应导出的路径：**核实 exact Task instance + riNN@vNNN + Wisdom target + RF id + Result path/hash + accepted review；在 Application I1 QW 注册此来源，再在本地 I5 W 做适用性判断、完成 local Evidence Run、写 serves: 与禁止越界。RF 不能直接绑定 Design；只有本地已签名且 I1 GI6 已结算的 Handoff 才能被 Design 消费。

**更清楚的预期回应：**“RF1 是已接受的 Task finding，但它本身不是 Design Handoff。我会先将这个确切版本注册为 QW 的外部证据，再完成本地 Wisdom 的适用性、边界和设计后果。Handoff 草稿准备好后会等你本人签 ✅ <initials> <YYMMDD>；我不会代签或在此之前交给 Design。签名后还需结算 I1 GI6，Design 才能固定精确 path/version/hash。”

**检查点：**这是最强的权限边界之一；控制器顶部 “it signs” 的用词可能压过正文里更精确的人签规则。

## 7. Before / After 英文重写示例

以下改写保留原意，只调整有歧义的英文源句。

### 7.1 Workflow 定义：分开 RunType 与 Run Instance

**Before**（haipipe-insight-workflow/SKILL.md:51）

> Workflow Definition = I0..I5 RunTypes + Run Specs + GI policies + Routes

**After**

> Workflow Definition = reusable Run Specs + the dependency/route graph compiled from them + completion rules.  
> A Workflow Runtime records the concrete owner-native Run instances selected for this execution, their inputs, results, receipts, statuses, and dependency/gate decisions.  
> Each Run has one bounded target and one declared owner; categorization metadata may describe the work, but does not create a lifecycle layer.  
> Question Groups and CELLs remain derived scheduling/status views, never Runs. Workflow progress is derived from Run status and dependency conditions; there is no Phase object or current-Phase state.

这需要先为 I0/I1 等当前没有 Run identity 的工作按其产物和 owner 建模：若是可审计的执行工作，建立完整 Run contract；若只是注册表/Folder/控制状态变更，则记录为对应资源更新。不能只改名字就生成虚构 Run，也不能把旧 I# 顺序当作工作流生命周期。

**建议的执行方式。** 定义时先声明可复用 Run Spec 和有条件的依赖/Route；创建某个 Board 的 Workflow Runtime 时，仅物化本次需要的具体 Run instances。调度器按依赖就绪情况选择一个 Run id，而不是推进阶段或只返回 RunType。执行前固定目标与输入版本，并应用对应的释放/授权规则；执行后写入带来源的 Result 与 receipt，再由 owner/gate 检查它们是否满足完成条件。满足条件的下游 Runs 才变为 ready；缺输入、拒绝或失败以 Run 状态和明确依赖呈现。更新输入时保留旧 Run/Result 历史，并按依赖关系标出下游结果需重算或已过期。注册表、Folder、Page、Gate 等更新仍由其资源 owner 处理，除非它们本身被定义成有独立 Ticket→Result→Receipt 的执行工作。Workflow 仅在完成规则满足时关闭；若无可推进 Run 且存在明确阻塞，记录 held 并结束本次回应，保留续接状态。

### 7.2 Handoff 只能由人签名，且不是 Brief

**Before**（haipipe-insight-workflow/SKILL.md:19、:20）

> ... and it signs the W handoff that haipipe-design-workflow takes as its Brief.

**After**

> ... and it verifies and records the person-signed W handoff.  
> Design consumes the exact signed handoff as Insight input; its Brief and Goal remain Design-owned.

### 7.3 Task workflow 表命名

**Before**（haipipe-page-insight/ref/workflow-table.md:25、:27）

> ## Phase × Run Map  
> | Phase | Folder / episode | Purpose | Allowed Run operations | Cardinality | Gate / authority | Close |

**After**

> ## Workflow activities × Run ownership  
> | Workflow activity | Folder / scope | Purpose | Run identities used | Cardinality | Gate / authority | Close |

在表前补充：“Rows below describe resource updates, dependencies, or control/checkpoint activities; they are not Runs by default. Count only declared owner-native Run identities; checkpoints and dispatches are not additional Runs.” 这样保留 Scope、Bind、Evidence、Reason、Publish 等活动而不伪造 Run。

## 8. 跨族问题及责任归属

| 问题 | 证据 | 责任归属 / 协调建议 |
|---|---|---|
| workflow/phase.yaml 在 Folder 与 Page 契约中的身份不同 | Folder 把 current.phase/folder-kind 作为 in-place identity；Page Workflow 说 phase 是 controller progress label，文件名无 authority。见 board/haipipe-folder/SKILL.md:61、:264；page-workflows/haipipe-page-workflow/SKILL.md:57、:111 | 共享 Folder/Page owners 定义 Run 模型及旧字段映射；Insight 仅跟随明确的兼容合同 |
| Design 是 sibling family，W handoff 是 Insight 输入而不是 Application parent 或 Design Brief | 当前树有独立 skills/insight/ 与 skills/design/；design/haipipe-design/SKILL.md:58、:62 将它当 signed insight handoff；Design Workflow 明说无 Phase layer（:48）。Insight 仍提不存在的 skills/application/ 与 application-wf | Insight owner 修路由/ownership prose；Design owner 对齐 intake 名称。保留 Application-context 的含义，不建父族 |
| Page workflow pass 与 Insight Run/RunType 状态不能混用 | Page adapter 说 Page Run close 不关 Page/GI（insight/haipipe-insight/ref/page-v2-adapter.md:26）；共享 Page Workflow 说自动 Page pass 是 Workflow Runtime，不是 Page Run（page/page-workflows/haipipe-page-workflow/SKILL.md:65）；Insight dispatcher 把 pass 嵌在当前 RunType（haipipe-insight-workflow/SKILL.md:378） | Page owner 明确 controller Runtime label；Insight owner把具体 owner-native Run id 与嵌套 Page pass 分开报告 |
| Workflow Runtime 所依赖的 root principle 链接缺失 | task/haipipe-workflow/ref/workflow-runtime.md:3 链接根 WORKFLOW-DESIGN-PRINCIPLE.md，当前树未找到该文件 | Workflow contract owner 修复引用或收录必要原则；本次仍可按 Runtime Contract 审阅 |

## 9. 建议的修订顺序

1. **先定 Run 合同：** 定义 Run Spec 与 Run instance 必需字段、owner、target、输入、Result、receipt、状态、重试/版本和关闭条件；逐项判定 I0/I1 等目前没有 Run identity 的工作是可执行 Run，还是资源/控制记录。
2. **定义 Workflow Runtime：** 以 Run Specs 和依赖/Route/Gate 条件生成执行图；运行时按具体 Run id 追踪状态、输入、结果和收据。Question Group/CELL 仅作派生调度视图，不作为执行身份，也不设 current Phase。
3. **从领域模型移除 Phase：** 重组六个合同与目录，删除 phase frontmatter、phase-owned/live Phase 文案和 Task 表中的 Phase 轴；I0–I5 若仍有价值，逐项映射到明确的 Run Spec、资源类型或控制记录，不能默认继续作为顺序生命周期。
4. **迁移持久化与共享接口：** Folder/Page owner 定义 Folder kind、旧字段和旧路径的无 authority 兼容映射及移除期限；新记录、新接口不再暴露 Phase。对 workflow/phase.yaml、phase(...) 等遗留物逐项处理，不做历史数据的盲目字符串替换。
5. **修正手递与族路由文字：** 删除 “it signs” 的主语歧义，改称 Design Insight input；清理 skills/application/、application-wf 等过期 owner 引用，确认 Application-context Insight 不是父技能族。
6. **修复失效操作链接并复核：** 恢复或更正 fn/meta.md、fn/question.md、fn/chain.md、fn/verdict.md 的引用；最后检查路由、Run identity、Page pass 嵌套、Evidence/semantic lineage、partial-final、Design intake 与签名/settlement。旧字段按迁移映射处理，不对历史 Board 做全量字符串替换。


## 10. 已执行的更新与验证（2026-09-20）

本节记录用户确认实施后的源码更新；之前“仅写报告”的边界是评估快照。

### 当前模型与实现

- Insight door/controller 直接定义 Run Specs、依赖/Route、真实 native Run inventory、Result/receipt 和完成条件。Meta/Question/DIKW 是资源类型；GI 是有明确 owner 的断言。没有 Phase 对象、current Phase 或六个默认 Run。
- 六个资源技能迁到 `plugins/haipipe-toolkit/skills/insight/folder-kinds/`，去掉 phase metadata，继续使用原技能名。每项工作引用真实 Page/Task/Discovery Run 合同，控制动作不生成伪 Run。
- 新增 [Run 工作流合同](../../plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/run-workflow.md)，包含具体 Spec 模板、可解析的 Definition/Runtime 示例、按需创建、精确复用、共享计算只计一次、held/complete 边界、依赖失效和原生重试/版本语义。
- 新增 [迁移规则](../../plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/migration.md) 和 [授权记录格式](../../plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/authorization.md)。只注册问题可在 `runs: []` 下完成；签名固定到完整 payload，证据/verdict 版本变化也需重新签署。
- Folder 发现器支持 `folder-kinds/`；身份读取采用 `workflow/folder.yaml current.folder-kind`，旧文件只在新记录不存在时提供 Folder kind 的只读导入。无效 canonical 记录、重复 kind 和与 Page 的冲突不会静默回退。Page/Board 的相关调用已同步。
- Board Workflow map 展示 Run Spec 模板和 Folder 资源表；Run Space 读取 aggregate Runtime 的 native ids、依赖、Result/receipt、control-only 工作和就绪/等待项。重复或缺失身份显示读取错误；新增、修改、删除 Runtime 文件会刷新投影。
- 修正 Task Insight 的旧表名/返回词、失效 procedure/父族指向和共享 Runtime 的缺失根文件链接；hand-off 保持由人签署、Design 消费确切版本的边界。

### 验证结果

- Board/Folder/Insight 相关测试 **92 项通过**：Folder owner 发现与身份兼容、Context 路由、Page owner ruling、Insight 签名检查、Run inventory 显示与缓存刷新、重复身份/伪分配拒绝、零 Run 控制记录、Plan Shape 和 RI 集成。
- Task Insight item 测试 **25 项通过**，合计 **117 项**。
- **14 个修改过的技能**通过 skill-creator 格式校验；新 YAML 示例可解析；Insight 的 **6 个 Folder contracts 无 findings**。
- 全库 Folder 检查仍有 **1 个既有 Discovery finding**：`haipipe-discovery-inquiry` 的 `workflow` 字段不以 `-workflow` 结尾。已用 HEAD 的原始校验器在该未修改 Skill 上重现；本次没有放宽检查或修改 Discovery 来掩盖它。
- 独立新上下文走查覆盖：复用证据并续接已有 Writing Run、增加分区后的 X/W 依赖失效、仅注册问题。发现的注册完成条件、签名更新和 Page policy 链接问题均修复，并经同一独立检查者复核。
- 相对 Markdown 链接检查及 `git diff --check` 通过。

### 实施范围

本次更新仓库内技能、共享解析器、相关只读界面与测试；没有运行真实 Insight 分析或改写实时 Board。存量 Board 保留原结果与签名历史，后续按迁移规则处理。指向旧技能物理路径的外部安装链接需通过正常安装流程刷新；本次没有重新安装外部环境。底层 Page 引擎仍有历史命名的 adapter 字段，未将它们作为新的领域概念或执行身份。
