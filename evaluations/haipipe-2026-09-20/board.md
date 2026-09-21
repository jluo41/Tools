# HAI-Pipe Toolkit Board 评估

**日期：** 2026-09-20  
**评估范围：** `plugins/haipipe-toolkit/skills/board/` 当前有效技能与直接支持材料  
**评估基线：** `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`

## 摘要

Board 家族能说明 Board 如何登记 Page、维护成员顺序、选择领域 owner，以及把页面内容问题交给 Page/领域技能处理。`haipipe-board-routing` 对 Board 状态、职责范围和人工审批边界的说明清晰；DesignBoard 也确实有可查看的跨 Folder 运行记录。

当前总体判定：**FAIL**。最重要的问题是 `haipipe-folder` 仍将 Phase 定义成工作流身份、表格行粒度和 Folder owner 配置；这与共享 Run 合约冲突，而且 Page 的 Folder parser 仍实际读取这些字段。另有三类直接影响用户操作的矛盾：审批规则把机器 `checked` 当作足以继续的条件；DesignBoard 文档要求 `adopt`，而当前 UI/投影用 `ready`；Board 文档中的 Page Run ID 与当前 Page owner 的 ID 规范不一致。

**Workflow / Run 总判定：FAIL。** 四份 Board `SKILL.md` 中：一份 FAIL（Folder），两份 PARTIAL（Board 主技能、DesignBoard），一份 N/A（Routing，不定义 Workflow）。Board 文件应把 Workflow 作为 Run Spec 图来引用，但仍须把 controller 坐标、步骤、工具调用和人工 gate 留在各自的内部语义中，不能机械地把所有出现的 `phase` 字符串都改成 `Run`。

## 覆盖范围与方法

| 检查对象 | 覆盖情况 | Workflow / Run 结果 | 说明 |
|---|---|---|---|
| [`haipipe-board/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md) | 全文，332 行 | PARTIAL | Board 路由、结构、状态、命令、审批和示例 |
| [`haipipe-board-routing/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md) | 全文，265 行 | N/A | 路由是操作程序，不是 Workflow 定义 |
| [`haipipe-folder/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md) | 全文，305 行 | FAIL | Phase 仍是活跃身份和 Workflow 表格粒度 |
| [`haipipe-plugin-design-board/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/SKILL.md) | 全文，218 行 | PARTIAL | 有跨 Folder Run ledger，但工作流仍称 Adopt 为步骤/状态 |

另读了 Board `README.md`；主 Board 的 `ref/board-form.md`、`ref/operations.md`、`ref/writing-rules.md`、`ref/board-example.md`、`ref/insight-space-mapping.md`、`fn/serve.md`；Page lifecycle workflow 实现；routing lanes 和 regroup 实现；Board agent、reviewer、auditor、creator、approver 文件及 approve-rules；Folder/Board parser 和状态、DesignBoard 投影相关实现。

为核实跨家族边界，定向查阅了共享 `haipipe-run` 合约、Page workflow 及其 workflow table、Page outline/template，以及 Design workflow、Design 和 Design brief 中与本报告发现相关的段落。这些定向片段用于判定 owner 合约冲突，不作为对这些技能的完整评估。

**未执行**技能、测试、服务、浏览器或实时用户流程；下文的交互检查是依据当前文档和代码的**桌面走查**，不是运行时或用户测试。历史 changelog 仅用于区分当前语义与历史兼容；未评估 legacy 内容、tests、fixtures、vendor 或 bulk assets。Board 侧未找到 `ref/page-template.md`；现行 canonical Page 模板位于 Page owner 目录。工作区原有未提交改动涉及其他技能/报告，未作为 Board 缺陷，也未更改。

## 发现

### P1 — Folder 仍把 Phase 当成 Workflow 身份和 Run 表格行

