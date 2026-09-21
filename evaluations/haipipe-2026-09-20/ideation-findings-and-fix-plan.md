# Ideation 全族问题复核与修复计划

## 1. 范围、快照与结论

- 日期：2026-09-20；HEAD：f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217。
- 原报告：[ideation.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/ideation.md)。本报告补充并修正其判断，不改写原报告。
- 本轮重新完整阅读 8 个 Ideation SKILL.md，复核相关 schema、示例、checker 和测试源码，并对照当前共享 Run、Page、Paper 合同。全族仍为原来的 8 个技能；Ideation 目录相对 HEAD 没有工作树改动。原轮已完整读取的 UI 元数据、changelog 和 8 份 reference 仍可作为同版本依据，本轮重点重读问题涉及的章节。
- 共享工作区已有大量其他家族的并行修改；尤其 Page 已明确 serialized phase 是 adapter dispatch 标签。本报告采用当前磁盘内容，不把原报告对兄弟家族的旧判断直接沿用。
- 本轮仅新增这份计划文档。没有修改技能、schema、脚本、测试或上游 reference，没有执行 checker、真实技能任务或外部查证。代码结论来自静态阅读，验收案例尚未执行。

**结论：保留 Workflow 定义和多候选决策合同两个主要问题，新增三项 P1：机器处置权与人类权威冲突、未入选候选阻塞选择门禁、交接缺少逐卡授权一致性检查。** 原报告中的 UI、one-off 路由和 Page phase 判断需要收窄；不能把所有专家技能都要求成独立 Workflow，也不能把能力标签机械改成 Run。

优先级口径：P1 表示影响 Workflow 权威、人的决定或合法交接；P2 表示字段合同或执行路径含糊；P3 表示可读性风险，尚无真实用户误用证据。

### 引用约定

下文短路径以 [Ideation 目录](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation) 为根；references/、scripts/、tests/ 均位于其 haipipe-ideation/ 下。每项主要证据提供可点击的当前文件行号，文字中的行号区间用于定位上下文。共享 Run、Page、Paper 文件单独链接。行号对应本轮快照，后续实施前应重新定位。

## 2. 对原报告七项发现的复核

| 原发现 | 本轮处理 | 修正后的判断 |
|---|---|---|
| 1. 三阶段 Workflow 无 Run 清单 | 保留 P1，收窄论证，见 F01 | 缺少 Run Spec 列表/图成立；“不建本地 Run”可以与使用外部 owner 的 Runs 共存，二者本身并不直接冲突。 |
| 2. 无逐候选人类决定 | 保留 P1，见 F02 | 多卡 disposition、posture、risk、理由缺少统一记录。需同时处理审阅范围和未回答候选，不能从未入选推断人已 defer/abandon。 |
| 3. 目标状态投影不清 | 保留 P2，扩为 F06 | 单一 I3 权威已明确；问题是字段映射、版本和漂移处理没有落到合同，不是已有多个合法选择权威。 |
| 4. Select UI 与边界相反 | 降为 P3，见 F10 | “Select”可以理解为协助选择，不能证明逻辑相反；短描述仍值得明确人的决定权。 |
| 5. one-off 实时来源路径 | 保留 P2，收窄为 F09 | allowed-tools 没列 web 不证明无法检索；Skill 委派及 owner 路由已存在。缺的是 one-off 的复用、检索、落盘与失败回退说明。 |
| 6. skipped pilot 投影 | 保留 P2，见 F07 | 字段用途和 matrix 映射含糊成立；reason receipt 有可能解释该字段，不能直接断言系统要求虚构 Task Result。 |
| 7. 入口可读性 | 保留 P3，见 F11 | 属于阅读顺序改进，未经真实用户测试，不计作执行失败。 |

另有三点明确更正：

1. [当前 Page receipt 合同](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md:572) 已将 phase 解释为序列化的 dispatch label，且声明 receipt 不是 Level-4 Run/Result。Ideation 应跟随该释义；没有证据要求为了术语一致立即重命名共享 schema。
2. 原报告对 7 个子技能统一给“部分”的 Workflow 指标过宽。单次 novelty、pressure、journal-fit、Nature overlay 是可复用能力；是否构成 Run 取决于 commission 和关闭合同，是否发布 Workflow 则取决于是否承担编排职责。它们不必各自发布独立 Workflow。
3. 原发现 5 对 Novelty 的引用应定位到当前 SKILL.md 第 18–22 行，而非第 15–17 行。

