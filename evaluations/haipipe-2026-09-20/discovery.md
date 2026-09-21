# Discovery 技能族评估报告

评估日期：2026-09-20  
仓库基线：HEAD f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217  
范围：Discovery 技能族的全部 16 个当前 SKILL.md，以及其直接支持文档、共享 Run 契约、少量运行时代码和直接相关的 Page/ARIS 合约。  
评估方式：静态阅读和桌面 walkthrough。没有执行任何技能、测试、外部服务、网络请求或工具调用；没有修改实现文件。

引用路径约定：`1_search/`、`2_review/`、`3_synthesize/`、`workflow-phases/` 相对 `plugins/haipipe-toolkit/skills/discovery/`；`haipipe-discovery/` 也相对该目录，其下的 DESIGN、agents、ref、scripts 等路径相对该 umbrella 目录；`run/`、`page/`、`references/aris/` 等共享路径相对仓库根目录。脚本简写 `paper_runs.py` 和 `paper_source_access.py` 指 umbrella 下的 `scripts/`。

## 结论

Discovery 的检索路由和单篇论文 Run 契约已有清晰且可复用的设计：一篇候选论文对应一个 Run；零到多个 Run 由 Topic 的范围决定；搜索、API 和审核调用本身不自动成为 Run。主要问题在于 D1 的当前概念与共享 Run 规范不一致：D1 仍被定义为一个“phase”，阶段动作表也列在 workflow 注册表中，而共享 Run 合约明确规定 Workflow 由 Run Spec 节点和图规则组成，不存在独立的 Phase 权威层。

这会让操作者无法从规范中稳定回答“这个 Workflow 定义了哪些 Run、每个 Run 的目标和关闭条件是什么”。同时还发现身份核验状态与人工文献核验状态混用、摘要阅读深度被生成器过早推断、搜索供应方可能产生超出 Discovery Result 契约的持久副作用、Research-lit 的来源选择描述互相冲突，以及合成技能把通用综述技能当作 craft worker 调用却未限定输入边界。

按 Discovery 的 16 个技能统计：2 个 Workflow/Run 评估为 Fail，5 个 Partial，3 个 Pass，6 个 N/A。这里的 N/A 表示技能本身是供应方/能力适配器，不拥有 Workflow 或 Run 定义，不代表该技能没有其他问题。

## 范围、基线与证据限制

- 指定目录中发现的当前 SKILL.md 数量和 BRIEF 中的初始 16 项一致，没有额外 Discovery 技能。
- Discovery 路径在基线中没有修改；基线为上文所列 HEAD。
- 发现若干 reference 子模块工作树有脏状态：cite-guard、grant-writer-skills、paper-rag-skill、paperspine、reprorun、research-agent-skills、research-co-pilot、scipilot-figure-skill。子模块提交与 HEAD 相同，但工作树有未提交内容。本报告没有读取或执行这些变更；external-skill-map 将其中 paper-rag-skill、research-agent-skills、research-co-pilot 列为参考或基础设施，而非 Discovery 的活动规范权威。
- 核对了 Discovery DESIGN、agents README 和相关 agent、Preferences、反馈/摘要支持技能，以及 lifecycle-map、BJTR alignment、page-types、paper-run-contract、discovery-yaml-schema、source-format、external-skill-map、external-capability-registry、workflow-table 等引用。
- 查阅了 Run 主规范、Page Workflow 中与 Run/phase/cycle 元数据相关的部分、论文运行时代码、PubMed 来源访问代码，以及 ARIS integration contract 和 reviewer routing 的相关段落。没有执行这些程序或调用上游工具。
- 历史反馈只作为历史证据处理。其中 2026-09-04 记录描述了一次 D1 fresh-context fixture，覆盖一篇论文、重复项和 Bib pending；它不是本次实时测试，也没有覆盖 provider 或 review worker。旧反馈记录不能替代当前执行验证。
- 这份报告对技能的可执行性和实际运行效果只作静态判断；以下 walkthrough 是桌面推演，不是现场执行结果。

## Discovery 技能清单与 Workflow/Run 裁定

