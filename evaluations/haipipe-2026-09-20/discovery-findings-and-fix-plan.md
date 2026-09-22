# Discovery 问题复核与修复计划

日期：2026-09-20。复核基线：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`；当前工作树，关键共享契约核对时间为 21:11 UTC 前后。  
原评估：[discovery.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/discovery.md)。  
本次产物仅为本补充报告；未修改技能、代码或原报告，未运行操作技能、测试、外部 API、安装器或迁移程序。本会话没有另一项已批准且正在执行的 Discovery 修复任务。

## 复核结论与范围

原报告中的 D1 Phase 权威、verification 混用、阅读深度、provider 副作用、research-lit 来源选择及覆盖快照问题仍有当前证据。Synthesis 的问题需要收窄为“调用方和通用 worker 的模式未对齐”：调用方已经要求 accepted Results，并禁止凭空补证据，不能说它完全没有边界。

另外确认两个原报告遗漏的跨族问题：Discovery 校验器只认识旧 Page Run 编号；Discovery 聚合 Bib 的当前写入位置又被 Page 引用契约明确停用。补充报告共列 **9 项问题：1 项 P0、6 项 P1、2 项 P2**。P0 表示阻断用户要求的模型一致性验收；P1 表示会影响写入、证据状态或跨族交接；P2 表示模式清晰度或维护信息问题。优先级不等于已经观察到生产事故。

全族仍为 **16 个 SKILL.md，未发现新增或退休的 Discovery 技能**。逐文件比较当前内容和 HEAD，16 个均相同，Discovery 目录没有未提交差异。原审查已经全文阅读这 16 个技能；本轮重读原报告，并对每个技能的相关规则、支持契约和必要代码重新定位证据。它不是第二次端到端执行测试。

仓库已有其他任务的改动，包括 Page、Insight、Board、Task、Display、0_utils、README，以及八个 dirty reference 子模块；均保留。共享 Page Workflow、Workflow runtime、table-workflow 的当前改动已纳入交接判断。新的 typed Page Run 名称在 HEAD 中已存在，不能把本次发现的错配归因于其他任务的新改动。

以下路径简称均为精确的仓库相对根：

| 简称 | 路径 |
|---|---|
| D | `plugins/haipipe-toolkit/skills/discovery/` |
| S | `plugins/haipipe-toolkit/skills/` |
| P | `plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/` |
| C | `plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/evidence/citations.md` |

注意：DESIGN.md 和 agents/ 位于 D 直接下级；Run、Page 的路径位于 S 下级。原报告的部分路径简称说明不准确，本报告以上表及完整链接为准。

## 对原报告的必要修正

1. **空 Runs Overview 本身不是缺陷。** `D/workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md:117–121` 明确说明这是未绑定 live Folder 的模板，因此不应伪造运行实例。实际问题是 Workflow Definition 仍由 Phase/Cycle 动作表担任，缺少完整 Run Spec 定义；修复不能往实例表填虚构 Run。
2. **arXiv PDF 下载不是默认副作用。** `D/1_search/arxiv/SKILL.md:109–111` 写的是 “When download is requested”。已明确请求的下载应保留。未经显式模式区分的 Wiki ingest 才是本项主要冲突。
3. **Synthesis 已有上层防线。** `D/3_synthesize/haipipe-discovery-synthesize/SKILL.md:51–55,69–94,98–122` 要求 completed/accepted Results、规范化 packet、缺口回到 ACQUIRE。D06 是 worker 模式的衔接缺口，尚无证据证明已发生引用污染。
4. **阅读深度的合法低阶值是 `metadata-only`。** `D/haipipe-discovery/scripts/paper_runs.py:126` 的枚举不是 `metadata`。原报告的示例不能原样落地。检索脚本也没有直接写入 Run 的 `runtime.yaml`；已确认的是它把检索到的摘要标成 Reading depth，不能扩大为所有 Run runtime 已被自动污染。
5. **引文需区分原文和释义。** research-lit:191 原文是 “always runs”；WebSearch 在 :185–189 没有对应 sources 条件。原报告的 “WebSearch always” 是概括，不是该行逐字引文。
6. **Page 边界并非全面一致。** Run 所有权原则值得保留，但编号识别和 CITE 存储交接存在 D07/D08 的明确冲突。

## 全族覆盖及 Workflow/Run 指标

指标：**A Workflow is a list of Runs. Workflow units use Run, not Phase.** 共享实现把 Run 列表进一步表达为含 gates/routes 的 Run Spec graph，不能用 Phase 或 controller 另设语义权威。一个检索调用、内部 Step、反馈轮次或文件不自动成为 Run。

本表将“Workflow/Run 模型”与“来源选择、写入或交互质量”分开评分。重新分类为 **2 Fail、2 Partial、4 Pass、8 N/A**；原表为 2/5/3/6。差异来自评价维度收窄，并不表示技能已修好。N/A 指只定义局部能力规程，未承担独立 Workflow/Run 定义；其其他问题仍必须修复。局部规程中泛用的 “Workflow” 标题建议改为 “Procedure”，保留内部 Steps。

| 当前技能（均在 D 下，全文基线未变） | Run 模型 | 本轮证据、问题与处置 |
|---|---|---|
| `1_search/alphaxiv` | N/A | SKILL.md:130–147 按 Wiki 目录存在自动 ingest；纳入 D04。 |
| `1_search/arxiv` | N/A | :28–40 是 provider procedure；:109–111 为显式下载；:158–177 自动 Wiki ingest。D04 区分两类写入。 |
| `1_search/deepxiv` | N/A | :197–215 对实际深读的论文自动 ingest；不是所有 search hits。D04。 |
| `1_search/exa-search` | N/A | :145–170 只对 research-paper 类结果自动 ingest；D04。 |
| `1_search/gemini-search` | Pass | :19–22,46–50,63–65 明确不是 Run writer，候选交给 dispatcher；作为 D04 的正例保留。 |
| `1_search/haipipe-discovery-search` | Pass | :74–114 把 admission/Run 分配放在 specialist；worker 调用不创建 Run。:116 的 VERIFIED 定义纳入 D02。 |
| `1_search/openalex` | Pass | :76–86 将 Run/Result/Bib 留给 dispatcher，one-off 无文件；保留。 |
| `1_search/paper-analyzer` | N/A | :15–45 是本地分析/笔记/图规程，不构成 Discovery Run Spec；输出所有权和 vault 前置条件纳入 D04。 |
| `1_search/semantic-scholar` | N/A | :158–182 自动 ingest 已展示论文；D04。 |
| `2_review/academic-researcher` | N/A | :141–176 通用 summary 模板不携带 Result/cite-key 约束；D06 adapter 处理。:216 的 “Study-Phase Retrieval” 是学术概念，不能机械重命名。 |
| `2_review/comm-lit-review` | N/A | :71–87,169–225 默认搜索且 unavailable 静默跳过；与 craft-only 调用不对齐，D06。 |
| `2_review/haipipe-discovery-review` | Partial | :37–49 每 source 一个 Run 且不自行分配，边界正确；:47–48 “shared Page phase” 是当前措辞问题，归 D01；verification packet 归 D02。 |
| `2_review/research-lit` | Pass | :103–115,360–372 明确由 Search 分配 Run，worker 不建 Run/Result/Bib；来源规则仍有 D05，acquire/synthesize 模式仍有 D06。 |
| `3_synthesize/haipipe-discovery-synthesize` | Partial | :143–151 不创 Discovery Run 的边界正确；:51–55,109–113 仍以 Page phase 指认 writer；:35–39 的 Page Run 名称过时。D01/D02/D06/D07/D08。 |
| `haipipe-discovery` | Fail | :91–133 把 D1 Phase 当当前权威；D01。closure、聚合和 Page 引用交接还涉及 D02/D07/D08/D09。 |
| `workflow-phases/haipipe-discovery-inquiry` | Fail | :12–13,27–51 明示 phase:D1 和 Phase × Run；D01。Page Run/Result 与跨面关闭还涉及 D07/D08。 |

Supporting material 本轮核对包括 D 的 DESIGN、agents 角色说明、source-format、paper-run-contract、external-capability-registry、lifecycle-map、discovery-yaml-schema、BJTR alignment、workflow-table；共享 Run、Page Workflow、Page interactive-writing-run、Outline citations；以及 paper_runs.py、paper_source_access.py、paper-analyzer 两个脚本的相关代码和相关测试的文本。反馈/preferences 的历史模式不作为当前 UI 运行证据。

## D01 · P0：D1 仍由 Phase/Cycle 表担任 Workflow 权威

**证据与位置。** [D1 Position](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/workflow-phases/haipipe-discovery-inquiry/SKILL.md:27) :27–51 写 “D1 is the sole Discovery Folder phase”，并称注册表为 “Phase × Run declaration”；frontmatter :12–13 为 `workflow: haipipe-discovery-inquiry`、`phase: D1`。`ref/workflow-table.md:73–79` 的 Full Workflow Table 把 SCOPE、PREPARE、ACQUIRE、SYNTHESIZE、CLOSE 放入 Phase/Cycle 行。`D/haipipe-discovery/SKILL.md:91–133`、`D/DESIGN.md:27–53` 和 `D/agents/README.md:9–10` 重复该权威关系。

共享 [Run 定义](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:193) :193–254 明确 “There is no separate Phase authority layer”；:234–235 要求一行是可独立关闭的 Run Spec，不能是 Phase、Step 或调用；:209–211 的 controller 仅是描述性路由标签。

**影响。** 新读者需要在 D1、Task、Page 两套流程和 rNN 实例之间自行猜测：五个动作是不是五个 Runs、谁持有 gate、何时完成。把 Phase 字样换成 Run 会错误产生 SCOPE Run、Search API Run 或 umbrella synthesis Run。

**修复方案。** 保留 Discovery Folder 的领域与产物契约，把可执行定义明确列成参数化的 `paper-analysis` / `source-analysis` Run Specs，写明 target、actor、input、技术 exit gate、terminal route 和 cardinality。D1 可以继续是 Folder/兼容路由标识；controller 不得与 Run graph 争夺 gate/route 所有权。SCOPE/PREPARE 等词改为调度说明，内部实际工作归属于相应 Run Steps 或外层 Folder 初始化/汇总，不冒充 Workflow 节点。

建议将当前目录移至 `D/folder-kinds/haipipe-discovery-inquiry/`，保留 skill name，避免额外创建第二个入口。该目录方案属于实施建议，需与正在改动的 STRUCTURE/Folder registry 统一；当前文件不移动。同步检查所有有效引用、agents、图、模板和 metadata。Page API 的 `phase/cycle/next_cycle` 可作为标注清楚的序列化兼容字段保留（P/SKILL.md:345–347）。保留历史记录，不批量改写历史引用。

**验收。** 活动 Workflow Definition 的每个工作单元均能映射到一个 Run Spec；实例数来自实际 allocation，零命中和 unchanged duplicate 不分配；没有额外 Phase authority；每个 Phase 命中均能归入历史引用、领域学术用语或明确的兼容字段。空实例表继续允许为空。目录移动后，两套安装器的递归发现仍得到唯一的 16 个技能入口，没有因兼容副本产生重复；这次内部移动不引入新的 top-level package。

**负责人/确定性。** Discovery 主改，Run/Task Workflow 与 table-workflow 共同确认 schema；概念冲突已确认。

## D02 · P1：身份解析、人工引文核验和引用可发布状态混在一起

**证据与位置。** [search-worker return](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/agents/haipipe-discovery-search-worker-agent.md:63) :63–74 返回 `verification: VERIFIED | NEEDS-VERIFICATION`；search router:116 将 VERIFIED 定义为独立 canonical identity confirmation。[source-format](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/ref/source-format.md:29) :29–40 则要求同名状态由人确认，:100–105 的 one-off 例子也直接显示 VERIFIED。`paper-run-contract.md:241–245` 和 `paper_runs.py:829–833` 要求 `bib.verification.status=verified` 必须有 `person:…` 与时间。

另一个已核实的措辞差异：synthesize/SKILL.md:135 把 derived Bib 称为 “union of complete verified Results”；paper-run-contract.md:324–329、`paper_runs.py:807–853` 和 `C:51–54` 允许技术 complete 的 entry 进入 union，把人工 verification 放在后续 ready/closure gate。

**影响。** 人看到 “VERIFIED” 无法知道是机器找到了权威记录，还是自己已完成引用核验。技术完成、预备聚合和可发布之间也容易混淆。现有校验器确实要求人工回执，因此本项不是已经证明可自动绕过人审的漏洞。

**修复方案。** 候选 packet 使用 `identity_resolution: confirmed | needs-review`；人工状态继续唯一存放在 `runtime.yaml#bib.verification`。Card、one-off 和 review packet 分别展示其所依据的状态，不把 candidate 的 confirmed 升格为人的 verified。旧泛化 verification 字段只能作为 identity/unknown 的兼容输入，不能自动生成核验人和时间。统一说明：预备 payload/union 可包含 complete、pending 的材料；真正的 CITE ready、Page release 和 Task epistemic close 必须满足人工 gate。D08 决定最终 payload 容器，但不会改变这一状态区分。

