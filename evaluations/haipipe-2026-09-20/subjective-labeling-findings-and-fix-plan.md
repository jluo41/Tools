# HAIPipe Toolkit：主观标签、判断与跨技能交接审阅

日期：2026-09-20。HEAD：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。对象是**当前工作树**，不是仅审阅该提交。收尾证据复核：`2026-09-20T17:59:38-04:00`。

**初始总体判断：部分符合。** Toolkit 已有较好的证据定位、人工决定与机器建议分离、版本绑定和独立复核设计。主要缺口是：枚举名称被当成完整量表；同一判断在模板、提示词和校验器中变义；无法判断被压成低分、失败或再次审核；局部主观判断有时被描述成机械事实。审阅时记录了 16 个可追踪条目，其中 14 项未关闭；SL05、SL11 已被阅读期间的并行修改解决其文档冲突。**当前实施状态以本文“实施跟进”表为准。**

审阅阶段只新增了这份审阅报告，没有修改 skill、代码、配置或其他报告；该阶段也未执行工作流、模型调用、摄像头、安装器、测试或外部服务。后续修复与验证见上方“实施跟进”。下述用户影响属于基于源码的推演，不是已观察到的事故。临床阈值本身的医学适当性不在本次审阅范围。

## 实施跟进（2026-09-20）

以上范围表和第 3 节记录的是审阅时的基线。以下状态覆盖当时“14 项未关闭”的计数；保留原观察与行号，便于追溯，不再代表当前未修复清单。

| 条目 | 当前处理 | 验收与限制 |
|---|---|---|
| SL01–02 | 已修：Individual 把趋势定义为精确相邻序列比较；无校准材料时 confidence 为 unavailable；judge 对缺维度、非法 severity 和不一致 verdict 失败关闭。 | 冷上下文用合成输入核对 rising、unavailable 与 parser 拒绝案例。完整模型/API 路径未运行。 |
| SL03 | 已修：Discovery 分开检索覆盖、逐来源 appraisal、摘录 fidelity confidence 与综合结论 confidence；覆盖事实落在 Page `## Source map`，候选收据落在 YAML `sources`；`report.outcome` 与 Task `status` 分离。Ideation、Insight 也有各自判断锚点和 abstention。 | 冷上下文覆盖 Search/Review/Synthesize；终态场景保留 `report.outcome: mapped` 并以 Task `status: inconclusive` 表达未决综合。无跨领域分数映射或概率解释。 |
| SL04 | 已修：Insight 加入 `UNDETERMINED` pooling 结果及对应 hold/partial-final 路线；未决时不授权 subgroup counsel、GI5 handoff 或 Design binding。 | Insight 冷上下文的低精度比较正确返回 `UNDETERMINED`、精度缺口和无 counsel；Insight 家族测试 20/20。 |
| SL05 | 已关闭：保留既有 Card/Test/Pressure 投影与 skipped/defer 契约。 | 冷上下文冲突审阅保留原始判断并按 HOLD 处置。 |
| SL06 | 已修：Venue Fit 为 strong/conditional/weak/off-fit/unknown 提供分档依据与 overall 不平均规则；Ideation receipt 绑定 Run、评价者、量表和精确输入，分歧写入独立 resolution。 | 两条合成原始评价记录验证了 unknown/HOLD 和原值保留；没有声称做过独立评审或一致率研究。 |
| SL07–08 | 已修：Discovery 冻结问题专属 admission 规则与候选决策凭据；paper-analyzer 改用带定位符的逐标准证据状态，并默认 draft/not-assessed。 | Discovery Search/Review/Synthesize 冷上下文路由通过；未调用外部检索服务。 |
| SL09 | 已修：Design 语义/视觉标准需要具体观察与通过/失败/不可评条件；unresolved 要记录原因、下一责任人和输入，不自动变 ready。 | 合成 Verify 结果被 checker 接受为完整 unresolved，但未判为 ready；只运行一次 Verify。 |
| SL10 | 已修：Board 区分确定性检查、语义判断和人类偏好/授权；checked 不等于授权，机器规则不自动升级成普遍政策。 | 冷上下文 Board/Approver 情境通过。 |
| SL11 | 已关闭：Writing 继续使用一个保真 rubric 与有限 review→revise 流程；旧 humanizer 入口保持退役。 | 本次未重新运行 Writing 全路径。 |
| SL12 | 已修：Paper Round、Display reviewer 与 field-test 分别定义本地严重度/处置；field-test 分离期望是否满足和原因归因；视觉材料缺上下文时可判 not-verifiable。 | 冷上下文协议路由通过。真实现场目标、渲染和完整 Round 闭环未运行。 |
| SL13 | 已修：Meal cam 区分多项视觉推断、no-food-visible、uncertain 与 service_error；Run receipt 记录模型/rubric/时间/输入摘要；纠正以 append-only sidecar 保留旧值、操作者和时间。 | 冷上下文核对了标签语义；未连接摄像头或视觉 API，也未验证真实摄入。 |
| SL14 | 已修：`install.sh` 与 `install.ps1` 都排除精确退役目录 `display/_todo`，README 已说明。 | 已静态比对两个排除路径；未在 Windows 上运行 PowerShell 安装器。 |
| SL15 | 已修：Discovery、Ideation 与 meal-cam 增加评价者、标准版本、输入快照/哈希及保留分歧/纠正的记录；Design/Writing 继续用各自 Run/Result receipt。 | 相关冷上下文 mock 收据可追溯；未做跨 Toolkit 评审者一致率校准。 |
| SL16 | 已修：核心 owners 与 Labeling bridge 将运行 Workflow 写为 Run Specs/Instances 与依赖/Route 图；P0–P5 只作兼容投影；引擎 gates 改用 receipt/integrity 状态，Run planner 支持可选项为 0；安装器旧技能可达性已修。 | Labeling 定向测试 42/42 通过。完整引擎初次运行的 12 个 embedding 用例受环境缺少 `sklearn` 阻塞；修复两个旧 gate fixture 后未重跑完整套件。 |