| # | 技能 | 类别 | Workflow / Run 裁定 | 主要说明 |
|---:|---|---|---|---|
| 1 | 1_search/alphaxiv | Search provider | N/A | Run metric 不适用：这是独立 provider procedure；:130-147 有条件 Wiki ingest，副作用另列于发现 3。 |
| 2 | 1_search/arxiv | Search provider | N/A | Run metric 不适用：provider procedure 本身未定义 Discovery Run；:158-177 写明 Research Wiki ingest，:109-137 处理 PDF。 |
| 3 | 1_search/deepxiv | Search provider | N/A | Run metric 不适用：本身只定义 provider procedure；:197-215 为 Wiki ingest 路径。 |
| 4 | 1_search/exa-search | Search provider | N/A | Run metric 不适用：本身只定义 provider procedure；:145-170 将搜索结果接入 Wiki。 |
| 5 | 1_search/gemini-search | Search provider | Pass | :20-22 将 Gemini 定位为 candidate scout/非 Run writer；:48-50、:63-65 明确 Run 分配及 one-off 留给 dispatcher。 |
| 6 | 1_search/haipipe-discovery-search | Discovery router | Pass | :74-114 明确一篇候选论文一个 Run、Trigger 可产生零到多个候选，并把 worker 调用留在内部。 |
| 7 | 1_search/openalex | Search provider | Pass | :74-86 将 Run/Result/Bib 写入交给 dispatcher，并规定 one-off inline/no-files。 |
| 8 | 1_search/paper-analyzer | Analysis utility | Partial | :15-45 把步骤称作 “Workflow” 并生成结构化笔记/图等持久产物，但未定义其与 Discovery Result 的归属关系。 |
| 9 | 1_search/semantic-scholar | Search provider | N/A | Run metric 不适用：本身是 provider procedure；:158-182 有 Wiki 持久写入指引。 |
| 10 | 2_review/academic-researcher | Review/craft worker | N/A | 通用研究辅助技能，:141-176 未声明 Discovery Workflow/Run；由 synth 调用时需限制为已接纳 Result 的 craft 模式。 |
| 11 | 2_review/comm-lit-review | Review/craft worker | Partial | :169-277 定义通用搜索/检索工作流；被 synth :96-122 调作 craft worker 时可能引入未接纳来源。 |
| 12 | 2_review/haipipe-discovery-review | Discovery reviewer | Partial | :37-49 有正确 Run 边界，但 :47-49 让 Page CONTENT 沿 “shared Page phase” 进行；需按 Page owner 的兼容元数据解释。 |
| 13 | 2_review/research-lit | Literature review | Partial | :60-85、:191-206 的 source-selection 规则冲突；:356-372 的 HAI durable 模式边界良好。 |
| 14 | 3_synthesize/haipipe-discovery-synthesize | Synthesis controller | Partial | :96-122 将通用综述/研究技能作为 craft worker 调用，但没有限制为 admitted Results-only 输入。 |
| 15 | haipipe-discovery | Family umbrella | Fail | :91-107 区分 Task 与 Page 工作流，但 :115-133 将 D1 描述为唯一 Discovery “phase”，冲突共享 Run 合约 :193-254。 |
| 16 | workflow-phases/haipipe-discovery-inquiry | D1 controller | Fail | :12-50 将 D1 标为 phase 和 “Phase × Run declaration”；workflow-table :117-124 的 Runs Overview 没有 live rows。 |

裁定阈值：Pass 表示技能有可评估的 Run 边界，并明确符合共享概念；Partial 表示边界大体可用但存在重要歧义或组合模式风险；Fail 表示当前规范与共享概念模型直接冲突；N/A 表示该技能只提供 provider/standalone 操作规程，没有声明 Discovery Workflow/Run 模型，因此此项不适用。N/A 不代表其操作规程没有其他可审查的问题；例如 Wiki/PDF 副作用仍列为单独发现。Provider 文档中的 “Workflow” 小节若只是列举单次能力的步骤，按局部 procedure 处理，不将每个 Step 转成 Run。

### 按技能的支持资料覆盖

下表列出除每个技能自身完整 SKILL.md 外，实际用于交叉检查的直接支持资料。公共支持资料在下一个小节列出。这里的“相关段落”表示按该技能行为所需部分核对，不表示对共享文件每一行都作了独立审计。

