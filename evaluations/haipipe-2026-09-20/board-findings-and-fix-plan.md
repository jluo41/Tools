**Board 全家族问题复核与修复计划 · 2026-09-20**

本报告补充 [原评估 board.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/board.md)，以当前工作区重新判定问题。最重要的变化是：**Folder 的 Phase 身份合约已在现有未提交改动中改为 Run Spec 与资源身份分离，原来的核心 FAIL 不再成立。** 当前仍有 13 项待处理问题，其中优先修正机器检查与人工 gate 的冲突、DesignBoard 的交付状态，以及过时的 Page Run ID。家族 Workflow/Run 指标更新为 **PARTIAL，尚未完全达标**。

本次完成的是问题说明与实施计划。此任务没有单独获准的实现工作；仅新增本补充报告。下述已有改动是复核开始前工作区中的内容，不能归为本次修复，也不据此认定其他任务已经通过验收。

**复核基线与覆盖**

- HEAD 仍为 `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`，但工作树已明显变化。复核时间为 2026-09-20，美国东部时间约 17:11；行号针对本次读取的工作树。
- 当前 Board 目录仍有 4 份有效 `SKILL.md`，本次全部重读。Board 主技能和 Folder 技能已有未提交改动，Routing 和 DesignBoard 技能在本次检查时没有工作树差异。
- 相关已有改动还涉及 Board 的 `foldercontracts.py`、`check.py`、`context-record.py`、`servers/workbench-insight/insightboard.py`、Insight Space 映射及相关测试，以及 Page 的 `folder_contract.py`、Page workflow 等。Insight 已出现 `folder-kinds/` 和 `workflow/folder.yaml` 迁移。保留这些改动，计划中的共享修改应与相应任务合并处理。
- 复核依据是源文档、声明、代码分支和路径查找；没有执行操作技能、服务、测试或浏览器流程。下文的验收条件均是未来实现后的要求，不是已取得的测试结果。

| 当前技能 | 本次覆盖 | Workflow/Run 指标 | 证据与边界 |
|---|---|---|---|
| [haipipe-board](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md) | 全文 332 行 | PARTIAL | 42–48 行混用旧 RP 命名与 workflow pass；README 仍用 Phase 表描述流程；已明确 pass 不等于 Page Run |
| [haipipe-board-routing](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md) | 全文 265 行 | N/A | 123–153 行是路由操作的五步程序，不定义独立 Workflow；67 行把 group 定义为责任范围，合理 |
| [haipipe-folder](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md) | 全文 274 行 | PASS（当前模型） | 42–45、123、175–188 行以 Run Spec 定义工作流；235–249 行把旧 Phase 文件限定为身份读取兼容；剩余 shell 示例问题不构成 Phase 模型失败 |
| [haipipe-workbench-design](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/SKILL.md) | 全文 218 行 | PARTIAL | 48–49 行仍把 Commission、Generate、Verify、Adopt 并列为 Steps；Run Space 确有按 Run 展示的记录，但最后一个单位已不符合 Design owner |

本次支持材料核对覆盖：Board README；`ref/board-form.md`、`ref/operations.md`、`ref/insight-space-mapping.md`、DesignBoard `ref/space-mapping.md`；Board agent roster、approver 与 approve-rules；`fn/serve.md` 的范围规则；`regroup.py`、`lanes.py`、Folder parser/CLI、Page 状态生成、workflow receipt 路径、Design/Insight 相关投影。共享合约定向核对了 `haipipe-run`、Page workflow/outline、Page Run families、Design workflow/door/brief 和 Insight door。支持材料是按发现定位复核，并非重新逐行审计所有代码。

原评估中没有变化且本次发现不依赖的 writing-rules、board-example、reviewer/auditor/creator 全文未重复审阅；沿用原评估的覆盖记录，不将其计作本次新验证。legacy、历史 changelog、第三方引用树、vendor、bulk assets 和测试实现未做完整审计；仅查找了未来可用的测试文件。没有评估运行时表现或真实用户行为。

**评判口径**

