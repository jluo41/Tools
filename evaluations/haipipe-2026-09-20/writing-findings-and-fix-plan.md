# Writing 家族：复核发现与修复计划

> **Current status — v2 applied (2026-09-20):** The approved design uses one haipipe-writing entry point, external skill adapters, and shared evaluation. **Section 10 supersedes Section 7 and the earlier recommendations to rebuild the standalone humanizer.** Sections 1–9 remain the historical review snapshot. Section 11 records implementation and validation; earlier plan-only statements describe their original stage.

## 1. 结论与快照

**本次仅提交 findings + fix plan；没有实施技能、代码或共享协议修改。** 原报告 [writing.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/writing.md) 保持原样。本补充报告修正原报告的证据范围，并给出实施顺序、依赖和验收条件。

- 复核日期：2026-09-20。HEAD：f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217。
- Writing 目录相对 HEAD 没有改动，两份现行 SKILL.md 均重新核对；原 W1–W14 尚不能关闭。W10 收窄为措辞歧义，W13 降为 P3。新增 W15：humanizer 的规则标题被包在代码围栏内。
- 共 15 项：6 项 P1、8 项 P2、1 项 P3。P1 涉及可执行宿主、科学意义、复核可靠性或本轮明确的架构约束；P2 涉及一致性、使用说明与交互；P3 为局部文字错误。未发现足以定为 P0 的证据。
- 共享工作树已有其他任务对 Page、Paper、Insight、Board、Display、工具和总览文档的修改，references 中也有脏子模块。本报告以复核时磁盘内容为准；这些改动均未接管或覆盖。实施前须重读相关文件，不能把本报告行号当作补丁锚点。
- 采用文件阅读、路径检索、Git 差异和源码静态检查。没有执行技能、CLI、测试、构建或外部服务，也没有启动新的子代理。下文的运行结果均是未来验收要求，不是已通过的测试。

总体判断仍是：**通用 Writing 部分符合；humanizer 在当前宿主接入与语义保真上不符合；Page 写作交接部分符合，需跨家族协调。** 通用 Writing 的局部修订保护、内容与风格权限划分值得保留。优先修复 humanizer 的输入、输出、科学含义保护和候选复核链，再清理说明与元数据。

## 2. 覆盖与位置记法

以下缩写对应实际目录。后文如 W/SKILL.md:189，表示该目录下文件及本次快照中的行号。

| 缩写 | 目录 |
|---|---|
| W | [haipipe-writing](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing/haipipe-writing) |
| H | [haipipe-paper-revise-humanizer](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing/haipipe-paper-revise-humanizer) |
| WF | [Writing 家族](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/writing) |
| PW | [Page workflow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow) |
| P | [Page](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page) |
| PA | [Paper](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper) |
| K | [haipipe-toolkit](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit) |

| 范围 | 本次覆盖 |
|---|---|
| 通用 Writing | W/SKILL.md 全文；realize-from-plan、writing-dna-adapter、anti-slop-adapter、change-record、holes、weaving、plain-rules、ai-tells 等现行参考；anti-slop 规则数据、归属说明与变更记录相关段落 |
| 学术 humanizer | H/SKILL.md 全文；pattern-catalog、before-after、venue-sciwrite 三份参考；CHANGELOG 与 slop.py |
| 家族入口 | WF/README.md、WF/CHANGELOG.md；两个技能的版本与当前调用关系 |
| 实现与现有测试 | 静态核对 wdiff 的生成、应用、校验和参数；score 参数与筛选；agree 版本比较；anti_slop 诊断、事实 token 比较与参数；阅读 test_roundtrip 及 test_anti_slop 相关覆盖。未做全量代码审计或执行验证 |
| 共享交接 | Page workflow 的当前 ontology、兼容字段、交互 Run/Version/Step、变更卡片和用户返回模板；Paper 的当前 Section/Story/Venue 权威与生成物边界；共享 family 总览 |
| 排除项 | 未评审整个 Page/Paper/Insight/Design 家族；未检查真实稿件、私人样本、venue 数据或上游子模块内容；不重新核实 NIH/NSF 的外部政策和样例授权 |

## 3. 必须统一的模型

**Workflow is a list of Runs. 工作流以 Run 为单位，不以 Phase 为单位。**

修复时应由共享 Workflow/Run 所有者给出一个可引用的权威定义，Writing 引用它并说明自己的职责。依赖、路由和图形可以表达这些 Runs 之间的关系；它们不能引入第二套 Phase 工作单元。

- Run 对应有明确目标、范围、所有者和退出条件的委托。worker 接受某个 Run 的工作，不自行分配 Run 或决定人的接受状态。
- Page 的 Version、Step 在现有 Run 内记录候选和完整的限定工作循环。READ、AUDIT、编辑、SECOND PASS、工具调用是内部动作；它们不自动成为各自的 Run，也不自动成为各自的 Page Step。
- 同一目标与范围内的普通反馈沿用当前 Run。新目标、实质范围变化或不可变 Result 的后续工作，由宿主依据其合同处理；不得为了换词、显示状态或调用检查器新建 Run。
- 单独编辑一个文件时，遵循该请求的授权和实际宿主；不凭空要求 Board、Page Ticket、PDF 或科研审批。
- 历史记录、物理目录名、兼容 API 字段需要分类保留。不能全局替换 phase、stage 或 run；注释行块的 “lane run” 也不是 Workflow Run。

当前 PW/SKILL.md:23–30 以 Run Spec Routes 编译的 directed graph 描述 Workflow，:57–61 明确把 phase/cycle/next_cycle 限定为控制器兼容字段。这已有清楚的权限区分，但仍需与本轮要求的 list-of-Runs 定义对齐。不能把兼容字段解释为继续使用 Phase 工作单元的理由，也不能仅凭未重复定义就判定每个 worker 失效。

## 4. 发现总表