| 技能 | 交叉检查的支持资料 |
|---|---|
| 1_search/alphaxiv | external-capability-registry、source-format、ARIS integration-contract（provider 写入边界） |
| 1_search/arxiv | external-capability-registry、source-format、paper-run-contract、ARIS integration-contract（PDF/Wiki 写入边界） |
| 1_search/deepxiv | external-capability-registry、source-format、ARIS integration-contract（Wiki ingest） |
| 1_search/exa-search | external-capability-registry、source-format、ARIS integration-contract（Wiki ingest） |
| 1_search/gemini-search | external-capability-registry、source-format |
| 1_search/haipipe-discovery-search | search-worker agent、creator-agent、source-format、paper-run-contract、external-capability-registry、workflow-table |
| 1_search/openalex | external-capability-registry、source-format |
| 1_search/paper-analyzer | external-capability-registry、paper-run-contract、paper_analyzer 相关脚本写入行为 |
| 1_search/semantic-scholar | external-capability-registry、source-format、paper-run-contract、ARIS integration-contract |
| 2_review/academic-researcher | haipipe-discovery-synthesize 的调用定义、paper-run-contract、source-format |
| 2_review/comm-lit-review | haipipe-discovery-synthesize 的调用定义、research-lit durable 模式、paper-run-contract |
| 2_review/haipipe-discovery-review | reviewer-agent、paper-run-contract、source-format、workflow-table、Page Workflow 的所有权边界 |
| 2_review/research-lit | haipipe-discovery-synthesize 的调用定义、workflow-table、source-format、paper-run-contract |
| 3_synthesize/haipipe-discovery-synthesize | 三个被调用的 review/craft 技能、creator-agent、paper-run-contract、source-format |
| haipipe-discovery | DESIGN、agents/README、PREFERENCES、lifecycle-map、BJTR alignment、page-types、paper-run-contract、discovery-yaml-schema、source-format、external-skill-map、external-capability-registry、workflow-table |
| workflow-phases/haipipe-discovery-inquiry | workflow-table、lifecycle-map、DESIGN、agents/README、共享 Run SKILL.md、Page Workflow、paper_runs.py、paper_source_access.py |

### 排除项与未读材料

- **第三方/上游**：没有浏览或执行任何外部 provider、ARIS、文献索引或插件服务；没有把其网站/API 当前行为当成已验证事实。reference 子模块的脏工作树变更未读取，且不作为本地 Discovery 规范依据。第三方上游文档和服务本身属于未核验材料。
- **历史材料**：读取了列明的 Discovery/Search feedback README 和指定的 2026-06 至 2026-09 反馈记录，用于标注过去覆盖；没有穷尽各目录所有历史反馈、旧版快照或 CHANGELOG。它们不作为当前行为证据。
- **资产**：没有逐个检查图像、截图、附件、生成文件或其他非文本资产；除明确列出的直接相关代码外，也未遍历无引用关系的所有脚本和模板。
- **未读范围**：所有 16 个当前 Discovery SKILL.md 均已全文阅读；未读部分主要是上述第三方上游材料、脏子模块差异、未选取的历史记录和无关资产/代码。此限制已用于收窄结论，不将其描述为已测试的运行时事实。

## 支持覆盖与未覆盖项

已读完 16 个当前 SKILL.md，并交叉阅读了相关支持资料。主要对照关系如下：

- 共享 Run 权威：run/haipipe-run/SKILL.md，特别是 Workflow Definition 和 Run Spec 边界。
- Discovery 自身边界：discovery/DESIGN.md、agents/README.md、haipipe-discovery/SKILL.md、workflow-phases/haipipe-discovery-inquiry/SKILL.md。
- 论文 Run 契约：haipipe-discovery/ref/paper-run-contract.md 与 source-format.md，并核对 paper_runs.py 的相关状态校验。
- 生成器风险：paper_source_access.py 的 reading_depth 赋值和摘要落盘路径。
- Page 的独立领域：page/page-workflows/haipipe-page-workflow/SKILL.md 中 Run 所有权与序列化 phase/cycle 字段。
- ARIS 副作用规则：references/aris/skills/shared-references/integration-contract.md 和 reviewer-routing.md 的相关定义。
- 历史反馈：只用于判断曾覆盖过哪些 fixture，不将历史结果外推为当前验证。

未读取脏 reference 子模块的未提交内容、没有运行任何工作流或脚本，也没有对外部服务进行核验。这些限制不影响发现的文档内部矛盾，但意味着 provider 行为和真实端到端用户体验还需要之后的运行验证。

## 保留的优点