用户要求是：**A Workflow is a list of Runs. Workflow 的工作单位使用 Run，不使用 Phase。** 在当前仓库中，定义层是带依赖、路由的 Run Spec 列表/图，执行层是实际分配的 Run Instances。每个实际 Run 必须有可识别的目标、owner、身份、关闭条件及结果/收据；工具调用、内部 Step、一次反馈、状态标签和普通 gate 不自动成为 Run。[共享合约 193–210、226–255 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:193)

保留兼容 API 字段不是模型失败。Page owner 57–61 行明确 `phase`、`cycle`、`next_cycle` 是序列化 dispatch/progress 标签；新 Folder 合约也限定旧 `workflow/phase.yaml` 只导入资源 kind。修复应消除这些词在当前说明中的语义权威，不能全局替换字段、历史记录、目录名或函数名。[Page owner](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md:57)

**R00 · 原 P1 Folder Phase 模型：核心问题已改，接续现有迁移验收**

原报告指出 Folder 把 Phase 当身份、Workflow Table 以 Phase/Cycle 为行。当前 [Folder 技能 42–79、121–123、175–188、235–249 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md:42) 已明确：Folder kind 是资源身份，Workflow 使用 bounded Run Specs；新身份记录为 `workflow/folder.yaml`；旧 Phase 字段不产生执行权威。

这已延伸到实现：[Page Folder parser 54–78、117–164、179–180 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/src/folder_contract.py:54) 去掉 `FolderContract.phase`，优先读取 `folder.yaml`，legacy fallback 只返回 `folder-kind`；[Folder CLI 42–52 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/foldercontracts.py:42) 显示 Folder contracts。[Insight Space 映射 47–62 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/insight-space-mapping.md:47) 与 [InsightBoard UI 1366–1384 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/servers/workbench-insight/insightboard.py:1366) 也已分开 Run Spec、实际 Run 和 Folder resource。

结论：不重复提出整套 Folder Phase 重构。由现有迁移的 owner 完成兼容验收：canonical 文件优先；缺省时旧文件只贡献 kind；不合法身份/冲突不静默 fallback；新写入没有 Phase 身份/进度字段；保留旧记录字节；UI 不把 Folder resource 数量当 Run 数量。当前代码证据支持模型已修，但此报告没有执行测试，不能确认跨家族迁移已全部完成。剩余文字/示例问题见 F05、F10。

**F01 · P1 · 机器 checked 被描述成足以越过人工 release gate**

证据：[approve-rules README 77–85 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/approve-rules/README.md:77) 写 “The RUN does not wait for the human field”，并明确仅凭 `checked: ✅` 推进；[approve-rules.md 76–87 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/approve-rules/approve-rules.md:76) 继续将 `approved:` 称为 OPTIONAL；[approver agent 24–29、71–80 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/haipipe-page-approver-agent.md:24) 称 checked 会释放 “next phase”，且要求只把这份规则文件作为 authority。

当前 [Page Outline 573–607 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-outline/SKILL.md:573) 明确允许 checked v0 做部分证据工作，但 copilot 和 auto 都不能越过需要人的 Content-release gate。这是当前有效说明之间的矛盾；旧人类引语被用来指导当前行为，因此不能一律按历史材料排除。

影响：人以为还在等自己批准，agent 却可能继续 CONTENT；机器通过、人工批准、可继续证据工作三者混在一起。这里确认的是指令可能诱导错误放行，未证明现有执行器已实际绕过 gate。

修法：同一补丁更新 README、approve-rules.md、approver 的字段/authority/返回说明，写清机器只记录检查结果，owner 的 release gate 决定哪些后续工作可做。保留 checked 与人工 tick 的分工及独立 reviewer。建议英文：

> `checked:` records the machine result. Continue only work permitted by the owning Run Spec and mode. A passing check never substitutes for a person-reserved release gate. Report permitted work and the next unmet gate separately.

验收：fresh-context 场景中，checked v0 可继续被允许的证据工作；人工 Content gate 未满足时不能写 CONTENT；已有有效人工批准可被引用；反馈中的 machine result、allowed next work、human gate 分别明确。Owner：Board approver + Page Outline/Workflow；共享去重键 `PAGE-RELEASE-GATE`。

**F02 · P1 · DesignBoard 的 adopted/Adopt 与当前 ready/Delivery 合约冲突**