**证据：** [`haipipe-folder/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md) 第 4–12 行将 Folder 描述为 “a domain workflow phase”，并列出 authoring a workflow-phase skill、Phase × Run Map；第 44–64 行把一个 domain workflow phase 列为 Folder 一种、将 `workflow/phase.yaml` 定义成当前 Phase 身份和转换；第 140–144 行规定 Workflow Table 的行粒度为 `Phase/Cycle`；第 161–173 行要求技能元数据 `phase: I4`；第 195–210 行继续以每个 Phase 的 Run Profile 和 Phase × Run Map组织定义。

共享 [`haipipe-run/SKILL.md`](../../plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md) 第 193–210 行明确 Workflow Definition 是有向 Run Spec 图，且没有独立 Phase authority；第 226–255 行规定 Workflow 表每行对应一个可独立结束的 Run Spec，而非 Phase、Step 等。Page `folder_contract.py` 第 54–80、116–168 行当前仍读写/校验 `metadata.phase` 与 `current.phase`；Board `foldercontracts.py` 第 42–52 行仍打印 Phase contract。因此这不是只留在历史材料中的命名，而是会影响当前 Folder 身份、schema 校验和路由的契约冲突。

**影响：** 创建 Folder 或编写领域技能的人会被引导先定义阶段身份和阶段转换，再把 Run 映射进去；与共享 Run Spec owner 合约不一致。不同技能可能对何者是可关闭工作单元、何者只是控制器坐标做出不同决定。parser 同时依赖这些字段，所以只改文案也会制造“文档新 schema、解析器旧 schema”的破坏性漂移。

**建议：** 将 Folder owner 模型改为“领域 Folder 的 Workflow 声明 Run Spec 图；领域技能定义各 Run Profile”。Workflow 表行粒度应为 Run Spec，并描述 bounded target、Run Type、cardinality、acceptance rule。Steps、tool calls、snapshots 和 human gate events 除非单独满足 Run 合约，否则留在所属 Run 内。需要与 Page owner 一起迁移 parser、schema、CLI 输出和示例。迁移前明确记录兼容期：序列化字段 `phase`、`cycle`、`next_cycle` 和旧物理路径 `workflow/phase.yaml` 仍是 controller/compat labels，不因此恢复 Phase authority；不能做全局字符串替换。

### P1 — 机器 checked 被写成可越过人类审批的放行条件

**证据：** [`agents/approve-rules/README.md`](../../plugins/haipipe-toolkit/skills/board/agents/approve-rules/README.md) 第 77–81 行写明 “The RUN does not wait for the human field”，仅凭 `checked: ✅` 即可继续；[`haipipe-page-approver-agent.md`](../../plugins/haipipe-toolkit/skills/board/agents/haipipe-page-approver-agent.md) 第 24–29 行称 `checked` 会释放 “next phase”。同一 approver 文档第 111–115 行又明确 agent 不能写入 Folder owner ruling 或人工 tick。

当前 Page owner [`haipipe-page-outline`](../../plugins/haipipe-toolkit/skills/page/haipipe-page/page-workflows/haipipe-page-workflow/SKILL.md) 第 573–583、593–607 行规定：证据阶段在某些情况下可先继续，但机器 checked 不释放 CONTENT；需要人的 gate 必须由人批准，Auto 模式对 CONTENT 同样执行该约束。Page workflow table 第 182–185 行也区分 controller 行与真实 Run 实例。

**影响：** agent 或操作人会把机器检查成功误读为人工已同意，尤其可能让内容生成绕过 CONTENT release gate。文档一边不允许 agent 写人的决定，一边又将 `checked` 描述成推进许可，用户无法据此判断哪些工作可以继续、哪些必须暂停。

**建议：** 统一写成：`checked:` 记录机器检查结果；它只允许 owner Run Spec 和当前 mode 明确允许的后续工作，不能替代 person-reserved release gate。逐条注明审批对象、可提前进行的证据工作、需要暂停的内容工作，以及谁能写入人工批准。把 approver 的 “next phase” 改为准确的 owner-defined next Run / permitted work，并避免将 controller 坐标写成领域阶段。

### P1 — DesignBoard 的 Adopt 指令与当前 ready/Delivery 状态不符

**证据：** [`haipipe-plugin-design-board/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/SKILL.md) 第 48–49 行把流程列为 Commission、Generate、Verify、Adopt；第 64–66、87–90、107–124、144–164 行持续将任务/Run/交付描述为 `adopted`，并说明 adopt 操作。其支持映射 [`ref/space-mapping.md`](../../plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/ref/space-mapping.md) 第 5、9–13、34–35、68 行也复述 Adopt 状态。

当前投影代码 [`live/design.py`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py) 第 38–39 行将 `adopt` 映射为 Delivery，并注释这是 legacy storage；第 514–520 行以独立 Verify 通过作为 Delivery gate，旧 adopt 记录可保留但不要求；第 715–718、880–882 行将 ready 基于 Verify 推导，旧记录映射到 Delivery。UI [`live/designboard.py`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/live/designboard.py) 第 301–303、417–420、475–494 行展示 ready 任务并在导出中发送 `state=ready`。代码审阅显示文档与现行投影语义不一致；未启动 UI 实测。