1. Search router 对 Run 数量和边界描述清楚。haipipe-discovery-search/SKILL.md:74-114 将一篇候选论文定义为一个 Run，并明确搜索 worker/API/reviewer 调用不是 Run；一次 Trigger 可以得到零个、一个或多个候选。这与共享 Run 模型的方向一致。
2. 论文 Run 契约区分技术执行完整与 Bib 人工验证。paper-run-contract.md:219-245 说明技术产物齐全时，Bib 仍可能 pending，并由关闭规则阻止 Topic 完结。
3. 来源格式倾向逐篇证据，不靠宽泛元数据表格。source-format.md:6-10,72-88 对粒度、证据和读者可读性有具体约束。
4. Discovery 与 Page 有独立 Run 车道。workflow-table.md:90-100 与 paper-run-contract.md:331-345 提供了区分 Discovery paper/source Runs 和 Page-owned Runs 的依据。
5. 文档承认一篇用户问题可能需要零个或多个 Run；应继续保留动态数量，避免为每个 controller action 或 provider call 创建 Run。

## 人类可读性与交互评估

- 路由器按“one-off”与持久 Task 区分入口，方向正确；但 provider 隐式写入会削弱可预测性。用户在提交 URL 前应能知道是否会创建文件或修改 Wiki，详见发现 3。
- 论文 Run 能将技术产物完成与人工 Bib 核验分开，允许清楚表达“工作已完成但 Topic 尚不可关闭”。风险在状态名 verification 复用和 UI 是否显式展示 pending 回执，详见发现 2 与 walkthrough C。
- Search、Review、Synthesis 之间的责任原则上可读，但 Run Overview 为空、Phase/Cycle 控制器表占据注册表位置，令新读者需要拼读多份材料才能得到实际 Run 清单。详见发现 1。
- 本次没有观察真实 UI，因此不对反馈按钮、应用/拒绝反馈、暂停/恢复控件的运行体验作结论；对这些交互的覆盖限于文档和反馈说明的静态检查。

发现优先级：P0 表示共享模型级的定义冲突，会影响整个 Workflow/Run 解释；P1 表示可能改变来源范围、持久副作用或闭环状态的操作歧义；P2 表示维护信息过期但不直接改变 Run 语义。

## 发现 1 [P0]：D1 的 Phase 模型与 Workflow = Run Specs 冲突

### 证据

- workflow-phases/haipipe-discovery-inquiry/SKILL.md:12-50 将 metadata 标为 workflow: haipipe-discovery-inquiry 和 phase: D1，并说 “D1 is the sole Discovery Folder phase”；随后将宏流程列为 “SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE”，并使用 “Phase × Run declaration”。
- workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md:8-18 将 D1 task workflow 和 Page Face workflow 展示为序列，并称其为 D1 phase。
- workflow-table.md:52-79 将 d1.scope、prepare、acquire、synth、close 列成 D1 Cycle 表；主要表头是 Phase | Cycle。它把控制器动作放进 workflow/phase 注册位置。
- workflow-table.md:117-124 的实际 Runs Overview 没有 live rows；这使读者看不到任何按共享契约定义的 Run Spec 清单。
- workflow-table.md:126-151 将 paper-analysis/source-analysis 列为 Run Profiles，同时说 Page Runs 另有所有者、上述动作不是 Runs；这部分是有用区分，但与前述 Phase 注册表放在一起，仍未形成“Workflow 由哪些 Run Specs 组成”的权威答案。
- haipipe-discovery/SKILL.md:91-107 区分 Discovery Task 工作流和 Page 工作流，但 :115-133 又把 workflow-phases 目录称为唯一 D1 phase owner。
- discovery/DESIGN.md:27-53、agents/README.md:9-10,45-47、lifecycle-map.md:14-22,74-85 仍沿用当前 Phase/D1 术语，扩大了不一致的影响范围。
- 共享规范 run/haipipe-run/SKILL.md:193-254 明确写明：Workflow Definition 是由有界 Run Spec 节点和图入口/终止规则组成；没有独立 Phase authority layer；一条 Workflow 表项必须对应一个可独立关闭的 Run Spec，不能是 Phase、Step 或调用；Step 是 Run 内部动作；只统计已物化的 Run 实例。

### 影响

使用 Discovery 文档的人无法判断 D1 本身是否是一个 Run、还是由多个 Run Specs 组成的 Workflow，或只是 Task controller。将 SCOPE、PREPARE、ACQUIRE、SYNTHESIZE、CLOSE 一律理解为 Run 会造成虚增；把它们当 Phase 则违反共享定义。注册表中的 Runs Overview 又是空的，所以真正的 Run Specs、动态数量和关闭规则没有被集中声明。

