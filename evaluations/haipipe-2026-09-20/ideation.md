# HAI-Pipe Ideation 技能族评估

## 快照与范围

- 日期：2026-09-20。
- 基线提交：f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217，与评估简报一致。
- 当前磁盘盘点：指定的 8 个 Ideation 技能路径全部存在，未发现额外的 Ideation SKILL.md；本次核读时这些技能文件没有工作树改动。
- 共享工作区已有其他 reference 子模块状态变化（cite-guard、grant-writer-skills、paper-rag-skill、paperspine、reprorun、research-agent-skills、research-co-pilot、scipilot-figure-skill 均显示修改），evaluations/ 为共享评估目录中的未跟踪内容。它们不是本次审阅对象；本报告只写入 ideation.md。
- 范围：8 个完整 SKILL.md；Ideation 伞技能直接链接的 8 份 reference 全文；8 份 agents/openai.yaml 和 8 份 changelog；为核对含义而读取 checker 中的相关门禁代码；完整读取 Paper P0 Ideation 适配技能，并读取共享 Run 与 Page 合同的相关章节。未执行这些技能、没有调用外部服务、没有运行测试，也没有改动技能或代码。走查为桌面推演，不是实际用户测试。
- 排除项与限制：external-skill-map.md 中提到的第三方技能仅作为本地文档所记录的历史来源，本次未重新审计上游仓库；没有发现本目录下的 README、模板或图片资产。未逐篇审计 Task、Discovery、Venue 与整套 Page 生命周期合同，故跨家族意见仅限于直接交接处与已读共享合同。
- 引用规则：下文短写的 Ideation 路径以 plugins/haipipe-toolkit/skills/ideation/ 为基准；scripts/check_ideation.py 以 haipipe-ideation/ 为基准。run/、page/、paper/ 的路径以 plugins/haipipe-toolkit/skills/ 为基准。行号来自本次核读的当前磁盘文件。

## 完整覆盖

| 技能 | 覆盖的当前说明与直接支撑材料 | 排除项或限制 |
|---|---|---|
| ideation/1_generate/haipipe-ideation-generate | 完整技能、UI 元数据、changelog；evidence-bundle.md、idea-card.md、manifest-and-sync.md | 第三方生成器上游实现未复核 |
| ideation/2_test/haipipe-idea-pressure-test | 完整技能、UI 元数据、changelog；idea-card.md、workflow-table.md、receipts.md；只读核对 checker 的 feasibility 规则 | 未运行压力测试或 checker |
| ideation/2_test/haipipe-ideation-test | 完整技能、UI 元数据、changelog；workflow-table.md、idea-card.md、manifest-and-sync.md、receipts.md、venue-fit.md；只读核对 test gate | 未执行专家路由 |
| ideation/2_test/haipipe-journal-fit | 完整技能、UI 元数据、changelog；venue-fit.md、evidence-bundle.md | 未查询期刊网站；这是文档评估，不是期刊规则核验 |
| ideation/2_test/haipipe-nature-paper-review | 完整技能、UI 元数据、changelog；venue-fit.md、external-skill-map.md | 未审计 Nature 上游技能或现行投稿规则 |
| ideation/2_test/haipipe-novelty-check | 完整技能、UI 元数据、changelog；evidence-bundle.md、receipts.md、external-skill-map.md | 未检索文献或打开外部来源 |
| ideation/3_select/haipipe-ideation-select | 完整技能、UI 元数据、changelog；receipts.md、idea-card.md、venue-fit.md、end-to-end-example.md；只读核对 selection/handoff gate | 未写选择收据或实际 Paper 交接 |
| ideation/haipipe-ideation | 完整技能、UI 元数据、changelog；evidence-bundle.md、idea-card.md、workflow-table.md、receipts.md、venue-fit.md、manifest-and-sync.md、external-skill-map.md、end-to-end-example.md 全文 | checker 与测试夹具只读到支持本报告判断所需处；未运行它们 |