**验收。** 同一 fixture 的 runtime pending、Card 和人类响应一致；即使 candidate confirmed，仍显示待人工核验；只有真实 person/by/at 回执可改变人工状态；complete 与 verified 两种过滤规则分别用于明确的阶段，文档、聚合器和 close gate 无矛盾。

**负责人/确定性。** Discovery owns identity/Result receipt；Page/Outline owns CITE ready/release。字段混用与过滤措辞差异已确认，实际误导发生频率未测。

## D03 · P1：摘要被检索到，就被标注成已经检查的 reading depth

**证据与位置。** [paper_source_access.py](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/scripts/paper_source_access.py:175) :175 执行 `reading_depth = "abstract" if pubmed.get("abstract") else "metadata-only"`；:200 写入 retrieval 字段；:238 的 Markdown 标签为 “Reading depth”；:303 也打印该值。脚本 :258–263 只落盘 Retrieved abstract。另一方面 `paper-run-contract.md:235–240` 定义 reading_depth 为 “actually retrieved and inspected”。

**影响。** 仅下载摘要的动作会被展示为摘要分析已完成。之后的综述可能误判事实的阅读基础。当前代码把检索记录和 runtime analysis 两处 depth 分别校验合法枚举（paper_runs.py:288–328），并未证明二者所描述的是同一个检查事件。