### 推荐修正

将 D1 定位为 Discovery Task controller。控制器动作保留为内部路由、阶段/状态或 gates，但不放进 Run Spec 表。Workflow Definition 只列出具有独立目标、Result 和 close rule 的真实 Run Specs，以及 Workflow 图的入口、终止条件和依赖关系。声明持久 Topic 可生成零个或多个 Discovery Runs，每个 Run 对应一个已接纳的 canonical Subject；provider、API、reviewer 和 synthesis 调用仍是内部 Step/控制器动作，除非单独的 Run Spec 明确赋予独立目标、Result 和关闭规则。

应刷新 workflow-table，使 Runs Overview 真正列出 Run Specs 或明示 Workflow 不定义任何独立 Run Spec、Run Profile 由何处实例化；将当前 Phase × Run 表重命名/移出 Workflow Definition，作为 controller routing/state 表。同步更新目录名、phase:D1 metadata 和当前说明文档的交叉引用。不要把 phase:D1 机械替换成 run:D1：D1 控制器不是一篇 paper/source Run。

### 兼容性边界

Page Workflow 的 page/page-workflows/haipipe-page-workflow/SKILL.md:345-347 允许 phase、cycle、next_cycle 作为序列化的描述性元数据。它由 Page Workflow 所有者定义，不应被误判为 Discovery 自己的 Phase authority，也不应在修复 D1 时全局删除这些兼容字段。BJTR alignment 和 schema 中明确标为历史/legacy 的 0/1/2/3、manifest type/role 字段也应继续作为 legacy/read-only 解释；它们不能替当前 D1 Phase 模型辩护。

## 发现 2 [P1]：两种 verification 的语义冲突，摘要深度也有过度推断

### 证据与风险

- agents/haipipe-discovery-search-worker-agent.md:32-42,63-75 使用 verification: VERIFIED | NEEDS-VERIFICATION 表示候选论文身份解析结果。
- haipipe-discovery/ref/source-format.md:20-40 又将 Card 上的 verification: VERIFIED 定义为由人对照可信 publisher/index 确认 title、authors、venue、locator。
- paper-run-contract.md:219-245 中 bib.verification.status 为 pending/verified，且 verified 需要 person 的 by/at 信息。即使技术执行完成，Bib 仍可 pending；paper_runs.py:232-244,823-833,903-923 校验该人工回执并可返回 CLOSURE_HELD citation-verification=N。
- paper_source_access.py:174-212 在 PubMed abstract 存在时将 reading_depth 设置为 abstract；:258-263 则生成摘要文件。共享契约要求 reading_depth 表示实际检索并检查过的深度，而非仅有可用内容。

摘录：worker 字段为 “verification: VERIFIED | NEEDS-VERIFICATION”；Bib 合约使用 “bib.verification.status: pending/verified”；生成器依据 PubMed abstract presence 设置 “reading_depth=abstract”。三个字段看似相似，实际描述的是身份解析、人工引文确认和已检查的阅读深度。

把身份解析标成 VERIFIED 容易被误读为 Bib 已经通过人的引用核验；用 abstract 可用性直接标注 reading_depth，又可能让下游以为摘要内容已被读取和检查。

### 推荐修正

将候选身份状态改为不与 Bib 语义冲突的字段，例如 identity_resolution: confirmed | needs-review。仅将 bib.verification.status 用于人工文献身份/引文核验，并继续要求 by/at 证据。Card 若无必要可删除 verification 字段，或改成 identity-only 的明确定义。

将来源信息分为 available_depth、retrieved_depth 和 inspected_depth/reading_depth。只有有证据表示正文/摘要被实际读取或检查后，才递增 inspected depth；仅发现 PubMed abstract 或下载/生成本地文件，不等于已检查。

### 建议的英文 status 改写示例

Before:

    verification: VERIFIED

After:

    identity_resolution: confirmed

Before:

    reading_depth: abstract

After:

    retrieved_depth: abstract
    reading_depth: metadata

After an actual inspection, the Run may advance reading_depth to abstract. Keep Bib verification separate and pending until the required person and timestamp receipt exists.

## 发现 3 [P1]：Provider 的持久写入会越过 Discovery Result/one-off 边界

### 证据