| ID | 优先级 | 当前结论 | 主要责任范围 |
|---|---|---|---|
| W1 | P1 | 确认并扩展：旧宿主引用也残留在通用 Writing | Writing + Paper/Page |
| W2 | P1 | 确认：意义保真与自动调整主张/引文冲突 | Humanizer |
| W3 | P1 | 确认并扩展：通用 ai-tells 示例也新增事实 | 两个 Writing 技能 |
| W4 | P1 | 源码确认：Paper Note 没有被 check 校验 | 共享 wdiff + Humanizer |
| W5 | P1 | 确认：现行 Phase 用语、工作流定义和交接需统一 | Writing + Page/Paper/Workflow |
| W6 | P1 | 确认共享分类文档不符；未证明运行时父层路由 | 结构总览 + Insight/Design + Writing |
| W7 | P2 | 确认：句子拆分指令冲突 | Humanizer + Writing 参考 |
| W8 | P2 | 确认：slop 能力与用法说明过度/过时 | Humanizer |
| W9 | P2 | 确认：标题评分需要显式参数 | 通用 Writing |
| W10 | P2 | 收窄：no-op 条件已存在，always 措辞含混 | Writing + Page 交接 |
| W11 | P2 | 确认：集成状态、引用路径/章节与工具索引陈旧 | Writing 家族文档 |
| W12 | P2 | 确认：模式、输出和后续反馈约定不完整 | Humanizer + 宿主 |
| W13 | P3 | 确认；由原 P2 下调：we 人称错误 | Humanizer catalog |
| W14 | P2 | 确认版本顺序问题；日期含义需核实 | Writing 元数据 |
| W15 | P2 | 本次新增：关键规则误入代码围栏 | Humanizer SKILL 排版 |

## 5. 逐项证据、影响与修复建议

### W1 · P1 · 现行 worker 依赖不存在的 revise 宿主与规则文件

**位置与证据。** H/SKILL.md:68–70 强制读取 S-Venue-0-venue.md 与 ../../paper/haipipe-paper/ref/prose-quality.md；:96、:139 把候选模式及执行顺序交给 haipipe-paper-revise。仓库中没有该 prose-quality.md、revise hub 或 revise-content 技能。W/SKILL.md:328 仍说已移出的 revise-content “still owns when the pass runs”；W/ref/weaving.md:9–15 仍以该 worker 和其 write-principles.md 为现行调用者/规则来源。PA/README.md:3–7、:134–136 明确退休的是旧编号 S-stage runtime。

**影响。** 新上下文无法找到必需规则或模式所有者；接着猜测替代合同，会使 venue、内容范围和写入目标不可靠。H 的 tex 直接应用路径还可能与当前 Paper 生成物边界冲突：PA/haipipe-paper/SKILL.md:310–331 要求文字回到拥有它的 Page，delivery 下 TeX/Word 为生成物。

**修复。** 由 Paper/Page 确认 humanizer 的两种入口：当前 Section/Page 委托，以及用户直接指定的独立文件。前者从现行宿主解析 Story Section row、选定 Venue/requirements、证据绑定、候选位置和写入权限；后者用已提供的文件及明确请求开展限定编辑，不强制创建 Page。删除对不存在宿主的现行依赖；weaving 保留通用方法，编排回交实际调用者。真正必需且缺失的具名合同应报告准确路径；可选样本缺失不应一律阻塞。

**验收与依赖。** 依赖 W5 的宿主映射，供 W4/W12 使用。当前调用路径均能解析；Page 模式不会手改生成 TeX；独立文件模式无需虚构 Page Ticket；缺失必需输入时返回一个具体缺项。仅将旧名换成新名不算完成。

**原报告修正。** 不能宣称所有 S page 或 Stage Contract 已删除。PA/workflow-phases/haipipe-paper-section/SKILL.md:74–76 明确保留源文件中的 Stage Contract，:82–90 仍有合法 S-… Section 标识。也不能用仓库检索推断用户项目中不存在 S-Venue 文件；确定失效的是上述静态技能依赖和旧编排假设。

### W2 · P1 · 保留科学意义与自动改内容的指令互相冲突

**位置与证据。** H/ref/venue-sciwrite.md:18 禁止增删/重排主张及改变限定语、数值、引文；:34 禁止校核时重写数值或引用位置。H/SKILL.md:51–53 却要求为无支撑主张 “add evidence or soften”、降动词强度、补范围；H/ref/pattern-catalog.md:102–106 将五个引文变为一个，:108–111 要量化或删模糊限定，:150–160 要补证据、弱化或换成数值。

**影响。** 同一次语言编辑可能悄悄改变作者承诺或证据链，作者难以判断被接受的是措辞还是新论断。优美的句子会掩盖尚未决定的科学内容。

**修复。** 将保护内容的规则置于所有层级和示例之前。固定内容的 humanizer 只改表达；证据不足、引用相关性不清或强度不匹配时，定位并交给内容/证据所有者。不得为了消除某类词而删引文、改限定或补数字。用户明确授权内容修订时，按该新范围和证据重新处理；语言规则不能成为永久禁止作者修正主张的规则。grant 模式同样不能凭风格请求重设 aims、实验或合作方。

**验收与依赖。** 原五个 citation key、所有数值、术语、因果强度、限定语和主张顺序在语言修订中保留；无依据主张返回具名问题；内容修订另有明确授权及来源。W3/W7/W8/W12 必须继承此优先级。

### W3 · P1 · 多个 Before/After 将新增事实伪装为表面改写

**位置与证据。** H/ref/before-after.md:5–18 的 After 新增 noise-aware reweighting、三个 benchmark、F1 提升 3–6 points 和 accuracy 差异，却称保留事实。H/ref/pattern-catalog.md:60–62、:74–75、:92–100 等还新增 p 值、数据集、规模和结果。问题不限于 humanizer：W/ref/ai-tells.md:31–36 的 After 新增 “which the baselines miss (Table 2)”。NIH 样例在 H/ref/before-after.md:24–26 标为 constructed，NSF 样例在 :60–63 声明其 After 来源；这些标注不能让未提供的材料自动成为实际稿件证据。

**影响。** 两个技能都会读取的示例教给 agent “把空泛写具体”可以靠增加研究事实。抽象保真规则与实际示范相反，容易污染真实文稿。

**修复。** 逐个检查当前会被加载的 Before/After。语言例应在 Before 或明确的同一示例输入包中提供全部事实，After 仅改变表达；需内容规划的例子明确标为上游内容工作，不能作为自动 humanizer 的示范。保留真实来源/授权说明，不擅自把真实示例改称 unrelated 或 synthetic。缺失支持的句子保持原义并另记问题，指令不能写进稿件正文。