**修复方案。** 用现有 `full_text: found/not-found` 表达可用性，把检索器字段/展示改为 `retrieved_depth`；保留 `runtime.analysis.reading_depth` 作为实际分析者检查过的深度，并附可定位的 read receipt。不必再增加一整套重复字段。未完成检查时不自动升级 reading_depth；如保留现有枚举，低阶值使用 `metadata-only`。旧记录中的 retrieval.reading_depth 迁移成 retrieval hint，不能自动认定发生过检查。完整文章链接不自动升级为 full-text。

字段更名需版本化 source-access schema，先让读取端兼容旧字段，再切换新记录的写入和展示；不得在旧记录缺少 inspection receipt 时自动补出“已读”的结论。

**验收。** mock PubMed 有 abstract 时只提升 retrieved depth；读取并提供摘要 locator/receipt 后才提升 analysis depth；只有全文链接时仍不能标 full-text。source-access 展示、runtime 和下游 packet 使用同一语义。校验能检查回执和 locator 是否存在；它不能独立证明模型“理解”了文章，这一限制须保留。

**负责人/确定性。** Discovery scripts/contract/worker；代码分支与语义冲突已确认。没有执行真实 PubMed 查询。

## D04 · P1：Provider 的写入模式未遵守调用方的 one-off/Result 边界