实施检查遵循仓库 README 的 fresh-context 要求。冷上下文仅使用合成输入；凡依赖真实用户数据、图像渲染、摄像头、外部检索、模型端点或 Windows 环境的路径均未冒充端到端验证。原证据索引的行号是审阅快照；当前工作树请按文件与字段定位。

## 1. 范围、方法与已变化的基线

“主观标签”包括人或 agent 赋予的类别、质量等级、置信度、相关性、证据强度、适用性、建议和人工处置。不把所有 `label`、`score` 都当成主观判断：引用键、Run ID、字数、模型输出概率、确定性数据标签及运行状态需要分别识别。

以 [BRIEF][brief]、[inventory.json][inventory] 和 13 族原评估/补充报告的相关发现为背景，重新检索全部 SKILL 的判断词、定性要求和 Workflow 用语，再追到当前协议、模板、persona、必要的解析/校验代码。**这是全 Toolkit 的横向定向审阅，不声称逐行重读全部约三万行 SKILL 或全部支持文件。** 重点标签界面见下表；没有把历史评估直接当成当前缺陷。

清单核对：原 inventory 有 138 个技能；本次初筛磁盘有 142 个 SKILL，其中 4 个 `display/_todo/` 未列入 inventory。阅读期间独立 humanizer 入口被移除，收尾磁盘为 141 个：137 个主清单技能、4 个退役但仍可被安装器发现的技能。Insight 的 6 个资源技能由 `workflow-phases/` 移至 `folder-kinds/`，数量不变。

| 家族 / 磁盘 SKILL 数 | 本次重点判断界面与支持材料 | 结论与阅读边界 |
|---|---|---|
| Discovery / 16 | Search admission、Review packet、Synthesize outcome、Result/Bib verification；schema、source-format、paper-run-contract；paper-analyzer 模板和 Semantic Scholar 筛选 | 证据来源较清楚；confidence、admission、评分与验证用语有缺口；未调用检索服务 |
| Ideation / 8 | Generate、Novelty、Pressure、Fit、Nature、Test、Select；Idea/Direction/Fit Cards、receipts、sync、worked example、checker | 比较轴和人机权限清楚；强弱分界仍需细化，跨表投影冲突已在收尾前修订 |
| Insight / 8 | D/I/K/W 与 Question 分类、strength、POOL/SPLIT、GI；partition、workflow、Wisdom handoff | DIKW 与签名边界清楚；强度量表、pooling 的不确定结论不完整 |
| Design / 4 | Brief、Commission、Generate、Verify；unit-contract、run-profile、Page Design 投影 | 冻结标准、逐条证据、独立性较强；定性标准与 unresolved 恢复有缺口；未逐份审阅所有 venue style profile |
| Page / 15 | CHECK 四轴/四种 verdict、人工接受、Evidence approval、写作反馈与 post-run analysis | 可保留 NOT VERIFIABLE 和原始反馈；终局判断与控制标签应继续分离 |
| Board / 4 | Approver、Reviewer、四类规则、checked 与人工 tick | 人工权利清楚；“可写成规则＝无需再判断”的解释不成立 |
| Paper / 9 | Venue authority、P0 投影、Round concern severity/处置、Story 对证据的消费 | authority 与处置证据较清楚；Fit 接口和 severity 定义不完整；未审计 venue 子模块全部文献/样本 |
| Task / 49 | Individual reporter/judges、persona/schema/parser；Data review checklist、AIData 标签、Task/Workflow 模板 | 重点详查 Individual；工程类型/数值字段作区分筛查，未运行模型、数据或部署 |
| Writing / 1 | 统一 Writing 入口、共享 evaluation/rubric、weaving、anti-slop adapter、change records；复核 humanizer 退役 | 最新文档已明确保真、不可评、reviewer mode 和有限修改；不再保留旧 humanizer 冲突为现行缺陷 |
| Display / 14 | figure-to-svg 复核、renderer/caller 接受边界；4 个 `_todo` 的评分/Workflow | 10 个现行技能与 4 个退役文件分别判断；未渲染素材或测量实际视觉质量 |
| 0_utils / 10 | field-test 分类、Skill Coverage 质量状态、meal-cam 食物识别、remote-error 证据状态 | 若干定义可直接复用；field-test triage 和食物标签有缺口 |
| Project / 2 | feedback/digest 的 KEEP/DROP、NEW/MERGE/DUP 和人工确认；meeting 路由 | 定向检查未见需单列的问题；非全面项目审计 |
| Run / 1 | 当前 v0.27.0 的 Run 判定、所有者、状态与下游接受 | 共享定义明确；不替各领域定义主观量表 |

`references/`、历史反馈、CHANGELOG、生成资产、外部运行库和真实用户项目未作全面审计。独立包 `plugins/subjective-label/` **不等于** HAIPipe Toolkit；这里只核对 Toolkit 的 Labeling bridge、该包入口和 Workflow/Run 接口，不把这次报告冒充其全部 8 个技能的专项审计。

工作树在本次阅读中持续变化。收尾前已确认：[Task 主模板][task-template] 使用 `run_specs`；[Task 主技能][task-current] 将 Plan/Build/Execute/Report 称为 lifecycle commands；[Individual CLI][judge-cli] 已加载 ground truth，并对 mismatch/不可用作处理；[安全 persona][safety-system] 已限制基于预测自行给出行动指令；[Run 当前入口][run-current] 已更新为 v0.27.0。同时，[Ideation Run Specs][ideation-runs] 已补齐实际 owner 与关闭规则；[Writing 共享评价][writing-evaluation] 已落地。原报告中对应的旧问题不再原样列为未修。行号指本次证据快照，后续实施应按引文与字段重新定位。

## 2. 值得保留的设计