**影响：** 用户可能以为 Verify 后必须执行一个不存在的 Adopt Run，或认为 CSV 会输出 `state=adopted`，从而漏掉已经完成的交付或误判批次状态。

**建议：** 将现行 workflow 描述为 Commission、Generate、Verify 的 Run Spec 图；Verify 通过后 Delivery 是只读交接，不要求额外 Adopt Run。新文档、截图和 CSV 示例使用 `ready`。只将历史 `adopt` 记录称为兼容记录，并说明 UI 把它归到 Delivery。DesignBoard 行里的 `step` 应标为 Run action/type，避免把交付操作误认为每一个工具调用都是 Run。

### P1 — Board 主技能中的 Page Run ID 规范过时

**证据：** [`haipipe-board/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md) 第 42–45 行把 `rp00_mermaid-structure` 与 `rpNN_pNN[-pNN]` 描述为当前命名；第 247–250 行把 `rp00` 结构 Run 作为活跃例子。当前 Page workflow owner [`haipipe-page-workflow/SKILL.md`](../../plugins/haipipe-toolkit/skills/page/haipipe-page/page-workflows/haipipe-page-workflow/SKILL.md) 第 130–145 行使用 `rp-struct-NN`、`rp-scratch-NN`、`rp-sec-NN`、`rp-para-NN_Pxx[-Pyy]`，其中 `rp-struct-01` 是当前结构 Run 示例。Page owner 将 compact ID 作为历史只读格式；Page renderer 也带 legacy 识别路径。

**影响：** Board 用户根据技能新建或识别 Page Run 时，容易写入当前 renderer/owner 不承认的 ID，或把历史格式误认为新建要求。

**建议：** Board 示例链接到 Page owner 当前 Run identity 规范，并将 `rp00_*`、`rpNN_pNN` 标成历史记录格式。不得借机重命名兼容记录或 legacy adapter。

### P2 — Board 把 Workflow Runtime、Run 与 Phase controller 混在一句话里

**证据：** Board README 第 25–35 行用 Phases 00–04 展示 Page workflow；第 37–48 行又区分 Page Run、Task Run 和不算 Page Run 的 workflow pass。主技能第 36–48 行称 `RUN` 调用一次 Page workflow pass，通过 “phase controller” 执行；第 75–79 行称 Page child 的 `workflow/` 是 Page-phase receipts；第 199–200 行仍称 Page phases。当前 controller 实现 `page-lifecycle.workflow.js` 按 dispatch 坐标处理生成、snapshot 和 check；Page owner workflow table 第 67–76、182–185 行区分 controller/context/check 行与实际 Run Spec 实例。

**影响：** 操作人可能把一次 Board `RUN` 当成单个 RP/RE/RD 或 Task Run，也可能把每个 controller 阶段和 snapshot 都计作 Run。两种误读会使 ledger、计数和重开语义不一致。

**建议：** 将 Board 命令说明改为：`RUN` 启动一次 Page Workflow Runtime execution；它遵循 Page owner 定义的 Run Spec 图，并在 receipt 记录 dispatch coordinates。该执行本身不生成 RP/RE/RD 或 native Task Run。Snapshot、Check dispatch 和工具调用留作 controller Steps/receipts，除非 owner 定义了满足 Run 合约的独立 Run Spec。状态栏将 workflow readiness/controller progress 与真实 Run ID 分栏显示。

收据路径也应说明清楚：Board 主技能树示例第 75–79 行的 `_runs/page/<page-id>/` 是当前 Board runtime 读取的位置；Page owner 第 129–134、355–375 行还描述 standalone `workflow/receipts/` 和兼容路径。两者不是可随意混用的同一个 Run ledger。不要把旧 `workflow/phase.yaml` 路径名当作 Phase 语义的依据。

### P2 — Design 与 Insight 已是独立 Board 类型，但入口路由/注册材料不完整；README 仍提 Application 父家族

**证据：** 主技能 [`haipipe-board/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md) 第 21–31 行的 route table 有 Insight lane，但没有 DesignBoard lane；第 55–67 行的 Board kinds table 只列 Generic、Task、Discovery，但文档后续第 140–143 行使用 Insight Board，第 229–230 行使用 DesignBoard。Board `ref/board-form.md` 第 7–17 行同样只列前三种。DesignBoard 技能第 153、191–195 行说明 checker 识别 `design-board` 与 `insight-board`。