**证据与位置。** umbrella:456–459、search router:127–132 规定 one-off inline、无持久文件；search-worker:19–20,55–60 要求只读。实际 provider 文本如下：

| 技能/位置 | 当前明确写入条件 |
|---|---|
| [alphaxiv:130–147](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/alphaxiv/SKILL.md:130) | “Required when research-wiki/ exists”，读完该论文后 ingest。 |
| arxiv/SKILL.md:158–177 | 同样按 Wiki 存在自动 ingest 所有已展示 hits；PDF 另由 :109–111 的显式 download 参数控制。 |
| deepxiv/SKILL.md:197–215 | Wiki 存在且论文被深读时 ingest；不是简单 search hit 就写。 |
| exa-search/SKILL.md:145–170 | Wiki 存在且结果 category 为 research paper 才 ingest。 |
| semantic-scholar/SKILL.md:158–182 | Wiki 存在时 ingest 已展示论文。 |
| [paper-analyzer:30–45](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/paper-analyzer/SKILL.md:30) | 无模式分支地生成 note 和更新 graph。generate_note.py:17–25 要求 vault；:205–222 写到 vault/20_Research/Papers 并生成带占位符的模板。update_graph.py:17–25,45–50 同样依赖 vault。 |

**影响。** 用户只想看一个答案，项目里有无 Wiki/vault 却可能改变副作用；durable worker 又可能另写一套笔记。paper-analyzer 在没有 vault 时会按源码退出；有 vault 时生成的模板也不能被误认为已完成的分析 Result。没有运行这些写入，故报告描述的是指令/代码路径。

**修复方案。** 复用 Gemini/OpenAlex 已有的 adapter 边界，给 provider 明确调用模式：候选/one-off、Discovery 已分配 Run 的 read worker、用户显式要求的 standalone export。前两种返回 packet 或只写 dispatcher 明确分配的 Result 路径；Wiki、Obsidian graph 和独立 PDF archive 由明确请求触发，不能由目录存在替代用户意图。已明确请求下载或导出的授权继续有效，不额外增加确认轮次。

paper-analyzer 的 HAI 模式直接返回结构化分析 packet；vault 导出保留为显式 standalone 能力，并列出 vault/输出路径前置条件。临时检索缓存和交付给用户的持久文件应分别说明，不能把合理的临时检索误判为独立 Result。不要改变 references/ 上游副本；在 first-party adapter 中完成边界。

**验收。** Wiki 有/无、vault 有/无均不改变默认 one-off 的持久写入行为；durable 模式只有一个指定的 Result authority；显式 download/export 仍可用；缺 vault 给出具体缺少输入，而非默默失败；占位模板不会作为 complete analysis 被接纳。

**负责人/确定性。** Discovery Search/providers；模式冲突与 vault 依赖已确认，未观察真实副作用。

## D05 · P1：research-lit 的 source 选择被无条件检索段落覆盖

**证据与位置。** [Source Selection](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/2_review/research-lit/SKILL.md:60) :65 写 “Only search the listed sources”；:72 例子是 Zotero only；:66 的 all 排除 S2/DeepXiv/Exa/OpenAlex/Gemini。后文 :185–189 无条件要求 WebSearch，:191 明写 arXiv API “always runs”。:94 的 `web` 已将 arXiv 等包含在该渠道，合法 ID 清单没有独立 `arxiv`。

