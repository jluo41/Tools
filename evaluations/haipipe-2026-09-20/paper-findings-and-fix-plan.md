# Paper 家族问题核对与修复计划

## 1. 结论与本次边界

**当前最先应修的是 assembly 的生成目录保护与错误配置示例。** 随后统一 Paper 的 Run 定义、Page 适配和 Run 归属，再迁移 Venue 合同及其范例。本文列出 12 项待处理问题：4 项 P1、5 项 P2、3 项 P3。P1 表示可能损坏文件、违反指定的核心工作流模型，或直接破坏主要交接合同；P2 表示活动说明之间不一致，影响路由或使用；P3 表示局部阅读与交互改进。

本文是对 [原评估 paper.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/paper.md) 的补充与校正，原文件保持不变。**只写问题和计划，没有实施任何修复，没有运行技能、测试或 build。** 本文的验收场景均供后续获准实施时使用。

核对日期为 2026-09-20；根仓库 HEAD 为 `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。当前 Paper 仍有 9 份活动 `SKILL.md`。本次重读原报告，并核对九份技能涉及的问题段落、当前 Page/Run 合约、Paper UI、assembly 代码和 Venue 材料；未重新逐页通读所有 Venue 正文或来源 PDF，也未进行用户实测。

工作区已存在其他工作的未提交改动。Paper 的 assembly skill、builder 和 Section skill 已开始采用 `results/<re-run>/payload/<unit>/...` Display 路径；共享 Page、Display、Insight 等也有改动。本文保留这些改动，不把它们计作本任务成果。当前目录清理代码的位置已从原报告的约第 849 行移到第 994 行，风险仍在。下文行号均按本次读到的工作区，后续并行编辑可能移动行号。

`paper/venue/` 是 Git 子模块，gitlink 为 `b7d3e51af3790381d00747a6356266356f0e2e51`，核对时该子模块自身状态干净；其实际路径见 [.gitmodules:186](/Users/jluo41/Desktop/Tools-SPACE/.gitmodules:186)。没有发现 Venue 内的 `AGENTS.md`/`CLAUDE.md`。后续 Venue bank/playbook 修改应按子模块工作处理，不能无意改变根仓库指针。根仓库中另有 8 个 reference 子模块显示工作树脏；小写 `m` 本身不证明指针变化，原报告的“指针修改”措辞应收窄。

## 2. 对原报告的校正

| 原判断或疑问 | 本次核对后的判断 |
|---|---|
| Workflow map 不是 Run inventory，因此不符合模型 | **收窄。** 定义视图与实际执行清单可以分开。问题是 Paper 未提供完整、可对应的 Run Spec 清单与路由，且插件两处清单有差异；“定义图不证明已执行”应保留。 |
| Venue README “recommend a venue” 越权 | **撤回越权结论。** 提供建议不等于替作者决定。应修正旧入口、旧挂载地址，并说明建议如何交给 Ideation/Story 和人类决定。 |
| CONTEXT/OUTLINE/EVIDENCE/CONTENT/CHECK 应保留为内部 Steps | **更正。** 当前 Page owner 明确把这些字段限定为 dispatch/progress labels，且写明它们不是 Run Specs，**也不是 Steps**。不能批量替换成 Run 或 Step。 |
| 17 份 Venue 页面缺少合同直接证明 gate 失效 | **收窄。** 确认缺少新接口，不能据此证明运行时放行、所有论文被阻塞或消费者没有外部合同。旧页可以用于 broad screen，不能自动冒充通过 deep-fit 的合同。 |
| 复制 assembly 示例立即因缺少 pages 报错 | **补足条件。** 未填 profile 等占位符可能先失败；有效填写这些字段后仍缺少 `[pages]`。删除风险要求读取 compile order 等前置步骤成功且目标目录存在；没有观察到实际删除事件。 |
| MISQ 文档未说明数值结果例外 | **收窄。** 后文已明确说明 healthcare/policy 例外；问题是前文绝对禁令未更新，且有“没有冲突”的表述，使读者必须自行裁定哪个版本生效。 |
| Paper Round 与 Page round 的关系没有依据 | **基本排除。** Page receipt 确有数字 `round`，validator 也有重开计数规则；剩余是把 RD、controller round、写作 Run Version 三者说明清楚。 |
| Insight 的 “Application Insight workflow” 仍需修改 | **当前工作区已消失。** 现行 Insight 明确 Run Spec/Runtime 和 Folder kind，属于其他任务的未提交变化；不重复安排修复，也不据此宣称整个 Insight 家族已验收。 |

QBv 页面中“no run reads it”等自述是页面当时的状态文字，不能代替本次执行证据。Story 的 C1–C8 阅读顺序、Section 的内容结构、Round ledger 的逐项清单也不是天然的执行 Workflow，不应全部改成 Run。

## 3. 全家族覆盖与 Workflow = Runs 指标

采用两层检查：**Workflow 的定义列出有界 Run Specs 及路由，运行时列出这些 Specs 对应的实际 owner-native Runs 和收据。** Run Type 是可复用类型；Step 留在 Run 内。Page、Folder、Space、Gate、controller action 不因出现在流程图或界面中就成为 Run。每份 PageType 可以引用共享 Workflow，无需各自复制一份清单。

下表只评 Workflow/Run 语义；配置安全、模板完整性另列问题，避免混成一个分数。“部分符合”表示已有正确边界，但活动适配或清单尚未对齐；不是运行测试通过。

| 当前技能 | 本次核对定位 | 当前判定与修复关联 |
|---|---|---|
| [haipipe-paper][paper] | 28–40、54–86、152–158、227–246、497–501 | **不符合**：P0–P4 与 `[phase]` 仍是活动入口，Run 身份说明落后。F02/F05。 |
| [haipipe-paper-workflow][workflow] | 21–30、40–79、225–247、257–281 | **不符合**：定义单位仍是 journey phase/position，没有完整 Run Spec 合同。F02。 |
| [haipipe-plugin-paper][plugin] | 370–399；space-mapping 7–17 | **部分符合**：正确区分计划和执行，但缺 Run Type→Spec→Instance 对应，清单漏项。F06/F11。 |
| [haipipe-paper-assemble][assemble] | 289–317、363–400、419–444、460–471 | **部分符合**：编译是有界操作，manifest 权威清楚；应绑定编译 Spec 并修正 CHECK phase 文案。F01/F02/F05。 |
| [haipipe-paper-venue][venue] | 21–24、29–47、93–121、199–207 | **部分符合**：正确作为参考 PageType，仍用 Page phase 入口；合同缺口单独列为 F03/F07/F08。 |
| [haipipe-paper-ideation][ideation] | 29–47、64–116、187–194 | **部分符合**：I3 与非 Run 同步边界明确，仍写 P0 phase。F02/F05/F12。 |
| [haipipe-paper-story][story] | 21–26、52–95、415–417 | **部分符合**：前瞻 Story 与证据结果有区分，仍处于 P1/共享 Page phase 叙事。F02/F05。 |
| [haipipe-paper-section][section] | 25–44、96–125、225–266 | **部分符合**：Page、证据、外部 Task 边界大体清楚；P3、Page RUN 与 owner 文案需对齐。F02/F04/F05。 |
| [haipipe-paper-round][round] | 22–63、186–195、231–260、332–360 | **部分符合**：明确 Round 不是 Run，batch/ledger 设计可保留；P4 与加载顺序陈旧。F02/F05/F12。 |

按这个更明确的指标，本次为 **2 项不符合、7 项部分符合**，取代原报告将模板质量混入指标后的“4 失败、5 部分”。总体仍未满足指定模型。Insight 和 Design 应始终作为独立一等家族；Paper 中的 `article/application category` 是投稿类别业务用词，不构成 Application 父家族。

## 4. 逐项问题与拟议修法

### F01 · P1 · 编译目录无安全边界，配置示例与当前输入合同不一致

**位置与证据。** [TOML 示例:1][config-example] 的第 7–12 行把 `source.room` 设为 `../1-<desk><year>`，全文没有 `[pages]`。相对地，[assembly canonical config:295][assembly-config] 明确 `[pages] main/order` 是输入，`[source] room = "latex"` 是生成目录。[builder:55][builder-path] 直接解析配置到 `LATEX`；[builder:142][builder-order] 读取 `CFG["pages"]["order"]`；[build():987][builder-delete] 在读取 order/main/appendix 后，第 994 行直接 `shutil.rmtree(LATEX)`。当前新增的 Result payload 路径检查不保护这个删除目标。

**影响。** 作者照示例配置不能完成当前 build；若只补 `[pages]` 而保留旧 room，前置读取成功后可能删除旧稿件目录。此风险由代码条件推出，未实际执行或证明已发生数据损失。

**拟修。** 由 Paper Assemble owner 同步示例与 canonical config，并在任何写入/删除前集中校验 schema 与全部生成路径。按当前合同，将 room 解析为本 Paper 的 `delivery/latex`，拒绝根目录、Paper/delivery 本身、`..` 或符号链接逃逸，以及输入 Page/Story 路径的重叠。若要支持其他生成目录，先声明独立且同样严格的合法范围。必要时先生成临时目录，成功后替换，避免破坏上一次可读产物。保留当前 Display Result 迁移。

**验收。** 示例可填成有效最小配置；缺字段给可操作的错误。使用临时目录的后续测试覆盖安全 room、旧 room、根目录、输入重叠、符号链接；所有非法配置在写入前退出，保留 sentinel 和已有稿件。编译内部检查、拷贝和工具调用不因此各建一个 Run。

**依赖。** 可首先独立修复，无需等待术语迁移。

### F02 · P1 · Paper Workflow 尚未以 Run Specs 与实际 Runs 为工作单位

**位置与证据。** [Workflow:21][workflow-model] 定义 journey phase 与 Page phase；第 40–79、225–247 行以 P0 Ideation、P1 Story、P2 Evidence/Execution、P3 Section、Compile、P4 Round 定位工作。[umbrella:227][paper-verbs] 暴露 `[phase]` 并在第 240 行解释为 PAGE phase。四个 PageType 仍放在 `workflow-phases/`，README 第 99–105 行将其作为活动结构；[Paper UI:219][ui-positions] 又把 P0/P1/P3/P4 贴在持久目录上。

**影响。** “当前在 P3”不能告诉作者哪个有界工作尚未完成、由谁处理、用了哪些输入、收据在哪里。P0–P4 混合容器、外部工作通道与动作，不能一一直接改名成 Runs。

**拟修。** Paper Workflow owner 依据中立 Run 合约建立唯一清单，字段至少包括 `spec_id / run_type / goal-target / actor-owner / inputs-dependencies / entry-exit / result-receipt / routes / cardinality / internal Steps`。将现有 `paper.*` 类型作为候选词汇逐项判断：可独立委托且可独立闭合的工作才保留为 Spec；单次选择、路由或门槛判定若只是控制动作，就作为 Gate/Route/control record。未开始的计划不伪造实例；已经在 Task/Discovery 等执行的工作只引用原生 Run。补充每个 Runtime 的实际 Run 清单与未满足依赖。

Story/Section/Round 继续持有长期内容与记录；G0–G5 保留既有决策权限。完成模型后再调整活动文案、目录分类和入口参数。旧路径若要兼容，使用明确 resolver/迁移表；不要把两份可安装 `SKILL.md` 留在递归扫描的 skills 树里。参数 `[phase]` 可先作为注明用途的旧适配参数，不能继续决定语义 Workflow。

**验收。** 从想法、Story、Section、编译、审稿回复任一入口，都能追到声明的 Spec 或明确的控制动作；实际 Run 有 owner、目标和收据。反馈、重试或一次工具调用不会自动增加 Workflow 行；状态答复给出待做工作、依赖和需要的已有门槛决定。活动说明不再把 Phase 作为流程单位，兼容字段有单独说明。

**依赖。** Paper Workflow 主责，Page/Run owner 对齐字段与生命周期；与 F04/F05 共同定合同，F06 和全家族文案迁移随后进行。

### F03 · P1 · Venue 当前模板及 bank 未提供技能要求的版本化合同

**位置与证据。** [Venue contract:93][venue-contract] 要求 `versioned_contract`，定义 current/partial/stale/superseded，并规定缺失/非 current 状态不能关闭 deep-fit、G0 或新的 Story/Section release。第 199–201 行又将它列入 closing checks。[template.md:1][venue-template] 全文 84 行没有该 block。本次对 `venue/bank/1-QBv-desks/QBv*/QBv*.md` 中文件名与父目录同名的 17 份当前 desk 页查找 `versioned_contract`、`contract_version`、`schema_version`，命中数为 0；这只是字段存在性核对。

**影响。** 人和代理无法从当前可复制范例获得一致交接接口。已有丰富正文不等于合同 current，读者容易把旧 `taste ✓` 或页面存在误作放行证据。

**拟修。** Venue owner 先统一模板和 schema，再建立一份 PACK-BACKED、一份 CfP-ONLY 的合规示例，随后逐页记录 17 份迁移状态。未核实的内容保持 partial/stale/UNKNOWN；不要只填日期就改为 current。消费者需绑定精确 contract version、target/category、官方来源 Result 和相关未知项，并保留旧决策所消费的历史版本。官方规则的重新采集是后续单独工作，不在本次计划审阅中宣称已完成。

**验收。** 模板有合法接口和诚实初始状态；两个 profile 均能产生可消费合同。17 份页面全部有迁移记录，允许仍不 current。partial/absent 可供 broad screen，但不能凭文件存在关闭 deep fit/G0；current 必须满足技能现有条件。无需新加一轮 Venue 人工批准，保留 `page_ruling: none` 与论文目标决策的区分。

**依赖。** Venue PageType 与 bank 子模块 owner 共同负责；Page CHECK、Ideation/Story/Section owner 核对消费端。F07/F08 随模板迁移处理。

### F04 · P1 · Paper-local Evidence/Display 的 owner、family 与 Task-lane 说法不一致

**位置与证据。** [page-integration:59][integration-owner] 把 `pm-/pa-/pr-` 称为 Task-lane Runs；[run-naming:10][naming-owner] 却将其 owner 写为 Paper Section/Round Page 的 Evidence/Display lane，第 167–176 行示例使用 `family: page`。[Section:96][section-runs] 又区分本地 typed Runs、Page interaction 和外部 Task。共享 [Page Run families:34][page-families] 当前定义 RP/RE/RD，并为 RE 给出 `re-value`、`re-display`、`re-cite` 标识。

**影响。** “在哪里执行”“哪个 Folder 拥有记录”“receipt.family 填什么”被混在一起。代理可能误派任务、生成无法匹配的收据，或错误地把证据结果计入写作前置条件。现有证据确认文档矛盾，尚未证明运行时已错派。

**拟修。** Paper、Page/Run、Task/Discovery、Display owner 共同确定 owner/worker/dialect 的区分，并说明 pm/pa/pr 与 RE 的关系：仍支持的 Paper 扩展、只读旧别名，或后续迁移对象。本文不自行决定新的 schema 值。以一份可执行的合同表统一 integration、naming、Section 和插件引用；已落盘 ID 保留，外部结果继续用完整原生地址，禁止复制成第二个执行记录。

**验收。** 对 Page 本地 Evidence、Display worker 输出、外部 Task Result 三个样例，所有说明指向同一 owner、identity、family、Ticket/Result 和 acceptance；不会因同一结果被多处引用重复计数；Evidence 完成不自动满足 RP 人类写作关闭条件。

**依赖。** 先明确共享 authority，再改 Paper adapter；不能仅做文字替换。

### F05 · P2 · Paper–Page 适配基线过期，仍要求新建已退役的 RP 标识

**位置与证据。** [integration:25][integration-baseline] 冻结于 2026-09-13 的三个 Page 文件 hash，并要求变更后重审；当前三个 SHA-256 均不同（见第 7 节）。[run-naming:77][naming-rp] 将 `rp00_mermaid-structure | rpNN_pNN[-pNN]` 称为 current，并要求每次从 rp00 开始；该文件第 211 行同时使用 `rp-struct-01`。共享 [Page families:38][page-families] 已把旧 rp00 标为 compatibility input，新分配必须用 typed RP。Page 与中立 Run 两个 owner 的现行说明对此一致。

[Page Workflow:57][page-workflow] 明说 serialized `phase/cycle/next_cycle` 不是语义权限或 Steps；Paper integration 第 34–42 行仍列两套 phases。Round 第 22–23 行要求 Page→PageType→PageWorkflow，与 [共享加载顺序:72][page-load] 不符。Section/Venue 的 “concrete Page RUN” 又容易把 Page 的整个自动 pass 当成 RP，尽管共享第 65–70 行规定它是 Workflow Runtime。

**影响。** 新上下文可能按过时指导分配 ID、加载错误的 authority，或把整个 Page pass、controller receipt 和有界交互 Run 混为一谈。冻结 hash 不能证明当前兼容。

**拟修。** 按当前共享基线重审并更新适配文档、umbrella、四个 PageType、Venue 和 assembly 的相关入口；明确 Runtime、RP/RE/RD、controller action。新分配使用 owner 现行 grammar，旧 rp00 保持可读历史。判断类 `ridea/rclaim/rtask/rnarra` 已在 naming 第 183–211 行明确为有目标的判断 Runs，不应随意降成 Step；应补它们对应 F02 的 Spec、owner 和出口，重复反馈仍是内部 Step。只有完成兼容核对后才更新基线 hash，不能机械抄新值。

**验收。** 新 Page interaction 示例不再要求分配 rp00；旧记录不重编号。加载顺序与共享 owner 一致；controller labels 不被重命名为 Steps/Runs；一次 Page Runtime 不额外计成写作 Run。判断完成不替代 I3、G3 或 Task 委托。

**依赖。** Page/Run owner 主导共享语义，Paper owner 完成适配；与 F02/F04 联动，保留其他任务的 Display Result 改动。

### F06 · P2 · 插件定义清单不完整，Run Type 与 Spec 尚未对应

**位置与证据。** [plugin:370][plugin-grammar] 将 Workflow 定义为记录移动及关卡，列 10 个 `paper.*` 类型；[space-mapping:7][space-map] 只有 9 行，缺少技能第 394 行的 `paper.section.route`，其 main/appendix folder 表也只列 story.route/compile/Page workflow。[UI:2589][ui-map] 正确标明这是定义视图；该句本身不是问题。

**影响。** 读者无法判断 Section 的独立路由是遗漏、合并还是未实现，也无法从类型地图找到某个目标所对应的 Spec 及实际执行。

**拟修。** 在 F02 后以 canonical Spec 清单派生或逐项校对地图，明确 Type→Spec→owner-native Instance/receipt；若 section.route 应为控制动作，显式合并并同步两表，不能为了补数量虚构 Run。保持地图只读及 planned/allocated 区分。Setup Apply writer 当前未实现的边界继续明确，不借此计划扩大为新建 writer。

**验收。** 每个活动类型/Spec 都有对应或注明合并/控制动作；地图不存在未解释的漏项。点击运行状态只能指向真实 owner 的记录；没有执行的工作保持 planned/unavailable，不能给出假成功。

**依赖。** F02；Paper Plugin 与 Board renderer owner 共同维护。

### F07 · P2 · Venue 模板未完整表达 CfP-only 分支和当前内容角色

**位置与证据。** [Venue profiles:49][venue-profiles] 明确没有 pack 时不能编造观察，只能有来源的 DESK RULE 或标明的 OWN ESTIMATE；第 71–78 行 authority 列表未说明 OWN ESTIMATE 如何归类。[template:44][venue-template-units] 无条件要求 “what the pack found / What the pack refuses / papers' own words”，前面的无 pack 提示只改变 unit 来源。技能第 123–152 行要求七种可检查的内容角色，但模板未给清晰的合同状态与 Gaps/Handoff 区域。当前模板第 25–27 行已明确 Diagram 不是 Page section，应保留。

**影响。** CfP-only 作者可能为了填满骨架而虚构 exemplar 观察；模板与技能不一致，增加人工解释和补栏成本。

**拟修。** 模板显式声明 profile，并按 profile 条件生成 unit guidance。无 pack 时显示观察 unavailable、已有官方规则和已标记估计；由 Venue owner 定义 OWN ESTIMATE 在 authority 类型中的对应。确保七种内容角色都可定位，但不要求恰好七个固定标题或 unit。合同与 gaps/handoff 直接复用 F03。

**验收。** 两种 profile 都可诚实填完，不凭空制造 pack 来源；没有来源的数值保留 UNKNOWN 或标明估计；结构角色能映射到技能，模板不恢复旧 Diagram/Files 章节。

**依赖。** F03 schema；Venue owner。

### F08 · P2 · Venue 活动参考入口仍携带旧地址与旧 Page 结构

**位置与证据。** [venue README:31][venue-readme] 仍称挂载于 `paper/_venue`，实际 gitlink 为 `paper/venue`，并使用旧 “venue stage” 入口。[QBv1:38][qb-misq] 自称其他页面模板，要求 `## Diagram` 和旧 Files 分组；[QBv17:23][qb-wise] 仍将 QBv1 作为参考，自己也在第 48 行保留 Diagram。Venue skill 第 58/62 行将两者列为参考实现。[PNAS template:1][pnas-template] 仍路由至 `2a-venue.md`、`0-lifecycle` 和 `stages/5-section-edit`；Section 第 225–227 行已规定这类旧材料只提供信息，不能成为 structure-source。