## 3. 问题清单

### F01 · P1：Workflow 缺少实际 Run Spec 列表与活动归属

**位置与证据**

- [伞技能第 50–61、78–82 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/SKILL.md:50)：自称 three-stage state machine / workflow，同时说明编号是 capability group，不是 Run ID。
- [workflow-table.md 第 7–15、33–36 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/workflow-table.md:7)：列 I1、I2a–d、I2、I3，却未列实际 Run Specs；生成、检查、比较、handoff 被统一称为非 Run。
- [共享 Run 合同第 193–250 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:193)：可执行 Workflow 的权威是 Run Spec 图，每一节点必须独立关闭，并有 owner、目标、actor、gate、route 等。

**通俗影响**：agent 知道要做哪些事，却不知道完整 Workflow 实际委派哪些 Runs，以及卡片生成、综合评估和人类决定归属于谁的 Run 或内部 Step/Gate。无法一致计数、恢复和关闭。

**拟议修法**：保留能力组目录；把现有 I1/I2/I3 表明确标为能力与路由表，另发布 Workflow 的 Run Spec 列表及依赖图。逐项应用共享六项判定，明确 owner-native Run Type、目标、输入、退出条件、Result/receipt、数量公式和恢复方式。复用已有结果或只做投影的 invocation 可以分配零个新 Run。禁止本地第四执行库的规则可保留；若语义综合或人类决定满足独立 Run 条件，须先与共享 owner 确定合法 owner/Run Type，不能通过改名虚构身份。

**验收**：所有可执行 Workflow 节点均为实际可 commission 的 Run Spec；每项能力能映射到某个 Run 内的 Step/Gate、外部 owner Run 或无 Run 的适配操作。I1/I2/I3、单次 query、一次模型调用、一个 receipt 文件都不会被直接计为 Run。

### F02 · P1：人类收据不足以表达多候选的分别处置

**位置与证据**

- [Select 第 43–57 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/3_select/haipipe-ideation-select/SKILL.md:43) 允许选择零个、一个或多个候选，要求保存未入选者的处置理由；workflow-table.md 第 65–68 行要求每个 reviewed candidate 的 dated human receipt。
- [receipts.md 第 95–143 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/receipts.md:95) 只有全局 decision、selection_posture、accepted_risks；只有入选者有 card 关联的 target/Story 条目。
- [示例第 148–180 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/end-to-end-example.md:148) 中机器分别建议选择 i01、放弃 i02、暂缓 i03，但收据只记录 i01，没有逐卡人类处置。

**通俗影响**：同一人选两个 Idea，分别接受不同风险，或选择一个同时明确暂缓/放弃其他项时，无法从唯一收据完整还原决定。“没有被选”也可能被误写成“人已决定暂缓”。

**拟议修法**：版本化扩展 selection schema，声明本次审阅的 card 集合；每个已回答候选恰好一条 disposition、理由及人类决定来源，入选条目再绑定 posture、risks、target/category/contract、Story。尚未回答的候选保持 open/unreviewed，不补造 defer。顶层 decision 和旧列表可作为兼容摘要，不能成为第二写入源。历史 v2 记录只能还原其中实际写明的决定。

**验收**：一份收据能无歧义表示“i01 proceed、i02 caution、i03 defer、i04 abandon、i05 未回答”；逐卡风险不会串用；重复、遗漏已声明完成审阅的卡、无来源的处置会被报告。系统可准备收据，但不会把机器建议或静默当成人的回答。

### F03 · P1：Generate/Test 的处置权限与人类权威直接冲突

**位置与证据**