- **知识判断没有被压成一个总分。** [Novelty][novelty-status] 定义 novel/partial/preempted/inconclusive/unverified，并要求 closest-work 比较、阅读深度和停止条件；[Test][test-axes] 保留 identification、feasibility、fit 等独立轴，明确不平均掉 fatal blocker。
- **证据、解释和授权各有位置。** [Direction Card][direction-card] 分 observed signals 与 interpretations；[Venue][venue-authority] 区分官方规则、样本观察、本地选择和未知；[Wisdom][wisdom-sign] 将签名绑定到 exact payload，父证据改变后不能沿用旧签名。
- **未知可以是诚实结果。** [Page CHECK][page-rubric] 有 `N/A` 与 `NOT VERIFIABLE`，每个 MEETS 需要可见证据；[Data review][data-review] 区分 PASS/WARN/FAIL/N/A 并要求引用具体行；[Skill Coverage][coverage-status] 明确未知不是 pass，行数不是质量。
- **人机决定分开。** [Select][select] 的推荐不等于选中；当前版本已保留未答复卡片为 open。[Page 写作][interactive] 保存原话与解释，不把 Applied 当接受；[post-run analysis][post-analysis] 的偏好推断只能是 candidate；[Project digest][project-digest] 给出 KEEP/DROP 示例、来源行和确认边界。
- **Writing 已提供可复用的轻量评价样板。** [共享 rubric][writing-rubric] 区分 MEETS/NEEDS WORK/N/A/NOT VERIFIABLE，要求位置和依据；[evaluation][writing-evaluation] 记录 candidate hash、rubric hash、真实 reviewer/mode、覆盖范围、初末两次判断和未解决问题，局部修改不必重新全篇打分。
- **独立复核有可操作定义。** [Design Unit][design-verify] 要求真正新上下文，不能只改 actor 名；候选 hash 与逐 artifact × criterion 覆盖明确。[anti-slop adapter][anti-slop] 明确分数只是诊断，不是 AI 来源判决或接受 gate。

## 3. 具体问题

严重度统一为：**P1**＝可能改变证据结论、发布/选择 gate 或安全复核意义，应在下一次依赖该判断前修；**P2**＝影响可复现性、解释或后续交接，纳入近期修订；**P3**＝局部文案。本文没有证据支持生产事故或 P0 紧急事件。

### SL01 · P1 · Individual 的 confidence 与趋势标签缺少可判定语义，安全提示词又互相冲突

**观察。** [Report schema:36–44][report-xml] 要求 `rising | stable | falling | mixed`、`high | medium | low`，并要求 “One-sentence cause”；[Pydantic:67–72][report-schema] 只约束枚举。未在这些 persona/contract 中定义趋势窗口、最小变化、mixed 边界或 confidence 所指对象。更直接的矛盾是：[safety system:31–34][safety-confidence] 明说 “Trajectory range alone is not predictive uncertainty”，但 [safety schema:30–32][safety-schema] 又问 “Does confidence match forecast spread?”；[loader:65–71][judge-loader] 会把二者拼成同一个 prompt。

**影响（推断）。** 同一条预测可得到不同趋势/置信度；schema 中的“cause”会诱导把伴随事件说成原因；安全 judge 可能继续按已被 system 否定的依据评分。

**修法。** 明确哪些字段机械派生、哪些是解释。趋势采用 owner 明示的窗口和规则；confidence 改为带对象和依据的判断，校准材料缺失时允许 unknown/unavailable，不能强填 low。`why` 改为有证据的解释或明确未知，不能强迫因果归因。先统一 system、XML 示例与模型，再处理下游展示。验收包括同一轨迹、缺校准输入、多个可解释原因三种边界用例。

### SL02 · P1 · Judge 的分数、总 verdict 和缺失值不能稳定重算

**观察。** [Patient judge:33–36][patient-judge] 的 pass 为 average ≥4，warn 为 average 3–4 **或任一 warning**，边界 4 和高分带 warning 同时满足两类。[Safety:42–45][safety-verdict] 未覆盖“三项为 3、其余为 4、无 critical”的情况；多数维度也只给 1/5 端点，没有 2/3/4 锚点。[Safety:50–53][safety-unavailable] 要求 unavailable，但 [schema:53–55][safety-schema-constraints] 仍强制五项整数分，结构无逐项 applicability/evaluability。更严重的是 [parser:130–144][judge-parser] 静默跳过缺分维度，并把未知 severity 变为 `info`；[Judgment:34–40][judgment-model] 不验证完整维度集合或 verdict 与 issues 的一致性。

**影响（推断）。** 漏评可能仍形成有效 JSON；`CRITICAL` 等非规范值可能降成 info；同一评分向量可被不同 judge 判 pass 或 warn。CLI 新增的 forecast 检查缓解了部分事实风险，但没有解决该判决协议。

**修法。** 用不重叠、穷尽的决策表计算总 verdict；确定性长度/阈值检查与语义评分分开。逐项增加 `assessed | not-applicable | unavailable`，不以 0 或低分替代未评。缺维度、重复维度、非法 severity 应报契约错误，保留原文；不要降级。验收以边界分数、warning+高分、缺一维度、未知 severity、全部不可评五类输入为准。

### SL03 · P1 · 核心 confidence / strength 等级只有枚举，尚无共享记录要求与领域锚点

**观察。** [Discovery schema:224/238/255][discovery-confidence] 使用 high/medium/low；[Novelty receipt:151–153][novelty-confidence] 使用 high/medium/low/none；[Direction:24][direction-card] 又没有 none；[Knowledge:49–52][knowledge-strength] 使用 STRONG/MODERATE/WEAK “plus a reason”。来源、限制和理由要求有价值，但这些接口没有规定 confidence 的对象、各档边界、缺证据与证据冲突如何区别，也没有跨字段等值转换规则。