**影响。** 从当前技能跳到旧参考后，作者会看到另一套“必须”规则，可能复制错误的 Page 结构或找不到文件。推荐目标本身不是越权，但未说明如何回到当前 Ideation/Story 决策链会增加误读。

**拟修。** 主入口修正路径与 owner 路由；将两个“参考实现”迁移到现行模板，或暂改成明确的旧内容参考。对原始 playbook 的旧工作流命令加醒目的历史/参考说明及当前入口，不批量改写研究引文、观察值或所有历史 Phase 用词。保留 Section 的 EXACT/SHARED/ABSENT BY DESIGN/MISSING 四种关系；例如 MISQ 不存在独立 related-work 单元的情况，不应为了模板完整而捏造 desk 单元。

**验收。** 从 skill→template→reference→Section 的阅读路径只有一个当前 Page 结构权威；旧流程文字不会被当作可执行命令。活跃引用均可解析，历史来源仍可追溯。

**依赖。** F03/F07；Venue 子模块与 Paper Section owner 协调。子模块提交和根仓库指针更新单独 review。

### F09 · P2 · MISQ 摘要规则保留两套前后冲突的强制语气

**位置与证据。** [MISQ abstract style:52][misq-style] 禁止具体数值、要求不超过约 160 词；第 75 行说新例子不矛盾，第 79、84、101–102 行却明确 healthcare/policy 的 effect size 例外和约 185 词上限。[MISQ profile:27][misq-profile] 将 120–160 作为 target、185 作为 max；[builder venue_findings:823][builder-venue] 也输出对应检查发现。