- [伞技能第 244–251 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/SKILL.md:244) 明定只有人可以 select、defer、abandon；idea-card.md 第 165–167 行要求 deferred/selected/eliminated 均有人类收据。
- [manifest-and-sync.md 第 222–225 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/manifest-and-sync.md:222) 却写“Generate or Test may … defer, or eliminate Ideas”，没有限定为投影既有人类决定。
- 同文件第 131–150 行同时出现 state: deferred/eliminated 和 selection_authority: none、receipt: null；[示例第 141–151 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/end-to-end-example.md:141) 在人决定前写 i03 remains deferred。
- receipts.md 第 129–130 行把 open 与 deferred 都映射到 decision: defer，也需要区分“未决定”与“人决定暂缓”。

**通俗影响**：一个 agent 可以依据同步文档把机器的淘汰建议写成最终卡状态，另一个 agent 又依据主合同拒绝该状态。Paper 显示的“暂缓/淘汰”可能没有人真正作出决定。

**拟议修法**：为 recommendation、科学门禁状态、human disposition 分别定义写入权。Generate/Test 只写前两者；最终 disposition 只能从 I3 收据投影。同步若显示历史 disposition，必须能追溯其决定版本，同时继续保持同步本身不具有选择权。修正上述措辞和示例；不得仅新增一个机器可写的“人类状态”字段。

**验收**：机器推荐 abandon 后，卡和 P0 人类 verdict 仍保持 open，直到有人回答；人已明确 defer 的卡可被正确投影且来源可追溯。新 Test 证据不能自动改写或撤销历史选择。

### F04 · P1：选择门禁把未入选候选的未完成检查算成全局失败

**位置与证据**

- [check_ideation.py 第 782–809 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/scripts/check_ideation.py:782)：decision 为 select 时，第 797 行先调用 check_test()，第 809 行才读取 selected_cards。
- [同脚本第 668–748 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/scripts/check_ideation.py:668)：遍历所有 admitted Ideas；任一 unverified/inconclusive claim 报错，未知 identification 或 pending/skipped pilot 也报错。只有特定 terminal_preemption 路径跳过后段检查。
- Select 第 43–54 行允许候选带显式 HOLD、选择其中一部分；end-to-end-example.md 第 130–160 行同时给出 i03 hold/pending/defer 与选择 i01 的合法业务叙述。

**通俗影响**：已经准备好的 i01 可能因为暂缓中的 i03 而无法交接，迫使人处理本来不打算推进的候选。按当前调用链，上述示例状态会进入失败条件；这是静态推导，尚未做运行复现。

**拟议修法**：分开“portfolio 结构与状态真实有效”“整个 Test 已完成”“这次所选卡可交接”三个判断。Select/Handoff 加载全体候选并保留 HOLD，但只对实际入选集合执行严格的完成与资格检查；仍保留全体 admitted cards 的结构、来源、广筛等合同要求。保留或显式版本化 --gate test 的整体完成语义，不能把未完成 Test 悄悄变绿。

**验收**：i01 完成、i03 明确 HOLD 且未入选时，i01 的合法选择/交接能通过；改为选择 i03 必须失败；全体 Test 若仍有未完成项，其整体完成 gate 仍不得声称完成。既有单卡拒绝 unverified 的行为继续保留。

### F05 · P1：checker 未把入选卡、目标与交接绑定成同一份授权

**位置与证据**

- [check_select 第 809–840 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/scripts/check_ideation.py:809)：检查 selected card 路径和三个列表的长度；没有按 card identity 验证 selected_cards、story_routes、target_routes 的一一对应。target route 的 contract 只检查路径。
- [check_handoff 第 864–903 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/scripts/check_ideation.py:864)：检查 source/卡/fit/contract 路径及必需字段，没有比较 handoff 的入选集合、目标和 Story 是否等于那份人类收据，也未从此调用链核对最新 sync revision。
- check_test 第 737–738 行跳过 terminal_preemption 的后续检查，第 762 行按机器 next_route 是否为 select 决定是否检查 deep fit；check_select 缺少独立的“实际所选卡必须可选”断言。
- [receipts.md 第 132–140、193–210 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/receipts.md:132) 要求每张实际入选卡的 claims 为 novel/partial、准确目标/Story 和最新同步；[venue-fit.md 第 167–178 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/venue-fit.md:167) 明定文件存在不等于 contract current。