**影响（推断）。** high 可能分别代表检索覆盖好、论文方法好、个人相信结论或检索已完成。收到一个 STRONG 的 Wisdom/Design consumer 无法知道强的是证据、推断还是建议；理由可追溯不等于标签可复现。

**修法。** 共享的是记录外壳，不能把不同领域量表强行统一：每个 owner 定义 construct、适用范围、最低证据、正/反/边界例子与 abstention。Discovery 的覆盖、研究质量、综合结论应分开；Knowledge 的 strength 要结合声明的 rival/boundary 判据。无经验证据时不把这些等级解释为概率。见第 5 节最小记录方案。

### SL04 · P1 · POOL/SPLIT 直接控制 counsel，却没有证据不足时的领域结论

**观察。** [Knowledge:83–86][knowledge-pool] 要求 pooling verdict “exactly `POOL` or `SPLIT`”；[partition:39–54][pool-routes] 规定 POOL 使非模板 W defer，SPLIT 允许独立 counsel/子 Board；[partition:33][pool-threshold] 有共享阈值文件要求，却没有定义判决所需的 exchangeability 标准、不确定性条件或异质性不足时的解释。

**影响（推断）。** 整体 Workflow 可以 HOLD，故不能断言系统强迫每次都给二元结果；但领域层不能清楚表达“评估已完成，仍不足以证明可合并或需拆分”。人可能把未检出差异误读成 POOL，或为完成流程硬选一个出口。

**修法。** 在判据冻结时声明比较对象、可接受差异/适用条件、所需证据和反证；增设明确的 inconclusive/undetermined 结论及相应 hold/补证据/有理由终结路线。它不能自动授权任一 counsel。用证据不足、冲突、支持合并、支持拆分四例校准，并保留 W 重新签名规则。

### SL05 · 已修（原 P1）· Ideation 的投影、skipped 和 defer 契约已对齐

**收尾观察。** 本次较早读取时，Card 与 Test/Pressure 在 central/supporting 汇总、skipped 是否要求 Task Result、recommendation 是否含 defer 上有直接冲突；当前版本已经明确：[Card:153–159][card-worst] 与 [Test:103–121][test-precedence] 把 Matrix ready 定义为 central contribution 摘要，选择资格另检查所有 Core Claims；[Card:139–152][card-pilot] 与 [Pressure:105–112][pressure-projection] 要求 skipped 保存原因、无 Task Result、投影 pending；[Card:107][card-recommendation] 已包含 defer。[checker][ideation-checker] 的 central 汇总及所有 claim 的选择检查因此不再构成上述冲突。

**后续验收。** 不再列为待修缺陷。用一张 central novel、supporting preempted 的 Card 确认展示“Matrix ready，但选择仍阻塞”的原因；用 skipped/no-result 和机器 defer/人未答复两例验证模板、checker、P0 的同义交接。这里只验证了当前文档与实现规则，未运行测试或完整用户路径。

### SL06 · P2 · Fit/credibility 的边界较弱，Venue authority 在交接时丢一类

**观察。** [Pressure:79–82][pressure-credibility] 和 [Journal Fit:61–63][fit-status] 列 strong/conditional/weak 等级，但没有分别定义可操作阈值；现有 [worked example][ideation-example] 给出示例，却未系统区分相邻等级。[Fit schema:154–159][fit-overall] 允许单项 off-fit 不强制拒绝，但 overall 的形成依赖自由解释。`ambitious/realistic/fallback` 已声明不是概率，这一点应保留。此外 [Venue:78–83][venue-authority] 有 `OWN ESTIMATE`，而声称 “without modification” 的 [Fit authority:30–37][fit-authority] 枚举漏掉它。

**影响（推断）。** 两位读者对同一条件可能标 weak 或 conditional；某些 off-fit 会被整体 strong 遮盖；有依据的估计进入 Fit 时只能改类或违反枚举。

**修法。** 冻结每个比较维度的满足/可修复/不满足/不可评边界及代表例子；overall 指向决定性的 criterion 和例外理由。portfolio role 要说明依赖的项目目标，不当作客观排名。Venue authority 由一个 owner 发布，Fit 直接复用完整词表。

### SL07 · P2 · Discovery admission 规则过于循环，检索元数据被命名成质量

**观察。** [Search:89–98][search-admit] 要求 “relevant enough to analyze”，[source map:64–66][source-admit] 示例仍只是 “directly relevant”。[Semantic Scholar:97–99][s2-quality] 把 `JournalArticle + min-citations 10` 叫 “High-quality journal papers”，并把 citationCount 排序叫 “Foundational / high-impact”；[同文件:203–205][s2-rank] 要求默认过滤和按引用数优先排序。

**影响（推断）。** 人可以准确复跑检索参数，却无法复现为何保留/排除某篇；引用数与文献类型形成的机械筛选容易被误认为方法质量审定，尤其影响较新或相反证据进入下游的机会。

**修法。** Search 前声明与问题绑定的 inclusion/exclusion、边界候选和优先级规则，记录重要排除及原因。把这些 filter 名称改成实际含义（例如 “journal articles with ≥10 recorded citations”）；质量留给 Review 的证据评估。不要要求对每个低相关命中做完整审阅。

### SL08 · P2 · paper-analyzer 的 0–10 评分无量表，未评价可被写成已分析/零分

**观察。** [Skill:35–45][paper-analyzer] 将 `$SCORE` 写入 graph，并承诺 comprehensive evaluation；[template:46/50,143–152][analyzer-template] 同时生成 `quality_score: [SCORE]/10`、`status: analyzed` 与五项 X/10；[update_graph.py:40,67][analyzer-graph] 的 score 默认 0.0。未见该入口定义分值锚点、权重、聚合或未评状态。

**影响（推断）。** 模板创建被误读为评价完成；默认零分与真实低质量混同；不同会话的 8/10 没有可比基础。正常手动补全可能避免它，不能把风险等同于已发生的错误输出。