- haipipe-discovery/SKILL.md:281-288 将未带 Task 的单 URL 请求描述为 one-off；:454-459 说明相关模式以 inline 输出、不创建文件为主。
- haipipe-discovery-search/SKILL.md:127-132 同样描述 one-off inline/no-files；agents/creator-agent.md:76-93 将创建者产物定位为配对的 Result。
- alphaxiv/SKILL.md:130-147 在 Research Wiki 已存在时要求 ingest。
- arxiv/SKILL.md:16-26,109-137,158-177 会将 PDF 放到 papers/ 并写 Wiki。
- deepxiv/SKILL.md:197-215、semantic-scholar/SKILL.md:158-182、exa-search/SKILL.md:145-170 有 Wiki ingest 路径。
- paper-analyzer/SKILL.md:15-45 会写结构化笔记/图等输出，但没有明确映射到 HAI Discovery Result 的所有权和路径。
- ARIS integration contract 对 Research Wiki 副作用和 artifact 所有权有独立政策；它说明这些路径并非单纯的 inline provider response。

摘录：umbrella 和 search router 把无 Task 的 URL 查找描述为 “one-off” 和 “inline/no-files”；provider 文档同时包含 Wiki ingest 或 PDF 写入路径。因而同一请求模式的输出持久性取决于被调用 provider 和目录状态。

### 影响

同一个 URL 或搜索请求在“one-off inline/no-files”与“存在目录即自动 ingest/write”之间可能产生不同副作用。用户很难预测一次查找会不会新建文件、修改 Wiki，或绕过由 Discovery creator 负责的配对 Result。对 synthesis 来说，不在 Result 中的资料也难以获得稳定的 provenance/核验状态。

### 推荐修正

在调用边界上明确三种模式：Discovery durable Task、one-off inline、独立 provider/Wiki 用法。Discovery 的 durable Task 中，provider 默认只返回候选和来源数据，由 Discovery creator 写规范化 Result；Research Wiki/PDF archive 写入必须是显式选择并由单一 owner 管理。one-off 模式应保持 inline/no-files。paper-analyzer 应返回可由 creator 纳入 Result 的 packet，或声明其文件输出只在独立 standalone 模式使用。把外部 Wiki/PDF 写入和 Result 创建分开记录，避免同一资料由 provider 与 creator 双写。

## 发现 4 [P1]：Research-lit 的 source-selection 声明与执行说明相矛盾

### 证据

- 2_review/research-lit/SKILL.md:60-85 规定只有显式列出的 source IDs 才运行；例如 sources:zotero 被解释为只运行 Zotero，默认 all 排除 S2/DeepXiv/Exa/OpenAlex/Gemini。
- :185-206 又说始终运行 arXiv API 与 WebSearch。
- :89-101、:191-229 的来源表及检索路径与前述默认/显式选择不完全一致。
- :356-372 有适合 HAI durable 模式的良好边界：不写 Run 文件、基于已存在 Result/citations 工作；这部分应保留。

摘录：同一技能一处写 “sources:zotero means Zotero only”，后文又写 “arXiv API always runs” 和 “WebSearch always”。这是行为规则之间的直接冲突，不是单纯说明不够详细。

### 影响

用户请求指定 Zotero 或其他窄来源时，技能可能仍悄悄触发 arXiv/WebSearch；反过来，默认 all 也可能遗漏读者以为包含的 Discovery provider。检索覆盖范围和“未搜索的来源”无法复核。

### 推荐修正

为 durable 和 standalone 模式共用一份规范 source-ID 表。all 应展开为明确的 ID 列表；显式 sources 清单只执行清单中的来源。若某来源被强制调用，必须标记为 required 并在调用之前纳入请求解释，不能在后文暗中覆盖选择。输出包含 searched/unsearched IDs 和每条证据的来源 provenance。持续保留 HAI durable 的不写 Run 文件、只用已接纳 Result/citations 规则。

### 建议的英文规则改写示例

Before:

    sources:zotero means Zotero only.
    Always run the arXiv API and WebSearch.

After:

    Run only the source IDs explicitly requested. The value all expands to the source IDs listed in the selected profile. Do not call arXiv or WebSearch unless its source ID is selected. Report selected, searched, and unsearched source IDs in the result.

## 发现 5 [P1]：Synthesis 把通用搜索型综述技能当 craft worker，输入边界不清

### 证据