**可用的纯语言示例（数据明确为此教学例构造，两边完全相同）：**

> Before: We conducted an evaluation of the method on three datasets. Minority-class F1 improved by 3–6 points over focal loss, while majority-class accuracy changed by at most 1 point.
>
> After: We evaluated the method on three datasets. Minority-class F1 improved by 3–6 points over focal loss, while majority-class accuracy changed by at most 1 point.

**验收与依赖。** 依赖 W2。每例的新增事实集合为空，或每项都能指到该例事先提供且获准使用的输入；不借通用例子给真实稿件加结果。覆盖普通学术、NIH、NSF 及通用 ai-tells。

**原报告修正。** 原建议将 “outperforms” 改为 “evaluate” 已删除比较性主张；其 After 还把给 agent 的操作指令混入正文，不应采用。本次也没有观察到真实执行产生幻觉，证据指向示例设计缺陷。

### W4 · P1 · Paper 候选格式被现有 check 跳过，署名默认值也不可靠

**位置与证据。** H/SKILL.md:98 用 record --host paper 并声称 check 审核它；W/ref/change-record.md:91–100 定义 Paper 输出为 > Note:。W/cli/wdiff.py:152–168 只处理 > ✎，check 解析器 :184–185 没有 host 参数；:180 默认 who=CC，而 H/ref/venue-sciwrite.md:46 要求 verified model label。现有 W/tests/test_roundtrip.py:27–37、:56–61 的 Paper 用例确认了输出 Note 和旧 Board 记录保留，但仍调用只识别 Board 的 check，不能证明 Paper 校验有效。

**影响。** “零条问题”可能意味着零条 Paper 记录被检查；作者会误以为候选格式和锚点已验证。默认 CC 可能错误署名。

**修复。** 在宿主确认候选协议后，为 check 增加显式 Paper 支持（例如 --host paper），保留现有 Board 默认兼容。返回识别/检查/忽略/问题数量；预期有候选却检查零条时，不能标作已验证。Paper 候选重建应能分别还原原文和新文，并检查签名、日期、标记和锚点。普通 > Note: 也是合法 typed lane（W/ref/change-record.md:21），因此须先定义候选识别方式或限定预期记录范围，不能把每个 Note 都按 diff 拒绝。命令显式传真实宿主确认的 who 和日期。完成前，文档只能承诺生成，不能承诺 Paper 机械校验。

**验收与依赖。** 依赖 W1/W12 的格式和位置约定。未来针对 Board/Paper 各有正、负样例；混合普通 Note 与候选 Note、坏标记/签名/日期、缺锚点、零候选均有清楚结果。候选模式只生成/追加候选，原文及旧 lanes 不变，也不调用 apply 或同步 TeX。token/格式检查不等于科学意义检查。

### W5 · P1 · 活跃 Phase 用语及 Workflow 定义未统一为 Runs

**位置与证据。** H/SKILL.md:62 的 Workflow 实为内部操作列表，:133–139 仍为 “REVISE phase” 旧 worker 编排。W/SKILL.md:189 与 W/ref/realize-from-plan.md:144 要回到 owning phase；W/ref/holes.md:52、:90 仍称 paper/EVIDENCE phase。P/ref/user-check-packet.md:214 输出 “no Content yet · phase <PHASE>”。PA/haipipe-paper-workflow/SKILL.md:21–29 明说 journey phase 与 Page phase，PA/haipipe-paper/SKILL.md:33、:37 仍以 phase 路由。

**影响。** 读者无法用同一模型理解委托、反馈和状态。简单把每个词替换成 Run 又会错误地增加执行单元或改变已有记录身份。

**修复。** 按第 3 节的强制模型，由共享 owner 统一定义及 Paper/Page 映射。H 的内部流程改为“本次语言工作的操作”，由实际 Run 委托；W 遇到内容/证据问题返回明确 owner，由宿主决定恢复或委托 Run。用户状态显示已核实的当前 Run/id/status，未委托就说明 none commissioned。将 phase receipt 明确称为控制器 dispatch receipt，若确为兼容字段则附准确协议引用。检查注释块用词，必要时将 lane run 说明为 annotation block，避免混淆。

**验收与依赖。** 活跃工作流定义和用户交接使用 Run；每个剩余 Phase 命中都有历史、物理路径或兼容字段解释。PW/SKILL.md:57–61、:572–575 的序列化 phase 不做无迁移方案的改名；paper/workflow-phases/ 目录也不因文字修订搬迁。同一 Page 局部反馈不增加 Run，内部模型/工具动作不增加 Step。W1 接入依赖此映射，Shared Workflow owner 的决定必须在 W/Paper/Page 一致可见。

**原报告修正。** 原 W5 英文建议把 reading/auditing/editing/checking 都称为内部 Steps，粒度仍过细。PW/ref/interactive-writing-run.md:16–18、:87–89 定义 Step 为完整限定循环；本计划使用“内部动作”。历史的 DRAFT phase 迁移说明不能与现行路由一并删除。

### W6 · P1 · 共享总览仍保留 Application 作为 Insight/Design 的组合层

**位置与证据。** K/skills/STRUCTURE.md:146–149 已更新 Insight 的描述，但 :148 仍写 application = “the Insight/Design join and its delivery channels”；K/README.md:14 仍为 Paper / Application。WF/README.md:14–16 仍以 application owns reports 作 family 示例。

**影响。** 与本轮要求“Insight、Design 为独立一等 family，没有 Application parent”不符，Writing 读者获得陈旧家族地图。此项按明确架构约束列 P1；现有证据仅证明文档分类，不能证明执行器实际走了错误父层。

**修复。** 结构/Insight/Design 所有者共同修正共享总览；Writing README 改为直接说明它为不同宿主提供 prose worker，采用当前实际 family 名。已有物理 application 目录、schema 枚举或历史材料是否仍为兼容对象，应单独分类，不能在本次文案修复中直接删除。funding application 的普通英文含义保留。

**验收与依赖。** 总览和 Writing 入口不再要求 Insight/Design 经过 Application；共享记录明确兼容例外。与 W5 可独立推进，但应和正在修改共享总览的任务协调。本报告未联系其他任务或代改共享文件。