**通俗影响**：数量相等、路径存在，仍可能把另一张卡或另一个期刊交给 Paper。机器 next_route 还可能影响所选卡是否接受完整检查。现有“全体过严”和“所选对象关联过松”同时存在，修 F04 时必须同步堵住这里。

**拟议修法**：按 canonical card identity 做集合和逐项连接：选择、Story、target、handoff 必须一一对应；实际入选卡独立接受 eligibility 检查，不依赖机器建议。验证 exact target/category 与真实 Venue contract 内容、版本和 currentness；复用 Venue owner 的读法，不另立规则来源。校验 handoff 指向同一 selection 版本、准确 claim/evidence/fit/feasibility 引用，以及约定的 sync revision/hash。按规范化物理 Story 路径检查独立路由，避免仅改角色名绕过。

**验收**：错卡但等长、重复卡、空 select、另一份 selection 路径、错误目标/category、过期或仅有空壳的 contract、旧 sync、未入选卡进入 handoff、preempted 卡被选，均有明确拒绝理由；合法多卡交接通过。机械检查只验证合同与来源关系，不宣称证明人的真实意愿或科学结论。

### F06 · P2：人类目标的派生字段及历史版本缺少明确映射

**位置与证据**

- [idea-card.md 第 97–122 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/idea-card.md:97) 有 human_target 状态及 recommended_target，称 venue_fit 为 projection。
- [venue-fit.md 第 135–142 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/venue-fit.md:135) 又有包含 target/category/contract/by/at/conditions 的完整 human_target；Select 第 103–105 行同时明确唯一 I3 权威。
- [manifest-and-sync.md 第 241–244 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/manifest-and-sync.md:241) 要求重选时保留旧 selection 和 handoff；当前示例主要使用固定的 workflow/selection.yaml、handoff/paper-ideation.yaml，没有给出完整的不可变版本与当前指针关系。

**通俗影响**：一个选择更新后，卡、fit card 和 handoff 可能留下不同版本的目标。固定路径被覆盖后，历史决定可能仍有链接却已经指向新内容。

**拟议修法**：定义字段级映射和刷新顺序；machine recommendation 独立保留，human_target 一律派生自指定 I3 版本。选用与现有 owner 一致的不可变决定/交接版本机制，固定路径可继续作为当前视图或兼容入口；引用同时带可判定版本。冲突时 HOLD 并指出应刷新哪份投影，不自动“选一个值”。实施前区分 G0 intended target 与 Story 后续 operational target/rebind，避免用早期 I3 覆盖合法的后续决定。

**验收**：同一决定的 card、fit、handoff 字段一致；改变目标生成新决定且旧记录仍可完整读取；旧选择不会因新证据自动消失，受影响的当前交接会要求重新决策；Story 后续换刊保持其 owner 边界。

### F07 · P2：skipped pilot 的 receipt 用途和矩阵映射含糊

**位置与证据**

- [Pressure 第 90–104 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-idea-pressure-test/SKILL.md:90)：pending/skipped 不需要 Task Result，也不能通过 Test gate。
- [idea-card.md 第 91–96、138–150 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/idea-card.md:138)：feasibility.receipt 示例为 Task runtime，又要求 positive/negative/skipped 都有该 receipt；后文另说 skipped 需要 reason receipt。
- Test 的 matrix feasibility 枚举包含 pending/positive/negative/waived/hold，未包含 skipped；当前规则没有明确映射。

**通俗影响**：agent 不知道跳过实验后该填压力评估收据还是 Task 执行结果，也不知道矩阵该填什么。可以保存“跳过”历史，但不能表示已经做过实验。

**拟议修法**：明确 pressure_receipt 保存 skipped 及理由；feasibility.receipt 仅承载实际 positive/negative 的 Task-owned 执行结果，skipped 可为空；waived 有独立理由。推荐 skipped → matrix pending，并保留 skipped 原因与下一步；若采用 hold，必须全族统一且写清二者区别。

**验收**：没有任何计算的 skipped 案例能诚实保存完整历史，不必造 Task Result；它不能满足所选卡的资格；positive/negative 和 waived 仍分别要求正确结果、明确豁免理由。

### F08 · P2：Novelty 与推荐状态的跨文件投影不完整

**位置与证据**