证据：[DesignBoard 技能 48–49、64–65、87–90、107–124、162–164、216 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/SKILL.md:48) 写 “Steps are Commission, Generate, Verify, Adopt”，queue 示例为 `JL · adopt`，还说发送系统取 `state=adopted`，CSV 包括其他状态及 declined。其 [Space 映射 5–13、34–35、68 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/ref/space-mapping.md:5) 同样过时。

当前 [Design workflow 41–64、135–142 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:41) 规定实际 Runs 为 `1 Commission + N Generate + J Verify`；Delivery 是只读交付投影。实现 [design.py 514–530、715–718 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/servers/workbench-design/design.py:514) 从独立 Verify 记录推导 ready；[designboard.py 301–303、417–432、475–494 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/servers/workbench-design/designboard.py:475) 使用 ready 计数，导出只收录有 ready draft 的项，不把普通未验证/declined 草稿混入该 bundle。

影响：读者可能等待额外 Adopt 决定、找不存在的新动作，或按文档筛选 CSV 导致没有可发送记录。此处不仅是换词，交付集合和完工判断也不同。

修法：Board 技能及映射统一使用 Commission/Generate/Verify Run、ready 和 Delivery；写明交付文本来自 Verify 指定的精确版本，self-check 通过不等于独立 Verify。历史 adopt 仍可读取，但不成为新流程。建议英文：

> The Workflow contains Commission, Generate, and Verify Runs. Delivery shows the exact draft whose independent Verify passed. The bundle contains only ready designs; historical Adopt records do not require a new adoption Run.

验收：混合 ready、仅自检通过、Verify fail、declined、legacy adopt 的案例中，文档描述与 UI/CSV 筛选一致；计数不包含虚构的 Delivery Run；人的等待项只来自当前 owner 允许的 gate。Owner：Design + Page Design plugin + Board Design plugin；去重键 `DESIGN-DELIVERY-STATE`。

**F03 · P1 · Board 仍指导读者分配旧 Page Run ID**

证据：[Board 主技能 42–48、247–250 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:42) 把 `rp00_mermaid-structure` 和 `rpNN_pNN[-pNN]` 写成现行格式；[Board README 39–48 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/README.md:39) 也如此。当前 [Page Run families 32–44、48–67 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/ref/page-run-families.md:32) 定义 `rp-struct-NN`、`rp-scratch-NN_<target>`、`rp-sec-NN`、`rp-para-NN_Pxx[-Pyy]`，旧 compact ID 仅为兼容输入。

影响：新建的 Run、恢复指令、文档示例与 owner 的 active namespace 不一致；一个新读者无法从 Board 入口学会当前命名。原报告说 renderer/owner 可能“不承认旧 ID”过强：兼容读取仍存在，确认的问题是新建规范错误，不是所有旧记录都无法显示。

修法：Board 两处共同改为引用 canonical Page Run families，并选用 `rp-struct-01` 等当前例子；Structure 活跃/关闭显示也引用 owner 的规则。正文把历史格式标成只读，避免重新编号旧记录。验收：新建/恢复初始 Structure 使用 `rp-struct-01`；参与者或反馈增加不创建新 Run；Section/Paragraph 使用各自序列；旧记录可读而新 writer 不生成 compact ID。Owner：Page identity owner + Board 文档；去重键 `PAGE-RUN-IDENTITY`。

**F04 · P2 · Workflow Runtime、controller 坐标和真实 Run 的说明仍混杂，receipt 示例不完整**

证据：[Board README 25–35、43 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/README.md:25) 以 `Phase` 表列 CONTEXT/OUTLINE/EVIDENCE/CONTENT/CHECK；[主技能 36–48、77、199–200 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:36) 仍称 “Page phase”“phase controller”“Page-phase receipts”；[agent roster 4–15、32–37 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/README.md:4) 把 producer 派发描述成 phase。相比之下，[Page workflow 63–96 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md:63) 已定义 `workflow_runtime_id` 与实际子 Runs 的边界。