**影响。** 请求 sources:zotero 或 sources:local 可能仍出网查文献。用户不知道实际覆盖了哪些渠道，也无法比较两次结果是否来自同一来源范围。

**修复方案。** 保留当前接口兼容性：明确 `all = zotero, obsidian, local, web`；`web` 的子渠道包括所选 arXiv API/WebSearch 路径，只有 web 被选中才运行它们；`gemini-search` 规范成 `gemini` 并去重。不要直接采用“必须显式 sources:arxiv”的旧建议，因为当前没有该合法 ID。所有来源不可用/fallback 都受已选择范围约束，不因 Zotero 缺失自动扩大到 web。统一输出 requested/attempted/unavailable/not-searched。

durable Search 有“两类渠道”要求（search router:50–56）。如果用户显式限制来源，返回其允许范围内的结果并记录未满足的 coverage gate，不偷偷增加渠道，也不宣称已经完成广泛 literature sweep。

**验收。** sources:zotero 和 local 都不发起 web/arXiv；web 明确报告它实际用了哪个子渠道；all 加可选 ID 只执行一次；未配置某来源时不捏造覆盖。窄来源请求与 durable coverage 不足被准确展示。

**负责人/确定性。** Discovery research-lit 与 Search dispatcher；文档直接矛盾已确认。未执行 connector/API。

## D06 · P2：Synthesis 的 craft 调用模式没有传递到所有通用 worker

**证据与位置。** [Synthesize durable procedure](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/3_synthesize/haipipe-discovery-synthesize/SKILL.md:98) :98–122 已要求 accepted Results、draft packet 和缺口回 ACQUIRE；:109–110 列出 research-lit、comm-lit-review、academic-researcher。但 comm-lit-review:169–225 从 Zotero/Obsidian/local/外网开始完整检索，:83–87 还要求 unavailable “Skip it silently”；academic-researcher:141–176 的 summary 只有普通 formatted citation。research-lit:103–107 将 durable worker 定义为 candidate harvest，:360–372 又定义为主题 synthesis packet，未显式区分这两个调用角色。

**影响。** 调用者知道自己要“把现有证据写清楚”，worker 却可能理解成“重新搜索一轮”。反复读多份长文才能消除冲突，也增加 provenance 校正成本。已有 parent 约束使得“必然污染结果”不是合理结论。

**修复方案。** 在本地 adapter/调用契约中增加明确角色 `acquire-candidates` 与 `synthesize-results`。后者只接收已接纳 Result IDs、Card/Bib keys、阅读深度和问题；输出复用现有 registry 的 claim/theme/支持与反对 Results/limits/gaps 格式。发现缺资料时返回 Search Trigger，不在 craft worker 内扩源或另写文件。research-lit 保留现有 durable 无 Run/Bib 写入约束；comm/academic 加上该模式适配。standalone comm 的不可用渠道在最终 coverage 中显示，可继续运行，不逐次打断用户。

**验收。** 只给两个 accepted Results 和一个未回答问题时，三个 craft worker 均仅返回这两个 Result 的论证及 gap；不调用搜索、不伪造 cite key、不写新 Run；acquire 模式能正常返回候选。缺输入不假装完整综述。

**负责人/确定性。** Discovery Synthesize/craft adapters；模式未对齐已确认，未发现实际越权产物，因此列 P2。

## D07 · P1：Page Run 名称已更新，Discovery 仍按旧规则识别

**证据与位置。** D1 SKILL.md:35–41,92–96 和 synthesize:35–39 指示 `rp00_mermaid-structure` / `rpNN_pNN[-pNN]`。当前 [Page Run 契约](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:29) :29–48 使用 `rp-struct-NN`、`rp-scratch-NN_<target>`、`rp-sec-NN`、`rp-para-NN_Pxx[-Pyy]`；:124–133 指明 `runs/<typed-id>.md` 与 `results/<same-run>/`。这些新名称在 HEAD 已存在。

[paper_runs.py:19](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/scripts/paper_runs.py:19) 的 PAGE_RUN_RE 只匹配旧两类；:210–229 仅排除匹配项；:739–746 会把剩余 Result 当作 Discovery pair 校验。故按源码推演，`results/rp-struct-01/` 会进入 Discovery map，触发 runname-invalid，且只有 .md Page ticket 时还会触发 orphan-result。这是静态可确定的分支，不是已执行的测试结果。现有测试 :413–427 仅覆盖旧 `rp00_mermaid-structure`。

**影响。** 用户按当前 Page 文档完成结构讨论，却可能被 Discovery checker 告知 Run/Result 损坏，无法清楚区分是 Page 未完成还是被错误识别。Run 计数和关闭状态也可能被误报。