**影响。** 只读前半的作者会删去后半允许的核心发现；读完全篇又要自行决定哪个禁令生效。pack 观察、作者策略和官方规则的界线也不够醒目。

**拟修。** 将规则收敛为一处当前说明：常规行为研究的表达建议、healthcare/policy 例外、目标区间及有来源的异常范围；历史补充保留为来源说明。profile/check 输出应注明它检查的是 pack 建议还是经核实的官方规则，必要时记录作者采用的 local policy。本文不把 160/185 宣称为现行官方投稿限制，也不未经证据更改机械阈值。

**验收。** 同一篇稿件不会因读到不同小节收到相反指令；观察/建议/官方规则各有来源与状态，style、profile、检查文案的含义一致。是否影响 ready 状态须由实施者核对实际消费者，本文未运行验证。

**依赖。** Venue 与 Assemble owner；F03 的 authority 分类可复用。

### F10 · P3 · PNAS 的 fit 指引与 Significance 写作入口缺少互链

**位置与证据。** [QBv13:9][qb-pnas] 描述两份指引断开；本次直接检查 [taste.md][pnas-taste] 与 [Significance style.md][pnas-style]，前者只提 significance statement 概念，没有通向 style 的路径，后者也没有返回 taste 的链接。template 有 style 路径，但仍是 F08 的旧工作流入口。