## 总体判断

这组技能的证据边界与专业分工写得细致。尤其值得保留的是：Discovery 与 Task 各自拥有来源和执行结果；Idea Card 保存结论并指回来源；novelty 与 identification 分开；期刊筛选分为广筛和 finalist 深评；Nature 只做编辑形状判断；Page 只投影，不取得选择权。这些边界在 evidence-bundle.md、idea-card.md、venue-fit.md 和选择技能中互相支撑。

对本次强制模型的总评为 **部分符合，核心 Workflow/Run 定义不通过**。8 个 SKILL.md 正文中几乎没有把 Ideation 活动称为 Phase；显著问题是把 Generate、Test、Select 描述为“三阶段”工作流，却没有给出该 Workflow 的 Run 清单或 Run Spec 图。共享 haipipe-run 合同把 Workflow Definition 定义为 Run Spec 图，并明确没有单独 Phase 权威层。Ideation 的 workflow-table.md 却把 I1、I2a–d、I2、I3 列作工作流式序列，同时声明其中的候选生成、检查、比较、交接都不是 Runs，且不得创建本地 Ideation Run。当前文档因而阻止了工具调用被误算为 Run，却没有说明 Workflow 由哪些 Runs 构成。

“Stage”与当前 schema 字段 stage 是活跃的能力组标记，不是历史字段；I1/I2/I3 也不是 Run ID。不能把目录名、stage 或每条内部检查机械改名为 Run。应由家族合同明确：哪些有独立目标、责任人、Ticket/Result、关闭规则和收据的活动才是 Run；其余保持为某个 Run 内的 Step、Gate 或投影操作，并在 Workflow 中列出真实 Run Specs 与 owner。

## 高优先级发现

### 1. 工作流声称为三阶段，但没有 Run 清单

**优先级：P1 — Workflow/Run 模型未定义。**

证据：

- haipipe-ideation/SKILL.md:4-10 称 “three-stage Ideation family”；:50-53 又称 “three-stage state machine”，并说编号子技能拥有各 stage 的 craft；:82 称 “durable three-stage workflow”；:179 指向 “phase table”。
- haipipe-ideation/SKILL.md:28-47 的图用 1 GENERATE → 2 TEST → 3 SELECT 表示顺序，但没有 Run identity；references/end-to-end-example.md 的 1 Generate / 2 Test / 3 Select 示例同样没有标出哪些节点是 Run、Step 或 Gate。
- references/workflow-table.md:7-20 将 I1、I2a–d、I2、I3 按 purpose、writes、owner、exit、human gate 排成流程表；:33-36 随即写道 “Search calls, candidate generation, card edits, test reconciliation, journal comparison, and handoff are not Runs”，只有 Discovery 或 Task 中的新分析/计算才是 Run。
- 共享 run/haipipe-run/SKILL.md:35-58、82-124 规定 Workflow Definition 拥有 Run Spec 图，单个 Run 需要 bounded target、身份、commission、close rule、持久结果及独立关闭；一次路由器调用也可能不产生任何 Run。

问题与影响：表格看起来就是 Workflow 的权威步骤表，但它列出的主要工作又被排除在 Run 之外；没有别处给出实际 Workflow Run 列表。新 agent 因而无法知道 Generate、Test、Select 是独立 Run、父 Run 内的 Step，还是仅为 capability group。它也无法可靠判断哪些地方应生成收据、何处关闭、什么输入变化要续跑。

建议：将现有表准确命名为“能力组与 Run 边界图”，明确 I1/I2a–d/I2/I3 是当前能力标识，不是 Run ID，也不是完整 Workflow Definition；另由 owner 发布实际 Workflow Definition/Run Spec 列表，并对每个活动应用 haipipe-run 的六项判定。Discovery/Task 计算继续使用 owner-native Run；卡片编辑、novelty query、矩阵汇总、P0 sync 仅在满足独立关闭条件时才升级为 Run，否则留在其父 Run 的 Step/Gate 或适配器里。实施前须解决“不得建本地 Ideation Run”与“Workflow 由 Runs 构成”的直接冲突。