- [Novelty 第 138、161–162 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-novelty-check/SKILL.md:138)：receipt 的 evidence_depth 为 none/metadata/abstract/full-text，并要求投影到 Card。
- [idea-card.md 第 83、107 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/idea-card.md:83)：Card depth 为 metadata-only/abstract/full-text，未写 none 或 metadata 映射；recommendation 又缺少 Select 和 sync 中使用的 defer。
- [Test 第 99–112 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-ideation-test/SKILL.md:99) 的 matrix novelty 按 central claims 汇总；idea-card.md 第 151–156 行描述所有 Core Claims 的最差状态；receipts.md 第 135–136 行对入选卡要求所有 claims 均 novel/partial。

**通俗影响**：无检索任务无法按 Card 枚举忠实保存 none；不同文档可能写出不同的机器推荐值；读者容易把 central 汇总的 ready 误当作整张卡可以选择。

**拟议修法**：发布明确的 projection 表和兼容读取规则，统一 depth 及 recommendation 的写入枚举；none 必须保持“没有读取证据”，不能升级为 metadata。分别命名 central contribution summary 与 selected-card eligibility，说明 supporting gap 如何展示，以及为何汇总 ready 仍可能不可选。这里可能是不同用途的两种读法，不把它直接定性为科学门禁自相矛盾，也不顺手放宽所有 claims 的选入要求。

**验收**：none、旧 metadata-only、metadata、abstract、full-text 有确定映射且无证据升级；defer 建议不会改变人类 state；central novel + supporting unresolved 能保留正确 matrix 摘要和不可选状态，界面不会只显示一个误导性的 ready。

### F09 · P2：one-off 来源检索与持久化边界未形成完整路径

**位置与证据**

- [Novelty 第 18–22、168–173 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-novelty-check/SKILL.md:18)：明确 Discovery owns finding/reading，但 durable load 说明与 one-off direct sources 要求未连成完整操作路径。
- [Journal 第 94–99 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-journal-fit/SKILL.md:94)、[Nature 第 91–95 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/2_test/haipipe-nature-paper-review/SKILL.md:91) 要求当前官方来源；Journal 已明确未查证时 provisional。
- 伞技能第 90–94 行限制 read-only audit 搜索范围，第 330–334 行要求 inline 不落盘，用户要求保留后才进入 durable unit。

**通俗影响**：缺的并非证据原则，而是临时问答中何时复用、何时交 Discovery、检索是否产生持久 owner artifact、不可访问时如何继续。不同 agent 可能擅自扩成持久项目，或只给引用外观而未完成查证。

**拟议修法**：三个 specialist 共用简短路径：先复用可核验来源；build/refresh 且任务需要查证时走 owner 的检索能力；inline 不因此自动创建 Ideation portfolio。新的持久 Discovery 产物遵循该 owner 的任务范围和保存约定。用户限制 no-search 或 read-only audit 时保留限制，缺失证据返回 provisional/HOLD、明确下一步；不得用记忆代替当前规则。不要仅靠在 allowed-tools 加一个工具名来声称修好。

**验收**：已提供 verified sources、需新查证、来源不可达、no-search、read-only audit 五类请求都有清楚输出和状态；内联任务不无故创建文件；任何无法查证的投稿规则和 novelty 不被升级为已验证。

### F10 · P3：Select 首屏文案没有显示协助决策的定位

**位置与证据**：[Select UI 元数据第 2–3 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/3_select/haipipe-ideation-select/agents/openai.yaml:2) 为 HAI Idea Select / Select tested ideas and journal targets；正文第 20–22、50–52 行明确不可代人决定。

**通俗影响**：只看选择器时可能误以为自动选题选刊；这是一项可能的理解偏差，没有实测证据。

**拟议修法**：保留稳定 skill 名称，把短描述改为协助比较并准备人的 idea/target 决定，例如 “Compare tested ideas and prepare your idea-and-target decision”。

**验收**：首次阅读者能说清模型比较、人作决定；不必为了文案修改技能 ID 或调用路径。

### F11 · P3：入口缺少先讲用户任务与结果的短版导航