**影响。** 作者从任一端进入，需要自行搜索另一份材料，不清楚是在判断面向广泛读者的价值，还是已经在写具体段落。

**拟修。** 增加双向链接与一段读取顺序：先参考 paper fit/taste，再按当前 Story 的 Section row 和 Venue contract 写 Significance。taste 是本地编辑口味参考，不应新设为“允许写该段落”的官方资格审批。

**验收。** 两个入口都能一步找到另一份，且明确各自用途；没有新增官方 gate 或无来源的准入条件。

**依赖。** F08 当前路由；Venue 子模块 owner。

### F11 · P3 · Paper drawer 提示漏 Delivery，文案源位置说明不完整

**位置与证据。** [drawer JS:7][drawer] 称 four Spaces，第 42 行 hint 只有 Setup/Ideation/Story/Run；[renderer:2801][ui-spaces] 实际显示五个，包含 Delivery。[plugin:94][plugin-copy] 将 plugin labels/briefs/hints 归到 live/paper.py，未涵盖 JS 注册处。

**影响。** 作者不容易发现交付入口，维护者可能在错误文件改提示。

**拟修。** 将提示与五个实际 Space 对齐，并说明 renderer 与 drawer registration 各自的文案位置。仅修文案，保留现有只读路由。

**验收。** 文档、hint 与五个实际 Space 一致，Delivery 可被理解和定位。