- 3_synthesize/haipipe-discovery-synthesize/SKILL.md:96-122 将 research-lit、comm-lit-review、academic-researcher 作为 draft craft worker 调度。
- research-lit:356-372 有明确的 HAI durable 模式，可基于已存在 Result 与 cite。
- comm-lit-review/SKILL.md:71-110,169-277 有独立的广泛检索/检索与综述输出模式；没有 HAI 的 durable Result/Bib 输入限制。
- academic-researcher/SKILL.md:141-176 提供通用研究总结，但没有 Discovery Result 路径/cite-key 的约束。

摘录：haipipe-discovery-synthesize 将三个技能调度为 “draft craft worker”；comm-lit-review 同时包含 standalone search/retrieval 流程，而调用说明没有写出 craft-only、已接纳 Results only 的输入约束。

### 影响

Synthesis 可能把新的、未接纳的搜索结果带入 Topic 结论，无法稳定说明每条主张来自哪个 Result、哪些证据仍 pending。worker 名称相同但模式不同，也使执行者不容易知道调用后是否会触发搜索或持久写入。

### 推荐修正

定义显式 craft-only 调用模式：输入只允许已接纳的 Discovery Results、citation keys、reading depth、限制条件与待回答主张；输出只包含 claim/theme/contradiction、支持的 Result IDs/cite keys、证据深度和缺口。新的资料需求应返回为 Search Trigger，由 Discovery 搜索路由处理。craft worker 内的工具调用仍然是 Step；不得仅为隔离每次模型/API/tool 调用而新建 Run。

## 发现 6 [P2]：Workflow registry 中的覆盖表已过时

workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md:191-199 说明覆盖数据截至 9/13；:203 仍将 haipipe-discovery 标为 v0.13.0 / 461 lines。当前 haipipe-discovery/SKILL.md:15-18 标记 v0.14.0、更新时间 2026-09-19，文件实际为 464 行。

此表可能是人工维护的历史摘要，而非权威机器生成结果；但读者无法知道哪些项过期。建议把版本/行数/覆盖率这类校验资料与 Workflow Definition 分开维护，标明生成日期和生成方式，或删除无法持续保持准确的列。更新这个表时同时处理上文的 Runs Overview 空表问题。

摘录：coverage 表列 “haipipe-discovery v0.13.0 / 461 lines”；当前技能 metadata 列 v0.14.0 且 updated 2026-09-19，文件为 464 行。

## Desk walkthroughs（静态推演，非现场运行）

### A. 单 URL 的 one-off 解释

输入：用户发来一个 arXiv URL，想要快速了解论文；没有 Task。

按 haipipe-discovery/SKILL.md:281-288 和 search router :127-132，走 inline one-off；可按请求让 AlphaXiv 提供概述或由 provider 返回来源数据，不创建 Discovery Task/Result，也不创建 Run。停止条件是回答了用户问题或说明仍缺少什么。

暴露出的歧义：alphaxiv/SKILL.md:130-147 在 Research Wiki 目录存在时可能要求 ingest。静态规范未充分说明这条 Wiki 写入是否适用于 one-off。改进后应能明确回答用户：“我会只在回复中给你论文概述，不会保存到 Research Wiki”，或者当用户选择 Wiki 归档时先走明确的 durable/standalone 模式。不得将 provider 的身份解析状态解释为人工 Bib 已验证。

### B. 持久 landscape Topic

输入：用户要做一个可复核的领域 landscape，跨多个主题，需要合成结论。

预期路径：创建或选择 durable Topic，明确范围和来源；为每个接纳的 canonical Subject 建立一个 Discovery Run（总数可为 0..N）；对每个 Result 进行 review、记录来源与阅读深度；synthesis 只使用已接纳 Results；出现证据缺口时回到 Acquire；Page 内容由 Page Workflow 所属车道处理；Bib 人工验证未完成时，技术 Runs 可完成，但 Topic 仍不能关闭。

桌面推演发现：Run Profile 表列出 paper-analysis/source-analysis，但 Runs Overview 是空白，D1 的 Phase/Cycle 表又与真实 Run 列表混在同一注册区域。用户无法在规范中迅速确认实际 Run Spec、每个 Result 和 close condition。一个可复核的完成视图应列出 searched/unsearched channels、admitted/unresolved subjects、Run 状态、Bib pending 状态和 Result 链接。此次只是静态检查；不表示 UI 已具备或缺少这些展示。

### C. DOI 解析后摘要可用、引用待人工核验