**修法。** 优先采用逐维证据与问题；确需数值时先定义锚点与算法。模板状态用 draft/unassessed，缺评分为 null，只有维度完整且证据可定位才写 assessed。Discovery Result 不应吸收一个无依据的综合分作为证据。

### SL09 · P1 · Design 冻结了判据，但定性判据过短；unresolved 被统一路由回再次 Verify

**观察。** [Unit contract:68–75][design-criterion] 的示例只有 “Respectful, non-coercive wording”；同文 [104–109][design-method] 要求 semantic/visual 命名 observation method，却未在该示例给判定边界或例子。[Unit:114–120][design-verify] 和 [Workflow:129–139][design-route] 把任意 unresolved 检查记作 records-check failed，再由人 queue review。未区分缺图像/输入、规则冲突、无法判断与 reviewer 技术故障。

**影响（推断）。** 标准虽然事先冻结，两个独立 reviewer 仍可能相反；如果 unresolved 来自规则本身或证据缺口，重复审核相同候选不会补齐条件。独立性不能代替判据清楚。

**修法。** 对关键 semantic/visual criterion 冻结简短观察方法、通过/失败/无法评的例子；不必为每条美感建议建数字量表。将 unresolved 的 reason 分类并路由到补输入、澄清 criterion/新 Commission 或技术重试。真实不可评保持可见，不能通过刷 reviewer 变成 pass。保留 exact candidate hash 和完整覆盖要求。

### SL10 · P2 · Board 将“可写成规则”与“机械可判定”混同，并存在过度推广反馈的文案

**观察。** [Approver:39–42][approver-cut] 称 agent 规则有 “right answer independent of intent” 和 “same verdict tomorrow”；[rules README:18–20][rules-cut] 说可写下就 “never needs judging again”。但 [R4/R11][outline-rules] 需要识别矛盾、具体主题和读者理解，显然含语义判断。[README:35–36][rules-promote] 又说 “Every 🛑 ... is PROMOTED”，与 [Approver:138–143][approver-promote] 先区分 steer/rule、[Page:300–304][preference-boundary] 只有明确授权才提升规则的边界不一致。

**影响（推断）。** `checked: auto` 容易被理解为纯机械证明；一次局部偏好可能被当作跨场景规则。当前禁止 agent 写人工 tick 的约束明确，**此处不是声称它已允许伪造人工批准**。

**修法。** 分为 deterministic check、evidence-based semantic assessment、human preference/authorization；自动记录不改变判断性质。规则提升保留原话、适用范围、反例、来源与明确决定；把 “Every” 改为“可推广的候选，经范围与授权确认后”。

### SL11 · 已修（原 P1）· 独立 humanizer 退役，风格修订已归入共享保真规则

**收尾观察。** 较早读取的独立 humanizer 同时要求调整 claim strength 与保持其不变；该入口已在阅读期间删除。[当前 Writing:73–101][writing-current] 明确它不再是第二入口，使用统一 rubric、有限的 evaluate→revise→evaluate 循环，并将改变证据/因果强度的决定交回 owner。[共享 rubric:29–44][writing-rubric-preservation] 禁止用风格总分平均掉内容错误；[evaluation:9–24][writing-evaluation] 要求保留初末候选的判断与实际 reviewer mode。这实现了 [既有 Writing 计划][writing-plan] 的相关方向。

**后续验收。** 不再列为待修缺陷。用“文字显得太像 AI，但证据只支持原有弱结论”的例子检查：修改只处理明确表达问题，数字/引用/因果强度保持；内容问题回到 owner，未解决时不报 ready。保留 anti-slop 非 detector、非接受 gate 的边界。本次未实际调用 Writing 或确认所有旧调用者都已迁移。

### SL12 · P2 · Paper/Display 的 severity 未定义，field-test 的归因分类缺少未决出口

**观察。** [Round ledger:239–255][round-severity] 必填 “issue kind and severity”，但该契约未给词表/行动含义；[figure-to-svg:286–301][figure-review] 的 JSON 有 severity，未定义可用值和容差，虽已有明确返工路径及用户接受偏差的出口。[field-test:85–90,127–130][field-triage] 只允许 MATCH/SKILL GAP/EXPECTATION GAP，并要求 triage “exactly three bins”：infra、false positive、law gap。

**影响（推断）。** 同一问题跨 Round、视觉 review、friction report 的严重度无法比较。一个 agent 未遵守清楚规则的行为失败，或暂时无法归因的差异，容易被塞进 law gap/expectation gap，进而修改本来正确的 skill。这里不主张所有领域共用同一套 severity。

**修法。** 各 owner 定义严重度的用户后果、必须动作和边界例子，跨族仅显式映射。field-test 分开“是否满足冻结期待”和“原因是否已确定”；允许 behavioral nonconformance、unresolved/mixed attribution，保留证据后再裁决。视觉检查指定尺寸/缩放/可接受近似，缺实际 render 时不可宣称已判视觉合格。

### SL13 · P2 · Meal camera 把一次模型识别当作食物名称，无法区分视觉未知与服务失败

**观察。** [identify_food:97–108][meal-label] 只要求一个短名称，食物不可见和 API error 都返回 None；[receipt:232–251][meal-receipt] 用食物名或 `(unidentified)`，没有 inferred/human-confirmed 或原因。[Episode:26][meal-episode] 的名称来自首次识别；实现也声明 episode heuristic 不是物理食物逐项辨识。

**影响（推断）。** 读者可能把“镜头可见食物”理解为“实际吃下的食物”；遮挡、无食物、请求失败无法分辨；纠正一次识别没有声明可追溯入口。已有 episode 限制应保留，不再把“没按物理食物分段”单独当新缺陷。

**修法。** 显示为 inferred label，区分 no-food-visible / uncertain / service-error；允许多个可见候选或 abstain。若用户纠正，保留旧值、纠正者与时间。可保留适当的识别事件引用，**不要求默认保存隐私图像**，也不以臆造数值 confidence 代替解释。