Board 主技能树只展示 Page 下的 `workflow/`，没有画出当前 Board aggregate receipt 路径。[page-run-contract.md 194–200 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/page-run-contract.md:194) 指定 `<board>/_runs/page/<page-id>/<run-id>.json`；[Page 状态读取器 182–196 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/src/page_phase.py:182) 从此处读最近 receipt。原报告把该路径误说成主技能 75–79 行已存在，本次更正为“树中漏示”。

影响：人可能把一次 Board RUN、每个 controller 标签或一次 snapshot 当成一个实际 Run，或去错误位置找收据。已有“pass 不等于 Page Run”的说明有价值，应保留并补完整。

修法：用 owner-defined Run Spec 列表/图解释 Workflow，单独列 controller dispatch map。`RUN` 启动一次 Runtime execution，可能协调多个原生 Runs；CONTEXT/CHECK 是否产生实例按 Page owner 判断。补 runtime envelope 和 owner-native receipt 的路径及用途。读取适配器中 `phase()`/`phase` 字段的改动只限必要注释和可见文案，不改兼容 API。验收：读者能指出 Workflow、实际 Run、内部 Step、gate、controller label 五者；不会按五个标签计五个 Run；能从 Board 找到真实 runtime receipt。Owner：Run + Page + Board；去重键 `WORKFLOW-RUN-BOUNDARY`。

**F05 · P2 · Board 类型入口缺项，Insight 路由指向缺失技能，Application 父家族文案残留**

证据：[Board 主技能 23–31、57–67 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:23) 没有 DesignBoard 路由，kind 表只列 generic/task/discovery；[board-form.md 8–15 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/board-form.md:8) 同样不完整。[checker 303 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/check.py:303) 已接受 `design-board` 和 `insight-board`。Insight lane 写 `haipipe-plugin-insight-board`，但对 `plugins/**/SKILL.md` 查找该 `name:` 无匹配；本次 Board 全量清单也无此技能。当前实际存在 [haipipe-insight 23–43、74–79 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:23) 和 Board 内的 Insight renderer。

此外，[Board README 19–21 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/README.md:19) 仍写 “Application Pages by the Application family”，[Folder 251–252 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md:251) 残留 “New Application Pages”。前者明确保留已退休的家族关系；后者可能仅指一类产品页面，语义需澄清。

影响：入口会把读者送到不存在的技能，或遗漏已经支持的 Board 类型；Design 与 Insight 的一等家族身份难以从 Board 文档看出。

修法：补齐五种 Board kind 和真实 owner/呈现入口。Insight 指向现有独立 family door/workflow 以及 Board presenter 映射；先由 Insight owner 确認具体入口，不为填表虚构或新建插件。Design lane 指向现有 Board Design plugin。移除 Application 父家族表述；产品意义的 application 可保留为普通名词，但不要承担 owner 含义。验收：每个路由名在可安装技能树中可解析，五种 kind 的发现/注册/owner 均明确；Insight/Design 不挂在 Application 下。Owner：Board + Insight + Design；去重键 `BOARD-FAMILY-DISCOVERY`。

**F06 · P2 · Routing 把展示注册表当成找 owner 的唯一来源，新增成员步骤缺少 kind 分支**

证据：[Routing 141–158 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md:141) 要求从 `board.md ## Pages` 这个 “ONLY registry” 找 owner；[Board 主技能 118–121 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:118) 和 [board-form.md 122–136 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/board-form.md:122) 则允许 Task Board 只列 Job headings，实际 Task 成员由树发现。`lanes.py` 46–65 行只读取显式 `.md` roster rows，不会发现未重述的 Tasks。主技能 130 行“add a question/group”没有就地说明 kind；operations 的创建段 57–59 行已有 Task 例外，但 63–68 行 Add 段仍通用地要求 Q Group/Q Page。

影响：agent 可能把已存在的 native Task 判成“没有页面拥有此工作”，提出重复 Q Page；只含 Job headings 的 Board 可能被错误理解为空。原来关于 owner 应先解析的建议应升为明确的 membership/registry 边界问题。

修法：先读 Board kind、用该 kind 的 membership discovery 找对象，再由 `## Pages` 决定显示组/顺序；随后加载 Folder/领域 Page owner，选择内容字段。Q/S 创建和 lanes/regroup 明确适用范围；Task/Discovery 走 native owner。验收：仅含 Job headings 的 Task Board 仍能正确路由到现有 Task；通用 Board 未登记的已有 Page被提示注册而非重复新建；不因 native tree 外形不同而重构目录。Owner：Board routing + Task/Discovery；去重键 `BOARD-MEMBERSHIP-ROUTING`。