Board [`README.md`](../../plugins/haipipe-toolkit/skills/board/README.md) 第 19–21 行仍将其描述为 “Application Pages by Application family”。这与本次要求的产品家族模型冲突：Design、Insight 应各自作为一等 owner；Application 不再是它们的父家族。另有 Design brief owner [`haipipe-design-brief/SKILL.md`](../../plugins/haipipe-toolkit/skills/design/haipipe-design-brief/SKILL.md) 第 21、36–44 行将 Application 作为 Brief 主题/构建对象使用；这处语义是否仅指交付产品，还是保留了旧家族模型，需由 Design owner 明确，不应由 Board 评估擅自改写。

**影响：** 从通用 Board 入口进入时，用户可能创建通用 Board 而不是 Design/Insight Board，或无法找到对应 owner 技能。README 又把独立家族重新挂回 Application 名下，降低设计与洞察流程的可发现性。

**建议：** 在主 route table 和 Board kind registry 中明确列出 Insight Board 与 DesignBoard，分别链接 owner，说明它们是独立家族。移除 README 中 “Application family” 的家族关系表述。让 Design owner 确认 Brief 中 `Application` 的具体含义，再决定是否改名；单个路径示例不能单独证明父家族仍存在。

### P2 — regroup 操作说明超过了脚本实际迁移范围

**证据：** [`haipipe-board-routing/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md) 第 104–113 行称 `regroup.py` 用于任何 group rename/split，并将操作描述成 `git mv` 文件夹/文件、加 alias、grep 更新引用的组合迁移。实际 [`cli/regroup.py`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/cli/regroup.py) 第 84–102 行只枚举 Board 根目录下的 Page；没有根目录 Pages 时提示已位于 folder，并跳过不匹配当前 group key 的 Page；第 105–112 行的 `--apply` 执行的是匹配 root Page 的 `git mv` 到 Q group folder。它不会处理 nested Page、alias 或引用文本。

**影响：** group rename/split 后，操作者可能只运行脚本就认为迁移已完成，实际 nested Page、alias 和引用仍旧；也可能遇到“已在 folder”的信息后误以为所有迁移内容均已处理。

**建议：** 限定描述为：该脚本只把文件名 group 前缀匹配现有 group key 的 Board 根目录 Pages 归入相应 Q folder；nested Pages 不在其范围内。Rename/split 的 alias、引用更新和 nested Page 迁移需要另外规划，并在执行前逐项检查结果。

### P2 — 状态示例显示 LAND，但 renderer 输出 controller readiness

**证据：** 主技能第 202–207 行的示例用 `⏱️ LAND` 表示状态；当前 [`src/page_phase.py`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/src/page_phase.py) 第 93–98、448–454 行选择未完成的 CONTEXT、OUTLINE、EVIDENCE、CONTENT 或 CHECK controller coordinate；LAND 是 evidence work 的一个 action/Run 内容，不是此状态摘要所渲染的 coordinate。`status.py` 第 317–329 行在 Page focus 之外新增第四行显示该进度，因此也不应将其改名成真实 Run ID。

**影响：** 用户会把一个 readiness/controller 标签当成 Run 或实际处于 LAND Run，造成状态误读。

**建议：** 用 renderer 当前能产生的 controller coordinate 更新示例，例如 `⏱️ EVIDENCE`，同时标注其为 workflow readiness/controller progress。若 Board 要显示 active Run，单独显示 owner Run ID 与状态；不要用 `LAND` 冒充 Run。

### P2 — Board 操作入口对 Page 模板和 Task/Discovery 写入方式不够明确

**证据：** 主技能第 294 行和 [`ref/operations.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-board/ref/operations.md) 第 52–53 行引用 Board 本地不存在的 `ref/page-template.md`，作为新建 Q/S Page 的模板。当前 canonical 模板位于 Page owner 的 [`page-template.md`](../../plugins/haipipe-toolkit/skills/page/haipipe-page/ref/page-template.md)。另主技能第 123–138 行把 “add a question/group” 概括为更新 `board.md` 与 source tree，但 generic Board 可创建 Q Page，Task/Discovery Board 则使用其 native Job/Task tree 和对应 owner contract；第 55–67 行的分类表没有为此差异提供入口提示。