### W7 · P2 · 同类长句被同时要求“不要拆”和“拆开”

**位置与证据。** H/SKILL.md:115 为 “compress, don't split”；H/ref/pattern-catalog.md:119–126 为 “Split them”；H/ref/venue-sciwrite.md:30 又限定 complete idea。W/ref/ai-tells.md:27、W/ref/plain-rules.md 的 Sentences 节也给拆句偏好；W/SKILL.md:69 则要求 Section 一 Bullet 一句。

**影响。** 同一段落在不同参考文件间反复拆合；还可能破坏 Page 的 Bullet/句子映射或证据锚点。

**修复。** 用主张、因果连接、阅读负担和宿主映射决定压缩或拆分。约 30 词仅为检查提示。固定 Section 映射若需变动，返回计划所有者；允许拆分时保留所有限定语、引文、主张关系和可追踪地址。

**验收与依赖。** 依赖 W2/W5。清楚的长句可保留；含多个独立意思的句子可在获准范围内拆分；不为了节奏分数增加句子或更改 Outline。不为每个新句创建 Run。

### W8 · P2 · slop.py 的实际范围小于“六层审计”的表述

**位置与证据。** H/CHANGELOG.md:2 称 six-layer audit becomes CODE。H/cli/slop.py:31–84、:143–164 是词形、节奏和阈值统计，未实现 venue/claim-evidence/grant 语义判断。docstring :4 列 --control FILE，但 :167–172 仅接受 files、--gate、--detail。H/SKILL.md:72–80 没有清楚说明此工具的调用条件与限制。

**影响。** 用户和 agent 容易把统计筛查当成完整审阅；复制命令会失败。为了过数字密度或节奏阈值而改稿，还会与 W2/W7 冲突。

**修复。** 将当前入口明确写成可选的模式/节奏诊断，提供现有参数可运行的示例；删除过时 --control 用法，除非另有实需才实现。说明既有 --gate 是显式选择的统计退出行为，不能决定科学正确性、AI 来源或人的接受。用新的更正条目说明能力边界，保留历史 changelog 的事件记录。

**验收与依赖。** 依赖 W2/W7 的保真与拆句规则。帮助文案、示例和 parser 一致；短样本和合法学术结构不触发强制改写；无论分数如何都继续按宿主完成语义检查。实现本项不需要扩建为另一个六层自动重写器。

### W9 · P2 · score.py 默认不会检查标题

**位置与证据。** W/SKILL.md:257 说 score.py 会标出标题；W/cli/score.py:72 的 --headings 是 headings only，:96–100 默认跳过标题且只列达到分数门槛的行，:108–109 也明确无命中不等于清楚。

**影响。** 按文档运行默认命令可能漏掉用户最先看到的标题；加 --headings 也不会同时检查正文。

**修复。** 工具说明分别给正文与标题用法：python3 <W>/cli/score.py FILE，以及 python3 <W>/cli/score.py FILE --headings。保留 worklist 的定位，不把分数当成清晰度判决。局部反馈不必重跑整页评分。

**验收与依赖。** 文档准确说明两种模式互斥和分数门槛；以后检查帮助及一个标题/正文样例即可。此项可独立做文档修复，无须为了配合旧文案改变默认扫描行为。

### W10 · P2 · no-op 已有例外，always 仍使记录要求含混

**位置与证据。** W/SKILL.md:76–79 在 genuine wording changes 后写 Before/After “always required”；:86–88 明确无 prose 变化时不返回 Before/After 或 preference card。PW/ref/writing-step-template.md:113–124 同样只为 material wording change 创建卡片。

**影响。** 局部上下文能解释 always 的范围，但孤立摘取该句会让 agent 为接受、导航或无修改反馈生成空变更卡片。未发现实际执行造卡片的证据。

**修复。** 合并为明确条件：有文字变动保存干净 Before/After 和本地原因；无文字变动只记录 disposition 及原因。保留原始反馈、applied/accepted 区别和延后偏好分析规则。

**验收与依赖。** 同一套例子覆盖有改动、未采纳、保持原文、接受已有候选及纯导航；只有真实文字变化产生卡片。沿用 Page 模板，无须建立新的日志格式或 Run。

### W11 · P2 · 文档仍称 diff 集成尚未完成，并指向错误章节

**位置与证据。** WF/README.md:27–29 说 should become a consumer / until then；H/SKILL.md:98、W/SKILL.md:391 已规定调用 wdiff。格式映射实际位于 W/ref/change-record.md:77 起的 §4，WF/README.md:29 与 W/SKILL.md:394 都写 §3；父 README 中 ref/change-record.md 也不是相对于该 README 的正确文件位置。另 W/SKILL.md:366 写 Three checkers，:369–373 列了四个 CLI 和一个测试。

**影响。** 读者找不到协议，或误以为要再写一套 diff 逻辑；工具数量与职责不清。

**修复。** 写清当前已共享 diff 生成，校验范围按 W4 的真实状态表述。父 README 使用 haipipe-writing/ref/change-record.md 的正确相对链接及 §4 标题锚点；技能内引用同步修正。工具索引按实际项目列出职责，不沿用错误数量。

**验收与依赖。** 路径、章节和调用关系一致；文档不把“生成支持两种格式”扩大成“两种格式均已校验”。最终状态说明依赖 W4，路径修正可先做。

### W12 · P2 · 自动应用、候选复核和作者反馈缺少统一的交接约定

**位置与证据。** H/SKILL.md:64–83 默认自动修改 tex、留 %% 注释，再说人可用 > USER: restart；未定义该反馈写到哪里、重开谁、如何拒绝某一改动。:96 的候选模式依赖不存在的 hub。H/ref/pattern-catalog.md:33–39 要先 Audit 再 Rewrite/Report，:247–249 要 cleaned text + report；H/ref/venue-sciwrite.md:3、:49 则将候选模式交给作者，并规定源 .md 中 Note、禁止同步 TeX。

**影响。** 作者不能清楚区分原文、已应用文本、候选和已接受版本，也难以只拒绝一处修改。不同宿主可能写错源文件或输出一份未保存的“清理后全文”。