输入：一个 DOI 指向有 PubMed abstract 的论文；用户要核对摘要和全文可用性。

预期：解析 canonical Subject；运行对应的 paper Run；记录抽取/检索到的来源；只有真的检查摘要后才将 reading_depth 标为 abstract；全文链接可记录为 availability，但链接存在不等于读过全文；技术产物可 complete，而 bib.verification.status 仍为 pending，直到规定的人工作业回执到位。

建议的英文响应范例：

    I resolved the DOI to “<title>”. I retrieved the PubMed abstract and checked that text; I did not inspect the full paper. The citation entry is still pending human verification, so the Run artifacts are complete but the Topic cannot close yet. Full-text access: <found/not found link>.

当前生成器可能仅凭 PubMed abstract 存在就写 reading_depth=abstract；上面建议的响应依赖真实检查状态，不能由摘要可用性自动得出。

## 英文规则改写草案

以下为规则草稿，可供后续技能修订使用；本次未将其写入任何 SKILL.md。

### D1 / Workflow 边界

Before:

    D1 is the sole Discovery Folder phase and owns the domain/Task workflow: SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE.

After:

    D1 Inquiry is the Discovery Task controller. Its internal actions are SCOPE, optional PREPARE, ACQUIRE, SYNTHESIZE, and CLOSE. The Workflow Definition lists only independently closable Run Specs and their routes. A durable Topic may allocate zero or more Discovery Runs, one per admitted canonical Subject; Search, API, reviewer, and synthesis calls remain internal Steps or controller actions unless a separate Run Spec gives them an independent target, Result, and close rule. Page-owned Runs are declared by the shared Page Workflow and do not enter the Discovery Run count.

### Candidate identity 与人工 Bib verification

Before:

    verification: VERIFIED

After:

    identity_resolution: confirmed

规则补充：This field records candidate identity resolution only. Set bib.verification.status to verified only when the required person and timestamp receipt exists.

### 检索范围

Before:

    sources:zotero means Zotero only.
    Always run the arXiv API and WebSearch.

After:

    Run only the source IDs explicitly requested. The value all expands to the source IDs listed in the selected profile. Do not call arXiv or WebSearch unless its source ID is selected. Report selected, searched, and unsearched source IDs in the result.

### Synthesis craft mode

建议新增英文输入/输出约束：

    In craft-only mode, use only the admitted Discovery Results and citation keys provided in the input. Do not search for new sources or write standalone artifacts. Return claims, themes, contradictions, supporting Result IDs and cite keys, inspected depth, and evidence gaps. Route new-source requests back to Discovery Search as Triggers.

这些是重写草案，不意味着本次已改动实现或技能文件。

## 跨技能族所有权与修复顺序

- **Run 共享定义**：run/haipipe-run 是 Workflow Definition 由 Run Specs 构成的规范所有者。Discovery 应遵守该模型，而不是在本地建立第二层 Phase authority。
- **Page Workflow**：Page Writing 有独立 owner 和 Run lane；D1 不应将 Page Run 计入 Discovery Runs。Page 序列化的 phase/cycle/next_cycle 字段属于兼容性描述元数据，不应和 Discovery 的 Phase authority 混为一谈。
- **Ideation、Insight、Design**：Discovery 应维持与这些领域的并列关系。发现的 Discovery 配置只在 haipipe-discovery/SKILL.md:295 使用 applications/ 目录作根路径检测；未发现它定义了 Application 父级或继承关系。不要将 Discovery 改造成 Application 下属层级。
- **Legacy BJTR/manifest 字段**：已明确标记为旧格式/只读的历史字段可以保留兼容读取；不应据此保留当前 D1 控制器的 Phase 注册模型。
- **推荐修复顺序**：
  1. 先改写 D1/registry 的当前术语与结构，清楚区分 Task controller、Workflow Definition、Run Spec、实际 Run、Step。
  2. 合并 identity resolution 与 Bib 人工验证的字段语义，并修正摘要阅读深度来源。
  3. 明确 provider、creator、Wiki/PDF archive 的单一持久写入所有者和运行模式。
  4. 统一 Research-lit source-ID 选择行为。
  5. 加上 synth craft-only 合约及来源闭环。
  6. 更新或去除过时覆盖表数据。
  7. 修复完成后再运行端到端验证，覆盖 one-off、持久 Topic、provider side effects、review、Bib pending/verified 与 Page handoff。