**影响：** 用户可能因错误模板路径停止操作，或在 Task/Discovery Board 中创建 Q Page，绕开 native task-block/owner 结构。

**建议：** 将模板链接改到 Page owner 的 canonical 路径，或维护明确的 Board 本地副本并标明来源。给“add question/group”增加 kind-aware 步骤：先确认 Board kind，按其 Folder/领域 owner 决定成员和内容 schema；Board 仍只负责登记、排序和 group 描述。

### P3 — Folder 把 shell 脚本样例写成通用 Run 结构

**证据：** [`haipipe-folder/SKILL.md`](../../plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md) 第 117–124 行将 `runs/<run>.sh` 与 result path 写成通用运行形状。共享 Run 合约也涵盖 Markdown Page Writing、YAML Design/Labeling Tickets 等非 shell Run Type。

**影响：** 新建不使用 shell 的 Run Profile 时，用户可能误以为每个 Run 都要有 `.sh` 执行器。

**建议：** 明确 `.sh` 只是某个 shell dialect 的例子；Run Type、Ticket、执行器和 Result 由 owning skill 的 Run Profile 决定。通用 Folder 结构只约定可发现的 Run identity/receipt，不规定所有 Run 都有 shell 文件。

### P3 — Routing 的职责说明有少量可减噪、补全项

Routing 技能第 141–150 行要求使用 Page contract，但没有在相邻步骤明确先解析 Page/Folder kind 及领域 owner；第 77 行列出可选 `## Board Structure` 而遗漏之后第 193–197 行用于 Board-level findings 的 `## Board Map`；第 246–251 行要求写后汇报，但没有规定只读或无写入提案时如何收尾。第 36–55、186–200 行包含较多历史 merge 背景和旧引语，增加当前操作流程的阅读负担。

建议补充“先查 Folder kind/domain owner，再套该 Page contract”、同时说明 Structure 与 Map 的用途、并允许 `Writes: none` 的完成摘要。历史背景可移至 changelog。Routing 的五步程序和每轮写入反馈仍是程序步骤，不应被改造成 Runs。

## 桌面走查

以下为依据文档与当前实现做的静态桌面走查，没有运行任何技能、服务或 UI，也没有模拟真实用户。

1. **打开已有 Board 并查看/serve：顺畅。** `ref/operations.md` 第 18–24 行将打开既有 Board 明确规定为 VIEW：先读 owner/config，再刷新或启动实际页面服务，并报告问题；`fn/serve.md` 对 root 与 route 的约束清楚。用户不易将打开 Board 误当成写入授权。
2. **添加 question/group：需要先做 Board kind 分支。** generic Board 的 Q Page 与 Task/Discovery Board 的 native Job/Task 结构不应共用一个含糊写入步骤。现在 `add a question/group` 的入口没有足够明确地先分辨两者。
3. **路由一个 Page 问题并提交 Board 变更：总体可理解。** Routing 将 Board 登记/排序与 Page 内容 owner 区分，并把 Board materialization 的审批和 Page 内容改动的授权分开。执行 regroup 前则必须说明脚本只处理匹配根 Pages，避免使用者以为 rename/split 全部完成。
4. **DesignBoard 添加 batch 并检查交付：文档和投影不一致。** 技能让用户寻找 `adopted`，当前代码投影以 Verify 后的 `ready` 作为交付状态，旧 adopt 记录才会映射进 Delivery。修正文案和导出状态即可使完成判断一致。
5. **从 Folder 开始定义一个领域 Workflow：当前容易走错建模方向。** 新作者会先按 Folder 技能创建 `phase` identity、Phase/Cycle 行和 Phase × Run Map，再与共享 Run Spec 图合约及 Page Folder parser 发生冲突。应先定 owner 的 Run Spec 图，再定义每种 Run Profile，同时列出兼容字段的暂留条件。

## 精确文案替换建议

以下英文块可作为更新技能时的直接起点。`phase` 只在明确代表序列化 controller 坐标/兼容文件字段时保留。

**1. Folder Workflow 与表格契约**

当前：

> “Each Folder is one domain workflow phase.”  
> “Workflow Table: one row per `Phase/Cycle`.”

建议：