**F07 · P2 · regroup.py 的能力被写成任意 rename/split 迁移**

证据：[Routing 104–113 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md:104) 称脚本是 “migration tool for any group rename or split”。实际 [regroup.py 84–111 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/regroup.py:84) 只移动匹配当前 group 前缀的 Board 根 Pages；nested Pages 不进 moves。它不重写 alias 或引用。[operations.md 120–124 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/operations.md:120) 已准确限定为 root Page folderization。

影响：执行者可能以为脚本没有 moves 就表示 rename/split 已完成，实际上路径、alias、引用仍未迁移。Routing 113 行已说迁移有三部分，应保留；问题是 106 行把工具范围说大了，并非文档完全没提其他工作。

修法：复用 operations 的准确范围，明确 root folderization 与 group rename/split 的操作清单。暂不扩大脚本功能。验收：说明能解释 root match、nested Page、unmatched root、已有目标四种情况；no moves 不被报告成全面迁移完成；rename/split 单独检查 alias 和引用。Owner：Board routing；去重键 `BOARD-REGROUP-SCOPE`。

**F08 · P2 · 创建 Page 的模板链接失效**

证据：[Board 主技能 294 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:294) 指向 `ref/page-template.md`；[operations.md 52–53 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/operations.md:52) 使用同目录模板名称。Board 本地没有该文件，存在的 canonical 文件是 [Page owner 的 page-template.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/ref/page-template.md)。

影响：第一次创建 Board/Page 的人会在必须加载模板时走进死路，或自行拼一个过时的 Page 结构。

修法：两处都明确指向 Page owner canonical 模板，从各文档位置计算正确相对路径；不复制第二套模板。将 source、操作配方和 owner 定义一起核对。验收：按文档直接定位模板成功；示例使用当前 Page 结构；Task/Discovery 仍走 owner generator。Owner：Board + Page；去重键 `BOARD-PAGE-TEMPLATE-LINK`。

**F09 · P2 · 状态示例不是当前 renderer 会产生的状态**

证据：[Board 主技能 199–207 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:199) 显示 `⏱️ LAND`；[Page 状态模块 94–100、449–455 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/src/page_phase.py:94) 当前选择 CONTEXT/OUTLINE/EVIDENCE/CONTENT/CHECK 或 CLOSE，并带对应 emoji，LAND 是另一粒度的 action。[status.py 317–334 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/status.py:317) 还存在 Page focus 输出四行、CLI help 却说 three-line 的小不一致。

影响：人无法判断状态栏是 workflow readiness、正在做的动作还是 Run identity，难以凭示例解释自己的输出。

修法：按真实 renderer 输出更新例子，例如 readiness 部分可为 `⏱️ 🃏 EVIDENCE …`；正文清楚说明这是 controller/readiness 汇总。需要展示实际 Run 时另给 canonical ID，不把 LAND 或标签改名冒充 Run。同步 help 的行数描述。验收：Board/Group focus 三行，Page focus 存在有效状态时四行；示例与 formatter 一致；标签和实际 Run 身份可区分。Owner：Board status + Page presenter；去重键 `BOARD-STATUS-COPY`。

**F10 · P3 · Folder 的通用运行形状只展示 shell Tickets**

证据：当前 [Folder 98–113 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md:98) 的 Folder-local 和 Job-backed 两种形状都使用 `runs/<run>.sh`，没有就地注明只是 shell 示例。共享 [Run 合约 363–377 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:363) 中 Page Writing Ticket 使用 `.md`；[Design workflow 88、104、122 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:88) 使用 `.yaml`。

影响：新作者可能为不需要 shell 的 Run 添加假执行器。当前 Folder 已要求按 profile 选择，这降低了风险，故保留 P3，不再将它当核心模型错误。