英文改写示例：

> Before: “It owns the three-stage state machine … Its numbered children own the craft inside each stage.”
>
> After: “Generate, Test, and Select are Ideation capability groups, not Run IDs. The Workflow Definition lists the Run Specs actually commissioned and names each Run’s owner. Apply haipipe-run’s close and identity tests before allocating a Run; keep specialist checks, card edits, and P0 projection as internal Steps or adapter work unless they close independently.”

### 2. 人类收据无法表达对每个候选的决定

**优先级：P1 — 选择历史可能不完整。**

证据：

- haipipe-ideation-select/SKILL.md:43-57 要求机器逐候选建议，并要求人对零个、一个或多个 Idea 做选择；同时要求把每个 nonselected card 作为 deferred 或 eliminated 保存，并记录理由。
- 其收据示例 :71-97，以及 references/receipts.md:95-123，只有一个全局 decision（select/defer/abandon）、一个全局 selection_posture、selected_cards、只针对入选卡的 Story/target routes 和一条全局 accepted_risks。
- references/end-to-end-example.md:148-180 展示 i01 被选、i02 abandon、i03 defer 的组合；示例收据只记 decision: select 和 selected_cards: [i01]，没有记录由谁对 i02、i03 作了何种决定或各自理由。
- scripts/check_ideation.py:789-821 也只校验全局 decision 与入选卡、Story、target 路由的数量关系；模式没有 candidate-level dispositions。

问题与影响：人可以选 i01，同时要求 defer i02、abandon i03，甚至对不同入选 Idea 分别接受不同风险。现有单一 posture 和扁平风险列表不能把这些决定绑定到各自卡片。未入选卡的最终状态可能被误写成机器建议，或只更新卡片而无法从唯一的人类收据追溯。

建议：收据增加逐候选决策列表，要求一次审阅涉及的每张 admitted card 恰好一条：card、human disposition、理由；入选条目再包含该卡的 proceed/caution posture、逐卡 accepted risks、target/category、Story route。顶层 decision 可作为汇总字段，但不是多卡决策的唯一记录。checker 应验证覆盖完整、同一 card 不重复、入选项才有 target/Story，且 Page 只投影此收据。

英文 schema 方向示例：

    candidates:
      - card: cards/i01_idea.yaml
        disposition: select
        posture: proceed-with-caution
        accepted_risks: ["Keep claims associational until identification improves"]
        target: {name: "Journal", category: "Original research"}
        story_route: {role: Story-A, path: "..."}
        reason: "..."
      - card: cards/i03_idea.yaml
        disposition: defer
        reason: "Closest-work review is only abstract-depth"

## 中优先级发现

### 3. 目标与选择状态的投影关系没有写清

**优先级：P2 — handoff 字段可能漂移。**

证据：

- references/idea-card.md:97-108 在 Idea Card 写 venue_fit.human_target、recommended_target 和卡状态；:120-122 才说明 venue_fit block 是 projection。
- references/venue-fit.md:129-143 在 Venue Fit Card 又定义完整 human_target，包括 status、target、category、venue_contract、by、at、accepted_conditions。
- haipipe-ideation-select/SKILL.md:103-105 与 references/receipts.md:132-143 则称 workflow/selection.yaml 是 single selection authority，并规定 target 由人拥有。

问题与影响：准确目标存在于 Venue Fit Card 和 selection receipt；Idea Card 还保存 human_target 状态与推荐目标。文档虽称 selection receipt 是唯一权威，且 Idea Card 的 venue_fit block 是 projection，却没有把它明确连到该 receipt，也没有写更新顺序、冲突检测规则。人可能更新 receipt 却忘记卡片，后续 Paper handoff 读到旧 fit target。