**位置与证据**：[伞技能第 84–120、148–181 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/SKILL.md:84) 很快进入多 owner 装载、BJTR 和文件树；one-off 保存边界直到第 330 行再次说明。

**通俗影响**：新读者在确认自己会得到临时候选、查证表还是持久交接之前，先要读内部结构。信息多数已存在，主要是顺序成本。

**拟议修法**：入口增加 3–4 句任务导航：brainstorm、测试一个 Idea、维护可交接 portfolio；解释缺证据状态、保存时机和人的最终决定。后置完整 owner 路由，保留按需装载；补一个小术语表区分能力组、Run、Step/Gate、投影、receipt。

**验收**：fresh-context 阅读后能选对入口、识别缺少的输入，并知道本轮会否落盘/交接；不能因简化首屏丢掉审计模式、证据或人的边界。

## 4. 全族覆盖与 Workflow/Run 指标重判

| 技能 | 当前主要问题 | 本轮对 Workflow/Run 的判断 |
|---|---|---|
| haipipe-ideation | F01、F02、F03、F06、F09、F11；拥有共享合同与 checker 的 F04/F05/F07/F08 | 家族可执行 Workflow 定义不完整；已有 no-local-Run 和 owner 边界保留。 |
| haipipe-ideation-generate | F01、F03、F08；受 F02/F06 的状态投影影响 | 是生成能力/路由入口；其 durable 活动归属待家族 Run 清单说明，不把每次 lens/dedupe 变成 Run。 |
| haipipe-ideation-test | F01、F03、F04、F05、F07、F08 | 承担编排，需说明实际委派 Runs、内部 reconciliation 和 gate 的关系。 |
| haipipe-idea-pressure-test | F07、F01 的挂接 | 本地执行边界较明确：新计算归 Task Run；自身是否独立 Run 由 commission 决定，不要求独立 Workflow。 |
| haipipe-novelty-check | F08、F09、F01 的挂接 | 专家能力；query/阅读/逐 claim 比较不自动构成 Run。“run-wide/no-search run”宜改成 assessment/invocation，除非确指已分配 Run。 |
| haipipe-journal-fit | F06、F09，受 F05 目标验真影响 | broad/deep 是任务内工作划分；无需为了两种 fit 创建两个 Run。 |
| haipipe-nature-paper-review | F09、F01 的挂接；共享 target/projection 合同影响 | 条件加载的 editorial overlay；每个 lens 不创建 Run，绑定投稿条款仍由 Venue 提供。 |
| haipipe-ideation-select | F01–F06、F10 | 人类决定仅在满足共享六条件时成为独立 decision Run，否则是明确归属的 Gate；receipt 存在本身不足以推出 Run。 |

四个专家能力的“是否独立发布 Workflow”指标为不适用；其作为家族 Workflow 成员的映射仍需 F01 补齐。没有发现新增的第九个 Ideation 技能，也没有发现本族把 Insight 或 Design 归入 Application 的要求。

## 5. 共享边界与术语处理

| 事项 | 归属与实施要求 |
|---|---|
| Workflow | Workflow 是 Runs 的列表；分支和依赖由这些 Run Specs 的 routes 形成图。工作单元统一称 Run，不新增 Phase 权威层。Capability table 不能冒充 Run 清单。 |
| I1/I2/I3、目录编号、manifest stage | 当前能力/进度元数据，不是 Run ID，也不是已经废弃的兼容字段。可保留，但须明确与 RunSpec/Run Instance 的关系。 |
| Page phase 字段 | 当前已明确为序列化 dispatch metadata；保留兼容读写，界面/说明可叫 dispatch receipt。不得改成 run 而把一次 controller dispatch 变为 Level-4 Run。 |
| Paper P0 | [Paper adapter 第 29–47 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-ideation/SKILL.md:29) 的 journey phase 是历史旅程/Page 角色称谓；应由 Paper 说明与 Workflow Runs 的挂接，不改 Story00/P0 身份或历史路径。 |
| Task、Discovery | 保有执行/来源 Run、Result、Bib、runtime 的权威。Ideation 只保存判断和指针，不新增执行库，不复制原始结果。 |
| Venue、Story | Venue 负责 current contract 的结构和验真；I3 负责 G0 intended target，Story 负责之后 operational target/rebind。F05/F06 须遵守这条时间边界。 |
| Page/Paper 投影 | 同一 evergreen P0；工作视图刷新、adopted Content release、delivery 保持分离。同步和 Page CHECK 均不产生 I3 决定，也不自动分配 Page Run。 |
| 历史和兼容 | changelog 历史用词不计当前缺陷；旧 receipt/card 可读，不从缺失字段猜人类决定。schema 变更和 enum alias 要显式版本化。 |