**依赖。** 无模型依赖，可作为独立小改；Paper Plugin/Board owner。

### F12 · P3 · Ideation 的状态数量与 Round 的三个“轮次”需要更直白的说明

**位置与证据。** [Ideation:101][ideation-surfaces] 说“三个 states”却列语义源、working、released、delivery 四行。Round 第 60–63 行区别 Paper Round 与 Page workflow round，方向正确；[Page receipt:82][page-receipt] 确有 `round` 字段，[validator:656][page-round-validator] 明确何时递增；另有 [interactive writing:14][writing-versions] 的 Run/Version/Step 体系。

**影响。** 状态答复容易只报一个“最新版”，掩盖 working/released/delivery 的差异；“又开一轮”可能让作者不清楚是新 reviewer batch、controller 重开计数，还是同一写作 Run 的新 Version。未发现据此实际错建 Round 的证据。

**拟修。** Ideation 改成“一个语义源与三种 Page surface”，每项分别报告 revision/receipt。Round 补简短对照：Paper RD 标识反馈批次，controller round 是兼容收据计数，Version 是固定写作 Run 内的候选记录；各由其 owner 决定，不能互相推导。状态摘要优先报告 concern 覆盖、对应修改、待决定事项与冻结 build。

**验收。** sync 不创建 RP 或 I3 选择；重复反馈留在同一个固定目标的 Run/Version/Step 规则内。一个 reviewer 的多条意见仍进入同一批次 ledger，不按意见数创建 RD；`applied` 仍不等于 `answered`。只请求现有合同保留给人类的实质决定、最终回复和关闭，不增加逐条额外批准。