修法：把 `.sh` 标为 shell dialect 示例，再并列 Page `.md`、Design `.yaml` 的 profile 链接；通用规则使用 `<ticket>`，extension/Result 由 owner 指定。验收：读者能为 Task、Page、Design 各选正确 Ticket，空 Run 库不会被自动 scaffold。Owner：Folder + Run；去重键 `FOLDER-TICKET-DIALECT`。

**F11 · P3 · Routing 当前操作文案混入历史背景，无写入时的回报不够明确**

证据：[Routing 36–55、186–200、246–251 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md:36) 把旧 merge 和引语放在主流程里；205–214 行允许 PROPOSED/REPORTED，但 footer 只说 one line per write 和用户下一步；77 行 materialize 提 Board Structure，未说明 196 行 Board Map 的位置。[board-form.md 115–120 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/board-form.md:115) 已区分这两种内容。

影响：熟悉仓库的人能补齐含义，新读者却须从历史讨论还原当前规则；无写入提案和等待人工意见的状态容易被模板伪装成“已经完成”。这些主要是可读性和反馈完整性改进，不是已确认的数据破坏。

修法：先呈现当前 scope→owner→surface→write→handoff 程序，把历史原因移到 changelog；用一句话区分 Map 与 Structure；给 no-write 返回示例 `Writes: none; State: PROPOSED; Next: review the proposed page list`。只在确实需要用户动作时写该动作，已获授权的 agent 下一步不转交给用户。验收：LANDED/PROPOSED/REPORTED 都能明确写了什么、未解决什么、谁接下来行动；冷读者不依赖 JL 历史即可完成路由。Owner：Board routing；去重键 `BOARD-ROUTING-READABILITY`。

**F12 · P3 · DesignBoard new-folder 的 row 参数缺少直接定义**

证据：[DesignBoard 技能 73–84、144–145 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/SKILL.md:144) 解释过隐藏的 Brief row id，但动作签名仅写 `{row}`；[Space 映射 49–57 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/ref/space-mapping.md:49) 同样如此。[UI 318 行和 new_folder 633–646 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/servers/workbench-design/designboard.py:633) 表明传入值是 row 的内部 `id`，无显式 line 列时为 `R<N>`，不是屏幕任务标题或整数下标。

影响：由 API/agent 调用时会猜错参数并得到“not in Brief”拒绝；按钮本身提供正确值，因此没有证据证明正常 UI 点击失败。

修法：动作文档就地写清 row 是从当前 Brief 解析出的 key，给 `{"row":"R3"}` 例子，同时保留 UI 展示完整任务标题的规则。验收：显式 line id 和隐式 R 编号两种 Brief 都能定位；标题不会被当作 key；重复点击的拒绝保持可读。Owner：Board Design plugin；去重键 `DESIGNBOARD-ROW-KEY`。

**F13 · P2 · 新确认：历史 Design Run 的显示 ID 被改写为不存在的 Delivery ID**

证据：[DesignBoard renderer 394–400 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/servers/workbench-design/designboard.py:394) 在 Run 列执行 `r["id"].replace("_adopt_", "_delivery_")`；[Page Design renderer 897、1104 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/servers/workbench-design/design.py:897) 的链接文字/tooltip 也改写 ID。与此同时，[Design workflow 81–82 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:81) 要求呈现同一 Run identity，不 mint、rename、copy 或 recount。

影响：历史 `rd01_adopt_x` 会看起来像 `rd01_delivery_x`，用户复制到搜索、收据定位或讨论中时难以对应磁盘。确认的是显示文字改写；底层 ticket_path 仍指向原文件，不应说成源码文件被重命名或链接已证实损坏。

修法：Run ID 列、链接文字和 tooltip 保留原始 id；另把 action/type 显示为 `Delivery (legacy)` 或相应解释。新 Workflow 仍不分配 Adopt/Delivery Run。验收：同一个历史记录在 Board、Page、文件和 receipt 中 id 完全一致；只改变操作标签；点击仍到原 Ticket；新记录按当前 Commission/Generate/Verify 合约处理。Owner：Design + Board/Page Design presenter；去重键 `DESIGN-LEGACY-ID-DISPLAY`。

**需要跨家族确认的内容**