建议：明确 workflow/selection.yaml 是唯一人类写入源；Idea Card 与 Venue Fit Card 的 human_target 一律标记为只读派生视图，给出从 receipt 的字段映射、何时刷新及冲突处理，并在 checker 中验证 target、category、status 和 person/date 一致。若下游必须保留独立 field，则每份 schema 都应注明其“projection of selection receipt”，不能只说 fit card 保存比较细节。

英文改写示例：

> “Only workflow/selection.yaml records the person’s target choice and accepted risks. Idea Card venue_fit.human_target and Venue Fit Card human_target are read-only projections of that receipt. Refresh them after selection; any mismatch is a handoff HOLD.”

### 4. “Select” UI 描述与人类决策边界相反

**优先级：P2 — 首屏文案可能让人误以为模型代为选择。**

证据：3_select/haipipe-ideation-select/agents/openai.yaml:1-4 把技能显示为 “HAI Idea Select”，短描述为 “Select tested ideas and journal targets”；相同技能的 SKILL.md:20-22 明确说它不得 “choose on the user’s behalf”，:50-52 要求向人询问。

影响：用户只看到技能选择器或卡片时，可能把它理解成自动选择工具；正文后来再解释边界会产生意外。

建议：将显示名或短描述改成帮助式而非代选式，例如英文 “Compare tested ideas and prepare your idea-and-target decision”。正文的 machine recommendation / human decision 分界值得保留。

### 5. 单次 novelty / venue 请求的实时来源路径不具体

**优先级：P2 — agent 可能把“引用当前来源”误做成记忆回答。**

证据：2_test/haipipe-novelty-check/SKILL.md:15-17 仅规定 durable work 加载 Discovery；但 :167-173 的 one-off 仍要求 direct sources。2_test/haipipe-journal-fit/SKILL.md:94-99 的 one-off 要求 official-source links 与 access dates；2_test/haipipe-nature-paper-review/SKILL.md:93-95 要求在说投稿规则前浏览官方页。三个技能 frontmatter 的 allowed-tools 只有 Bash、Read、Write、Edit、Grep、Glob、Skill，没有写清 one-off 如何把新的外部查证路由到 Discovery。

影响：one-off 与 durable 行为差异没有讲明白。Fresh agent 可能拿模型记忆满足“direct source”，也可能没法取得当前投稿条款却继续给目标判断。

建议：在三个 one-off 小节增加同一条可执行路由：优先复用本地已验证 Discovery Result/Venue contract；缺失时调用 Discovery 官方来源检索并保留链接、访问日期与深度；若用户只要内联讨论或当前任务不能检索，明确把 novelty/desk rule 标为 provisional 或 HOLD，不把记忆写成事实。写清楚该检索不是 Ideation 本地 Run。

### 6. skipped pilot 的卡片 receipt 用途和 test projection 不清

**优先级：P2 — 不应要求虚构 Task 结果，也不应把 skipped 当成完成。**

证据：2_test/haipipe-idea-pressure-test/SKILL.md:90-105 定义 pilot.status 可为 skipped，并说明 pending/skipped 不需要 Task result、不能通过 Test gate；haipipe-ideation/references/idea-card.md:138-150 又要求 skipped pilot 有 feasibility.receipt，同时示例把 feasibility.receipt 写成 Task runtime 路径；test-matrix schema 的 feasibility enum（2_test/haipipe-ideation-test/SKILL.md:41-54）没有 skipped，只有 pending、positive、negative、waived、hold。

问题与影响：如果 pilot 被跳过，agent 无法判断 feasibility.receipt 应指向压力收据还是不存在的 Task Result，也不知道 matrix 应以何状态投影 skipped。共享 checker 会阻挡未解决 feasibility，这个阻挡本身正确，但字段说明不足以告诉 agent如何如实保存“已跳过”的历史。