跨族意见仅覆盖上述交接点，不代表已审计整个 Task/Discovery/Venue/Page/Paper 家族。实施时先读它们的最新合同，避免覆盖当前并行修订。

## 6. 拟议实施 Workflow：Run 清单、依赖与关闭条件

以下是供后续实施使用的拟议 Run Specs，尚未 commission、未分配任何 rNN/rp 身份，也不表示本轮已经开始修复。每项只在后续实施任务中确定 actor、Ticket 和实际 owner 地址后执行；产物均可独立审阅和关闭。没有必要再建立一个重复计数的 umbrella Run。

| 拟议 Run Spec | 有界目标与主要文件 | Actor/责任 | 依赖 | 产物与关闭条件 |
|---|---|---|---|---|
| fix-contract | 解决 F01；伞技能、workflow-table、共享 owner 交接说明 | Ideation 实施者；共享 Run/Page/Paper owner 核对 | 最新工作树及共享合同 | 实际 RunSpec 清单/图、活动归属表、保留字段清单；所有节点满足 Run 判定，无身份双计数。 |
| fix-decision | 解决 F02/F03/F06；Select、receipts、idea-card、venue-fit、manifest-and-sync | Ideation 实施者；Paper/Story 接口核对 | fix-contract 的边界决定 | 逐卡决策 schema、open/人类处置规则、字段映射、历史/当前版本关系、v2 兼容方案；各文档使用同一权威和映射。 |
| fix-gates | 解决 F04/F05；check_ideation.py 与门禁说明 | checker 实施者；Venue/同步校验接口核对 | fix-decision；fix-specialists 的枚举合同 | 分离结构/整体完成/所选资格，完成逐卡 join、目标合同和版本校验；记录各拒绝原因。与 schema 同批整合，避免中间版本错误放行。 |
| fix-specialists | 解决 F07/F08/F09；Pressure、Novelty、Test、Journal、Nature 和相关 reference | 专家技能实施者 | fix-contract、fix-decision 的权威及保存边界 | pilot/depth/recommendation 投影表；one-off 复用/检索/保存/回退说明；无证据升级、无新选择权。 |
| fix-examples | 解决 F10/F11，并让全族示例反映前述合同 | 文档实施者 | 前四项的合同与实现 | 多候选端到端示例、首屏导航、UI 文案、术语/版本说明及对应 changelog；不机械改写共享兼容字段。 |
| verify-family | 验收修复后的完整 Workflow 及兼容性 | 后续明确承担验证的实施者；按 README 使用 fresh-context subagent | 上述实现整合完成 | 按下一节记录实际命令、场景、结果和限制；所有阻断项闭合，输出独立验证记录。 |

**建议执行顺序**：fix-contract → fix-decision → fix-specialists 的合同部分 → fix-gates → fix-examples → verify-family。专家文案可以在合同稳定后与 checker 工作分别推进；不在 schema 尚未定稿时各自写一套枚举或选择规则。

**最小优先批次**：先合并人的决定、状态与 checker 修复，覆盖 F02–F06；它们互相依赖，不能只放宽全局 gate。F01 的 owner 决定须先明确，但不应把整套共享 Run 系统重构变成本族纠错的前置工程。F10/F11 最后做。

**实施前需要明确的设计决定**：Run Type/owner 的具体复用对象；selection 版本与固定路径的关系；--gate test 的整体完成语义如何保留；Venue/current sync 校验复用哪个 owner 接口。这些是实施者应在已有合同中查证并写成具体方案的事项，不是现在要求用户泛泛批准的空白问题。

## 7. 验收场景与证据要求