**修复。** 在开始时从请求和宿主确定 apply 或原文保留 candidate 模式、目标文件/范围、记录格式与写入者。自动应用仍可在已有授权内先内部审计再编辑，不增加每句审批。Page 宿主沿用候选/推广规则，独立源文件按请求直接改；生成 TeX 不作为 Page 写回目标。完成时返回实际保存的文本或候选、范围、关键原因、未解决问题及真实检查状态。反馈使用现有宿主入口，支持按句子标识提出“保留原文”“接受候选”或继续改；撤回为一条新记录，不删除旧签名历史。

**验收与依赖。** 依赖 W1/W2/W4/W5。作者能从交接直接定位原文和候选；拒绝 S2 不改 S1/S3；applied 不等于 accepted；候选模式原文不变；Page 不额外执行发布/导出。先审计后编辑可在一个已授权操作中完成，原报告不应将其一概视为必须暂停的审批冲突。

### W13 · P3 · we 的人称错误

**位置与证据。** H/ref/pattern-catalog.md:24 称 we 为 third-person plural；:138 正确称 first-person plural。

**影响。** 基础说明自相矛盾，降低可读性与信任；不构成 P1/P2 级执行阻断。

**修复与验收。** :24 改为 first-person plural，并避免把某一种人称当作所有学术稿件的必需形式。两处一致，保留 venue 与作者语态。可随 W2 的 catalog 修改一起完成，无共享依赖。

### W14 · P2 · 版本头和 changelog 顺序不能可靠表示当前状态

**位置与证据。** W/SKILL.md:13 为 0.18.0；W/CHANGELOG.md:1 同为 0.18.0，:300–303 却在末尾新增 0.19.0。W/cli/agree.py:114–121 只拿第一条可识别版本作比较，因此该状态可绕过预期检查。H/SKILL.md:13 的 last_updated 为 2026-08-05，而 H/CHANGELOG.md:1 是 0.3.0 · 260908。

**影响。** 人和静态检查器难以判断最新行为，后续修复也可能用错版本基线。

**修复。** 先确认 0.19.0 是已发布、待发布还是误置记录，再整理本地版本顺序并同步 frontmatter。humanizer 日期按字段约定及实际修改同步，不能仅因 CLI 更新就断言 SKILL 日期必然错误。若增强 agree，检测本地发布序列中“尾部新版本/顺序含混”，不要直接选择最大 semver；humanizer 历史含上游 2.x 与迁移后 0.x，必须区分版本谱系。保留真实历史日期与出处。

**验收与依赖。** 两技能的当前版本可被唯一解释，frontmatter 与最新本地发布记录一致；若修改 checker，增加排序异常及迁移历史不会误报的样例。最终版本记录在实际修复后更新，不在本次报告中预定发布号。

### W15 · P2 · 关键 gate 与候选说明误入同一个代码块

**位置与证据。** H/SKILL.md:67 打开代码围栏，直到 :101 才关闭。其间 :85 的 Venue-grounded clarity gate 标题、:87–94 四个 gates 以及 :96–100 的候选说明均位于围栏内。

**影响。** Markdown 阅读时关键规则没有标题和列表层级，链接/强调也作为代码显示；读者容易把这些规则当作前面操作示例的一部分。

**修复。** 在内部操作示例结束处关闭围栏，将 gates、模式和 diff 命令放在正常标题/列表下；命令单独用带语言类型的代码块。结合 W1/W2/W12 整理段落顺序，避免修版式后再大幅挪动。

**验收与依赖。** Markdown 中四个 gates 是真正的规则列表，候选模式段落与操作示例分离，围栏配对正确。此项为新发现，尚未渲染验证；实施后的文档预览应检查其呈现。

## 6. 对原报告的明确更正

本报告保留原 ID 方便追踪，以下判断以本补充报告为准：

1. **W1：** 旧编号 S-stage 退休不等于所有 S-… Page 或 Stage Contract 废弃。当前 Section 明确保留后者。必需 Page 合同也不应无条件套到独立文件编辑。
2. **W3：** 不采用原报告的 “outperforms → evaluate + 操作指令” After；它不保留同一主张。不能在无来源依据时把例子改标成 unrelated。问题是显示的 Before/输入不足以支撑 After，非已证实实际生成幻觉。
3. **W5：** 内部 READ/AUDIT/check 调用不能各记为 Page Step。共享宿主已有 Run 边界与兼容字段说明，修复应对齐它们并落实 list-of-Runs 定义。
4. **W6：** Writing README 的 application owns reports 本身不证明父层关系；更强的证据是 STRUCTURE 的 Insight/Design join。未审计运行时父层分派。
5. **W9：** --headings 是只检查标题，并非在默认正文检查中附加标题。
6. **W10/W12：** 将 no-op 视为条件措辞歧义；先 Audit 再 Apply 可以是同一次授权中的内部顺序，不自动产生额外批准要求。
7. **W13/W14：** we 错误降为 P3；humanizer last_updated 是否失真须结合字段含义，不单凭较新的 CLI changelog 判定。

## 7. 分批实施计划

以下是后续实施方案，**本次没有开始任何一批修复**。表中的批次是维护工作顺序，不是 HAI Workflow 的 Phase 或自动新建的 Run。

| 顺序 | 具体工作与交付物 | 依赖 | 完成条件 |
|---|---|---|---|
| 0 · 重读共享状态 | 查看 Git 状态与当前文件；确认共享文件正在进行的修改；形成准确待改文件清单 | 无 | 不覆盖已有修改；本报告证据仍适用或已逐项更新 |
| 1 · 定宿主与单位 | W1/W5：由 Workflow/Page/Paper 明确 Runs、内部动作、当前输入和写回位置；Writing 接入；W6 由结构所有者修正 family 总览 | 批次 0 | 当前 Section 与独立文件两种路径明确；Workflow 定义是 Runs 列表；兼容字段有分类；无 Application parent |
| 2 · 统一写作权限 | W2/W3/W7/W13：设置保真优先级；重写危险样例；统一拆句；修正人称 | W2 本身可先起草；最终接口依赖批次 1 | 实际示例与规则同义，来源明确；语言修订不做内容决策 |
| 3 · 完成候选复核 | 先 W12 确定模式/格式/目标，再 W4 实现 Paper checker 和署名，最后同步 W11 的集成说明 | 批次 1；保真验收依赖批次 2 | 生成、校验、保存、反馈在同一宿主协议上闭合，原文与候选可重建 |
| 4 · 清理入口与呈现 | W8/W9/W10/W11/W15：工具用法、no-op 条件、链接、代码围栏；W14 整理发布元数据 | W9/W10 可独立；最终声明依赖批次 2/3 | 文档命令与实现一致；关键规则可读；版本唯一；不夸大校验能力 |
| 5 · 验证与复审 | 对实际改动执行针对性验证和 fresh-context 场景，记录证据；回看全部 15 项 | 前四批对应修复完成 | 每项有通过证据或明确未完成原因；共享问题未完成时不宣称家族全面符合 |