建议：明确 skipped 仅要求 pressure receipt 中的状态和理由；它不要求 feasibility.receipt/Task runtime，Idea Card 的 pressure_receipt 保留历史；Test Matrix 映射为 pending，且仍不得进 Select。positive/negative 才要求 Task Result；waived 则使用单独的 waiver 理由。更新示例与 gate 一致。

### 7. 入口页缺少面向新读者的简短“我现在能做什么”

**优先级：P3 — 可读性与 fresh-context 成本，非逻辑冲突。**

证据：haipipe-ideation/SKILL.md:84-120 一开始就进入 build/refresh 与 read-only audit 模式、Task/Discovery/Run/Venue/Paper/Page owner 加载顺序；:148-179 紧接 BJTR 容器、I1/I2/I3 路径和多份 reference。入口描述有价值，但新用户尚未看到“会先问什么、可以得到什么、何时需要本人决定”的短版说明，就需要读一串内部 owner 与文件名。

可能影响：熟悉仓库的 agent 得到具体装载顺序；第一次使用的人需要先理解内部路径，才知道这次请求会产出临时候选、查证结果还是人类目标决定。当前文档信息是有的，问题主要是顺序与认知负担，不应误报为逻辑错误。

建议：在 owner 清单之前加一段 3-4 句的 plain-language quick start，说明三类用户请求（内联 brainstorm、测试一个 Idea、保存 portfolio 并交 Paper）、缺证据会如何标记，以及最终选择/target 必须由人决定；其后保留现有装载规则。术语表可顺手定义 Capability group、Run、Step/Gate、receipt、Paper P0。

英文改写示例：

> “Use this family to brainstorm provisional ideas, test an admitted Idea, or maintain a durable portfolio for Paper. If evidence is missing, we label candidates provisional and route source questions to Discovery or feasibility work to Task. We compare options and prepare the handoff, but you choose each Idea and its target.”

## Workflow / Run 指标

标准：通过要求清楚表达 Workflow 是 Run 列表并说明该技能的工作是 Run、某个 Run 的内部 Step/Gate，或纯投影操作；部分表示没有把普通工具调用错误升级成 Run，但缺少 Workflow/Run 归属；不通过表示权威定义与模型冲突。

| 技能 | 结论 | 当前证据与判断 |
|---|---|---|
| haipipe-ideation | **不通过** | haipipe-ideation/SKILL.md:50-53、78-82、179 定义 three-stage Workflow，却无 Run 清单；workflow-table.md:33-36 把核心活动排除为 Runs。 |
| haipipe-ideation-generate | **部分** | SKILL.md:4、21、73-75、107-110 称 Stage 1 / next stage；没有生成活动属于何 Run 的说明。I1 是能力标签，不是 Run ID。 |
| haipipe-ideation-test | **部分** | SKILL.md:4、17-18 是 Stage 2 router；novelty、pressure、venue 是独立专家能力，matrix 是投影；没有 Run Spec 对应。 |
| haipipe-idea-pressure-test | **部分，Run 边界意识较好** | SKILL.md:50-54 明确新计算要 commissioned 为 Task Run，且不创建本地 Ideation Run；尚未说明 pressure assessment/pressure receipt 是另一个 Run 还是 Test Run 内部分析/收据。 |
| haipipe-novelty-check | **部分** | 逐 claim 检索、阅读和对比适合作为内部 Steps，但持久 novelty receipt 没有 Run/Step 定位；:150、158 的 “run-wide limit” / “no-search run” 未说明指 Run 还是单次 invocation。 |
| haipipe-journal-fit | **部分** | broad screen 与 deep fit 是清楚的两段工作，但它们是 workflow steps 还是有独立目标的 Runs 未定义；:92 又用 Stage 3 指选择。 |
| haipipe-nature-paper-review | **部分** | 文本把它界定为 editorial overlay，当前规则交给 Venue contract，这避免将每个 lens 误称 Run；持久 overlay receipt 没有说明是 Test 的内部步骤/结果还是独立 Run。 |
| haipipe-ideation-select | **部分** | 明确只有人决定，也防止 Page CHECK 覆盖人类收据；但 Stage 3 无 Run 归属，多卡收据不能完整承载逐卡决定。 |