**依赖。** F05 的术语对齐；Ideation/Round 与 Page owner。

## 5. 修复顺序、责任与依赖

| 批次 | 具体产物 | 先决条件 | 负责人边界 | 完成标准 |
|---|---|---|---|---|
| A：生成目录保护 | F01 schema/path guard 与同步配置示例 | 无 | Paper Assemble；保留当前 Display 改动 | 非法 room 在任何写入前失败，源文件与上次产物安全；有效示例可用。 |
| B：共同语义合同 | F02 Run Spec/Runtime 清单；F04 owner/identity 表；F05 Page 适配决定 | 读取当前 Page/Run owner 与在途改动 | Paper Workflow 主责；Page/Run、Task/Discovery、Display 会签自己接口 | 每个有界工作、控制动作、Page 容器有唯一解释；兼容项与新分配规则明确。 |
| C：活动入口迁移 | umbrella、四 PageTypes、Venue/assemble 入口、README/路径索引、F06 插件地图 | B | Paper + Board；涉及路径时由安装/路由 owner 核对递归发现 | 九份技能与 UI 使用同一模型；旧路径可读且无重复安装；地图与清单对应。 |
| D：Venue 合同与范例 | F03 schema/template、F07 两种 profile、F08 两份参考实现，再覆盖 17 页迁移状态 | 合同设计可与 B 并行；消费端整合等 B | Venue PageType、bank 子模块、Ideation/Story/Section | 两类模板诚实可用；未知项可见；合同版本可被精确消费。 |
| E：阅读与交互精简 | F09 MISQ、F10 PNAS、F11 Space 提示、F12 状态摘要 | F11 独立；其余依赖相关合同稳定 | 对应文件 owner | 一处现行指令、一处来源；用户能读出当前产物、待做工作和下一决定。 |
| F：获准实施后的验收 | 定向静态检查、临时目录安全检查、真实入口的新上下文场景记录 | A–E 对应改动已完成且允许验证 | 相关 package owner；技能验证按根 README | 记录结果及未覆盖平台/环境，不将静态阅读写成测试通过。 |