关键依赖：W5 → W1 → W12 → W4；W2 → W3/W7/W8；W4 → W11 的最终校验声明；实际修复 → W14 发布记录。W6 的共享分类修正可与 Writing 本地工作并行安排，但需要单一文件所有者协调；本轮不执行并行代理或交叉写入。

实施范围建议集中在 W/H 的 SKILL、相关 ref、WF/README、wdiff 与必要的现有测试扩展。score 的缺陷主要在文档；slop 不需扩成新的自动改写系统。共享 Page/Paper/Workflow/STRUCTURE 修改分别由其所有者完成，Writing 不独立发明第二套协议。references 上游内容不在计划的修改范围。

## 8. 验收矩阵

这些场景用于将来的修复验收。应保存输入、实际输出/差异、调用参数、宿主记录和结论，不能只记录 agent 自述“遵循规则”。

| 场景 | 可观察的通过条件 | 对应问题 |
|---|---|---|
| 独立文件只改一个词 | 仅目标及必要语法接缝变化；不要求 Page/Board；有精确差异与原因 | W1/W12 |
| 继续 Page 的 S2 反馈 | 沿用当前 Run；反馈原文保留；保存实际候选并返回所需段落/链接；无范围外改动、自动接受或重跑全页 | W5/W10/W12 |
| 接受已有候选或保持原文 | 有 disposition；没有伪造 Before/After、偏好卡片或新 Run | W5/W10 |
| 原文保留的学术候选 | 原文、既有 lanes、TeX 不变；候选完整；who/date 来自真实宿主；Paper check 确实识别记录 | W4/W12 |
| 坏候选与普通 Note 混合 | 识别坏标记、签名、日期、锚点；普通 typed Note 不误判；零检查条数不能伪装通过 | W4 |
| 学术主张、引文簇和限定语 | citation keys、数字、术语、因果/不确定性和主张顺序保留；缺证据单独反馈 | W2/W3 |
| NIH/NSF 风格请求 | 不新增 preliminary data、partner letters、资助事实；不凭语言请求重构研究 aims | W2/W3 |
| 长句与一 Bullet 一句 | 优先保留意义与宿主映射；必要结构变更交给计划 owner；不为过阈值而拆句 | W7/W8 |
| 必需 venue/Story 输入缺失 | 报告准确缺项及 owner；不猜新路径。仅缺可选样本时仍能做授权的通用语言修订 | W1 |
| Outline/Evidence 与风格冲突 | 保留内容权限，返回缺口；不靠弱化主张或从 DNA 样本借事实解决 | W2；保留已有优点 |
| 缺失或 partial Writing DNA | optional 缺失不阻断；明确要求的 named style 缺失按合同处理；partial 如实标注；不重建全库 | 保留已有优点 |
| 合法领域词或短样本被 anti-slop 命中 | 输出局部诊断/限制，允许保留；不将高分当作 AI 来源或接受结论，不自动改稿 | W8；保留已有优点 |
| 无 Content 的用户状态 | 显示实际 Run 或尚未委托，不输出活跃 Phase 单元，不为模板填值新建 Run | W5 |
| 工具与说明 | 标题/正文评分各自按文档选择；slop 示例参数存在；路径/章节可解析；规则不陷在代码块 | W8/W9/W11/W15 |
| 家族与发布说明 | Insight/Design 独立；共享说明一致；本地版本与迁移历史可区分 | W6/W14 |

验证分两层：

- **针对实际改动的检查。** 若改 wdiff，扩展现有 roundtrip 思路，但 Paper 必须有可被拒绝的负例和“确实检查了多少条”的断言，不能沿用零问题即成功。若改 agree，覆盖本地乱序和上游版本迁移。若仅修文档，先做引用、参数与 Markdown 呈现核对，不因文案修复扩大到全仓库构建。
- **Fresh-context 验证。** 根 README:133–136 要求修改技能后由新上下文子代理执行真实任务，确认选中正确技能、遵守指令并产出目标结果。后续实施时分别验证通用 Writing 与 humanizer，并覆盖 Page 交接；本次没有修改技能，因此没有启动此验证。共享 Paper 修改还需遵循其目录验证要求。凡无法运行的检查，记录为未验证。

机械比较只能覆盖格式和受保护 token；“保留了同一科学承诺”“读者更容易理解”“反馈自然且范围正确”仍需逐句审阅实际输出。不能用通过 anti-slop、wdiff 或 agree 替代这些判断。

## 9. 共享责任与不确定性

| 事项 | 应确认的所有者 | 当前不能断言的内容 |
|---|---|---|
| Workflow 列表、Run Spec/Instance、兼容 phase 字段 | 中立 Workflow/Run + Page | 不能在 Writing 报告中决定全部运行时迁移细节或改序列化字段 |
| Humanizer 当前 Section 接入、候选存放和推广 | Paper Section/Story/Venue + Page | 当前无完整等价 revise hub；不能假设新开关/新 Ticket 字段已存在 |
| Paper Note 的区分与展示 | sentence/lane 协议 owner + Writing wdiff | 普通 Note 与候选 Note 如何无歧义区分，需在实现前定下来 |
| Application 分类 | 共享结构 + Insight/Design | 文档 join 已确认；运行时路由、历史兼容目录的全部用途未审计 |
| 版本与时间 | Writing 维护者 | 0.19.0 的发布状态、last_updated 的统一含义未确认 |
| 外部与真实项目输入 | 各项目所有者 | 私有 Stage Contract、venue 样本、真实稿件及样例许可没有验证 |

本计划不要求用户先回答上述所有事项才能修任何文件：规则冲突、样例、标题参数、no-op 措辞等可先做。需要共享决定的部分在依赖明确后实施，最后据实际验收关闭对应问题。

