**Run 家族：问题复核与修复计划**

本稿依据当前工作树重新核查原 [Run 评估报告](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/run.md)，用于列出问题和规划修复。本次只新增这份报告。本会话没有另外获批、正在实施的 Skill 修复任务。

Run 的独立目标、Ticket/Result 配对、失败收据和 Step 边界值得保留。当前最需要处理的是：Workflow 的 Run 列表定义、Task 模板与 Schema 的冲突、Page/Paper 的活动 Phase 术语，以及互相矛盾的 Page/Design 方言说明。Insight 已有明显迁移，原报告不能原样沿用。

**复核快照与覆盖**

- 日期：2026-09-20；首次源文件指纹快照为 21:08 UTC，结束复核为 21:18 UTC。比对的 25 个关键来源文件在此窗口内均未再次变化。HEAD 仍是 `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。
- 当前 Run 家族仍只有 **1 个 Skill，覆盖 1/1**。重新通读 [SKILL.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md) 的 689 行、[CHANGELOG.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/CHANGELOG.md) 的 60 行及 [agents/openai.yaml](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/agents/openai.yaml) 的 4 行。目录中没有其他 Skill、脚本或模板。
- Run 主文件没有工作树差异，SHA-256 为 `199a496d49648a83da27e4711393ea7e1eadd73720a0506019e24e0d4747622c`。工作树另有大量既存改动，包括 Insight 目录迁移、Page 与 Task-side Insight 文档修改、Board 适配以及其他家族修改；它们均被保留。
- 复核了原问题涉及的 Task 计划/报告模板及 Workflow Schema、Page glossary/入口/Workflow/交互方言、Paper Workflow/入口/插件/命名、Insight Workflow/迁移/Task 桥接、Design Workflow/Profile。核对了 Run 主文中的显式引用路径。跨家族检查是针对共享合约的追踪，不声称重新完整审计了所有消费者家族。
- 本次依据是文件内容、工作树差异和静态路径核对。未运行被评估的 Skill、业务流水线、外部服务或实现测试；交互影响是文档推演，未声称观察到真实用户失败。

**原报告哪些判断仍成立**

| 原报告问题 | 当前结论 | 本稿处理 |
|---|---|---|
| Workflow 被定义为 Run Spec 图 | 需收窄。缺少明确的 Run 列表主定义仍成立；图与列表本身可以共存，不能据此要求删除图或废除 Spec | F01：保留路由图，明确列表、计划项和实例之间的关系 |
| Task 仍用 Phases → Steps 模板 | 仍成立，且模板直接声称遵循不允许 `phases:` 的 Schema | F02 |
| Page glossary/公开入口仍用 Phase | 仍成立。`workflow/folder.yaml` 已替换部分资源身份路径，但没有改掉重复 authority 的 Phase 定义 | F03 |
| Paper/Insight 仍用 Phase，Insight 挂在 Application 下 | Paper 仍成立；Insight 主要迁移已出现在当前工作树，父层断言不能继续沿用 | F04、F08 |
| Paper 与 Run 的 RP 身份语法冲突 | 仍成立；同时发现 Run 的“穷举”说明遗漏当前 Scratch 方言 | F05 |
| Insight 路径错误，简介缺少家族 | 路径问题可复现；简介遗漏是发现性/可读性问题，不能声称已经导致路由失败 | F06、F11 |
| 主 Run 仍列出 Design Adopt | 仍成立；当前 Design 明文禁止新建该 Run | F07 |
| “only this contract and its UI metadata” 是范围承诺违约 | **撤回作为独立缺陷的判断。** 该句位于 Files，合理解释是目录文件组成，实际目录与它相符 | 重复方言导致漂移的维护风险纳入 F11，以 F05/F07 的实际冲突为证 |
| 入口概念密集、缺少短例 | 仍可作为编辑改进，未做用户测试 | F11，P3 |

另作两项原报告订正：其 Task 改写示例标作“原文”的整句不是源码逐字引文，准确现行文字是 `stage-plan.md:39` 的 `P: Phases → Steps ...`；直接把 Page 的 `[from <phase>]` 换成 `[from <run-id>]` 也缺少解析器支持的证据，本计划不把该接口变化当作已经确定的修复方式。

**逐项问题与拟修复办法**

优先级含义：P1 为会生成冲突记录、错误身份或直接违反指定模型的事项；P2 为契约歧义、过期方言和容易造成错误判断的说明；P3 为阅读与维护改进。以下“验收”均指未来实施后的标准，不代表本次已经完成。

**F01 · P1：Workflow 缺少“Run 列表”的首要定义与两种列表视图约定。共享问题：Run / Task Workflow / Page / Paper / Insight / Design。**

证据：[Run 的 Workflow Definition](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:193) 写 `Workflow Definition = bounded Run Spec nodes + graph entry/terminal rules`，226 行要求发布 Run Spec graph，252 行称 `The graph is the Workflow authority`。同时 [Task plan Schema](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-workflow/ref/plan-schema.md:19) 已经使用 `run_specs` 列表，[Report Schema](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-workflow/ref/plan-schema.md:69) 也有实际 `runs` 列表。

影响：读者必须自行推断“Workflow 是 Run 列表”如何对应计划与执行。Spec 模板、可变 cardinality 和多个实际 Run 容易在展示中混在一起。**已有列表 Schema 是反证：不能说系统完全没有列表，也不能说任何图都违反要求。** 问题是首要定义、图的角色和两个视图未对齐用户的指定模型。

拟修复：在主定义、ownership 表、Workflow 表格说明及消费者摘要中使用同一短句；保留 `run_specs` 与运行时 `runs`，明确 Spec 是计划表示、实例是实际工作记录。Route/dependency graph 是列表项之间的执行关系，允许分支、并发、HOLD 与返回；列表不意味着强制串行，也不预分配所有未来 ID。

```text
A Workflow is a list of Runs. Its definition describes planned Run work as
Run Specs; its execution lists the allocated Run Instances. Routes and
dependencies describe relationships among that work. Run Types supply
reusable defaults, and Steps remain inside their owning Run.
```

验收：所有共享定义明确写出该模型；一个 Spec materialize 两个实例时，运行清单显示两个不同 Run ID、Result 和 receipt，定义清单仍能保留一个参数化 Spec；图节点可以追溯到计划项，实际 Run 不因图或展示投影重复计数。此项是规范表达对齐，尚无证据证明现有运行器因图结构本身出错。

**F02 · P1：Task 的新计划与报告模板违反它自己引用的 Schema。共享问题，实施 owner：Task。**

证据：[workflow-template.yaml](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/workflow-template.yaml:29) 定义 `phases:`，将 Run、Gate1、Gate2 放在该列表内；[stage-plan](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/fn/stage-plan.md:36) 声称两个计划层使用同一 Schema，却要求 `P: Phases → Steps`，99–113 行要求按 Phase 分组并禁止 `id` 等字段。[stage-report](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/fn/stage-report.md:137) 要求 `same phases (Run, Gate1, Gate2)`，148、189、220 行继续输出 `phases`/`phases_completed`。现行 [plan-schema](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-workflow/ref/plan-schema.md:126) 明确规定 `run_specs` 是唯一 Workflow 行清单，禁止 `phases:`。

影响：从当前入口复制模板即可写出不符合其规范的文件；一个新 agent 无法同时满足两套要求。用户看到的“完成几个 phase”也无法对应真实 Run 与收据。这里的矛盾由静态文本即可确认，不依赖运行测试。

拟修复：一起更新模板、stage-plan、stage-report 及它们直接指向的当前示例。先判断执行、代码审查、结果审查是否独立受委托并可关闭：符合者列成 Run Spec，否则保留为所属 Run 的 Gate/Step。脚本 cells 不因改名而各自获取 Run ID。报告输出实际 Run ID、Spec 引用、状态、Result 和 receipt；计划 cardinality 与实际计数分开。

验收：Task 入口生成的最小计划能满足现行 Schema 的字段要求；报告逐个连接实际 Run 与其 Spec/receipt；新模板不产生概念性的 `phases:`；计划/构建/执行/报告四个管理命令不自动变成四个业务 Run。

**F03 · P1：Page 仍有活动的 Phase 权限模型和面向人的 Phase 入口。共享问题，实施 owner：Page。**

证据：[glossary 时间词汇](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/ref/glossary.md:174) 仍写 `workflow — which LOOP this is. Never repeats`、`phase — which AUTHORITY is acting ... REPEATS`；123–124 行把 receipt 称为 `one phase pass`。[Page Skill](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/SKILL.md:581) 仍说 page chat `knows the phases`，689 行公开 `[from <phase>]`，881–882 行要求加载 `current Page Phase contract`。但 [Page Workflow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md:57) 又限定 `phase/cycle/next_cycle` 只是 controller dispatch/progress 字段。

影响：同一套说明既把 Phase 当权限主体，又说它没有语义权威。用户选择工作的方式仍建立在旧单元上；agent 可能把 controller pass、Run、Step 或 receipt 混为一谈。当前工作树把部分 `workflow/phase.yaml` 改为 `workflow/folder.yaml`，修复的是资源身份路径，不能据此宣布本项关闭。

拟修复：由 Page owner 明确 CONTEXT、OUTLINE、EVIDENCE、CONTENT、CHECK 分别如何参与已有 Run 的工作与关闭；它们不满足 Run 条件时称为控制操作、Step 或 Gate。glossary、工作清单、chat 说明和命令帮助同步使用 Run 列表。明确命令 `from` 的实际语义：若它仍接受控制操作名，可公开称 `<operation>`；若要支持 Run ID，须连同解析和调度映射一起设计、验证。

验收：人看到的 Workflow 单位是 Run；内部操作不会被额外计数；同一段反馈继续落在原 RP 的 Step。兼容 `phase` 字段在专门的适配说明中有明确含义，不再被 glossary 定义为另一个 authority 层。**不确定项：本次没有核查解析器是否支持 Run ID，因此不承诺只改参数文字即可实现新入口。**

**F04 · P2：Paper 的 journey、Page 操作和 Workflow 工作清单仍混用 Phase 术语。共享问题，实施 owner：Paper，依赖 Page。**

证据：[Paper Workflow 的 Two meanings of workflow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-workflow/SKILL.md:21) 明文定义 `journey phase` 和 `Page phase`，并列 P0–P4 与 CONTEXT–CHECK。[Paper 入口](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/SKILL.md:227) 在 ideate/story/venue/section 中暴露 `[phase]`，240 行解释它是 Page phase。[Paper Plugin 的 Workflow grammar](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-workbench-paper/SKILL.md:370) 把 Workflow 解释为记录如何移动，展示的是计划 Run Types/Specs。

影响：读者看到旅程位置、控制操作、计划种类和实际执行四种东西，却没有首先得到一个一致的 Workflow Run 清单。不过 P0–P4 作为领域导航图可以保留，Run Type 目录也可以存在；原报告不应仅凭其存在判为错误。

拟修复：把旅程图明确为 Paper 导航/依赖视图，并另行指向实际 Workflow Runs。公开 selector 与 Page F03 一起对齐。计划类型表明确标注模板/计划语义，实际执行视图列出 owner-native Run ID 与 receipt。Compile 已被定义为 projection 时继续保持该边界，不因旧称 Phase 或名称含 run 而新造一个 Run。

验收：从一个 Section 请求能够辨认正在进行的 Page/Supporting Runs、下一项受阻的工作和用户需做的决定；P0–P4、Compile、聊天反馈不自动增加 Run 数；活动帮助文字不再把 Workflow 单位称为 Phase。历史文件名是否保留由 loader/兼容需求决定，不做无依据的目录批量重命名。

**F05 · P1：Page Run 的身份规则存在三处可直接相撞的现行说明。共享问题：Run / Page / Paper。**

证据：[Run Page 投影与命名](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:133) 及 162–173、316–320 行使用 `rp-struct-*`、`rp-sec-*`、`rp-para-*_Pxx`。[Paper 当前命名权威](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/ref/run-naming.md:77) 却要求从 `rp00_mermaid-structure` 开始，再使用 `rpNN_pNN`。当前 [Page 交互方言](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:34) 还列出第四类 `rp-scratch-NN_<target>`，而 Run 主文 406–407 行说 `These two forms are exhaustive`，并判定其他 interactive-writing 名称无效。此外，Run 313 行的全局 lowercase 规则与其自身 309–310 行大写 `P01` 示例不一致。

影响：同一有效目标从不同家族入口进入会得到不同 ID；Scratch 可能按 Page 方言创建后，又被主 Run 的穷举规则否决。大小写规则还会误导 agent 改写具有固定语法的段落地址。文本冲突已确认，实际校验器是否遵循哪一份规则本次未测试。

拟修复：Page 交互方言维护唯一完整语法，Run 与 Paper 仅摘要并引用它。同步当前四类 RP；删去失真的“两种穷举”表述。将 lowercase 规则限定在普通 slug，保留方言规定的 `Pxx` 地址大小写。旧 `rp00/rpNN` 的识别/拒绝/只读规则由 Page owner 明确，不自动重命名既有记录。

验收：Structure、Scratch、Section、Paragraph 四类样例在所有相关规范中得到一致判定；首次 Structure 是 `rp-struct-01`；新工作不再从 Paper 指令生成旧 RP；既有历史身份保持可追溯；P01 不被降为 p01；Step/Version 不消耗 RP 计数器。

**F06 · P2：Insight 实例契约的两个引用不能从 Run Skill 直接解析。Run 家族内可独立修复。**

证据：[Insight instance dialect](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:419) 给出 `task/page-types/haipipe-page-insight/ref/instance-items.md`，445 行只说 `ref/task-calls.md`。按该 Skill 所在目录解析，两个路径都不存在；现存目标分别是 [instance-items.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/instance-items.md) 和 [task-calls.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/task-calls.md)。其他本轮核对的显式 `../../...` 方言引用均能定位。

影响：新上下文 agent 为 RI 冻结输入或绑定共享 Task 配方时需要猜目录，容易跳过当前版本 Schema。第二个短引用可以被人理解为“Insight 参考目录”，因此应称为欠限定引用；第一个则是明确的相对路径缺项。

拟修复：分别写为 `../../task/page-types/haipipe-page-insight/ref/instance-items.md` 与 `../../task/page-types/haipipe-page-insight/ref/task-calls.md`，并用可点击相对链接。保留 Task-side RI 方言身份，不因为 Insight 已独立成家族就无依据搬移仍在使用的 Task 桥接文件。

验收：从 Run Skill 目录解析全部显式文档链接均存在；读者无需搜索就能到达 RI Schema 和配方调用规则；同一个冻结数据绑定的 retry 与新数据集的新 RI 仍按现有合同区分。

**F07 · P2：Run 的 Design 摘要过期，Design 自己的 Run 表又混入 Delivery 投影。共享问题：Run / Design。**

证据：[Run 家族分类](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:270) 仍列 `one Adopt decision`，286–288 行称当前 Profile 拥有 commission/generate/verify/adopt gates。[当前 Design Profile](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/references/run-profile.md:3) 只允许 commission/generate/verify，[Design Workflow 的历史边界](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:180) 明文规定旧 `rdNN_adopt_*` 仅作 legacy Delivery evidence，新 writer 不得创建。另一个表述矛盾在同文件 48–59 行：先称每行都是独立闭合的 Run Spec，再把 `delivery | Delivery projection | none` 放入 Run Specs 表；[Design owner](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design/SKILL.md:163) 又明确说 `Delivery is not a Run`。

影响：从通用 Run 契约进入会多委托一个已退休 Run；从表格复制则可能给只读 Delivery 创建伪 Spec 或 Run ID。这与允许保留 Delivery 作为路由终点并不矛盾，问题是表的行语义没有一致。

拟修复：把 Run 的 Design 摘要同步到三种现行 Run Type；将 Delivery 路由终点/投影从 Run Specs 清单移到单独说明，或明确表是组合视图且该行不属于 Run roster。保留“Verify pass 后就可 Delivery”的现行行为，修复不新增人工 Adopt 门槛。

验收：一个 Commission、一个 Generate、一个 Verify 的实例清单恰好是三个 Runs；Delivery 有来源/hash/verification 引用却无额外 Run ID；新样例不创建 `rdNN_adopt_*`；历史 Adopt 仍仅按 owner 声明的例外读取。

**F08 · P2，残留歧义：Insight 原来的 Phase/父家族问题已大幅修正，Task 桥接仍称“Application Run workflow”。共享问题，实施 owner：Insight / Task 桥接。**

现状证据：[Insight 主入口](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:41) 已明确 `not nested under an Application parent`，并把 `application` route token 标为 legacy scope selector。[Insight Workflow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:44) 明确没有 Phase 对象，Meta/Question/D/I/K/W 是 Folder kinds；原六个 `workflow-phases/` Skill 已在当前树迁到 `folder-kinds/`，metadata 使用 `folder_kind`。[迁移说明](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/migration.md:27) 规定新写 `workflow/folder.yaml`、不新写 `metadata.phase`。这些是当前可见的既存修改，不是本会话实施的成果。

剩余证据：[Task-side workflow-table](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/ref/workflow-table.md:4) 仍写 `haipipe-insight-workflow continues to own the Application Run workflow`；同文件原 Phase × Run 表已改为 Activities/checkpoints，并在 27–28 行明确活动行不分配 Run。

影响与不确定性：现行主入口已经否定 Application 父层，所以不能继续断言“Insight 当前仍挂在 Application 下”。桥接短句会让不了解迁移的人误读，但它也可能只是领域应用的简称；这是命名歧义，不能单靠 `Application` 字样推定家族所有权错误。`Application audience/context` 等产品领域用语不是本项清理目标。

拟修复：把桥接处明确写为 `InsightBoard Run workflow`，连到独立 Insight owner；沿用当前迁移工作，检查桥接引用的一致性。Insight 与 Design 保持两个一等家族；旧 `application` selector 的兼容角色单独说明。

验收：当前 owner、桥接和默认入口均无 Application 父 Skill 歧义；新写路径遵守现行 `folder-kinds`/`workflow/folder.yaml`；历史别名只做兼容。迁移的实现与回归测试未在本次复跑，因此这里只确认文档变化，不能宣布整条迁移运行验证通过。

**F09 · P2，复核补充：Run、attempt 与 Version 的开头定义容易使人错误分配身份。Run 主合同问题。**

证据：[主标题和首句](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:19) 是 `one attempt` / `A Run is one ... attempt`；但 52–53 行给 Run Instance 分配 append-only attempt history，[359–361 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:359) 又明确同一 Run 的 rerun 增加 attempt。236–237 行称 Version 为 immutable reopen episode，409–415 行则说明正在进行的 Version 是 append-only journal，关闭记录才不可改。

影响：只读开头的人可能认为每次失败重试或交互 episode 都要新 Run；读全文才知道“logical attempt”和记录中的 attempt 不是同一粒度。Version 的不同状态也需要读者自行补全。这是术语歧义，尚未观察到实际重复分配。

拟修复：用有界委托/固定契约定义 Run，说明它可含多个尝试；重试继续使用原 ID，material change 走新 Run。把 Version 写为“开放期间追加 journal，关闭后不可变；在适用方言内以新 Version 重开”。

```text
A Run is one durable, addressable commission for a bounded target and close
rule. It may contain several execution attempts. A retry under the same
frozen contract adds an attempt to the existing Run.
```

验收：初次失败后同契约 retry 得到一个 Run、两条 attempts；改变冻结数据/目标/验收时分配新 Run；普通 Page 反馈增加 Step，同目标重开增加 Version；已有关闭记录不被覆盖。若要保留“logical attempt”一词，必须与 attempt-history 的粒度明确定义，不能复用同词而无区分。

**F10 · P2，复核补充：未完成工作的时间字段规则与真实生命周期、Page 方言冲突。Run / Page 共享问题。**

证据：[Lifecycle](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:529) 在 SCAFFOLD 建立 planned receipt、之后才执行；[Runtime receipt](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:597) 却要求每个 newly allocated Run 的 `started_at` 和 `finished_at` 都是 RFC 3339，并允许 atomic scaffold 把两个字段设为同一时间。当前 [Page 交互契约](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:174) 明确 `unfinished/unknown timestamps are null`。

影响：照通用合同建 planned receipt 可能在工作未开始时就生成一个完成时间；照 Page 契约则留下 null。人查看持续时间或中断状态时会看到虚假的零耗时完成区间。它未必将 status 误改为 complete，但会让时间字段不能代表实际事件。

拟修复：把格式规则限定为“非空时间必须使用有偏移的 RFC 3339”。分配时可记录方言声明的 created/queued 时间；尚未开始/结束的字段留空。finished_at 只记录 owner 方言认可的真实终止事件，waiting-for-feedback 不算结束。即时完成工作可以同秒开始/结束，但 scaffold 本身不能证明完成。重开的 Version/attempt 时间继续留在其历史记录中。

验收：planned 未启动样例、running 样例、Page waiting 样例都没有虚假的 finished_at；终止样例有真实时间及 outcome；Page 与通用范例规则一致；因开始前校验失败而终止的记录可以保留 unknown/null started_at，同时如实记录终止原因与时间。

**F11 · P3：入口信息密集、家族摘要不完整，重复的方言摘要需要明确维护边界。Run 家族的阅读与维护改进。**

证据：[Skill description](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:3) 只点名 Execution/Discovery/Page/Labeling，正文 268–271 行已包含 Insight/Design；[UI 默认提示词](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/agents/openai.yaml:4) 一次列出 Definition/Execution/Type/Spec/Instance、Gates/Routes 等多个层次。主文 35–58 行早早介绍密集概念，完整 receipt 示例到 556 行才出现。F05/F07 展示了摘要与方言权威发生真实漂移的实例。

影响：新读者难以从一句请求判断要找哪个 owner、会生成几项 Run、何时需要人的决定。遗漏家族可能降低触发描述的完整性，但尚无 Skill 选择失败的观测。Files 段的“only this contract and its UI metadata”可以合理解释文件组成，本身不构成缺陷。

拟修复：在开头加入一个小型请求例，显示 Workflow Run 列表、内部 Steps、关闭规则及用户下一决定；description 点名独立 Insight/Design。默认提示词用“定义或审计一次有界工作”开头，内部字段由合同解释。正文保留共享不变量；方言摘要注明 owner 与规范链接，优先减少 ID/operation 完整枚举的多处复制。是否拆出新的 reference 文件是编辑选择，不是修复前提。

验收：新读者能用一个短例回答“目标是什么、哪个 Run、何时关闭、下一步由谁做”；各方言摘要与当前 owner 一致；不要求用户手填所有内部模型字段；不会因为加短例或完整家族名而声称已经完成用户体验验证。

**实施顺序、依赖与责任**

这是未来实施计划，不是本次新增的编辑授权。每个实施批次开始前重读目标文件和工作树差异，优先接续现有迁移，避免覆盖别的会话正在维护的来源。

| 顺序 / 批次 | 要做的改动 | 依赖 | 主要 owner / 验收门槛 |
|---|---|---|---|
| 1 · 固定共用定义 | F01 的 Run 列表与 Spec/Instance 关系；F09 的 attempt/Version 粒度；F10 的时间语义 | 当前 Run 主合同与方言 owner 的一致解释 | Run + Task Workflow；文本、计划/执行两个视图与最小 receipt 样例一致 |
| 2 · 修正直接错误 | F06 路径；F07 主 Run 中过期 Adopt；F05 中无效的穷举与大小写规则 | 当前 Page/Design Profile 已给出权威语法；路径修复本身不必等待批次 1 | Run；所有显式引用可定位，摘要不再否决当前合法方言或委托禁止类型 |
| 3 · 对齐 Task 计划链 | F02 模板、stage-plan、stage-report 及直接引用的当前示例 | 批次 1；保留现有 `run_specs`/运行时 `runs` 分工 | Task；计划和报告满足同一 Schema，脚本 Steps 与独立 Run 数量正确 |
| 4 · 对齐 Page/Paper 入口和身份 | F03、F04、F05；同步 Page glossary、命令帮助、Paper 命名及类型/实际 Run 视图 | 批次 1；Page owner 确定 controller selector 与实际 Run 选择的关系 | Page 主责、Paper 跟随；合法 RP 统一、原参数语义不被文档单方面改变、无伪 Run |
| 5 · 收口共享消费者 | F07 Design 表中 Delivery；F08 Insight/Task 桥接剩余称谓 | 批次 1；复用当前 Insight 目录与 metadata 迁移 | Design / Insight / Task；Delivery 不计数；Insight 与 Design 一等家族身份明确 |
| 6 · 改善阅读并验收 | F11 的入口短例、家族摘要、权威引用；对前述批次做 fresh-context 检查 | 正确性批次稳定 | Run 与受影响 family owner；下面的场景验收通过，记录未跑的平台/实现检查 |

批次 2 的定位修复可独立完成；跨家族术语和 Workflow 视图应等待批次 1 的共用定义稳定。目录/CLI/API 迁移属于相应 owner 的实际行为变更，不能用全库 `Phase → Run` 替换代替设计。历史 changelog、只读旧 ID、明确声明的 `phase()`/`meta.phases`/`opts.phase` 适配字段保留各自兼容含义。

**完成标准与有意义的验证场景**

根 [README 的 Skill development](/Users/jluo41/Desktop/Tools-SPACE/README.md:131) 要求 Skill 修改后在新上下文中用真实任务调用，并确认选择、执行和产物；未来实施者应遵循这一流程。本轮是报告复核，未执行这些调用。未来验证使用隔离样例目录和受控输入，避免让契约验收触发真实业务副作用。

| 场景 | 必须观察到的结果 |
|---|---|
| 一个分析目标包含多个工具调用并失败重试 | 一个 Run ID，多个内部 Steps/attempts；失败事实保留；实际 Run 数不因调用次数增加 |
| 一个参数化 Spec 产生两个独立目标实例 | 定义列表能表达 cardinality；实际列表列两项 ID 和两套 owner-native Result/receipt；两者可各自关闭 |
| Page 连续反馈、同目标重开、改目标 | 分别是 Step、Version、新 Run；四类 RP 名称一致；Scope 和关闭责任明确 |
| 尚未启动、正在执行、等待反馈、已终止 | 时间字段只表示真实事件；unfinished 的 finished_at 为 null；终止有 truthful outcome；等待反馈不显示为已完成 |
| Task 新计划和报告 | 模板与 Schema 可同时满足；旧 Phase 结构不再作为新计划格式；报告能连接每个实际 Run 和其 Spec |
| Paper 首次 Structure 与之后的写作 | 新入口统一使用 `rp-struct-01` 和当前 RP 方言；旧 rp00 不冒充当前 prerequisite；导航位置、Compile 投影不额外计数 |
| Insight 对新的冻结数据集复用 R 方法 | 新 `riNN` 绑定；Base R 不被重写/重复计数；同绑定 retry 留在原执行历史；独立 Insight owner 和当前路径可解析 |
| Design Commission → Generate → Verify → Delivery | 三个实际 Run，Delivery 为投影；新工作无 Adopt Run；Verify 来源与交付 hash 可追溯 |
| 兼容字段与历史样例 | 旧词被明确定位为兼容/历史；不从字段名称派生权限，不批量改写既有 Run 身份 |

静态验收包括显式引用定位、Markdown/YAML 示例一致性、规范列表与实际 Run 列表的字段对应，以及活动 Phase 使用的人工分类。若实施触及 parser/writer/validator，再运行对应包现有的相关检查；不以全库词频为零或重跑无关测试作为完成标准。

**本次 Workflow/Run 指标判定**

| 本次完整覆盖对象 | 当前判定 | 达到通过还需要什么 |
|---|---|---|
| `haipipe-run`（1/1） | **部分通过** | 明确 Workflow 是 Run 列表；同步 RP/Design 方言与 Insight 引用；澄清 attempt 和时间规则。Run/Step、闭合、owner-native 身份与历史保存原则已经具备良好基础 |

跨家族观察：Task 的活动模板和 Page/Paper 的活动 Phase 语义仍需处理；Insight 文档已明确移除 Phase 对象和 Application 父层，不能继续沿用原来的整体“失败”标签；Design 已按 Commission/Generate/Verify 区分 Run 与内部步骤。Route 图、Run Type 目录和只读展示都可以保留，只要 Workflow 的工作单位和实际清单始终是 Runs，且内部 Step、Gate、Version 与投影不被额外计数。
