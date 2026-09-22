# Run 家族评估报告

## 快照与结论

- 评估日期：2026-09-20。
- 仓库 HEAD：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`，与评估简报所列基线一致。
- Run 目录没有工作树改动。工作树另有 8 个 `references/` 项目处于修改状态；`evaluations/haipipe-2026-09-20/` 是未跟踪目录，含共享 brief、inventory 和 sessions 清单。本报告只写入本次指定的 `run.md`。
- 当前 Run 家族清单与磁盘一致：1 个 `SKILL.md`。同目录另有 `CHANGELOG.md` 与 `agents/openai.yaml`，都已检查。

**总体判断：Run 与 Step 的边界写得很强，但 Workflow/Run 指标为“部分通过”。** 主 Skill 大部分地方使用 Run，并明确工具调用、反馈轮次、版本与 Step 不自动生成 Run；然而它把 Workflow 的规范定义写成 Run Spec 图，而没有把用户要求的“Workflow 是 Run 列表”确立为首要表示。多个主要消费者还保留了活动中的 Phase 语义、旧模板或冲突的身份语法，尤其 Task 模板与 Page 公开入口会把新请求导入错误的结构。

## 覆盖范围

| 范围 | 当前材料 | 检查情况 | 排除与缺口 |
|---|---|---|---|
| Run 家族 | `plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md`（689 行） | 全文逐段阅读；核对定义、所有权、命名、生命周期、实例化、收据、推广、审计及交互例子 | 未执行 Skill、命令、外部服务或测试；Run 目录没有其他 `SKILL.md`、README、脚本、模板或资产 |
| Run 元数据 | `.../run/haipipe-run/agents/openai.yaml`（4 行） | 全文阅读，包括可见名称、简介与默认提示词 | 无 |
| Run 历史 | `.../run/haipipe-run/CHANGELOG.md`（60 行） | 全文阅读；将历史 Phase 文字与当前规范分开 | 历史条目只作演变证据，不当作当前运行行为 |
| Run 直接引用的方言契约 | Task `task-page.md`、`workflow-runtime.md`、`hierarchy.md`、`plan-schema.md`；Page `interactive-writing-run.md`、`paragraph-run.md`、`haipipe-workbench-page/ref/run-space.md`；Paper `run-naming.md`；Insight `instance-items.md`、`task-calls.md`；Design `run-profile.md`；Discovery `paper-run-contract.md`；Labeling `ref-run.md` | 检查了与 Run/Step、Workflow 表示、Phase、身份、结果、闭合和路径相关的段落及被主 Skill 依赖的断言；其中 Page 交互、Workflow Runtime、Paper 命名、Design 方言、Insight 实例是重点核对项 | 这些跨家族文件不是本次分配的完整评估对象；没有逐行审计其中所有非 Run 内容。主 Skill 中 `instance-items.md` 引用路径未能按相对路径解析，详见发现 3 |
| 主要消费者追踪 | Task 模板和计划/报告函数、Page 词汇表/入口/Workflow、Paper Workflow/入口/插件、Insight Workflow/Page-Type、Design Workflow/Run Profile | 按简报要求检查关键用户入口与可执行指令，核实共享 Run 合约如何被引用；仅报告职责归属和证据 | 此处是消费者追踪，不替代各家族的完整评估；没有检查所有子文件、实现代码或 UI 运行效果 |

### 清单对账与边界

简报初始清单列出 `run/haipipe-run/SKILL.md`，与当前磁盘唯一的 Run 家族 Skill 相符。Run Skill 所在目录没有新发现的支持 Skill；直接支持说明分散在 Task、Page、Paper、Insight、Design、Discovery 与 Labeling 的引用文件中。运行时代码、测试、图像资产、外部 references 项目均未执行或修改。以下交互例子是**桌面推演**，不是观察到的用户测试或运行时验证。

## 优点：应保留的契约

1. **Run 有可检验的产生条件。** 六项条件要求有界目标、稳定类型与地址、受委托的 actor/action、关闭规则、耐久收据、独立于展示界面关闭（`SKILL.md:82-98`）。这减少了把任意点击、脚本或讨论扩张成 Run 的风险。
2. **内部工作与独立 Run 的边界具体。** `SKILL.md:113-124` 明确将脚本、工具/API/模型调用、重试、agent turn 和内部轮次视为同一目标下的实现细节；只有可复用且可独立关闭的目标才拆 Run。Page 交互还具体规定反馈为 Step、重开为 Version、改目标才是新 Run（`:380-415`）。
3. **身份、Ticket、Result 和 receipt 关系可审计。** 本地与 Job-backed 存储、Insight 的 `riNN`、Page 的 `rp-*`、Paper 的 owner-native 地址，以及完整跨 Folder 引用都有例子；失败或阻塞也要留下事实收据（`:28-53, 330-361, 449-479, 526-616`）。
4. **跨 Page/Task 两个关闭边界清楚。** Page 候选不抢占 `rNN`，Task 返回结果并带完整身份、路径和指纹；两个 Run 分别保留各自的闭合状态（`:175-191`）。
5. **历史与兼容身份有明确例外。** 旧 Paper `pjNNtNNrNN`、旧 division-writing 记录可作为只读历史，日期只适用于既有记录，底层 `phase()` 只作适配元数据；这些字段不应被盲目改名或拿来另造 Run（`:284-285, 349-352, 597-601, 681-689`；Task `workflow-runtime.md:140-154`）。

## 优先发现

### P1 · 主合同把 Workflow 图当作规范表示，没有明确规定 Workflow 是 Run 列表

**证据。** `plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:193-230` 写道：“`Workflow Definition = bounded Run Spec nodes + graph entry/terminal rules`”，并要求“Every executable Workflow publishes one Run Spec graph”。`SKILL.md:252-255` 又称“graph is the Workflow authority”。

**问题与影响。** Skill 已定义 Run Type、Run Spec 与 Run Instance，但只把计划节点和 Route 编译出的有向图设为 Workflow 的规范模型；没有明确哪份 Run 列表是 Workflow 的人类可读清单，也没有说明图只是对列表中 Runs 的排序、分支和完成关系的表达。读者可能只交付图或 Spec 表，不交付实际 Run 列表；也可能把图边当作与 Runs 平行的工作单元。Task Workflow 同样定义“Run Specs + graph”，Page 与 Design 又把多实例收在参数化 Spec 行下，显示这不是一个孤立措辞。

**建议。** 把“列表”写成 Workflow 的外层契约，再说明定义阶段的 Run Specs 与执行阶段的 Run Instances 如何填充/实现列表。Gate、Route、depends-on、cardinality 仍保留为 Run 元数据或列表项之间的关系；它们不取代 Run 列表。Run Type 保持可复用默认值，而非 Workflow 内容的替代物。

### P1 · Task 的活动模板仍命令使用 Phases，生成的计划与当前 Schema 冲突

**证据。** `plugins/haipipe-toolkit/skills/task/haipipe-task/ref/workflow-template.yaml:29-33,48-50` 使用 `phases:`，并把 `Run`、`Gate1`、`Gate2` 当作 Phase 标题。被该模板引用的 `fn/stage-plan.md:28,99-105` 指示计划“Phases → Steps”，并将脚本单元分组成 Phase。报告函数 `fn/stage-report.md:7,91-127,137-209,216-222` 继续要求同样的 `phases` 与 `phases_completed`。相反，现行 `plugins/haipipe-toolkit/skills/task/haipipe-workflow/ref/plan-schema.md:126-128` 规定 `run_specs` 是唯一 Workflow 行清单，并明确禁止 `phases:`。

**问题与影响。** Task 计划/报告指令是可执行路径；依照它们生成的文件会违反当前通用 Schema。模板还把 Run 和 Gate 行放在 Phase 下，agent 无法判断哪些是独立闭合 Run、哪些是 Run 内部步骤，结果可能缺少可审计的 Run ID、Route 与 receipt。

**建议。** 将模板、stage-plan 与 stage-report 一起迁到 Run 列表；每个独立关闭目标列为 Run，每个脚本内步骤留在该 Run 的 Steps。报告按 planned Run Specs 与实际 Run Instances/receipts 分开投影。Plan、Build、Execute、Report 是 Task 生命周期操作，不要为了替换 Phase 而各自变成 Run。

### P1 · Page 的活动词汇表与公开命令仍把 Phase 定义为重复的 Workflow 权限单元

**证据。** `plugins/haipipe-toolkit/skills/page/haipipe-page/ref/glossary.md:171-181` 将 workflow 解释为“不重复”的 LOOP、phase 解释为承担 `00 CONTEXT … 04 CHECK` 权限且会重复、cycle 解释为 phase 内的一次 pass；`:217-230` 继续说 “RUN, not ADVANCE”、重复 Phase、下一 Phase 以及 “phase producer”。公开 Skill `plugins/haipipe-toolkit/skills/page/haipipe-page/SKILL.md:581-584,689,881-883` 仍向人暴露 phases、`/haipipe-page run <page> [from <phase>]` 和 “current Page Phase contract”。

**问题与影响。** 这是当前概念定义与公开 UI/命令，不是序列化兼容字段。它使 Page 领域把 Phase 当作选择权限与重复推进的核心，而 Run Skill 规定 Workflow 要组织 Run Specs/Instances。用户会按 Page Phase 提问，agent 也可能把 CONTEXT 到 CHECK 的控制节点误作 Run 清单中的 Run。

**建议。** 先按 Run 六项条件判定每个 Page 阶段是否真是独立闭合的 Run；符合者进入 Workflow Run 列表，不符合者仍是该 Run 内部的 Step、Gate 或 Route。公开入口用具体 Run ID/Run 选择器（如 `[from <run-id>]`），并显示下一项 Run 或需解决的 Gate；不要把现有 cycle 一律升级为 Run。

### P1 · Paper 与 Insight 的消费者还把 Workflow 单位称为 Phase；Insight 另有已退休的 Application 父层说法

**Paper 证据。** `plugins/haipipe-toolkit/skills/paper/haipipe-paper-workflow/SKILL.md:21-30,42-63,239-247` 以 journey Phases/positions 表达 P0–P4；公开路由 `plugins/haipipe-toolkit/skills/paper/haipipe-paper/SKILL.md:28-40,197-203,227-246,462,497-501` 仍暴露 `[phase]`。Paper 插件 `plugins/haipipe-toolkit/skills/paper/haipipe-workbench-paper/SKILL.md:370-399` 又用 Run Type/计划行与已分配 Run 表示工作，未明确把 concrete Runs 列成 Workflow 清单。

**Insight 证据。** `plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:38-62` 用 I0–I5 RunTypes、Run Specs、Routes 与 Runtime frontier 表达 Workflow；六个当前 rung 文件仍位于 `skills/insight/workflow-phases/` 并使用 `metadata.phase`。Task 侧 Insight 说明 `plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/workflow-table.md:3-6,25-32` 还称其为 “Application I0-I5 ladder”，并保留 “Phase × Run Map”；其父 Skill `.../haipipe-page-insight/SKILL.md:150-152,231` 复述此模型。

**问题与影响。** Paper 的 `CONTEXT/OUTLINE/EVIDENCE/CONTENT/CHECK` 或 Insight 的 rung 可能是操作阶段、门控或真正的 Run；当前材料没有用 Run 的独立目标/关闭规则来清楚划分。用户可能按旧 Phase 参数调度，agent 可能把所有 rung 误当 Run，或不知 Run 与 Checkpoint 谁拥有交付物。Insight 的 Application 父层说法还直接违反“Insight 是独立一等家族”。

**建议。** Paper/Insight 各自公开 Workflow Run 清单；Run Type/模板仅提供可复用默认值，Phase-like 流程条件改作列表 Run 之间的 Gate/Route 或 Run 内 Step。删除 Insight 的 Application 父层归属，保留 `Insight` 独立家族名。Paper 的 checklist 和 Page Step/Close 边界继续保持，不要把所有内部动作一股脑升成 Run。

### P1 · 主 Skill 与 Paper Run Profile 的当前 Page 身份语法不一致

**证据。** Run Skill `SKILL.md:162-173, 316-320, 365-407` 规定新 Page Run P 使用 `rp-struct-NN`、`rp-sec-NN`、`rp-para-NN_Pxx[-Pyy]`，并称结构 Run 是 `rp-struct-01`。其引用的 Paper 命名权威 `plugins/haipipe-toolkit/skills/paper/haipipe-paper/ref/run-naming.md:77-89` 却称 Page 当前语法是 `rp00_mermaid-structure | rp<NN>_p<NN>`，要求每个 Page interaction 从 `rp00_mermaid-structure` 开始。

**问题与影响。** 两个当前说明都宣称为现行规则，但身份格式、编号与“第一项”均不同。遵循 Paper 文件的 agent 会创建 Run Skill 判为无效、不能满足 Structure prerequisite 的 ID；遵循 Run Skill 的 agent 会违反 Paper 页面对 Page ID 的约定。

**建议。** 由 Page Run 契约统一这三类 ID 后同步 Paper 引用；若 `rp00` 是旧文件，就标为历史只读语法，并确保新的 Page/Paper 工作只从一处权威文档读取当前 ID 规则。

### P2 · Insight 实例方言的加载路径写错，默认提示词又只列出部分核心家族

**证据。** `SKILL.md:419-421` 将 Insight 所有实例 Schema 的路径写成 ``task/page-types/haipipe-page-insight/ref/instance-items.md``，但该文字若相对当前 Skill 解析会落在不存在的 `run/haipipe-run/task/...`。现存文件位于 `plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/instance-items.md`。`:445-446` 另称 “See the Insight `ref/task-calls.md`”，没有给出可直接解析的路径。Skill description `SKILL.md:3-10` 称合同在 Execution、Discovery、Page、Labeling 间共享，却在正文 `:152-154,261-271` 把 Insight 与 Design 列为主要 Run 家族。可见默认提示词 `agents/openai.yaml:4` 只列 Run Type/Spec/Instance 字段，没有提示这两个一等家族。

**问题与影响。** 新上下文加载 Insight RI 合同时会找错路径；摘要触发说明也更容易让 Skill 选择器/agent 将 Insight 和 Design 当成正文之外的方言或漏掉 Run 合同。用户看不到何时该为新数据绑定创建 `riNN`、或为 Design 任务套用该合同。

**建议。** 把路径改为明确相对路径 ``../../task/page-types/haipipe-page-insight/ref/instance-items.md`` 和 `../../task/page-types/haipipe-page-insight/ref/task-calls.md`。description/默认提示词明确点名 Execution、Discovery、Page、Insight、Design、Labeling，同时保留“它们是独立家族”的定义，不引入 Application 共同父层。

### P2 · Design 的范围清单仍把 Adopt 列为 Run，但现行 Design Profile 已不再允许它

**证据。** `SKILL.md:270-289` 将 “one Adopt decision” 列为 Design Run 家族，并称 Run Profile 含 “commission/generate/verify/adopt gates”。当前被引用的 `plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/references/run-profile.md:3-14` 的 Allowed Run Types 只有 `Design.commission`、`Design.generate`、`Design.verify`；当前 `haipipe-design-workflow/SKILL.md:25-36,56-58` 也把 Workflow 转为 Commission、Generate、Verify 后的 delivery 路由。Design Profile changelog 中的 Adopt 提法是早期历史，当前 clean-break `run-profile.md:187-192` 拒绝旧 schema。

**问题与影响。** 由 Run Skill 分类表或正文工作的 agent 可能尝试分配 `Design.adopt` Run，违反唯一当前 Schema。需要分清“人决定是否采用”的 Gate/外部 Page 交付决策与可独立关闭的 Run。

**建议。** 同步主 Skill 的 Design 枚举与当前设计方言；除非 Design owner 正式新增类型，不把 Adopt 决策列作 Run Type。可以写明采用/交付目前由 Workflow route 或其 owner Gate 处理，不创建 `Design.adopt`。

### P2 · “只有通用合同与 UI 元数据”的范围承诺不符合正文

**证据。** `SKILL.md:681-689` 声明 “This skill intentionally contains only this contract and its UI metadata. Existing specializations remain authoritative”。但同一文件前面已有 Page-facing projection 与跨 Task/Page closure（`:126-191`）、完整的 Interactive Page writing dialect（`:363-415`）、Insight instance schema 与生命周期（`:417-448`），并含所有方言存储和运行时规范（`:449-616`）。

**问题与影响。** 读者无法判断这些段落是完整规范、摘要、还是已经过期的方言复制；后续编辑可能只更新外部 Profile，主 Skill 的说明继续讲旧规则，或反过来。Paper RP 格式和 Design Adopt 当前就展示了这类漂移风险。

**建议。** 若维持正文中的方言摘要，把末尾改成如实声明：本页定义共享 Run 不变量并摘要关键方言，指定文件拥有各自存储/结果规则；用户操作前加载该方言。若希望它只做共享合同，则把 Page/Insight 细节移回各自参考文件，正文保留最小路由与边界摘要。

### P3 · 入口词汇密集，缺少“用户请求 → Run 列表 → 交付”短例

**证据。** 前 60 行集中介绍 Folder、Workflow、Run Spec、Run Type、Run Instance、Workspace Cell、Gate、Route；紧接着还有六项 Run 条件。可见 `agents/openai.yaml:4` 的默认提示词也一次列出大量类型和字段。完整收据例到 `SKILL.md:556-586` 才出现，没有从一句用户请求映射到需要的 Run/Step/用户决定的简短例子。

**影响。** 新读者必须先掌握内部模型，才能判断自己请求中哪些信息要给定、哪些由 Workflow/owner 补足，以及何时需要向人询问目标或验收。模型是技术合同，但入口对非作者/新上下文 agent 的认知负担偏高。

**建议。** 在概念详述前放一个极短的“新数据集重跑分析”或“改一段 Page”例子，显示 Run 清单、其 ID/目标、内含 Steps、人工验收点，以及新的 Workflow 实例会生成什么收据。将其标为说明例而非 Runtime 测试。

## Workflow/Run 指标判定

| 对象 | 判定 | 证据与判定理由 |
|---|---|---|
| Run 家族 `haipipe-run` | **部分通过** | 活动语义大多用 Run；`SKILL.md:113-124,380-415` 明确不把调用、反馈、Step、Version 误算为 Run。`phase()` 在 `:209-211` 被限定为路由元数据，`:195,234,254` 多以否定方式说 Phase 不再拥有语义。但 Workflow 的规范模型仍是 Spec 图，而非明确的 Runs 列表（`:193-255`），所以未满足用户要求的完整模型。 |
| Task / Workflow | **失败** | 当前计划 Schema 只接受 `run_specs`（`plan-schema.md:126-128`），活动 Task 模板/函数却要求 `phases → steps` 且报告仍含 `phases`。底层 JavaScript `meta.phases`、`opts.phase`、`phase(...)` 作为进度组的适配字段则是**兼容/内部标签**，不应改为 Run 或单独计数。 |
| Page | **失败** | 当前 Page glossary 与公开入口仍定义 Phase 为重复的 authority 单元并要求 `[from <phase>]`。另有 Page workflow/receipt 引用明确说明 `phase/cycle/next_cycle`、`workflow/phase.yaml` 与 `phase-cards.md` 是旧控制器序列化/路径兼容；那些具体字段可继续当适配名，不能用它们替代新的用户概念。 |
| Paper | **失败** | 当前 Paper Workflow/公开路由仍以 Phase/P0–P4 组织；Paper-local Run 命名本身区分清楚，但被引用的 Page interaction ID 是旧式 `rp00/rpNN`，与当前 `rp-struct/rp-sec/rp-para` 规则冲突。旧 `pjNNtNNrNN` 明确为只读历史，可保留。 |
| Insight | **失败** | 当前材料将 Application 作为 I0–I5 的父层，并有活动的 Phase×Run 映射、`workflow-phases/` 路径与 `phase.yaml` 约定。它不是仅在兼容说明中出现的旧字段。Insight 的新数据实例 `riNN` 与 Base R 的分离、冷冻输入和独立 Result 仍是应保留的 Run 约定。 |
| Design | **部分通过** | 现行 Design Skill 已明确拒绝旧 Phase-shaped 语法，并能区分 Commission/Generate/Verify 与 Step；没有发现 Application 父 Skill。但 Workflow 仍为 Run Spec 图而非 Run 列表，且主 Run Skill 把历史 Adopt 决策冒充当前可分配 Run。 |

**兼容/历史分层。** 主 Run 的 changelog 与主文中的“没有 Phase owner”、`phase()`/controller 标签说明属于历史或适配解释，不能盲目逐词换成 Run。Task Workflow API 的低层 phase 字段和 Page 迁移文档中明确的 `phase/cycle/next_cycle` 序列化别名可留在兼容代码/存档说明里。相对地，Page glossary 中 Phase=authority、Task `phases:` 计划模板、Paper `[phase]` 入口、Insight 当前 `workflow/phase.yaml` 和 Application 父层，是活动模型或新工作指令，不应归为历史豁免。

## 代表性桌面推演

以下是根据文档推演，不是 Live 用户测试。

| 用户请求 | 当前 Run 合同能否指路 | 风险/更清楚的用户交互 |
|---|---|---|
| “对新增数据集再跑一次分析，并请另一位审查结果。” | Insight 部分能：新数据绑定分配独立 `riNN`，沿用可复用 R 方法；Task 本地工作是否拆 Run 应由目标、验收和独立关闭判断。 | 主 Skill 给出的实例文件加载路径错了，用户提示词也没有点出 Insight。较清楚的回复应确认数据集/问题绑定与审查目标，列出 planned Run：`riNN` 数据分析与一个独立 review Run（若其有独立目标和闭合）；运行内工具调用为 Steps。随后显示实际 `Run ID → Result → receipt`，不把既定 Run 列表误称为 phase 图。 |
| “把 Page 的 P03 按这条反馈改好。” | 很好：保持同一个 `rp-para-NN_P03` Run，保存反馈 Step，必要时在同一目标内重开 Version；明确接受后才通过 Page Run exit gate。 | 回复应只问缺少的接受判断或作用范围，不把每次聊天都分配新 Run，也不声称文章已通过 Page CHECK。旧 Paper 命名文档仍可能错误引导到 `rp00_mermaid-structure`。 |
| “先做方案 A，再生成三个备选并独立验证。” | Run family 能表达“一个 Commission、多个 Generate、多个 Verify”及内部迭代；Run IDs、freeze、receipts 清楚。 | 当前 Design Profile 只允许 Commission/Generate/Verify，主 Skill 却说有 Adopt Run。回复应列出实际 Generate/Verify Runs 与依赖，说明采用由当前 owner gate/delivery route 处理，不新建 `Design.adopt`，除非 Design owner 更新契约。 |
| “做一个 Paper Section，从找证据到完成稿。” | Paper 的本地 `pm-/pa-/pr-` 命名和 Page/Task 各自 ownership 清楚。 | 公开 Paper `[phase]` 与 P0–P4 旅程会让人以为过程单元就是 phase。清楚的呈现应给出 Page Workflow 的 Run 清单；证据 Run、写作交互 Run、Task/Discovery Supporting Run 采用各自身份，Outline/反馈等内部动作留在 Step 或 Gate，Route 表达先后依赖。 |

## 关键段落改写建议（英文原文 → 英文建议）

### 1. 先写 Workflow 清单，再解释图关系

**原文**（`run/haipipe-run/SKILL.md:193-211`）：

```text
Workflow Definition = bounded Run Spec nodes + graph entry/terminal rules
                      + graph compiled from the Specs' directed Routes