### SL14 · P2 · 退役 display 评分仍可被安装：数字门槛与不完整视觉输入会重新成为指导

**观察。** [Display README:21–23][display-retired] 明确 `_todo` 为 retired；但 [install.sh:142–147][install-sh]、[install.ps1:65–72][install-ps] 都未排除 `_todo`。其中 [Slides:235–254][slides-score] 要求 1–5 判断投影可读性，输入却只给 outline 和 selected LaTeX；[Poster:562–601][poster-score] 混合确定性 clipping/数值核对与 “Would you be proud ...”，达到 9 就 PASS。

**影响（推断）。** 本文不把这些视作现行 Display owner；但安装可达性使旧评分成为真实维护风险。数字门槛可能遮盖未看全的幻灯片和未定义的美感边界。

**修法。** 若确属退役，先由 installer/包 owner 统一两平台的排除策略；若要恢复，按现行 renderer/caller 与 Run 契约重写。视觉维度必须读 exact rendered target；机械错误设独立阻断规则，定性项给证据与例子，不把任意 9/10 当发布证明。

### SL15 · P2 · 多份定性 receipt 没有足够的评价者/量表版本记录，也缺跨评价者分歧处理

**观察。** [Novelty receipt:113–155][novelty-receipt]、[Pressure receipt:67–103][pressure-receipt] 的局部 schema 保存 idea、证据与时间，未显式绑定 evaluator、criterion/rubric version 和被评 Card revision/hash；[Fit schema][fit-schema] 记录 Venue 版本与人工 target receipt，但这不等于逐项机器判断的身份。新增 [portfolio Run Spec][ideation-runs] 已要求 actor、frozen inputs 和 Task Result 索引，这是明显缓解；剩余问题是 specialist receipt 没有强制解析到该父记录的绑定字段/规则，特别是允许直接调用时如何继承。已有“disagreement survives”主要指来源之间矛盾。Design 和最新 Writing 已有明确 reviewer/version 记录，不能概括成全工具缺失。

**影响（推断）。** 同一 Card 之后改变时，难确认旧结论仍适用；两个 reviewer 的冲突可能被新文件覆盖或被“再审一次”掩盖。当前静态材料不能证明实际一致率低，只能证明协议不足以测量或审计它。

**修法。** 由各 owner 采用第 5 节最小判断记录，保存原始分歧而不是投票后删掉。重要冲突明确 resolver、需补证据和临时状态；身份/版本可引用已有 Run receipt，不重复抄写。先做少量独立复标和边界例子校准，再决定是否需要更重的评价系统。

### SL16 · P1（语义冲突）/ P2（文案）· Workflow/Run 指标仍未全 Toolkit 通过

**要求与当前正确基线。** **A Workflow is a list of Runs.** [Run:30–33,60–75][run-current] 明确 planned Specs 与 actual Instances；标签、评论、签名和 gate 本身不自动成为 Run。判断记录应落在真实的 owning Run/Result 或控制收据中，不为每个标签新建 Run。

| 范围 | 指标 | 观察与建议 |
|---|---|---|
| Run、Task Workflow 与当前主模板 | PASS（本次所查核心） | `run_specs` 已使用；不再复述旧报告的 `phases:` 模板缺陷。Task 专项 worker 仍有旧说明，见下一行 |
| Task 专项、Page | PARTIAL，主要是活跃文案 | [task-for-fit:18][task-phase] 写 “Phase 2: Build”；[CHECK:352][page-phase] 仍称 “this phase contract”；[Outline plugin:678][outline-phase] 有同类当前指令。改为 owning Run Spec、lifecycle command 或 controller dispatch，按真实语义选择，不能把每个词改成 Run |
| Discovery | FAIL，语义冲突 | [Inquiry:13,27,50][discovery-phase] 的 `phase: D1`、“sole ... phase”、“Phase × Run declaration” 仍赋予独立执行权威。把 controller routing 与真正 source-analysis Run Specs 分开 |
| Ideation | PASS（收尾时新增核心契约） | [能力路由表][ideation-workflow] 已与 [source/pilot/portfolio Run Spec 列表][ideation-runs] 分开；后者明确真实 owner、输入、actor、门槛、结果及退出，portfolio 使用 Task 原生执行语法；人类选择是其 interaction/gate，不按每次答复造 Run |
| Writing | PASS（本次所查核心） | [入口][writing-current] 与 [evaluation][writing-evaluation] 将局部评价/修订放在既有 Run，self-review、独立 CHECK 和人工接受分开；旧 humanizer 入口已退役 |
| Insight、Design | PASS（核心语义） | 资源 kind/Question/GI 不自动成 Run；Design 的 Commission/Generate/Verify 与 Delivery projection 分开；本次的标签修复不能重新制造上层 Run |
| Paper | 核心边界可保留，文案 PARTIAL | [Paper Workflow:51][paper-compat] 明示 `workflow-phases/` 是兼容路径；[Round:191][round-phase] 仍用 “shared Page phases”。保留地址，更新用户概念 |
| Board、0_utils、现行 Display、Project | 核心边界可保留；普通工具操作 N/A | 本次未把格式步骤、渲染调用、feedback turn 计成额外 Run；不能据此声明所有 refs/UI 已全量通过 |
| Display `_todo` 4 个文件 | 退役内容 FAIL；安装风险见 SL14 | [Slides:225/264][slides-score] 等仍按旧阶段持久化；先确定可达性，再决定移除或迁移，不直接造同数目的 Runs |
| 外部 Labeling bridge | 跨包 PARTIAL | [Toolkit presenter:330–337][labeling-presenter] 把 P0–P5 仅作 grouping，正确；但其指向的 [subjective-label Workflow:52–58,164][labeling-workflow] 仍宣称 Phase ownership。需由独立包 owner 对齐；本报告不扩大为整个包审计 |