| 事项 | 当前证据和确定性 | 负责方与处理方式 |
|---|---|---|
| Folder identity 迁移 | R00 的语义修改已存在；未执行集成验收 | Insight/Folder/Page parser owner 接续现有工作，Board 不重复重构；仅跟进 CLI/UI/文档遗漏 |
| 人工 gate | F01 是明确的现行契约冲突；未证实运行时实际绕过 | Page owner 定义放行语义，Board approver 消费；同一去重键归并所有规则文件 |
| Design ready、legacy Adopt | F02/F13 的 owner 与实现证据明确 | Design 定义状态，Board/Page presenters 同步；不能只修 Board 文案而保留假 ID |
| Design 的 Delivery 行仍列入 Run Specs 表 | [Design workflow 48–64 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:48) 一面说 every row 是 Run Spec，一面有 Delivery projection 行并说不是 Run；表格层面不一致，正文边界明确 | Design owner 将 Delivery 放到投影表或显式分段；Board 只引用真正三类 Run，不据此计第四个 Run |
| Page RD 与 Design rdNN 命名 | [Page Run families 36–44 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/ref/page-run-families.md:36) 用 `rd01_web` 等；[Design 122–142 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design/SKILL.md:122) 要求两套 Workflow 不共享 IDs/counters | 相同前缀不等于已发生冲突；由 Page/Design 核对 owner-qualified 地址与 allocation。列为待确认项，不据此启动全库重命名 |
| Design brief 的 Application 用词 | [Brief 21、36–44 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-brief/SKILL.md:21) 仍说 Application，但同文明确 Brief 是 Commission 前提而非 Phase | 可能指产品主题，不能直接等同于父家族；Design owner 澄清。Board README 的 Application family 则已明确过时 |
| Insight lane 的准确入口 | `haipipe-plugin-insight-board` 在当前插件技能树无定义；独立 Insight door 与 Board renderer 存在 | Insight + Board 共同选现有入口；这不是安装失败的证据，也不要求新造插件 |

**对原报告的必要校正**

原评估保留为历史快照。本次不改写它，但后续实施须采用以下校正：Folder 核心 Phase 问题已有改动；Page workflow 的实际路径为 `skills/page/page-workflows/haipipe-page-workflow/`，原报告部分链接多插入了 `haipipe-page/`；人工 Content gate 的 573–607 行属于 `haipipe-page-outline/SKILL.md`；Board 主技能树没有 `_runs/page` 行，是遗漏而非已说明；旧 RP 格式有兼容读取，不应笼统声称 renderer 不承认；regroup 的三部分要求已经写出，错误在宣称脚本覆盖任意 rename/split。旧报告中的英文 Before 概括不作为本次逐字证据。

**实施顺序、依赖与交付范围**

| 顺序 | 工作包 | 依赖 | 具体交付与完成条件 |
|---|---|---|---|
| 1 | 确认共享 owner 和既有迁移边界 | 当前工作树；R00 | 列清谁继续 Folder/Insight 迁移、Page gate/identity 的 canonical 文件；保留已有改动，不重复开一轮 Phase 重构 |
| 2 | 修 F01 人工 release gate | Page Outline/Workflow owner | 同批修改三份 Board 审批材料及其 authority/返回说明；checked 与人工批准不会互相替代 |
| 3 | 修 F02/F03/F04/F05 的现行合约与路由 | 第 1 步；Design/Page/Insight 当前契约 | Board README、主技能、DesignBoard 技能、两类 Space 映射、必要 agent 文案同步；正确 ID、状态、Run/controller 边界和五种 Board kind 均可从入口查到 |
| 4 | 修 F13 显示 ID、F09 状态示例/help | Design identity 及 Page formatter | 原始 Run ID 展示一致；action 标签可读；状态例子和实际 formatter 对齐。需要代码改动的范围限定于对应 presenter/help |
| 5 | 修 F06/F07/F08/F10/F11/F12 操作说明 | 第 3 步的类型/owner 入口 | kind-aware 路由、regroup 范围、模板路径、Ticket dialect、无写入反馈和 row 参数具备直接例子；不扩充脚本功能 |
| 6 | 针对实际修改做验收 | 前述所涉及补丁完成 | 按下表执行对应检查、记录结果；新失败归属具体 owner，确认后再继续修；完成 fresh-context 场景后再关闭问题 |