若只能先做最小修复，顺序是 **A → B 的共享合同 → C 的入口与适配 → D 的合同范例 → 其余文字与银行逐页刷新**。D 的完整官方来源刷新可能耗时，不应阻塞 A，也不应通过把所有页面标成 current 来缩短工作。

不为术语统一另建 Application 父家族。当前 [Insight Workflow:35][insight-current] 已列 Definition/Runtime 并声明无 Phase；[Design Workflow:48][design-current] 同样无 Phase layer。Paper 仅通过双方声明的资源/Result 交接，不能接管它们的 Workflow、Folder 或 native Run 编号。本次只核对该边界，不替代这两个家族的评审。

## 6. 后续验收场景与需要保留的交互约束

以下都是实施后计划，不是本次已执行结果。

1. **Workflow 身份检查。** 从九个 skill 入口追到同一 Paper Spec 合同，检查 `Phase`/P0–P4/旧参数的每个活动命中。语义违规应消除；历史 changelog、源码序列化字段、兼容路径逐个注明，不做“零字符串命中”式验收。实例清单可为空，空清单不能冒充有 Run 成功。
2. **想法→Story。** 生成与讨论 Idea 后，只有 I3 的有效人类选择能 admission；judgment Result、sync、Page CHECK 都不能代签选择。展示语义源和三个 Page surface 的版本差异。Venue partial 可用于筛选，不能假报 deep fit/G0 已过。
3. **Story→Section。** C1–C8 仍是前瞻内容蓝图；G1 可只释放部分研究，G2 接受空/矛盾结果，G3 逐 Section row 释放。没有必要等待整篇所有研究结束才允许一个已获授权的 Section 工作。Section resolver 保留四种关系，缺失与设计上不存在分别处理。
4. **Section 写作与证据。** 新 RP 用当前 grammar，普通反馈为 Step，同目标重开为 Version，目标变化才按 owner 规则新建 Run。Page Evidence、Display payload、外部 Supporting Runs 的 owner 与路径可追溯，不重复计数，也不覆盖旧 ID。
5. **整稿与审计。** 用临时 fixture 验证 F01；完整 build 的内部拷贝/渲染是编译 Run 内动作。ready 必须符合 G4 的完整入选 Section 集合与人类判断；早期 build 标 DRAFT。只读 audit 继续读取指定产物和 manifest，不因“检查”暗中 rebuild。manifest 保持唯一 delivery receipt。
6. **审稿回复。** 一批反馈绑定一个 base build；每个 concern 一次登记、明确 disposition/owner、关联返回的版本与回复。保持已应用修改与已回答意见分离，保留原始与回复 build。实质性取舍、最终 response/closure 仍由既有规定的人类负责；状态输出不把起草、建议或等待决定写成已批准。
7. **新上下文技能验证。** 根 [README:131][fresh-context] 要求技能改动后用 fresh-context subagent 做真实调用，并确认选择、遵循、结果。后续实施时遵循此要求，记录每条修改过的入口及共用场景；本次仅写计划，没有启动这项验证，也未新增测试。

状态答复可以统一为简短四项：**当前目标和 owner；已接受 Result/版本；尚未满足的依赖或 gate；作者下一项已有权限内的决定。** 把详细 schema、历史术语及迁移解释留在引用文档，减少重复全文加载和额外审批。

## 7. 证据限制与尚需决定的事项