**必须保留的现有能力：** W/SKILL.md:33–57 的最小修改范围；:61–108 的局部 Page 反馈与 applied/accepted 区分；:171–220 的计划/证据权威及冻结 DNA；:231–244 的可选诊断；既有签名记录的追加与可恢复性。修复目标是让 humanizer 和入口文档达到相同的清楚程度，而非扩大自动改写、审批或后台工作的范围。

## 10. Revised implementation plan v2 — one Writing entry point

### 10.1 Target and ownership

The latest discussion establishes the proposed direction: Page Section and Paragraph Runs call haipipe-writing; Writing selects external writing, style, or evaluation capabilities. Retire haipipe-paper-revise-humanizer as an independently discoverable HAI skill after its useful local protections and selected external replacement are connected.

Workflow remains a list of Runs. Section and Paragraph Runs remain sibling Page Runs. Writing, calling a method, evaluating, and revising are internal actions within the commissioned scope. They do not automatically allocate additional Runs or Page Steps.

| Owner | Responsibility |
|---|---|
| Page Run | Scope, frozen inputs, original feedback, Version/Step records, acceptance, promotion and lifecycle |
| haipipe-writing | Scoped prose generation/revision, method selection under the Run configuration, evaluation and revision, structured return |
| External capability adapter | Resolve one actual method/version, map its inputs, restrict its actions, normalize its output |
| Evaluator | Return text-specific findings and verdicts; identify whether the review is self, external, or independent |
| Page CHECK and person | Final version-specific review and human acceptance under their existing contracts |

### 10.2 Work package A — make Run-to-Writing invocation explicit

Update W/SKILL.md and the Page workflow table, interactive-writing-run.md, writing-step-template.md, and delegated paragraph-run.md contract. Reuse the existing worker_skill_chain and worker.name bindings; add the corresponding Section binding where needed. Do not introduce a separate writing scheduler.

Define one Writing request with the current Run/Version/Step identity, target and editable scope, mode (draft/revise/evaluate), recoverable baseline, plan/Bullets, bound Evidence, neighboring context, resolved requirements, original feedback, selected methods, and rubric identity. Missing optional style inputs remain optional; missing required inputs produce a named finding or block. Outline work is invoked only when the authorized request requires it.

The owning agent resolves the request, loads W/SKILL.md and the selected adapter/skill entry, invokes any declared tool, then processes the returned candidate or findings. YAML binding names identify the selected worker; they do not by themselves launch a model. The current feedback endpoint continues recording pending feedback for the agent's next turn. Automatic background execution is outside this plan.

Return a candidate, local changes/reasons, evaluation, method trace, and unresolved owner-routed findings. Page saves these into its current Version/Step. Independently delegated paragraph work retains its existing Result contract. Standalone file editing uses the same Writing interface without requiring Page-only artifacts.

Acceptance: both Section and Paragraph commissions actually select haipipe-writing; a local edit preserves out-of-scope prose and Run identity; a Section review checks cross-paragraph coverage and joins. A resumed Step does not reload every external skill or rerun the full Page workflow.

### 10.3 Work package B — define the external capability interface

Add proposed references under W: ref/method-adapter-contract.md, a small ref/writing-methods.yaml catalog, and ref/methods/ entries for selected capabilities. These names are proposed files, not existing runtime interfaces. Extend the current Writing DNA and anti-slop adapters rather than duplicate them.

Each catalog entry declares an id, role (writer/style/evaluator), actual installed entry or packaged implementation, version/hash, supported scopes, required inputs, output contract, permitted actions, attribution, and availability. The catalog is metadata; the agent executes the selected skill instructions/tools. Do not represent an unavailable external installation as a callable dependency.

Adapted external outputs are limited to candidate text, style inputs, or structured review findings. The adapter validates scope, protected content and output shape before Writing uses the result. A writer is not automatically an evaluator; an evaluation adapter must return findings without rewriting the authoritative Page. Conflicts with approved claims, evidence, venue rules or the user's scope return to their owner.

Run configuration selects only the needed capabilities and freezes their identities for that commission. An explicitly required but unavailable method produces a named block; an optional unavailable method is reported as skipped. Historical reviews retain the method/version that actually produced them. Changing a material frozen input follows the existing host policy.

For academic-humanizer, resolve an actual available external entry and add a review-compatible adapter. Keep references/ as provenance and comparison material under the current repository policy; merely recording that upstream source is not execution. If the external method is not installed, base Writing still works, and the selected external review is visibly unavailable. Its installation is a separate environment requirement, not silently performed by this plan.

Acceptance: one external evaluator completes a real invocation on a fixture and returns normalized findings with provenance. A second fixture capability can be selected by adding an adapter/catalog entry without editing the Page workflow. Writing works with zero external methods. No upstream source tree or vendored full workflow is copied into the active skills tree to simulate availability.

### 10.4 Work package C — establish the shared rubric and bounded self-review

Extract the reusable prose criteria from the existing four Page CHECK axes into a proposed W/ref/evaluation-rubric.md. Page CHECK references that common base and retains its own Page-specific mechanics, whole-Page scope, reviewer independence and close rules. Add W/ref/evaluation.md for applying the rubric during writing. This is one base definition with host-specific requirements, not two independently maintained rubrics.

The base axes remain Mechanics, Function, Evidence and Readability. Add resolved venue, Section/paragraph job, user requirements and selected specialist checks as applicable criteria before writing. Use MEETS, NEEDS WORK, N/A and NOT VERIFIABLE with applicability reasons. Missing evidence, altered claims, changed citation keys/numbers or unauthorized scope changes cannot be offset by a high style score. Metric tools remain diagnostic.

Each evaluation records the candidate version/hash, rubric version, evaluator identity/mode, criterion and source, target/quoted evidence, verdict, reason, smallest fix, and owner when the fix is outside Writing's authority. Preserve before- and after-revision findings against their respective candidates. Self-review must be labeled as self-review and cannot be presented as independent verification.

The default proposed cycle is candidate → evaluate → one bounded revision pass → evaluate the revised candidate → return. The Run may explicitly configure a different revision budget. Missing upstream inputs or no progress stop the automatic cycle and return the remaining findings. Later human feedback can continue in the same Run under its existing Step/Version rules.