以下均为未来验收计划，本轮没有执行。当前 [测试文件](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/tests/test_check_ideation.py:558) 已有 unverified 拒绝、单卡完整选择/交接、全局 defer 保留 open tests 等案例；尚未看到覆盖下列关键多卡关系的用例，不能把现有单卡成功当作全族保证。

| 场景 | 预期结果 | 覆盖问题 |
|---|---|---|
| 成熟 i01 + 未入选的 i03 HOLD | i01 可合法选择/交接；i03 状态真实保留；全体 Test 不误称完成 | F04 |
| 改为选择 i03；或选择 preempted 卡但 machine next_route=abandon | 均拒绝，不因机器 route 跳过资格检查 | F04/F05 |
| 两张入选卡分别 proceed/caution，另有 defer、abandon、未回答者 | 收据逐卡完整，风险不串用，未回答不产生处置 | F02/F03 |
| 机器建议 abandon，无人回答 | card/P0 人类 verdict 保持 open，建议可见 | F03 |
| selected/routes 数量相等但 card 不同或重复 | 拒绝；规范化 alias 后仍一一对应 | F05 |
| handoff 换卡、换 target/category/Story、换 selection 版本 | 拒绝且指出具体不一致字段 | F05/F06 |
| contract 文件存在但 target 错、stale 或缺真实块；sync 版本过旧 | 拒绝当前交接，保留历史记录 | F05 |
| 重选目标或新证据影响已选 Idea | 新决定与新交接可追溯；旧版本仍可读；不自动撤销人的旧选择 | F03/F06 |
| skipped pilot，无 Task 执行 | reason/pressure receipt 能保存；Task Result 可空；不能当作所选资格已通过 | F07 |
| none/metadata/旧 metadata-only；central ready + supporting unresolved | 映射无证据升级；摘要和资格读法分别准确 | F08 |
| inline/no-search/read-only audit/来源不可达 | 不越过搜索或保存边界，清楚给出 provisional/HOLD 和缺口 | F09 |
| P0 sync 后未进行 Page release | working 可以更新，Content/delivery 不被自动声称 current，也不新建第二 P0 | F03/F06、共享边界 |
| 旧 v2 receipt 与旧路径、序列化 phase | 兼容可读；缺失决定不补造；dispatch receipt 不计作 Run | F01/F02/F06 |

后续验证还应包括：

1. 对修改后的 schema/examples/checker 做定向检查；报告具体执行命令及结果，区分预期 HOLD、结构错误与运行错误。
2. 按 [根 README 第 133–136 行](/Users/jluo41/Desktop/Tools-SPACE/README.md:133)，技能变更需由 fresh-context subagent 在真实代表任务中调用，确认选对技能、遵循指令、得到预期结果。重点覆盖 inline 生成、单轴检验、多卡选择及 Paper 交接；不是只让 reviewer 读一遍文档。
3. 对所有 8 个入口检查 owner 按需装载与状态表一致；条件性的 Nature overlay 不扩大成每个请求必跑。
4. 检查工作树 diff，确认没有覆盖其他人的修改，没有无意改 references/ 子模块或安装器/marketplace；本计划不需要增删顶层包。

## 8. 限制与保留项

- P1 的文档矛盾和代码调用/比较缺口有直接静态证据；运行表现尚未复现，修复后的通过/失败结果必须由未来验收记录证明。
- 本轮未核验实时文献、期刊网站、数据伦理条款或真实科学结论；F09 评估的是操作合同，不是当前投稿规则。
- F01 不能仅由 Ideation 一侧凭空指定新的共享 Run Type；F05 的 contract currentness 也应复用 Venue 的现行权威读法。当前未确认全部 owner API 的可复用程度。
- F10/F11 属于可用性建议，优先级低于授权、门禁和状态一致性；改善程度需要 fresh-context 使用观察。
- 保留现有良好约束：指针式证据、不复制 Result/Bib、novelty 与 identification 分离、广筛与 deep fit 分开、Nature 只作条件 overlay、人的选择唯一权威、Page 工作/发布/交付状态分离。
- 共享工作区仍在变化。正式实施前重新检查 git status 和涉及文件的当前内容，再按上述顺序落地；本报告不表示任何源文件修复已经完成。