**修复方案。** 由 Page 提供权威 typed ID/receipt 分类契约，Discovery 按 owner/type 排除合法 Page lane，并继续严格校验自身 rNN。保持旧 Page 记录的只读兼容，不要求批量重编号。同步更新 D1、synth、lifecycle-map、workflow-table 等例子。不能简单忽略所有以 rp/re/rd 开头的目录，否则会隐藏拼错名称和损坏记录；不属于 Discovery 的记录应交给拥有者检查。

**验收。** 合法新四类 RP 和被支持的旧 RP 同处 Folder 时不进入 Discovery Run count/Bib，也不报 Discovery orphan；真正的 Discovery orphan、非法 stem 和错误 owner 仍被发现；损坏 Page pair 由 Page gate 报告。D08 若引入本地 RE/Delivery lanes，也须纳入共享分类方案。

**负责人/确定性。** Page owns names/type classification；Discovery owns inventory/checker。代码不匹配已确认，端到端真实 Folder 尚未运行。

## D08 · P1：Discovery 仍写 Page 明确停用的聚合 Bib 路径

**证据与位置。** `D/haipipe-discovery/ref/paper-run-contract.md:318–345` 把 `outline/evidence/bibex/<task>.bib` 定为派生聚合，且说 D1 root 不创建本地 typed CITE item。[builder 默认路径](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/scripts/paper_runs.py:877) :877–885 返回该路径；:926–933 的 --write 还拒绝写往其他 canonical 位置。

然而 [Outline citations](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/evidence/citations.md:37) 的 “Authority mode B · Discovery aggregate” 在 :37–48 指向 `results/<re-run>/result.yaml` 和 payload/；:107–109 明确 `outline/evidence/bibex/`、flat bibex/ 已停用，“not read, merged, or used as fallback”。:7–13 的 Page 引用标签是 `\cite{C_<slug>}`，Bib key 只是 Result payload 元数据；Discovery 的 source-format:26、paper-run-contract:334–335 仍以直接 Result/@cite lineage 且无本地 CITE item 描述 root Page。

**影响。** Discovery 可以输出自己认为 canonical 的 Bib 路径，Page 合约却要求另一个入口，且禁止旧路径 fallback。作者可能被要求重建来源、重复验证或手工拼接，完成状态也无法跨面一致。这比命名陈旧更实质。

**修复方案。** 首先由 Page/Outline 与 Discovery 对齐单一交接合同。推荐遵循现行 Page consumer 契约：Discovery 继续拥有一篇来源一个 primary Run/Result/Bib；Page 对已声明的 focal CITE item 创建/消费自己的 typed CITE Result，引用 Supporting Discovery Results，保存 `C_<slug>` 到 Result/Bib key/locator 的映射。union helper 只是 payload 派生操作，不能每调用一次就创建 Run；Page RE 只按已声明、可独立验收的 CITE target 分配，也不计入 R_discovery。

随后调整 Discovery builder 输出 API、root Page 例子、returned paths、check/close gate 和相关 fixture。旧材料的迁移必须保留 primary Bib、人工回执、来源指针和必要的旧址索引，先预览，不直接因新规范批量搬迁用户资料。本轮不执行迁移。最终 envelope 字段、CITE cardinality 和迁移策略仍需共享 owner 在实施第一步确认，不能由 Discovery 单方面复制一份 Page schema。

**验收。** 新 Topic 的 citation 从 Discovery primary Bib 到 Page CITE label/payload 全链条可定位；Page 不再依赖被停用的路径；无第二份被当作 primary 的 Bib、无额外 Discovery analysis Run；pending verification 阻止 CITE ready/Page release；旧材料不会被静默丢弃或伪造新的人工回执。

**负责人/确定性。** Page/Outline 主持交接 schema；Discovery 适配生成器/产物/关闭；Board/Delivery 消费者需要回归。契约与输出路径冲突已确认，实际 UI/渲染器读写路径尚未核验。

## D09 · P2：覆盖表是旧快照，不能作为当前兼容性凭据

**证据与位置。** [workflow-table Skill Coverage](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md:191) :191–203 声明 2026-09-13 快照，仍列 umbrella v0.13.0 / 461 lines；当前 umbrella:15–17 是 v0.14.0 / 2026-09-19，实际 464 行。表内还有旧 Page phase/编号/版本描述。它已注明部分共享项未独立测试，不能把该注记抹掉或把历史 PASS 说成伪造。

**影响。** 读者若把日期较旧的结构验证当成当前状态，会漏掉 D07/D08 的组合不兼容；多份手工版本/行数表也容易继续漂移。

**修复方案。** 将 Run Spec/ownership、当前机器可核对的 inventory 和历史 validation receipts 分开。版本/路径可从当前文件生成，行数无使用价值可删除；旧 PASS 保留日期、被测版本、fixture 范围，当前状态写“待本次变更后验证”。只在新测试真实通过后更新对应 receipt。