> “A Folder owns a domain Workflow defined as an ordered or routed graph of Run Specs. Each Workflow Table row names one independently closable Run Spec, including its bounded target, Run Type, cardinality, and acceptance rule. The owning skill defines the Run Profile for each Run. Steps, tool calls, snapshots, and human gate events remain inside their owning Run unless they independently meet the Run contract. Serialized `phase`, `cycle`, and `next_cycle` fields are controller compatibility labels during migration; they do not define Workflow authority.”

**2. Board `RUN` 与 Page Runtime**

当前：

> “`RUN` invokes one Page workflow pass through the phase controller.”

建议：

> “`RUN` starts one Page Workflow Runtime execution. It follows the Page owner’s Run Spec graph and records dispatch coordinates in its receipt. The runtime execution does not mint an RP/RE/RD Run or a native Task Run. Snapshot, Check dispatch, and tool calls remain controller steps and receipts unless the Page owner defines an independently closable Run Spec.”

**3. DesignBoard Verify 与交付**

当前：

> “Steps: Commission, Generate, Verify, Adopt.”

建议：

> “The Design Workflow defines Run Specs for Commission, Generate, and Verify. A passing Verify makes the item ready for Delivery; Delivery is the handoff, not a required Adopt Run. Historical `adopt` records remain readable as compatibility records and display under Delivery. Current exports use `state=ready`.”

**4. regroup.py 的范围**

当前：

> “Use this migration for any group rename/split: `git mv` the folder/file, add alias, grep and update references.”

建议：

> “`regroup.py` folderizes only root-level Pages whose filename group prefixes match an existing group key. Nested Pages, group aliases, and reference rewrites are outside the script’s scope. For rename/split work, plan and verify those moves and reference updates separately.”

## 其他明确的边界

- **不要全局替换 `phase`。** Page Workflow Runtime 中 `phase`、`cycle`、`next_cycle` 可继续作为序列化 controller 坐标；`workflow/phase.yaml` 也可能是兼容物理路径。将它们标注为坐标/兼容字段，不将其升级为 owner 身份或 Run 类型。相反，Folder 当前 `metadata.phase` 与 `current.phase` 实际参与 parser/schema 语义，需要与 Page owner 联合迁移。
- **不要重写 historical IDs 或 adapters。** 旧 compact Page Run IDs 和 legacy Design `adopt` 可以只读保留。文档应区分当前写入规范与历史可读格式。
- **不要把 Routing 操作程序变成 Workflow Runs。** 五步路由、反馈行、审批步骤仍是程序步骤；只有 owner 定义并满足 Run 合约的对象才是 Run。
- **Board group 是责任/组织粒度，不应自动映射成 Run 或 Phase。** Routing 第 67 行这一点表达正确，可保留。
- Design Folder 中还有一处需 Design owner 协调的命名风险：Design 技能以 `rdNN_*` 命名其 Run，而 Page Workflow 的交付 Run 也以 `rdNN_<target>` 命名。现有材料不足以证实实际碰撞；应核实各自物理 namespace/Run identity 是否足以消歧，不在 Board 文档中假定存在冲突。

## 修正顺序

1. **先修 P1 合约与 gate：** Folder Run Spec 模型需和 Page owner 一起定字段迁移/兼容方案；同批明确 machine checked、person approval 与可继续工作的边界。
2. **修正当前操作真相：** 更新 DesignBoard `ready`/Delivery 文案、Page Run IDs、Board runtime/controller 说明与示例；标明 Board receipt 和 standalone Page receipt 的各自用途。
3. **补齐家族发现入口：** 在 route table/kind registry 注册 Design 与 Insight 独立 Board owner；清除 Board README 的 Application 父家族说法，并让 Design owner 裁定 Design brief 中 Application 的用法。
4. **校准工具指令：** 缩小 regroup 脚本说明范围，修模板路径，给新增成员操作增加 Board kind/Folder owner 分支。
5. **最后做文档易用性收尾：** 更新 readiness 示例，限定 shell Run 示例，补 Routing Map/无写入反馈并搬移历史背景。

## 最终判定

已完整覆盖 Board 家族现存 **4/4 个 `SKILL.md`** 和直接相关的 owner、支持文档及实现片段。当前对 Workflow 的规范尚未收敛：Folder 核心模型仍 FAIL，Board 与 DesignBoard 为 PARTIAL，Routing N/A，因此家族总体 **FAIL**。本报告不包含技能执行、测试、浏览器或用户测试结果。