For a local wording request, evaluate preservation and the affected criteria plus the necessary seam. For a Section draft, evaluate its paragraphs and their joint argument. Do not reuse an old verdict for changed text without rechecking the affected criteria. Store the compact review in the existing Step journal; reference larger tool reports when needed. There is no mandatory new directory or Run for each check.

Acceptance: the rubric catches a changed causal claim and a dropped citation, flags an unsupported number as NOT VERIFIABLE, and identifies a missing paragraph job with a location and fix. Revision is re-evaluated, budget exhaustion is visible, and no score or self-review marks human acceptance. No-op Steps produce no fabricated change card. Formal Page CHECK retains its separate actor requirement.

### 10.5 Work package D — retire the standalone humanizer

After A–C are connected, move the useful meaning-preservation and venue constraints from H/ref/venue-sciwrite.md into the shared Writing contract with current owner references. Preserve definitions, numbers, citations, evidence-tied hedging, scope and author comments. Correct dangerous examples in W/ref/ai-tells.md; do not migrate H's unsupported numeric examples into the adapter.

Use the current anti_slop.py adapter for optional diagnostics. Compare H/cli/slop.py with the diagnostics that are actually required; migrate only useful missing behavior, with attribution, before retiring that file. Do not carry its empirical numeric-density or rhythm floors into the acceptance rubric.

Remove H from active skill discovery after migration. Keep history in Git and source/attribution records; do not hide an installable SKILL.md in a nested _old directory. Both installers recursively discover skills and their _old exclusions differ. Existing external installations or user-owned copies are not automatically deleted.

Update WF/README.md, W/SKILL.md's ownership/consumer section, current references and local changelogs. Preserve historical changelog/proposal/feedback text as historical evidence. This is a skill retirement inside haipipe-toolkit, not removal of a top-level plugin package.

Use Page's existing clean Before/After records and presenter for Page candidates. Do not rebuild the obsolete revise hub or make Paper Note candidates the new default. The --host paper generator remains an existing compatibility capability unless its removal is separately justified; its docs must accurately state that current check does not validate that format. Full Paper Note validation is needed only if a verified current consumer still requires it. It is no longer a prerequisite for the new Page integration.

Acceptance: current discovery offers haipipe-writing as the HAI writing entry point, active references do not route to H, the external academic evaluator is traceably selected when available, and base protections still work when it is absent. Existing Board diff behavior and signed records remain intact. No receipt claims that an unsupported Paper Note format was mechanically checked.

### 10.6 Order, files and completion evidence

| Order | Deliverable | Depends on |
|---|---|---|
| 1 | A: shared Writing request/response and Section/Paragraph bindings | Current host contracts and working-tree reconciliation |
| 2 | B: capability adapter/catalog, existing adapters mapped, academic evaluator entry | A |
| 3 | C: shared rubric, structured self-review, bounded revision and Step record | A; B for external evaluation |
| 4 | D: migrate local protections, retire humanizer, correct live references and metadata | A–C, preservation checks and dependency audit |
| 5 | Targeted validation and fresh-context skill trials | Implemented changes; repository validation guidance |

W/SKILL.md, WF/README.md and local changelogs change across these packages. Proposed new Writing references are method-adapter-contract.md, writing-methods.yaml, methods/ entries, evaluation-rubric.md and evaluation.md. Existing DNA, anti-slop, change-record, realization and AI-tell references are updated only where the new contract affects them. Page changes are concentrated in workflow-table.md, interactive-writing-run.md, writing-step-template.md, the delegated paragraph-run.md contract, and CHECK's shared-rubric reference. A new dispatcher, service or automatic subagent per edit is not required.

Future validation must cover: Section and Paragraph dispatch; standalone editing; no external method; a selected evaluator; a missing required method; an evaluator that proposes unauthorized content changes; factual preservation; re-evaluation; no-op feedback; same-Run continuation; and humanizer removal from both installer discovery paths. Apply the root README's fresh-context validation after implementation. This plan-only update executes none of these tests and does not start new agents.

### 10.7 Disposition of the original findings

| Findings | v2 treatment |
|---|---|
| W1/W12 | Replace the obsolete standalone host with A/D and the shared adapter/feedback contract |
| W2/W3/W7 | Enforce in shared Writing/rubric; fix retained examples; do not migrate conflicting external instructions |
| W4 | Use Page-native review records; correct compatibility claims; Paper-aware checker becomes conditional on an actual consumer |
| W5 | Keep Run-based integration and classify legacy fields; coordinate shared Workflow/Paper wording without new runtime identities |
| W6 | Remains a separate shared family-topology item; it need not block implementation of Writing's adapters |
| W8 | Retain only useful diagnostics through the selected adapter; no human/AI verdict or numerical style acceptance floor |
| W9/W10/W11/W14 | Correct as part of Writing documentation, Step conditions and release metadata |
| W13/W15 | Removed with the retired skill; any retained/adapted text must pass grammar and Markdown checks |

Removing a file is not by itself evidence that its underlying behavior is fixed. Close each finding only after the replacement path meets its applicable acceptance criteria. At the plan-only stage, this section changed the report only. The later approved implementation is recorded below.

## 11. Approved v2 implementation — 2026-09-20

Applied packages A–D: the shared Section/Paragraph/file request, selected-method
catalog and adapters, common rubric and bounded self-review, Page Step/CHECK
integration, and retirement of the standalone HAI humanizer. Writing is now
0.20.0. Existing shared work and reference submodules were preserved.

See [implementation and validation](writing-v2-validation.md) for the actual
fresh-context trials, exact preservation checks, commands and limitations.
Writing tests and four skill metadata checks pass. Page's guard suite has the
same five failures with and without these Writing changes; the comparison is
recorded rather than presented as a green suite. Bash discovery offers only
haipipe-writing in this family; PowerShell was inspected but is unavailable.

The external academic-humanizer is not installed in this environment. Its
adapter reports unavailable selection truthfully; native Writing remains
usable. Generic extensibility was exercised with two actual project-provided
fixture skills, not represented as upstream humanizer execution. W6 remains
outside this Writing v2 scope, and legacy Paper Notes still have no mechanical
checker; their documentation now states that boundary.