**验收。** 16 个当前技能和引用路径无遗漏；当前 metadata 可复算；过期验证不会显示成新验证；Run 模型表不再用 Phase/Cycle 作工作单元。历史未覆盖 provider/live APIs 的空白继续明确标注。

**负责人/确定性。** Discovery registry；共享 table-workflow 协调展示 schema。过时快照已确认。

## 修复后的 Workflow 模型草案

以下是待实施的边界草案，不是新增执行任务：

| Run Spec | 目标和负责方 | 输入/产物 | 完成与后续 | 基数 |
|---|---|---|---|---|
| `paper-analysis[subject, scope]` | 一个已接纳 canonical paper；Discovery creator 执行，read/review 为内部 Steps | 冻结问题、Trigger、identity；同 stem ticket、Card、facts、source-access、runtime、primary Bib | 技术 artifact gate；人工引用核验单独限制 promotion/epistemic close；完成后供 Page 消费 | 本次冻结范围的 N_p 个实际分配 |
| `source-analysis[subject, scope]` | 一个已接纳非论文 source；同一 Discovery owner | 对应 source kind 的证据与相同 pairing/receipt 约束 | 技术 gate 与真实局限记录；完成后供 Page 消费 | N_s 个实际分配 |
| Page-owned RP/RE/RD | Page 合同定义的结构、写作、证据、交付目标 | Supporting Discovery Results + Page 自己的合同 | Page gate/release 决定；Discovery 只消费有效交接回执 | 按 Page Run Specs 计算，排除出 Discovery count |

`R_discovery = N_p + N_s` 指该批次实际分配的分析目标；未接纳候选/查询/worker 调用不计数。unchanged duplicate 重用既有 Result；独立的新 scope 按共享 reopen/supersedes 合同处理，不能把同一论文跨历史的所有分析简单算成永远一个 Run。用户的一个问题可以有多个来源 Run；人类一次反馈一般只是既有 Page Run 内的一步。

定义表与运行实例表分开。实例表在没有真实 Folder/Run 时为空；HOLD/恢复记录已有 Run/gate 的状态，不为暂停或恢复新增 Run。

## 实施顺序、依赖与完成标准

| 顺序 | 工作包 | 依赖及范围 | 完成标准 |
|---|---|---|---|
| 0 | 确认共享基线与接口 | 重新读 status 和当前 Page/Outline/Run 契约；由协调者合并 D01/D07/D08 的共享决策，保护其他任务已改文件。 | 一个版本明确的 handoff schema、typed ID classifier、Run Spec 表 schema；列清兼容读取和当前写入边界。 |
| 1 | 统一 Discovery 定义与路径（D01） | 使用步骤 0；迁移的是技能目录/活动引用，不是用户 Run/Result 数据。保留入口名和 1_search/2_review/3_synthesize 能力组。 | D1 不再是 Phase authority；真实 Run Specs、gates/routes 和控制器说明分清；所有活动链接可解析。 |
| 2 | 修复 Page 交接与校验（D07/D08） | 先定 schema 再改 classifier/builder；Page 修改由其 owner 处理，Discovery 只适配。 | 新 typed RP/RE lanes 正确分类，CITE 输出落到现行契约；旧用户数据有明确兼容/迁移预览。 |
| 3 | 统一证据状态（D02/D03） | 人工核验规则可先确定；最终 Card/CITE 展示与步骤 2 对齐。 | identity、检索、检查、人工 verification、ready/release 各自只有一个含义；pending 不被自动升级。 |
| 4 | 明确 provider 和 worker 模式（D04/D05/D06） | 采用步骤 1 的 owner 和步骤 3 的 packet；不改 references/ 上游内容。 | one-off、durable、显式 export 的写入范围清楚；sources 严格执行；craft-only 不扩源。 |
| 5 | 更新阅读顺序、例子与 registry（D09） | 在最终字段/路径稳定后执行，避免重复维护过渡版本。 | 16 个技能的入口、模式、可见输出和 completion 能在第一次阅读时定位；旧表格只保留真实历史测试结果。 |
| 6 | 验收后记录结果 | 按下列矩阵跑必要离线测试和 fresh-context 任务；网络/API smoke 单独标出环境要求。 | 每项的证据、未测项和剩余限制可追溯；没有把静态检查写成 live PASS。 |

D04 的写入模式和 D05 的 sources 修复在语义接口确定后可以独立推进；D07/D08 的代码改动依赖 Page owner 的合同，不能先靠放宽检查或保留停用路径解决。报告阶段没有启动任何工作包。

根据 [README skill development](/Users/jluo41/Desktop/Tools-SPACE/README.md:131)，未来真正修改技能后须用 fresh-context subagent 在现实任务上验证“选中了技能、遵守指令、输出符合预期”。这是实施后的验收要求，本次计划报告没有调用技能或启动验证代理。