**影响（推断）。** 评价者身份、标签依据和 close authority 容易落到不同“进度单元”上；同一审核被多算或遗漏。现行规范的否定句、历史引用、保留目录名以及明确标注的 `phase()` adapter 字段不是同级缺陷，应保留兼容读取，不做全局替换。

## 4. 三条桌面交互走查

以下是文档/源码推演，未执行真实 Workflow。

| 情境 | 当前可能出现的歧义 | 建议呈现给人的结果 |
|---|---|---|
| Idea 主贡献 novel，supporting claim 已被先例覆盖 | 当前契约已区分 Matrix ready 与选择资格；仍需回归验证展示不会让人误解（SL05，已修） | “主贡献摘要 ready；该辅助 Core Claim 为 preempted，按当前选择规则阻塞。需修订该 claim/角色及依据后重新检查；机器建议不改变人的 open 状态。” |
| Design reviewer 无法判“non-coercive”，因为场景/判据不足 | unresolved → failed → queue another Verify（SL09） | “候选尚不可判。缺少拒绝/退出是否有后果的场景定义；需 Commission owner 澄清。已完成的字符数检查保留；不发布 ready。” |
| 报告有轨迹，无预测校准材料 | 被迫 high/medium/low，judge 仍可能按 spread 打分（SL01–02） | “预测摘要已核对；预测可靠性不可评，缺少校准依据。趋势名称按声明规则产生，不能据此推断原因或把区间窄解释为高置信度。” |

日常交互只需显示：**当前判断、关键依据、仍未知/有分歧之处、下一位决策者或所需输入**。完整出处、版本、规则放入可展开记录。不要为每次小改措辞强制多轮评分或人工确认；已有授权与局部 Run 的边界继续有效。

## 5. 原优先修复计划与验收条件（实施前基线）

以下表格保留修复前确定的工作顺序和验收条件，具体完成状态见前面的实施跟进表。

| 顺序 | 工作项 / owner | 具体完成条件 |
|---|---|---|
| 1 | SL01–02：Task Individual | system/schema/parser 使用同一判断协议；不可评不造分；维度完整性、severity、总 verdict 可确定性核对；旧 judgment 的 rubric/version 明示 |
| 2 | SL04、SL09：Insight / Design | 冻结领域判据；pooling 未决有出口；Design unresolved 按原因解决，不仅重新排队 |
| 3 | SL03、SL06、SL15：各判断 owner，共享轻量协议 | 每个 consequential label 有定义、相邻档边界、例子、证据、不可评和分歧规则；Venue authority 共用一个来源；不把 confidence 跨领域直接映射 |
| 4 | SL07–08、SL10、SL12–13：Discovery / Board / Paper / utilities | 元数据和语义评价分开；模板不预填完成/零分；局部偏好不自动变规则；severity 与 inferred food 可解释 |
| 5 | SL14、SL16：Installer + Workflow owners | 两平台对退役 skill 可达性一致；当前 Workflow 用 Run Specs/Instances；兼容字段保留且不授予语义权威；对齐外部 Labeling bridge |
| 6 | 所有改动 owner；含已修 SL05、SL11 的回归验收 | 选择正例、反例、边界、缺证据、冲突和旧版本样例，独立标注后比较原始标签/原因，裁决分歧；再做新上下文走查，不用只检查 enum 合法或关键词消失来代替语义验收 |

建议复用已有 Result/receipt，在 consequential judgment 上补齐以下最小结构；它是**拟议修改**，不是声称仓库已有该 schema：

```yaml
target: {id: "exact item/claim/artifact", version_or_hash: "..."}
judgment_kind: "novelty | identification | fit | readability | ..."
criterion: {id: "...", version: "...", owner: "..."}
assessment: semantic                 # deterministic / semantic / human-decision
value: "owner-defined label or null"
evaluability: assessed               # not-applicable / unavailable / disputed
evidence: [{source: "exact Result", locator: "claim/row/span"}]
reason: "decisive observation and rule; brief, reviewable rationale"
confidence: {value: "owner-defined or unknown", basis: "..."}
evaluator: {actor: "...", mode: "self | independent | human", receipt: "..."}
at: "RFC3339"
disagreement: {other_judgment: null, resolver: null, state: none}
next_action: "owner + missing input/repair/decision, or none"
```

这些字段可引用现有 Ticket、config 和 runtime，不必在每处复制；普通 style 建议可以用更短的 finding。人类 preference 不必伪装成 objective truth；机械派生标签不必额外要求主观 confidence。

三段优先英文改写示例：

1. **原**：`Does confidence match forecast spread?`  
   **拟**：`Assess predictive confidence only against the supplied calibration or uncertainty evidence. If that evidence is absent, record unavailable. Trajectory range is not a confidence measure.`
2. **原**：`Strength is STRONG | MODERATE | WEAK plus a reason.`  
   **拟**：`Use the strength rubric frozen for this claim type. Cite the evidence and rival tests that meet its stated boundary. If the rubric or required evidence is missing, record undetermined and name the next owner; do not force a strength label.`
3. **原**：`A review ... including a review with unresolved checks ... routes back to Verify.`  
   **拟**：`For each unresolved criterion, record whether the blocker is missing evidence, an unclear or conflicting criterion, or a review execution failure. Route it to the owner that can resolve that blocker. Repeat Verify only after the relevant condition changes or a technical retry is justified.`

与现有计划的合并边界：Individual 对应 Task F17/F18 的**后续协议问题**，不能再声称 CLI 没有 forecast 输入；Ideation 与现有 F03 人工处置修订并行，未选中不等于被拒绝的旧问题已经有改动；Writing 以已经落地的统一入口和 base-v1 rubric 为基线；Workflow 采用当前 Run v0.27.0，不能复活旧方言。上表是实施顺序，**不是另一组 Workflow 单元**。

## 6. 证据索引