- **已确认：** 12 项的文本/代码证据；九份技能范围；17 页合同字段缺失；安全目录校验缺口；当前 Page 与 Paper RP grammar 冲突。以上都来自本地只读核对。
- **尚未验证：** 运行时消费者是否在每个入口严格执行 Venue current 门槛；所有 pm/pa/pr 记录的真实 owner；既有论文会受多少影响；各平台编译及 UI 行为。不能从文档推导这些已通过或已失败。
- **需要 owner 定义：** pm/pa/pr 与 typed RE 的最终关系；哪些 `paper.*.select/route/setup` 是可闭合 Run Spec、哪些为控制动作；judgment Runs 与 canonical Spec 的绑定。必须依据目标和关闭条件决定，不能只依据名称。
- **不属于本次核实的事实：** 期刊最新字数、日期、费用、模板与官方提交规则；未联网重新查证，也未把本地 pack 说法当作当前外部事实。需要刷新时，应取得官方来源并留下 Result 与访问日期。
- **并行工作限制：** 当前 Page/Display/Insight 的改动仍未提交。实施前重新检查差异和 owner 合同，不能按本文行号覆盖他人工作；已观察到的 Insight 文案修正无需再做。

Paper adapter 当前记录的三个 Page 基线 hash 与本次读取值如下；这是漂移证据，不是兼容性通过证明：

| 文件 | adapter 中的 SHA-256 | 本次读取 SHA-256 |
|---|---|---|
| `page/haipipe-page/SKILL.md` | `64cca86d33b52a3a51ed5019d9cd84cb44555a4e8ec0acd5f15d5bef505982d` | `bfc7a4927d9e8cb52aa74fa0e832c5604b997dda59ef96e104a4fb88a5b3b200` |
| `page/page-workflows/haipipe-page-workflow/SKILL.md` | `e1eee1209ab87cd1e076fdf89cd573dc359c560002b2a92ffdf9977975a8a1a` | `2ccb22c9a027614c1c778c71c9ff5b7ec1738933da46970289c5181c19cbd533` |
| `page/page-workflows/haipipe-page-content/SKILL.md` | `20eefbc8122c8c22560d989a0363adda92243b5ca0bb95aeb640c0f7476d1ef` | `c2429be18d912f4ae0db44f85ca8a7121c17bf95ab7fe87ef0c40acb2895951c` |

本文的交付范围到此为止。后续修复须按具体授权推进；本任务不修改技能、代码、子模块、原评估或其他家族报告。

[paper]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/SKILL.md:28
[workflow]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-workflow/SKILL.md:21
[plugin]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-plugin-paper/SKILL.md:370
[assemble]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/SKILL.md:289
[venue]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-venue/SKILL.md:21
[ideation]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-ideation/SKILL.md:29
[story]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-story/SKILL.md:21
[section]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-section/SKILL.md:25
[round]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-round/SKILL.md:22
[config-example]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/ref/paper-build.toml.example:1
[assembly-config]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/SKILL.md:295
[builder-path]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/scripts/build_delivery.py:55
[builder-order]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/scripts/build_delivery.py:142
[builder-delete]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/scripts/build_delivery.py:987
[workflow-model]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-workflow/SKILL.md:21
[paper-verbs]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/SKILL.md:227
[ui-positions]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/paper.py:219
[venue-contract]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-venue/SKILL.md:93
[venue-template]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-venue/template.md:1
[integration-owner]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/ref/page-integration.md:59
[naming-owner]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/ref/run-naming.md:10
[section-runs]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-section/SKILL.md:96
[page-families]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/ref/page-run-families.md:34
[integration-baseline]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/ref/page-integration.md:25
[naming-rp]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper/ref/run-naming.md:77
[page-workflow]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md:57
[page-load]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md:72
[plugin-grammar]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-plugin-paper/SKILL.md:370
[space-map]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-plugin-paper/ref/space-mapping.md:7
[ui-map]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/paper.py:2589
[venue-profiles]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-venue/SKILL.md:49
[venue-template-units]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-venue/template.md:44
[venue-readme]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/README.md:31
[qb-misq]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/bank/1-QBv-desks/QBv1-misq/QBv1-misq.md:38
[qb-wise]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/bank/1-QBv-desks/QBv17-wise/QBv17-wise.md:23
[pnas-template]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/playbook-pnas/pnas/pnas-significance/template.md:1
[misq-style]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/playbook-utd-is/MISQ/MISQ-abstract/style.md:52
[misq-profile]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/profiles/misq.toml:27
[builder-venue]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/scripts/build_delivery.py:823
[qb-pnas]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/bank/1-QBv-desks/QBv13-pnas/QBv13-pnas.md:9
[pnas-taste]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/playbook-pnas/taste.md:1
[pnas-style]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/venue/playbook-pnas/pnas/pnas-significance/style.md:1
[drawer]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/assets/js/10-drawer/09-plugin-paper.js:7
[ui-spaces]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/paper.py:2801
[plugin-copy]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/haipipe-plugin-paper/SKILL.md:94
[ideation-surfaces]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/paper/workflow-phases/haipipe-paper-ideation/SKILL.md:101
[page-receipt]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/page-run-contract.md:82
[page-round-validator]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/src/page_lifecycle.py:656
[writing-versions]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:14
[insight-current]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md:35
[design-current]: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:48
[fresh-context]: /Users/jluo41/Desktop/Tools-SPACE/README.md:131