## 验收场景

以下全部为未来验收设计，尚未执行。现有测试文件只作为可扩展位置阅读，不以其存在推断测试已经通过。

| 场景 | 应观察到的结果 | 验证方式 |
|---|---|---|
| 一条 URL，只要概述；Wiki 目录存在 | inline；无 Wiki/独立 note/graph 持久写入；没有新 Run。 | fresh-context dry fixture，记录计划的调用/写入；必要时在临时工作区拦截 provider。 |
| 同一 URL，明确要求 download/export | 依授权写指定目标并报告路径；不因修复而取消已请求能力或重复确认。 | 参数/模式 fixture。 |
| durable 三候选，接纳两篇，其中一篇 unchanged duplicate | 只为新的已接纳目标分配；重用已有 pair；请求和 Step 不计数。 | 离线 allocation/Run Spec 场景。 |
| PubMed 摘要只检索未检查 | retrieved_depth=abstract；analysis depth 不自动提升；full-text URL 只表示可用。 | paper_source_access 的 mocked response + receipt 检查。 |
| candidate confirmed，Bib 尚待人核验 | 技术 complete 可以成立；人类响应明确 pending；CITE ready/epistemic close 被 gate 保留。 | 扩展 paper_runs 的 citation fixtures；真实 person 回执不由测试以外流程伪造。 |
| sources:zotero/local/web/all | 只执行对应集合；缺来源不偷偷扩展；gemini alias 不重复执行。 | 路由表用例 + fresh-context 选择验证。 |
| craft worker 收到两篇 Result 和一个证据缺口 | 只引用两篇；返回 gap/Search Trigger；零自发检索/新 Bib。 | research-lit、comm-lit-review、academic-researcher 各一个最小 fresh-context 用例。 |
| typed RP 与 rNN 同 Folder | 新旧受支持 RP 不算 Discovery；真 rNN orphan 仍失败；Page 自己检查其损坏记录。 | 扩展 test_paper_runs.py 的 :413 起旧 fixture，加入四类 typed IDs 和非法近似名。 |
| D1 root Page 的 CITE 消费与迁移 | primary Bib 与人工回执不丢失；CITE label→typed Result→Discovery Result 可追溯；停用路径不再成为新输出依赖。 | 跨 Page/Discovery 临时 Folder 集成验收，迁移 preview 不覆盖现有数据。 |
| 用户只要求改一句话或补充反馈 | 沿 Page 既有 Run/Version/Step 返回局部候选和 acceptance 状态；不新建 Discovery Run，不擅自扩展反馈范围。 | Page owner 的 fresh-context 交接用例。 |
| 可选 provider 不可用 | 清楚列出 unavailable/not-searched；其缺失不阻塞其他合法来源，但不宣称覆盖完整。 | 离线 unavailable fixture；真实 API 状态另列未测。 |

## 跨族责任与待定事项

| 共享问题 | 主责与 Discovery 工作 | 协调原则 |
|---|---|---|
| Run Spec graph、gate/route 和 controller 名称（D01） | Run/Task Workflow 定 schema；Discovery 发布符合 schema 的领域 Specs；table-workflow 更新展示。 | 不创建第二套 Phase/controller 权威，也不将内部 Step 一律升成 Run。 |
| Page typed IDs 和 lane 分类（D07） | Page owns valid names/receipts；Discovery inventory 使用其稳定分类。 | 保留已分配旧 IDs；数据迁移与当前命名分开，不能重编号伪造新工作。 |
| CITE output/聚合/释放（D02/D08） | Page/Outline owns consumer envelope、label 和 ready gate；Discovery owns primary Bib 与人审回执。 | 先对齐合同，再改 builder、check 和 Page consumers；同一问题由协调者去重。 |
| Folder 路径注册（D01） | Discovery 与 Board/Task/STRUCTURE owner 更新活动链接。 | 原目录名可留明确的兼容解析记录；避免新增同名 SKILL 造成递归安装重复。 |
| Insight/Design/Ideation | 保持独立第一类技能族和清晰 handoff。 | Discovery umbrella:295 的 applications/ 是根路径检测，不是 Application 父技能族；不据此发起无关重组。 |

D08 的具体 CITE envelope、每个 focal item 的基数和迁移方案仍待共享 owner 落定；本报告给出推荐方向，不把建议当作已生效规范。自动分类跨族 lane 的可复用实现也需在实施时查当前 Page 代码，不能只凭 ID 前缀做宽松过滤。

本次没有浏览上游服务或 dirty reference 子模块内容，没有穷尽所有历史 CHANGELOG、资产或前端渲染代码。没有 live API、UI、完整运行期测试结果。原报告的历史 field-test 日期继续只证明当时 fixture 的范围；provider 的现场副作用、真实人类交互体验和跨族 renderer 行为仍是待验证项。