### 活跃术语与兼容字段的分类

- 8 个 Ideation SKILL.md 正文中，直接出现 “Phase” 的关键位置是 haipipe-ideation/SKILL.md:179 的 “phase table”；其余主要用 Stage/three-stage。将该表称为能力组图和 Run 边界图即可，不该通过替换词语把 I1/I2/I3伪造成 Run。
- manifest-and-sync.md:19、31-34 的 manifest stage 字段明确表示当前 capability family，脚本 check_ideation.py:469-479 会将其作为必填字段验证；sync stage: I1 | I2 见 manifest-and-sync.md:93，脚本 :584、597-608 同样会验证。这些是当前 schema，不是已声明的历史兼容字段。可以保留作能力元数据，但不能拿来冒充 Workflow 的 Run 状态。
- references/receipts.md:27-49 当前示例含 Page-owned phase 字段和 phase: OUTLINE | CONTENT；本族 checker :242、246、275-281 读取并验证该字段。它不是本地 Ideation Run。page/haipipe-page/SKILL.md:129-134 明确 controller invocation 是 workflow pass 而非 Page Run，receipt 是 machine workflow record。因此不可盲目把 phase 改为 run。该活跃 Page 合同应交由 Page owner 版本化处理；若用户要求 UI 文案彻底移除 Phase，应提供新读者词与旧 schema alias/migration。
- paper/workflow-phases/haipipe-paper-ideation/SKILL.md:29-47 将 P0 称为 “Journey phase”，但它同时是 Page Type/Story00 页面角色。P0 的身份不能机械改成 Run；Paper owner 应说明该角色如何挂到 Workflow 与 Page Runs。
- changelog 的旧版变更说明是历史材料，不把其中的 Stage/phase 用词计作当前行为缺陷；external-skill-map.md 也只是来源说明。

## 人类交互桌面推演

以下是文档走查，不是运行时观察。

### A. 从宽泛方向开始生成

请求：“帮我围绕生成式 AI 和临床判断想几个论文点子。”

当前规则会先要求方向问题、范围和“值得继续测”的决策规则；核对是否有 pointer-based Task/Discovery bundle；没有来源证据时只能给 provisional Idea，不得将记忆、标题命中或用户猜测描述为观察信号。内联 brainstorm 不写文件，用户要求保存后才进持久单元。这个保护清楚。

建议的首轮答复应直接把限制转成可读状态，例如：“我目前没有可引用的 Task/Discovery 结果，因此下面是待验证方向，不是已观察的研究空白。我先列出需由你定界的人群、临床决策和时间窗，再给临时候选；若要把文献缺口当作事实，需要先查证这些来源。”这样既推进生成，也不会暗示已验证 novelty。若用户提供 brief，必须作为 scope context 而非 claim-support，见 evidence-bundle.md:48-64、86-101。

### B. “有没有人做过？能投 Nature 吗？”

请求同时包含 novelty、可检验性和 venue。当前设计正确要求按 Core Claim 查最近工作，完整阅读 closest work 后再给强判断；pressure 独立评估 identification/data/ethics/experiment；journal-fit 对所有 idea 广筛、只给 live finalist 深评；Nature overlay 必须针对具体 Nature-family target，当前条款另需 Venue contract。最易卡住的地方是 one-off 实时查证如何启动，见发现 5。

更清楚的答复应分别报告：“Novelty: HOLD（缺少逐 claim 的已验证 Result）；Testability: conditional（需先确认变量访问和最小实验）；Venue: 只能做 family-level provisional screen；Nature shape: 暂不判断，先确定是旗舰刊、学科刊还是综述。”然后列出需要 Discovery 查证的问题，不要拿一个总分掩盖各轴。