Workflow Execution  = Run Instances materialized from those Specs
```

**建议：**

```text
A Workflow is a list of Runs. Its definition lists the planned Run Specs;
execution records the Run Instances materialized from those entries. Routes,
dependencies, and terminal rules describe how the listed Runs proceed. They do
not replace the Run list or create additional Run units. Run Types provide
reusable defaults for listed Runs.
```

这样保留 Type/Spec/Instance 和分支语义，同时使 Run 列表成为模型主语；只有明确独立闭合的目标才列为 Run，其他交互保留为 Gate/Step。

### 2. 把 Task 模板从 Phases → Steps 改为 Run 列表 → 内部 Steps

**原文**（`task/haipipe-task/fn/stage-plan.md:28`）：

```text
Task Plans: Phases → Steps. Each Phase has a Goal, Inputs, Outputs, and Steps.
```

**建议：**

```text
Task Workflows list independently closable Runs. Each Run has a bounded Goal,
Inputs, expected Result, and close rule. Script or tool operations that serve
the same target stay as ordered Steps inside that Run.
```

同时把 `workflow-template.yaml` 的 `phases:` 变为 Schema 许可的 Run/Run Spec 列表，并使报告列出实际 Run IDs 与 Receipts。

### 3. Page 入口把 phase selector 改为 Run selector，保留普通阶段内动作

**原文**（`page/haipipe-page/SKILL.md:689`）：

```text
/haipipe-page run <page> [from <phase>]
```

**建议：**

```text
/haipipe-page run <page> [from <run-id>]
```

并在 Page glossary 加一句定义：`A Page Workflow is the list of commissioned Page Runs. Resume the selected Run or choose the next Run whose entry Gate is satisfied; an ordinary review cycle stays a Step within its Run.` 若内部 API 仍需 `phase` 序列化名，把它清楚标为 legacy/adapter 字段，而不是可见概念。

### 4. 将 Insight 从 Application 子层改成自有 Workflow 清单

**原文**（`task/page-types/haipipe-page-insight/ref/workflow-table.md:3-6`）：

```text
... haipipe-insight-workflow ... continues to own the Application I0-I5 ladder.
```

**建议：**

```text
Insight owns its I0-I5 workflow contract. Each Workflow lists its commissioned
Runs and their targets. Shared Run Types may supply defaults; gates and routes
describe decisions between listed Runs. There is no Application parent family.
```

这样既给 Insight 一等 Skill 家族身份，也不把 I0–I5 的所有检查、批准或工具调用都改名为 Run。

## 跨家族责任归属

| 问题 | 主要责任家族 | 合并评估时需协调的对象 |
|---|---|---|
| Run 列表 vs Run Spec 图 | Run/Workflow 共用概念 | `haipipe-run` 与 Task、Page、Design Workflow 定义；Run Contract 应提供统一短句，消费者保留各自业务字段 |
| Task 模板与 Schema 不一致 | Task | `workflow-template.yaml`、`fn/stage-plan.md`、`fn/stage-report.md` 对齐 `haipipe-workflow/ref/plan-schema.md` |
| Page Phase authority 与公开 selector | Page | `haipipe-page/ref/glossary.md`、`haipipe-page/SKILL.md`；区分正式 Run 与 Page 内 Step/Gate |
| Paper journey Phase、旧 `rp00` 语法 | Paper / Page | Paper Workflow/Router 改 Run 术语；Page owner 定义唯一 current RP ID 后同步 Paper 引用 |
| Insight Application 父层和 Phase × Run 图 | Insight（Task Page-Type 也含重复副本） | `haipipe-insight-workflow`、`page-v2-adapter.md`、Task-side Insight Skill/`workflow-table.md` 同步；Insight 不挂 Application 父层 |
| Design Adopt 的 Run 类型冲突 | Run 分类表 / Design 方言 | 以当前 Design Run Profile 为准更新 Run Skill，或由 Design owner 正式提出新的 Run Type 后同步 Schema |
| 错误的 Insight 引用路径与家族发现描述 | Run | 主 Skill description、默认提示词和 Insight 相对链接 |

## 推荐修正顺序

1. 先确定并发布共用定义：Workflow 是 Run 列表；Run Spec/Type/Instance 分别对应计划项、可复用默认值、实际执行记录；Gate/Route/Step/Version 的位置不变。
2. 修复会生成不合 Schema 文件的 Task 模板与计划/报告指令；同步 Page 的 glossary/命令和 Paper/Insight 的活动入口与 Workflow 表示。
3. 对照当前 Page 与 Design 方言，修正 Paper RP 格式与 Design Adopt 范围，修复 Insight 资料路径和 Application 家族表述。
4. 更新每个消费者的可见 Skill 描述/默认提示词，加一个简短的 Run 列表 desk example；保留只读历史、API 适配名和 Step/Run 不混淆规则。
5. 由各家族 owner 后续做一次全量一致性复核，包括模板、报告、示例和用户命令；本轮没有修改文件或运行测试。