第 2 步与 Design 状态文案整理在 owner 已明确时可以独立进行；同一 Board 主技能/README 的变更应合成一个补丁，避免各任务覆盖。F08 的链接和 F12 的参数说明不依赖 Folder schema 完成。R00 迁移验收可由现有负责方继续；只有确认发现新缺口才增加修改范围。不要为这次文案修正改 installer、marketplace 或 retired submodule 内容。

**未来验收矩阵**

| 验收面 | 应执行的检查/场景 | 通过条件 |
|---|---|---|
| 覆盖与文案 | 重读 4 份技能及被改的支持材料；逐项解析当前链接/skill name | 不缺类型；没有失效模板/假 owner；历史说明不冒充当前操作 |
| Workflow/Run 指标 | 新 Folder、Board RUN、Page feedback、Design item、Insight aggregate 五类案例 | Workflow 单位都是 Run Spec/Run；控制器、Spaces、资源、gate、Step 不凭名称分配 Run；实际计数来自 owner identity + receipt |
| Folder migration | 对现有 Folder 相关测试和 `cli/foldercontracts.py --check` 做适当的 owner 范围检查 | canonical/legacy 选择、冲突拒绝、新 writer schema 与去重均正确；跨家族旧问题单列归属 |
| Approval | 独立上下文读取完整技能及实际 packet，覆盖 checked v0、人工 approval 缺失/已给、人工 🛑 | 不把 checked 当人工 release；能清楚说出允许继续的工作和等待对象；不对 gate 作未经授权的决定 |
| Native Board 路由 | Generic 未登记 Page；Task Board 只列 Job headings；Discovery native tree；Design/Insight Board | 每次找到唯一 owner；不重建已有对象；不用 Q 模板冒充 native Task；不会加载不存在技能 |
| Design 状态与 ID | 复用 `test_design_board_plugin.py`、`test_design_plugin.py`、`test_design_run_gate.py` 中相关覆盖；仅为未覆盖的真实行为补必要用例 | 仅 exact Verify-passed draft 可交付；legacy id 字节一致；Label 改写不改变身份；current Run count 不含 Delivery projection |
| 状态和 Page identity | 运行与修改相关的 `test_status.py`、Page Run/phase ledger 覆盖，核对一个真实输出 | 状态与 Run ID 可区分；Board/Group/Page footer 行数正确；新/旧 RP 分配与读取边界一致 |
| Migration 工具说明 | 用受控例子审查 root/nested/unmatched/已有目标的 dry-run 结果，若没有改代码不扩大到无关迁移 | 明确哪些 moves 将发生；不会把 no-op 等同于 rename 完成；alias/引用是单独完成条件 |
| 人可用性 | 打开已有 Board、无写入提案、路由现有 Task、新 Design Folder、领取 ready 交付 | 输出能回答“在哪里、发生什么、由谁决定、下一步是什么”，不用先读 merge 历史 |

根 [README 133–136 行](/Users/jluo41/Desktop/Tools-SPACE/README.md:133) 要求技能修改后从 fresh context 验证真实任务。因此未来实现阶段应由独立上下文实际选择技能、遵循指令并完成受控场景，再核对产物。该要求目前列入计划，本轮没有修改技能，也没有启动该验证。测试只运行与最终改动相关的已有覆盖；无新失败或未解决疑点时不重复扩大检查。

**建议保留的设计**

继续保留 Board 的 source/projection 分工、Page owner 优先、仅为实际使用的 lane 建目录、只读/写入意图的区分；Routing 的提案与 materialize 分离、已授权决策及时落盘；DesignBoard 的跨 Folder 记录与下钻链接；Folder 的两张 Face、资源身份与 Run 进度分离，以及 Insight 新投影对模板/资源/实例的区分。修复目标是让这些既有边界在入口、规则和 UI 中一致。

本轮所有待办均为计划。当前完整技能覆盖为 **4/4**；Workflow/Run 为 **Folder PASS、Board PARTIAL、DesignBoard PARTIAL、Routing N/A**。要达到家族整体 PASS，须完成上述现行流程/命名修正，并取得对应实施验收结果。
