# Insight 技能族：问题复核与修复计划

日期：2026-09-20。基线提交：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`；本报告审阅的是其上已有修订的工作树。

**实施状态更新（2026-09-20）：** 用户随后批准修复、更新并测试。R01–R11 的源码和文档修改已落实；本轮结果见第 8 节。第 1–7 节保留为修复前的审阅快照，其中“本轮只新增本报告”“未测试”和旧行号描述的是当时的报告任务。

## 1. 结论与本次边界

**原评估的六项主要问题已经落实修订；当前工作不应再次从“移除 Insight Phase”开始。** Insight 入口、控制器、六个资源技能和 Task Insight 表述已采用 Run 模型。六个资源技能现在位于 `insight/folder-kinds/`，没有 `metadata.phase`。Workflow 的执行单位是实际分配的 native Runs；资源类型、Question Group、Page pass、GI 判断和注册表更新不因被列入流程而获得 Run 身份。

本次进一步确认了 **10 项待修问题和 1 项可读性改进**。最先应处理 Task 调用中的生产者 Run 身份与过早冻结输入；其次是共享身份解析、Board 注册和状态投影的一致性。当前核心模型已经对齐，但这些分支尚不足以支持“全技能族所有路径都可无歧义执行”的结论。

本报告重新阅读了[原评估及实施记录](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/insight.md)，并以当前文件核对。原报告第 1–9 节是修改前快照，第 10 节是已批准修复的实施记录；旧路径和旧行号不代表当前缺陷。

**本轮只新增本报告。** 没有修改技能、脚本、测试、原评估或其他任务的文件，没有运行测试、真实分析或实时 Board 操作。两项独立只读复核使用了用户指定的 GPT-6 Astra、Extra High 推理。以下验收条目是下一次实施的检查要求，不是本次已执行的验证。

### 优先级

- **P1：** 核心 Run 身份或常规执行路径存在缺口，应先于继续扩展功能修复。
- **P2：** 特定合法分支无法一致执行，或检查、写入、状态展示与契约不一致。
- **P3：** 不单独证明执行失败，但增加理解和维护成本。

## 2. 完整覆盖与当前状态

以下行数及定位对应本次工作树；其他任务仍在并行修改仓库，后续实施应再次确认位置。

| 技能 / 范围 | 本次覆盖 | 当前判断 |
|---|---|---|
| `haipipe-insight` | 全文 359 行、agent descriptor、全部 3 个 refs | 双路由和 Run 边界已修；分区接入说明与主文可读性仍需整理 |
| `haipipe-insight-workflow` | 全文 476 行、全部 3 个新 refs | Run Specs、实际 Run inventory、零 Run 控制动作、held/complete 已明确；示例与少数 GI 分支待修 |
| `haipipe-insight-meta` | 全文 104 行 | 已是 inventory 资源 owner；GI0 与实际执行工作分开；未新增独立缺陷 |
| `haipipe-insight-question` | 全文 139 行 | 注册不生成伪 Run；retarget 身份规则冲突，见 R03 |
| `haipipe-insight-data` | 全文 114 行 | 已是 Data 资源 owner；静态输入与 GI2 不一致，见 R08 |
| `haipipe-insight-information` | 全文 99 行 | 推导与 native computation 区分明确；未新增独立缺陷 |
| `haipipe-insight-knowledge` | 全文 96 行 | claim / pooling verdict 属资源语义；未新增独立缺陷 |
| `haipipe-insight-wisdom` | 全文 118 行 | 人签名、完整 payload 变化后重签、POOL deferral 已有规则；界面未充分投影这些规则，见 R07 |
| `haipipe-page-insight` | 全文 237 行、全部 4 个 refs、agent descriptor | `riNN` 与 checkpoint 已分开；生产者调用协议及 input 冻结缺口见 R01–R02 |
| `haipipe-task/fn/insight.md` | 全文 68 行 | 返回词已改为 checkpoint / Page workflow action；没有另建 Phase |
| 实现与共享边界 | 定向静态阅读 Folder parser、Page ruling、Context builder、Board checker、Run inventory、Ask、handoff、Design consumer 及相关测试；核对 Page Evidence、Run、Task 和共享 Runtime 契约 | 见 R04–R07、R10；不是整个 Board/Task/Design 代码库的全面审计 |

六个资源 owner 的版本史仅作历史定位，不作为当前操作指令。没有打开第三方 `references/` 内容、真实数据集或实时 Board。

## 3. 原问题的处置账本：哪些已经修好

| 原问题及原优先级 | 原因与影响 | 当前证据和处置 | 后续动作 |
|---|---|---|---|
| O01 · P1：Application Workflow 以 I0–I5 RunTypes / CELL 推进 | Folder 分类、工作目标和 Run 身份混用，无法可靠计数或续接 | [控制器:35](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:35)、[Run 合同:9](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/run-workflow.md:9) 现定义 Specs、依赖与实际 native Runs；控制动作允许 `runs: []` | 主体已修；只处理 R01、R09 等具体接入缺口，不再创造一套 Workflow 层 |
| O02 · P1：六个 owner 用 Phase 身份，Question 又禁止 Runs | 把资源当执行位置，也可能强行为注册动作造 Run | 六个技能已迁至 `folder-kinds/`、删除 Phase metadata；[Question:34](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-question/SKILL.md:34) 明确注册是无 Run 的控制更新；[迁移:3](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/migration.md:3) 限定旧字段权限 | Insight 主体已修；共享引擎旧 API 和外部安装另行跟踪 |
| O03 · P1：“workflow signs”，把 W handoff 叫 Design Brief | 主语可能授予机器签名权；混淆两个 owner | [控制器:17](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:17) 改为核对并记录人签名，Design 消费确切 Insight input 并拥有自己的 Brief | 文档已修；保留此边界，补齐 R07 状态投影 |
| O04 · P2：入口引用不存在的 `fn/*.md`、`skills/application/`、`application-wf` | 加载失败，族与责任归属不明 | [入口:32](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:32)、[Verbs:245](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:245)、[Ownership:304](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:304) 指向真实技能，独立 Insight/Design owners 明确 | 已修；旧 `application` 命令 token 明确是兼容 selector，不是父族 |
| O05 · P2：Task “Phase × Run”表及 Page phase 返回词 | checkpoint / 活动被误读成 Run 或阶段身份 | [workflow-table:25](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/workflow-table.md:25) 已改为活动与 Run ownership；[procedure:66](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/fn/insight.md:66) 返回 next checkpoint / Page workflow action | 已修；保持活动行不自动计为 Run |
| O06 · P2：auto charter 没有记录与核验格式 | 可能反复询问，或把许可延伸到无关工作 | [authorization.md:9](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/authorization.md:9) 已定义记录路径、actor、来源、board/runtime、scope、动作、失效与 control receipt | 已修；既有明确授权继续有效，签名和新计算释放仍按 owner 规则 |
| O07 · 共享问题：Folder/Page 对旧 `phase.yaml` 权威不同 | 身份读取和工作流进度混淆 | [Folder:55](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md:55)、[迁移:25](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/migration.md:25) 已统一 canonical `folder.yaml` / legacy 只读 fallback | 规范已修；实现仍有 R04–R05 |
| O08 · 共享问题：缺失的根原则文件链接 | Runtime 的上游依据无法加载 | [共享 Runtime:3](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-workflow/ref/workflow-runtime.md:3) 已改链真实 `haipipe-run` | 已修 |

**已批准修复任务的进度：** 上述主体修订及相关代码改动已经完成，未新增重复修复任务。原实施记录报告 117 项相关测试通过、14 个技能格式校验通过、6 个 Insight Folder contracts 无 findings；这些是上一轮结果，本轮未重跑，也不能据此宣称下列新增场景已被覆盖。

## 4. 当前待修问题

### R01 · P1 · Task 调用没有稳定分开计算 Run 与 DIKW Run

**文件与证据。** [task-calls.md:25](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/task-calls.md:25) 的 producer call packet 在第 36 行把 `execution` 写成 `<instance>#<riNN>@<version>`。第 48–52 行先搜索可复用支持结果，只有 “Otherwise” 才分配 RI；第 56–64 行随后分别产出 Supporting Result 和 RI 的 DIKW Result。[Run 契约:442](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:442) 要求生产者有自己的 receipt，且第 451–455 行要求每个执行地址有一个 Ticket / Result 配对。

**影响。** 新上下文执行者可能把计算和解释都记在 RI 地址上、漏记真正的 producer，或者在复用已有计算时漏建本次仍需要的 DIKW RI。这直接影响“Workflow 是 native Runs 清单”的可执行性和计数。

**拟修。** 分开 `producer_execution` 与 `consumer_insight_execution`。先独立决定是否复用、续接或分配 RI；再逐项决定是否复用支持结果。缺失的计算由 producer owner 分配其 native Ticket/receipt，接受后绑定进 RI；base recipe 仅作引用。补一个两种身份均完整的例子。

**验收。** “已有 support、需要新解释”和“缺失 support、需要新计算”两个场景均产生准确的 RI 与 producer 清单；每个 Result 归属于自己的 Ticket/receipt，base recipe 不重复计数。当前结论来自契约静态走查，未实际运行 adapter。

### R02 · P1 · `bind` 在支持证据到达前冻结最终解释输入

**文件与证据。** [instance-items.md:118](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/instance-items.md:118) 要求上游完成后才进入 final frozen interpretation input；[task-calls.md:59](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/task-calls.md:59) 也要求随后冻结局部 Evidence Results。但 [insight_items.py:469](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/scripts/insight_items.py:469) 创建空 `supporting_results` / `recipe_calls`，第 483–488 行立即写 input、hash 和 `frozen` checkpoint。第 499 行公开 CLI 只有 `check/table/cite/bind`；第 226–227 行会拒绝 frozen input hash 不匹配。

**影响。** 常规 bind → 获取证据 → 解释路径没有明确合法的补齐入口。执行者只能修改已冻结文件及其 hash、丢失新证据，或自行发明版本转换。语法检查通过不能消除这项时序冲突。

**拟修。** 区分不可变的 RI dataset/base/question/target 绑定与最终解释证据 envelope。分配时保留绑定与 planned receipt；依赖准备完成后，经明确操作冻结最终 input 并写 checkpoint。已有 frozen/published 记录不回写；为旧空 envelope 定义显式迁移或后继版本规则。

**验收。** 一个新 RI 可接收稍后完成的 Supporting Result 和 local Evidence Result，不改变任何此前已冻结字节；推理与独立 review 都固定最终 evidence envelope，retry 使用同一精确输入。先完成 R01 的身份规则，再实现此变更。

### R03 · P2 · Question retarget 无法同时满足稳定 ID 和 rung 前缀规则

**文件与证据。** [Question:49](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-question/SKILL.md:49) 要求稳定 `QD/QI/QK/QW` ID，retarget 只移动记录；同文件第 117 行要求 ID 前缀与目标 register 的 `question-rung` 相同。[question-groups.md:35](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/ref/question-groups.md:35) 允许改变 target 并重算 membership，而 [Page adapter:70](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/ref/page-v2-adapter.md:70) 说 target rung/scope 改变应新建问题。

**影响。** 把 QI3 改问 Knowledge 时，无法既保留完整 ID、又通过 GI1、又按 adapter 新建问题。随意改名会破坏旧引用，复制则可能留下两个有效 Queue target。

**拟修。** 明确一种 retarget policy。建议保留旧记录和历史，新建正确前缀的 successor，并记录 supersedes/alias；说明这与重复注册的区别。三个文件同步采用同一规则。

**验收。** QI→QK 后只有一个当前 answering target；新记录可通过 GI1，旧引用仍可追溯，历史与 Question Group 投影一致。

### R04 · P2 · 身份错误被 Board 检查吞掉，Ask 写入又使用另一套身份读取

**文件与证据。** [check.py:1973](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/check.py:1973) 在 canonical 记录无效或与 Page 冲突时返回空字符串；第 2016–2019 行因此跳过 kind-specific checks，没有报告 identity error。[groom_snapshot:1501](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/insightboard.py:1501) 调用此 checker，无 findings 时给出 clean 结果。另一方面 [_pages:135](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/insightboard.py:135) 只读 Page metadata，[register_question:1733](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/insightboard.py:1733) 据此选择并写 register。

**影响。** 同一无效/冲突身份可能在 Context 被拒绝、在 Board 检查中消失、在 Ask 中仍被写入。一个 Wisdom 页也可能失去 signature finding，却不新增 identity finding。这里确认的是检查和写入前置条件不一致，未证明实际 Design release 绕过。

**拟修。** 共享有明确 resolved/absent/error 结果的身份解析入口。checker 输出精确 routing finding；Ask 在任何写入前拒绝错误或冲突。Board 接入 canonical identity 后，缓存同时追踪相关 identity 文件的新增、修改和删除。

**验收。** 合法 canonical/legacy 在各入口得到相同 owner；无效和冲突得到可见错误；Ask 失败时 Page 与 log 字节均不变。依赖 R05 的解析行为。

### R05 · P2 · 身份解析器拒绝有效旧缩进，也会接受部分无效 YAML

**文件与证据。** [folder_contract.py:140](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/src/folder_contract.py:140) 取第一个 top-level `current`，第 153 行只识别两个空格缩进；第 50 行 `_clean()` 直接剥离引号。规范只声明 YAML/current.folder-kind，没有把两空格规定为兼容要求。

**触发例。** 旧文件的 `current` 直接子项若使用四空格，会被当成缺少 kind；两个 top-level `current` 会被静默取第一个；`folder-kind: 'wisdom` 的未闭合引号会被清洗成有效 `wisdom`。这是静态代码推导，本轮没有运行样例。

**影响。** 合法存量 Board 可能无法续接，错误记录却可能取得 owner 身份，与“无效 canonical 必须报错”不一致。

**拟修。** 使用能识别真实 mapping 深度、标量及重复键的解析方式；支持合法缩进，拒绝重复 current/kind 和无效引号。不能简单恢复会误读嵌套 kind 的宽松正则。canonical 无效仍禁止回退旧文件。

**验收。** 两空格、四空格 direct child 均可读；仅嵌套 kind、重复 mapping/key、无效引号均报错；canonical precedence 和 legacy read-only 行为不变。

### R06 · P2 · 内置 Ask 尚未覆盖空 register 和新控制收据合同

**文件与证据。** [Question:124](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-question/SKILL.md:124) 允许空 register，但 [_append_question_row:1751](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/insightboard.py:1751) 通过已存在的 `Q[DIKW]` 行定位 grid，空 grid 会报错。第 1783–1796 行写旧式日期句子，canonical log 不存在时退回 Page `## Log`，没有 runtime id 或精确 control binding；直接 Ask POST 返回成功前也没有后续控制记录步骤。当前 [控制器:377](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:377) 和 [Run 合同:184](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/run-workflow.md:184) 要求 owner log 的可索引控制收据。

**影响。** 首个问题无法通过内置 writer 写入；直接 UI/CLI 注册完成后，也可能没有新 controller 合同可引用的 registration receipt。agent 外层可以另外补记，因此不能据此说所有 agent 注册都失败。

**拟修。** 按合法 header 定位空 grid。让直接 Ask 与 controller 使用同一注册操作，记录 runtime、actor、target、assertion/outcome 和精确 receipt 地址；必要时创建 canonical log。维护历史日志可读，不因新注册把旧日志改写为伪历史收据。

**验收。** 空 register 可直接新增 QD1；注册不分配 Run；一次成功注册有明确可索引收据；`requested_answer_targets: []` 的 registration-only 请求可在 `runs: []` 下完成。依赖 R04；涉及 retarget 的扩展依赖 R03。

### R07 · P2 · “有签名”被界面当成当前可交给 Design

**文件与证据。** [handoff_records:480](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/insightboard.py:480) 只凭 `_SIGNED` 的匹配设置 `signed` 和 `bindable`；[Delivery:1469](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/insightboard.py:1469) 把签名数量称为 “ready for design”。实际 consumer [live/design.py:164](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py:164) 据此返回 `status: bound`。但 [Wisdom:62](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-wisdom/SKILL.md:62) 要求完整 signed payload 和依赖仍当前，[Handoff:106](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-wisdom/SKILL.md:106) 还要求 GI6 receipt。

**影响。** 新 partition/verdict 导致 W held/stale 后，历史签名仍可保留；界面却继续显示 ready/bound，用户无法分辨历史签署与当前可消费状态。

**拟修。** 区分 signature presence 与 current eligibility，投影 owner 已记录的 payload/current-dependency/GI6 绑定。历史或缺少证明的记录显示 historical/unverified，并给出缺项；展示器不自行替 native owner 作新审查或签名。

**验收。** 保留旧签名但 held/stale/缺 GI6 时不显示 ready/bound；确切当前绑定才可显示 ready。**已确认的是跨族状态展示问题；本轮没有验证实际 Design Commission/Release gate 是否会放行，不能报告为已证实的执行权限绕过。**

### R08 · P2 · Data 的静态输入分支无法满足 GI2

**文件与证据。** [Data Input:45](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-data/SKILL.md:45) 接受 Supporting Result **或** governed page-local static source；同文件 [GI2:99](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/folder-kinds/haipipe-insight-data/SKILL.md:99) 却要求每个值都有 Supporting Result，[控制器:287](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:287) 重复这个无条件要求。[Page Evidence:187](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-evidence/SKILL.md:187) 明确允许充分的 governed local material 使用零 Supporting Runs。

**影响。** 合法静态源虽经真正的 local Evidence Run 接受，仍无法按字面通过 GI2，容易逼出不必要的伪 Supporting Run。

**拟修。** GI2 明确两条来源分支：跨 Folder 必须 Supporting Result；充分的 governed page-local source 可零 supports。两者都需要冻结输入、精确 hash、typed local Result 和 Page acceptance。

**验收。** 静态本地观察例子以零 Supporting Runs 和一个实际 local Evidence Run 闭合；跨 Folder 输入仍不得借此绕开生产者 Result。

### R09 · P2 · Definition 与 Runtime 示例无法属于同一次执行

**文件与证据。** [run-workflow.md:88](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/run-workflow.md:88) 的 definition 只声明 `write.BI01.P01`，依赖 reused Evidence。第 116 行明确说它在下方 runtime 中索引；第 135 行引用 `definition-v001.yaml`，但第 142、160 行只列未声明的 `evidence.BI01.E01`，并设为 managed；缺少所选 Writing Run 和 reused dependency 的对应 inventory。

**影响。** 即使把所有占位符换成真实路径，照抄示例仍不能满足 Spec→Run 绑定，可能多分配一次 Evidence Run。YAML 可解析并不代表两个记录契约一致。

**拟修。** 采用一个连贯场景：已接受 Evidence 以 reused 记录，已有 Writing 以 managed/resume 记录；为两者明确 declaration/external-dependency 来源和 frontier。或把两个场景明确分开并各自提供完整 definition。

**验收。** 每个 managed Run/frontier Spec 都能在 pinned definition 中解析；支持依赖的 exact version/hash 和复用身份完整；没有额外分配或漏掉所选 Writing Run。

### R10 · P2 · 分区说明仍教旧 Task 配置与输出路由

**文件与证据。** [partition.md:33](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/ref/partition.md:33) 的当前 grammar 要求 `tasks/<group>/_thresholds.yaml`、`configs/<partition>.yaml`，并说手动 rerun 采用配置内 `store:`、dispatching probe 用 `RESULT_STORE` 覆盖。当前 [Task:123](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/SKILL.md:123) 使用 `scripts/config/<run>.yaml`；[Output root:153](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/SKILL.md:153) 的顺序是 consumer `RESULT_STORE` → Job `src/config-defaults.yaml` 的 store → Job 本身。Insight 已把 Probe 定为只读历史。旧 Task 布局还被 [_task_calls:1099](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/insightboard.py:1099) 的 `*/*/configs/*.yaml` 枚举沿用。

**影响。** 新项目按分区说明创建配置时可能走错 owner path 或误判输出位置；Board 的 Task-home 视图可能漏掉现行布局的调用。不能由此推断 aggregate Run inventory 也失效，它有独立 runtime reader。

**拟修。** 保留共享阈值和“同一方法、不同分区参数”的规则；物理路径、参数和 store 解析交还当前 Task/producer owner。旧路径和 Probe 行为移入明确的历史说明；Task-home 枚举使用当前 owner records/resolver。

**验收。** 一个当前 Job/Task layout 的分区调用能找到配置、Ticket、Result/receipt；显式 consumer store 和 Job 默认 store 均按 owner 合同解析。旧路径只作兼容读取，不能成为新 scaffold 模板。需要 Task owner 协调，未审计真实 launcher。

### R11 · P3 · 主入口和控制器的操作路径仍被重复规则及历史案例拉长

**文件与证据。** 入口 359 行、控制器 476 行，路由/执行/owner 边界在两者和 Run reference 重复；[控制器:88](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:88) 到 214 行的大段分区测试和 A00 历史案例位于 dispatch 之前。第 401 行声称“不含 SMS 或 domain”，但同文件第 99、118、139、408 行使用具体 domain/实例。[入口:259](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:259) 简写每个 Run 都要人释放，随后第 274–277、328–331 行才细分新计算、既有授权和 native Page gates。

**影响。** 执行者需要先读大量术语与历史再确定下一步；简写容易引起额外询问，规则修改也容易漏改副本。后文细则可以消除歧义，因此不把这些简写重复列为独立 P1/P2 权限缺陷。

**拟修。** 入口保留 scope 路由、下一 owner、返回物；Run reference 保留唯一执行合同；分区测试和历史案例移到有明确触发条件的 reference。统一简短术语表，并在 Run 行上直接显示适用授权和既有 receipt。保留六个 owner 的统一章节骨架和证据/签名边界。

**验收。** 新上下文 agent 对“复用证据续写”“只注册问题”“新增分区”三种请求能直接给出 owner、实际 Run 数、下一动作及确实缺少的决定；不重问已有明确授权，不要求新用户先理解整套历史案例。

## 5. 修复顺序、依赖与责任

此处列的是实施批次，不是领域 Phase，也不会为批次创建 Run。

| 顺序 | 修复范围 | 依赖 | 主要 owner / 协调方 | 完成标准 |
|---|---|---|---|---|
| 0 | 保留已经批准并完成的改动；确认当前 diff 与其他任务归属 | 无 | 本任务与并行 Task/Board/Run 维护者 | 不重做 O01–O08，不覆盖其他族的未提交工作 |
| 1 | R01：producer / consumer RI 协议 | 共享 Run identity 合同 | Task Insight + Task + Run | 计算复用和新计算均得到准确 native inventory |
| 2 | R02：分配与最终 input 冻结分开 | R01；版本兼容方案 | Task Insight 脚本及 refs | 支持证据可在冻结前补齐；已冻结历史不变 |
| 3 | R05 → R04：共享解析器，再统一 checker / writer / cache | Folder/Page 身份合同已存在 | Page + Folder + Board | 合法旧 YAML 可读；错误显式；错误身份不写入 |
| 4 | R03、R08、R09：retarget、GI2 分支、连贯示例 | R01 身份规则；其余可独立准备 | Insight controller / Question / Data + Page Evidence | 三组冲突各只有一个可执行解释，示例互相引用成立 |
| 5 | R06：Ask 空表与控制收据 | R04；共享 control receipt；retarget 扩展依赖 R03 | Board Ask + Question controller | 首问可注册；零 Run 控制请求按自己的结果关闭 |
| 6 | R07：签名与当前 Design eligibility 分开展示 | 精确 payload / GI6 记录解析，历史缺证策略 | Insight/Wisdom + Board + Design consumer | 不把历史签名显示为当前可用，不新增机器签名权 |
| 7 | R10：Task 分区路径和 Task-home 投影 | 当前 Task resolver；R01 的 producer refs | Insight + Task + Board | 当前布局可解析，旧布局明确为兼容 |
| 8 | R11：减少重复并走查整条路径 | 语义及接口已稳定 | Insight 文档 owner | 新上下文可按目标选 native Runs，不出现 Phase 或额外包装 Run |

R03、R08 和 R09 的文档准备可与共享解析器工作并行；写同一文件时仍应串行合并。跨族修复应由对应 owner 接管或明确协调，不能由 Insight 私自再定义一份 Task/Run/Design schema。

## 6. 总体验收：Workflow 必须可还原为实际 Runs 清单

下一次实施需逐项保留可审查的结果，而不是仅检查字符串是否包含 Phase。

| 场景 | 必须满足的结果 |
|---|---|
| 仅注册一个问题 | `requested_answer_targets: []`，`runs: []`，正确 neutral row/open cells + registration control receipt；无需回答问题或 GI6 才关闭 |
| 已有 accepted 计算和 local Evidence，续接 Writing | 复用依赖不重跑；只续接匹配的 native Writing Run；允许零新分配 Run；Step 不另计 |
| 缺失计算后进行 DIKW | 独立 producer native Run、必要 local Evidence Run、RI 各有自己的目标和 Ticket/Result/receipt；recipe、controller、checkpoint 不计 Run |
| 一个生产结果供多 cell 使用 | aggregate inventory 只计同一个 full native id 一次，明确多个 consumers |
| 先绑定 RI、后得到支持证据 | dataset/base/question 绑定保持不变；最终 interpretation envelope 在证据就绪后冻结；旧 frozen bytes 不改 |
| 没有 Supporting Runs 的静态 Data | governed local source + 实际 typed local Evidence Result 可按 GI2 关闭；跨 Folder 不得冒充静态本地来源 |
| QI 问题升级为 QK | successor / 历史关系清晰，只有一个当前 answering target，旧引用可追溯 |
| 增加一个分区 | 保留无关 D/I/K；更新 X 与全部受 verdict 影响的 W；signed payload 变化需新的人签名；历史签名不显示 ready |
| canonical / legacy 身份 | 两种合法缩进可读；重复/无效记录可见报错；canonical 无效不 fallback；错误身份 Ask 不写文件 |
| held / complete | 必需输入或人决定缺失时 held；请求的 answer/control outcomes、required work、final acceptance 都满足且 frontier 为空才 complete |
| 定义与 Runtime 对照 | 每个 managed Run 及 frontier Spec 能回到冻结 definition；reused Result 具备精确地址/hash；无 I#、CELL、GI 或 Page pass 伪装成 Run |

实施后的检查范围建议包括：对应回归测试、完整示例的语义关联检查、相关 Folder/技能校验，以及根 README 要求的新上下文技能走查。只检查 YAML 能解析或旧测试通过不足以覆盖上述语义。真实 Board 和外部安装的迁移应使用单独的明确目标与记录，不在报告工作中顺带执行。

## 7. 共享问题、剩余不确定性与未列为缺陷的项目

### 需要跨族跟踪

- **Page adapter API：** [Page Workflow:57](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md:57) 的 `phase/cycle/next_cycle` 已标为低层兼容字段，不是 Insight 的领域对象或 Run。彻底改名需要 Page 引擎及调用者一起迁移；不应只在 Insight 做字符串替换。
- **其他族的 live Phase 用法：** [Task:123](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/SKILL.md:123) 仍写 `Four phases`；[Discovery owner:27](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/workflow-phases/haipipe-discovery-inquiry/SKILL.md:27) 仍声明 Folder phase。它们会被支持性工作加载，应由 Task/Discovery 的族审阅协调处理。本报告没有将 Insight 已完成的迁移冒称全仓迁移，也没有越界修改它们。
- **既有 Discovery 校验 finding：** 该 owner 的 `workflow` 字段第 12 行仍为 `haipipe-discovery-inquiry`，与共享 checker 的 `*-workflow` 命名要求不符。上一轮已确认是修改前问题；本轮未重跑。应由 Discovery/Folder owner 决定正确 owner 名称，不能为使 Insight 总检查变绿而放宽规则。
- **外部安装链接：** 六个技能迁目录后，指向旧物理路径的安装链接可能需刷新。迁移文档已说明；本轮未盘点或重新安装外部环境，不报告其成功或失败。

### 证据边界

- R01–R11 以当前文档和代码静态路径为依据；未使用真实数据验证科学结论、并发 writer、项目 adapter 或浏览器端完整交互。
- 原 117 项测试结果是已完成修复的历史证据，不是本轮新增场景的执行记录。仓库还有其他任务的未提交变更；本轮没有替它们背书。
- aggregate Runtime reader 已支持零 Run 控制记录、重复/缺失身份的可见错误、runtime 文件新增/修改/删除后的刷新。它不替 native owner 重跑验证，这个角色限制本身不列为缺陷。
- Question 通用 Run Profile 的宽泛措辞受同文件 Plugins 限制；Wisdom 的签名规则在同文件 Task Face 与 controller 有明确 POOL deferral 例外。可在 R11 整理，但不将可由明确局部规则消解的简写夸大为新的阻断问题。
- 历史 CHANGELOG、评估快照、legacy 路径、只读迁移 token 不等同于现行 Phase authority；保留它们可追溯性是必要的。

本次交付是可执行的修复计划。下一次源码实施应以本报告确认的问题和对应验收场景为范围，继续使用已经建立的 native Run 模型。

## 8. 批准修复后的实施记录 · 2026-09-20

### 8.1 修复对照

| 问题 | 已落实修改 | 验证 |
|---|---|---|
| R01 | 先独立分配/续接 RI，再决定复用或新建 producer；新 recipe packet 分开 producer 与 consumer execution，绑定 producer Ticket 和完成 receipt 的哈希 | 新建与复用 support、身份混用拒绝、缺失/未完成 receipt 拒绝；独立临时双数据集执行 |
| R02 | `bind` 只冻结不可变 `binding.yaml` 并留下 planned receipt；新增 `freeze --item … --version … --evidence …` 在证据就绪后封存 input | 先分配后补证据、冻结拒绝覆盖、v002 保留 v001、旧空 input 的显式新版本迁移；按显式 evidence contract 保留旧 audit 方言 |
| R03 | 目标 rung 变化创建目的 register 的 successor id，双向 `supersedes` / `superseded-by`；旧 id/引用/settlement 留存，旧 open cells 有明确退休理由 | Question、Question Group、Page adapter 规则对齐；独立 QI→QK 草稿走查 |
| R04 | checker、Ask、Page、Context 共享身份解析；错误有明确 finding，Ask 拒绝错误身份；缓存观察 canonical/legacy 身份的新增、修改、删除 | 解析冲突、写入前拒绝、checker finding、缓存刷新回归 |
| R05 | 严格 YAML 读取 `current.folder-kind`；支持正常两/四空格及引号，拒绝重复映射、坏引号、非直接 current 字段；canonical 错误不 fallback | 共享解析器与 Page/Context/Board 消费者测试 |
| R06 | 空 regular Queue 可登记首问；写 canonical Outline log 和零 Run control-only Runtime；可索引既有明确声明该 control 的 Runtime；登记写入串行锁 | 首问 QD1、零 Runs/零 answer targets、actor/receipt、既有 Runtime 保持 held、未声明控制拒绝和锁冲突 |
| R07 | `workflow/handoff.yaml` 仅索引真实 GI5/GI6 owner receipts；校验 Page/dependency 哈希、签名、QW/partition 和当前 Queue cell。历史签名保留但不能独自成为 Design bound | 正向 exact binding、held Page、源文件变化、缺失 GI6、Queue 重开、日志追加稳定及重复 anchor 拒绝；Design consumer 集成 |
| R08 | Data 与 GI2 明确 governed static local source 分支：零 Supporting Runs，但仍需 frozen Local Input 和经过相应验证的 typed local Evidence Result | 文档一致性与独立静态 codebook 场景走查 |
| R09 | 示例统一为一个 managed/resumed Writing Spec + 一个 reused Evidence dependency，frontier 指向同一 Writing Spec | 可执行语义测试核对 Spec/owner/type/target/input/hash/dependency/frontier 对应关系 |
| R10 | 分区路径改为 `tasks/<block>/<job>/<task>/scripts/config`；输出绑定读取 Job defaults 及 native Ticket/receipt 的有效路径；保留旧布局只读发现 | 现代布局、Job store、忽略 stale config-local store、显式 native output override 与去重 |
| R11 | 入口增加简明术语表；controller 把 dispatch 前置；分区政策、Task RF bridge、资源布局和 handoff schema 按场景加载 | 入口从 359 行缩至 279 行，controller 从 476 行缩至 264 行；独立新上下文行为走查 |

空表测试同时暴露并修复了旧 Page 状态覆盖 Queue open cell 的推断。回答 Page 可以提供证据，但不能自行把 register cell 投影成已结算。

主要入口：

- [Insight 入口](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md)
- [Run definition/runtime 与登记控制](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/run-workflow.md)
- [Task producer/RI 与最终冻结流程](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/task-calls.md)
- [当前 handoff 证据与 GI5/GI6 格式](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/handoff-record.md)
- [Insight 迁移说明](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/migration.md)
- [Task Insight 迁移说明](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/migration.md)

### 8.2 实际执行的自动化验证

**185 项相关测试通过：**

- Task `test_insight_items.py`：36 项。
- Board/Page 定向套件：107 项，包含 `test_folder_contract.py`、`test_context_record_base.py`、`test_page_phase_ledger.py`、`test_insight_page_v2.py`、`test_insight_family.py`、`test_insight_board_plugin.py`、`test_plan_shape.py`、`test_insight_items_integration.py`、新增 `test_insight_definition_example.py`。
- Design presenter/action 集成 `test_design_plugin.py`：42 项。测试 fixture 使用明确标为 synthetic 的 owner receipts 和 register cells。

Task 和 Board/Page 套件使用系统 Python 3.9；现有 Design 测试使用 `list | None` 类型语法，改用本机 Python 3.13 并通过 `PYTHONPATH` 读取已安装的 PyYAML 后通过。未安装依赖或更改环境配置。

**结构及文档检查：** 9 个相关技能通过 `quick_validate.py`；6 个 Insight Folder contracts、0 findings；17 个当前 Markdown 相对链接均可解析；相关 tracked diff 的 whitespace 检查通过。可解析 YAML 之外，R09 有独立的语义关系测试。

**全局检查的既有异常：** 全族 `foldercontracts.py --check` 仍为 7 contracts / 1 finding：Discovery 的 `workflow: haipipe-discovery-inquiry` 不满足现有 `*-workflow` 名称约束。该问题在本轮前已记录，本轮未修改 Discovery 或放宽 checker。

### 8.3 验证范围

测试使用临时合成数据与文件，部分既有测试只读检查存在的样例 Board；真实业务 Board、生产数据、真实 launcher 和外部安装均未修改。本次不声称完成浏览器端完整交互或真实科学结论验证。历史输入、Results、签名和既有未提交工作保留。

handoff viewer 验证被记录的 pin 和 owner assertions；它不证明人身份、科学正确性或依赖列表的完备性。后者仍由对应 owner CHECK 负责。缺少当前记录的旧 signed Page 显示为历史/unverified，需在下一次授权使用时从真实证据补齐记录。

### 8.4 独立验证发现后的补修

根 README 要求的新上下文验证实际运行了 Task bind/freeze/check/table，并产生两项补修：

1. 原先只在新 recipe call 分支验证完成 receipt，复用 native support 且 `recipe_calls: []` 时仍可遗漏收据。现在每个新 support binding 都要求 `ticket` / `ticket_sha256` / `receipt` / `receipt_sha256`，并验证 receipt 的同一完整身份及 terminal status；缺失或 running receipt 拒绝冻结。
2. 直接用 `binding_sha256` 推断新证据校验规则，会追溯影响早先冻结的输入。现在新 freeze 写明 `evidence_contract: haipipe.insight-evidence/v1`；没有该 marker 的旧 frozen input 继续按其原方言只读检查；未知 marker 明确报错。新版本承担新规则，旧 bytes 不改。

这两项各新增了回归测试，已计入上述 36 项 Task / 总计 185 项。独立场景还校正了 Data 的泛化 “run-bound” 描述，以及迁移文字中把签名要求误读为当前可绑定状态的措辞。


独立复测最终通过：历史 A `2 items; 3 executions; 0 findings`；历史 B、此前复用实例及新 marker 实例均为 `1 items; 1 executions; 0 findings`。缺失/运行中的 producer receipt 拒绝且未创建 input；完成的复用结果可冻结；所有旧 frozen YAML 和 producer 文件哈希不变。Question successor、静态 codebook GI2、handoff 与三类 Board 路由草稿也完成。

[保存的独立验证记录与最终路由笔记](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/insight-fix-forward-validation.md)。原始 CLI 输出位于隔离目录 [最终复测命令记录](/tmp/insight-forward-kmDMy9/post-contract-marker/command-transcript.md)。独立执行没有发布 DIKW/RF，也没有代替人签名或科学 review。