以下 94 个证据链接已检查文件存在、行号有效与引用完整性；它们指向本次读取的工作树文件与起始行，正文写明适用行段。后续并行修改可能移动行号，实施前以字段、节名及引文确认。

[brief]: /Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/BRIEF.md
[inventory]: /Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/inventory.json
[task-template]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/workflow-template.yaml:19
[task-current]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/SKILL.md:123
[judge-cli]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/scripts/judge_report_cli.py:57
[safety-system]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/personas/safety-review/system.md:23
[run-current]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:30
[novelty-status]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-novelty-check/SKILL.md:91
[test-axes]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-ideation-test/SKILL.md:68
[direction-card]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/idea-card.md:18
[venue-authority]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-venue/SKILL.md:73
[wisdom-sign]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-wisdom/SKILL.md:62
[page-rubric]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-check/SKILL.md:308
[data-review]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/1_data/haipipe-data/fn/fn-review.md:114
[coverage-status]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/ref/skill-coverage.md:59
[select]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/3_select/haipipe-ideation-select/SKILL.md:45
[interactive]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:229
[post-analysis]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/post-run-analysis.md:47
[project-digest]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/digest.md:40
[design-verify]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/SKILL.md:114
[anti-slop]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing/haipipe-writing/ref/anti-slop-adapter.md:114
[report-xml]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-report/personas/patient-friendly/schema.md:36
[report-schema]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-report/src/report_schema.py:67
[safety-confidence]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/personas/safety-review/system.md:31
[safety-schema]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/personas/safety-review/schema.md:30
[judge-loader]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/src/persona_loader.py:65
[patient-judge]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/personas/patient-comprehension/system.md:33
[safety-verdict]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/personas/safety-review/system.md:42
[safety-unavailable]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/personas/safety-review/system.md:50
[safety-schema-constraints]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/personas/safety-review/schema.md:53
[judge-parser]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/src/judge_report.py:130
[judgment-model]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-judge/src/judgment_schema.py:34
[discovery-confidence]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/ref/discovery-yaml-schema.md:224
[novelty-confidence]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-novelty-check/SKILL.md:152
[knowledge-strength]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-knowledge/SKILL.md:49
[knowledge-pool]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-knowledge/SKILL.md:83
[pool-routes]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/ref/partition.md:39
[pool-threshold]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/ref/partition.md:33
[test-precedence]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-ideation-test/SKILL.md:103
[card-worst]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/idea-card.md:153
[ideation-checker]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/scripts/check_ideation.py:715
[pressure-projection]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-idea-pressure-test/SKILL.md:105
[card-pilot]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/idea-card.md:139
[card-recommendation]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/idea-card.md:107
[pressure-credibility]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-idea-pressure-test/SKILL.md:79
[fit-status]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-journal-fit/SKILL.md:61
[ideation-example]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/end-to-end-example.md:68
[fit-overall]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/venue-fit.md:154
[fit-authority]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/venue-fit.md:30
[search-admit]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/haipipe-discovery-search/SKILL.md:89
[source-admit]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/ref/source-format.md:64
[s2-quality]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/semantic-scholar/SKILL.md:97
[s2-rank]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/semantic-scholar/SKILL.md:203
[paper-analyzer]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/paper-analyzer/SKILL.md:35
[analyzer-template]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/paper-analyzer/scripts/generate_note.py:46
[analyzer-graph]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/1_search/paper-analyzer/scripts/update_graph.py:40
[design-criterion]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/references/unit-contract.md:68
[design-method]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/references/unit-contract.md:104
[design-route]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:129
[approver-cut]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/haipipe-page-approver-agent.md:39
[rules-cut]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/approve-rules/README.md:18
[outline-rules]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/approve-rules/approve-rules.md:24
[rules-promote]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/approve-rules/README.md:35
[approver-promote]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/haipipe-page-approver-agent.md:138
[preference-boundary]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:300
[writing-plan]: /Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/writing-findings-and-fix-plan.md:1
[round-severity]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-round/SKILL.md:239
[figure-review]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/display/figure-to-svg/SKILL.md:286
[field-triage]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/field-test/SKILL.md:85
[meal-label]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/scripts/meal_cam_loop.py:97
[meal-receipt]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/SKILL.md:232
[meal-episode]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/scripts/episode_tracker.py:26
[display-retired]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/display/README.md:21
[install-sh]: /Users/jluo41/Desktop/Tools-SPACE/install.sh:142
[install-ps]: /Users/jluo41/Desktop/Tools-SPACE/install.ps1:65
[slides-score]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/display/_todo/haipipe-display-slides/SKILL.md:235
[poster-score]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/display/_todo/haipipe-display-poster/SKILL.md:562
[novelty-receipt]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-novelty-check/SKILL.md:113
[pressure-receipt]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-idea-pressure-test/SKILL.md:67
[fit-schema]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/venue-fit.md:48
[task-phase]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/5_fit/haipipe-task-for-fit/SKILL.md:18
[page-phase]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-check/SKILL.md:352
[outline-phase]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-outline/SKILL.md:678
[discovery-phase]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/workflow-phases/haipipe-discovery-inquiry/SKILL.md:27
[ideation-workflow]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/workflow-table.md:1
[paper-compat]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-workflow/SKILL.md:51
[round-phase]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-round/SKILL.md:191
[labeling-presenter]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-plugins/haipipe-plugin-runs/SKILL.md:330
[labeling-workflow]: /Users/jluo41/Desktop/Tools-SPACE/plugins/subjective-label/skills/subjective-label-workflow/SKILL.md:52
[ideation-runs]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/workflow-runs.md:15
[writing-current]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing/haipipe-writing/SKILL.md:73
[writing-rubric]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing/haipipe-writing/ref/evaluation-rubric.md:8
[writing-rubric-preservation]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing/haipipe-writing/ref/evaluation-rubric.md:29
[writing-evaluation]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing/haipipe-writing/ref/evaluation.md:9