### C. 比较并交给 Paper

请求：“i01 和 i03 哪个值得做？选一个期刊并交给 Paper。”

文档正确要求展示全部 admitted candidates、分开列出研究增量、识别可信度、可行性、venue 风险、修复工作和 downside；machine recommendation 不等于选择；每个实际入选 idea 需各自 target/category 与 Story。

更易执行的询问为：“我的建议是 i01（原因……），i03 目前因……应 defer。请逐项决定 i01、i03 是 pursue、defer 还是 abandon；对每个 pursue 项指定期刊与 article category，并指出你接受的风险。你也可以暂时不选或多选。我还没有记录人类决定。”用户回答后再由唯一的人类收据授权 handoff。当前 schema 无法完整落下该回答中的逐卡 disposition，见发现 2。

## 建议优先级

1. 先与 haipipe-run、Page、Paper owner 对齐 Workflow Definition、Run Spec 与 Page controller receipt 的术语及身份；同时澄清 I1/I2/I3 是能力组还是 Run 列表。
2. 改 selection receipt 与 checker，使多卡 disposition、逐卡 risk acceptance、target/category、Story route 全有唯一可追溯的人类来源。
3. 声明 Idea Card / Venue Fit Card 的 human_target 都是 I3 receipt 的派生投影，增加漂移检查。
4. 更新 Select UI 短描述，并补齐 Novelty / Journal / Nature 一次性请求的实时来源路由。
5. 明确 skipped pilot 的字段和 test-matrix 映射；之后再做全族术语清理。保留历史 changelog 与兼容 schema，不改写既有 Run/Story/Page identity。

## 值得保留的优秀写法

- evidence-bundle.md:61-101 把内部证据地址、外部 Discovery Result/Bib/runtime 同 stem、Context-only 与 claim support 分开；可直接防止把搜索 hit 当结果。
- evidence-bundle.md:113-183 说明 owner 不转移、指针优于复制、推论与观察分开、冲突保留，且明确改题或改验收要重开 owner workflow。
- idea-card.md:126-167 把 Core Claims、novelty、identification、pilot、venue 分开处理；不以多数、分数或机器推荐取代人的决定。
- journal-fit/SKILL.md:15-42 与 venue-fit.md:11-42 保留 authority 标签并分 broad screen / current-contract deep fit，避免把声誉当作期刊规则。
- haipipe-ideation-select/SKILL.md:20-22、38-65 和 haipipe-paper-ideation/SKILL.md:187-194 明确 Page approval、Page CHECK、machine recommendation 都不产生 idea selection；只有 I3 人类收据授权 Story。
- manifest-and-sync.md:120-173 把 working、release、delivery 分开记录，防止把 Paper 工作视图误称已发布；这是好的投影合同，Run 修订不应破坏其状态语义。

## 交接给协调者的问题

- 主要归属：Ideation owner 与共享 Run owner；当前三阶段模型、I1/I2/I3 capability table、无本地 Run 规则需要共同裁定。
- Page 归属：references/receipts.md 的 Page phase receipt 是 Page-owned 活跃 schema，Page skill 明说 controller pass 不是 Run；应由 Page owner 决定兼容字段迁移。
- Paper 归属：haipipe-paper-ideation 的 P0 “journey phase” 是 Page/Story 角色，不应在 Ideation 中重命名为 Run；Paper owner需给它与 Run Workflow 的关系。
- 其余方面：Ideation 已明确把外部证据交 Discovery、内部计算交 Task、投稿约束交 Venue、文章结构与投影交 Paper/Page。未发现它把 Insight 或 Design 置于 Application 父家族之下；这两家族在本范围中也没有被要求承载职责。
- 未完成项：本报告没有运行 checker 或任何评测，没有外部文献/期刊规则验证，没有审阅第三方上游源文件，也没有完成整套 Page/Discovery/Task 兄弟技能评估。
