# Page 家族技能与交互审查

## 1. 快照与结论

- 审查日期：2026-09-20；基线及当前 HEAD：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。
- 当前工作树另有 8 个已修改的 `references/` 子模块：`cite-guard`、`grant-writer-skills`、`paper-rag-skill`、`paperspine`、`reprorun`、`research-agent-skills`、`research-co-pilot`、`scipilot-figure-skill`；另有未跟踪的 `evaluations/`。这些不是本次审查产生的改动；本次唯一写入是本报告。
- 所有 15 份当前 Page 家族 `SKILL.md` 均已逐份阅读并与技能清单/磁盘文件核对。审查还检查了相关引用、模板、代理说明和用于核对文档所述行为的少量本地 presenter/runtime 源码。
- **总体判断：人类写作协作、反馈、验收与交付的边界设计扎实；Workflow/Run 指标不通过。** Page 仍把 Workflow 定义成 Loop/阶段控制图，phase 既是重复工作的单位，也是当前界面与活跃指令里的用词；部分资料又把 controller-only 节点排除在 Run 外。这与要求的“Workflow 是 Runs 列表；工作流单位叫 Run，不叫 Phase”存在定义级矛盾。不能靠全局字符串替换修复：必须先确定 Workflow 中列出的 Run Spec 与已分配 Run Instance 的关系，并把非 Run 的 gate/router 控制信息放在 Run 单位之外。
- 这次只做文档/交互审查：没有执行被审查的工作流、没有调用外部服务、没有运行测试，也没有修改技能或代码。源码检查只是确认文档所称的 UI/action 是否存在；以下 walkthrough 均为桌面推演，不是现场用户测试。

## 2. 覆盖清单

以下 15 份是当前磁盘上的完整技能清单，全部逐份阅读。右栏概括检查的活动支撑材料；“Workflow/Run”按本次强制指标评定，而非按内容质量评分。

| 技能 | 已检查的支撑材料与交互面 | Workflow/Run |
|---|---|---|
| `plugins/haipipe-toolkit/skills/page/haipipe-page/SKILL.md` | `fn/runs.md`、`fn/serve.md`、`fn/reflect.md`；`ref/glossary.md`、`page-run-families.md`、`page-template.md`、`page-checklist.md`、`standalone.md`、`user-check-packet.md`；Page/Board Outline presenter、Page workflow stepper 与 standalone picker 源码 | **失败**：glossary 明确把重复单位定义为 phase；当前用户包仍显示 phase。RP/RE/RD Run 和内部 Step 的局部边界较清楚。 |
| `plugins/haipipe-toolkit/skills/page/haipipe-workbench/SKILL.md` | `ref/roster.md`；Page 插件选择器脚本与独立页面工作区 picker | **部分**：将 Page 生命周期展示成 phases；与当前实际插件入口和 roster 中已移除的控件不一致。 |
| `plugins/haipipe-toolkit/skills/page/haipipe-sentence/SKILL.md` | 句子级反馈说明、comment/change/typed-lane 控件相关源码 | **不适用**：它定义句子反馈动作与标记，不定义 Workflow；内容本身区分已发布评论与 Draft Run 反馈。 |
| `plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/delivery.md` | `ref/latex.md`、`word.md`、`slide.md`、`render.md`、`servers/workbench-page/exporters/README.md`；与 Design render 写入端的契约对读 | **部分**：RD/交付收据和各输出很明确；Render manifest 与 Design writer 对同一文件采用不同 schema，LaTeX/Word 引用的 display 路径也与 Evidence 当前契约冲突。 |
| `plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/SKILL.md` | `ref/space-mapping.md`；Design actions/runtime；Page Delivery Render 约定 | **部分**：独立 Design 家族和 `rdNN` 记录明确，但用户可见的 `STEPS` 把独立 Run 记录显示为 Steps。 |
| `plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/folder.md` | Page roster、Outline/Studio/Delivery/Folder 的插件顺序说明、当前 picker | **不适用（此技能不定义 Workflow）**：Folder 是材料/导航 surface；当前发现的是 Runs 顶层位置等导航说明陈旧，而非本技能把 Phase 定义为工作单位。 |
| `plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/SKILL.md` | `ref/content-preview.md`、`evidence-bundle.md`、`evidence/citations.md`、`displays.md`、`pagex.md`、`values.md`、`item-table.md`、`plan-grammar.md`、`record-shape.md`、`review-packet.md`、`skill-record.md`、`space-mapping.md`、`specimen-section-plan.md`；Board Outline live presenter | **部分**：Run Spec/Run 分层和 Step 语义总体好，但 reader-facing Page 结构陈述过时，space mapping 仍将旧标签映射为 Workflow phase。 |
| `plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/run-space.md` | Page 共享 roster；中立 `plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md` 的身份、计数、Step 边界 | **通过（本技能局部模型）**：区分 Workflow map/Run Specs 与 Run instances；明确不把 Step、gate、工具调用或兼容 label 升格为 Run。共享 roster 的旧 phase/pass 说法仍需同步修正。 |
| `plugins/haipipe-toolkit/skills/page/haipipe-workbench-studio/SKILL.md` | `ref/chat.md`、`ref/draw.md`；Board `servers/workbench-studio/chat.py` 活跃系统提示 | **失败**：Studio chat 资料与活跃 prompt 把交互按 5 个 Page phase 派发，prompt 要求每条回复显示 phase/cycle；Draw lane 有清晰的对象所有权与写入确认边界。 |
| `plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-check/SKILL.md` | Page check agent、`agents/README.md`、Board `approve-rules`、用户检查包 | **部分**：CHECK dispatcher 被称为非 Run，但仍以 phase 为路由单位；用户闸门卡漏显示 owner ruling 和完成计数。 |
| `plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-content/SKILL.md` | `ref/paragraph-run.md`、paragraph promotion 源码、interactive writing Run、user-check-packet | **部分**：将 paragraph feedback 放在 Run 内的 Step 边界清楚，但 CONTENT 发布门槛与 Outline 冲突。 |
| `plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-context/SKILL.md` | `ref/context-record.md`、workflow contract、用户检查包 | **部分**：PREPARE 被视为 phase 内周期；流程层仍由 phase dispatch 组织。 |
| `plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-evidence/SKILL.md` | workflow Evidence lane 段、Outline evidence 的 citations/displays/values/pagex、item-table、用户检查包 | **部分**：RE 身份、内部步骤和输入/结果冻结边界明确；Workflow 仍按 Evidence phase 表述，且 Workflow SKILL 引用了已退休路径。 |
| `plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-outline/SKILL.md` | Outline agent；`record-shape`、`content-preview`、`review-packet`、`plan-grammar`、`item-table`、`space-mapping` 及 evidence 子引用；Scratch/用户包说明 | **部分**：结构/提案/已分配 Run 边界好；仍称 Outline 为 phase，且 Shape 批准/CONTENT 发布条件存在互相冲突的规则。 |
| `plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md` | `interactive-writing-run.md`、`writing-step-template.md`、`workflow-table.md`、`phase-cards.md`、`page-run-contract.md`、`producer-contract.md`、`structure-run.md`、`interactive-execution-policy.md`、`post-run-analysis.md`、`measured-cost.md`；五个 workflow agent 与 README；共享检查包、Run families、Board approve-rules | **失败**：定义为 Run Spec 有向图，表中包含不实例化 Run 的 controller 节点；和所需“Runs 列表”不是同一模型。 |

### 范围核对与未读项

- 15 份技能清单与磁盘中 Page 路径下的当前 `SKILL.md` 数量/文件名相符。另读了中立 Run 合约，用来判定“Run 或内部 Step”；它不是 Page 技能，未对其全部依赖族进行全面审计。
- 除表中明确列出的文件外，未逐行阅读 Page guide 样例目录中的全部生成页面、版本快照、HTML/PDF/DOCX 等资产，也未审查外部/第三方 `references/` 子模块的全部内容。它们不是当前 Page 指令权威；8 个子模块只有 git 状态核对。
- 历史 CHANGELOG、历史用户反馈和归档内容未作为当前行为证据；个别技能在文内明确标记的历史兼容说明仅用于辨别历史词汇。没有把其当作当前 UI 的实测结果。
- 未读其它所有家族技能的完整内容（除中立 Run 合约和共享 Board approve-rules 外），因此跨家族归属意见只限于报告中点名的接口/文件；需要协调者对相邻家族作契约确认。

## 3. 总体质量与建议保留的设计

Page 的人机协作设计有值得保留的强项：

- `page/haipipe-page/fn/runs.md:12-59,163-223` 将建议列表设为只读候选，在用户选定前不分配 typed RP ID、Ticket 或 Result；优先恢复匹配的 open Run，避免重复建单，并把外派 Task 输出留在原生 owner。
- `page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:23-55,150-193,239-285` 与 `writing-step-template.md` 把一个可闭合目标定义成 Run，把原始反馈、候选文本、评分、诊断和修订保存为该 Run 中的 Step/Version。保存或应用不等于用户接受。
- `page/haipipe-page/ref/user-check-packet.md:28-129,131-244` 按用户可读顺序呈现范围、完整候选文本、状态与直接证据链接；Draft、Evidence Result、已采用 Content 与 Page PDF 有区分。
- Draft Table/Reading 只读、Scratch 是唯一浏览器写入口的原则在当前 Outline 说明与 `outline.py` presenter 中一致。句子技能也清楚区分发布后的 comment rail 与 Draft Run 内反馈（`haipipe-sentence/SKILL.md:55-61,74-84,150-184`）。
- Content 与 Evidence 技能反复说明 adopt/build/pre-check 等动作是 Run 内部动作或 Step，不自动新建 Run（`haipipe-page-content/SKILL.md:27-34,75-87,119-138,159-220`；`haipipe-page-evidence/SKILL.md:23-30,105-119`）。Design 插件把 Goal、项目状态、责任人与用户可读操作解释得好（`haipipe-workbench-design/SKILL.md:60-88,243-268,398-460`）。

## 4. 优先问题与建议

### P1 — 定义中的 Workflow/Phase 与必需 Run 模型相反

**证据。** Page glossary (`page/haipipe-page/ref/glossary.md:174-181`) 将 workflow 写成“which LOOP this is. Never repeats.”，把 phase 定义成重复的 authority；`:215-218` 进一步说 controller step 是 numbered phase dispatch，RUN 允许重复 phase。其引用的 workflow SKILL (`page-workflows/haipipe-page-workflow/SKILL.md:23-30,254-257`) 又将 Workflow 定义为 Run Spec 的 directed graph；表的 `:334-347` 含 Context/Check 等不产生 Run Instance 的 controller 行。共享 Run 合约 `plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:35-58,113-124` 也将 Workflow 写成完整 graph，并明确 router/pass 不一定是 L4 Run。

**问题与影响。** 这不是旧 API 字段的残留：phase 是 glossary 中的工作单位、技能中的调度概念，也是可见的 workflow 展示。Agent 会按 authority/phase 开始“下一段”，将同一持续目标拆成 pass；用户会看到 Phase 流程，却无法判断哪些是 Workflow Runs。controller-only 行又让“Workflow 的节点是否为 Run”没有一致答案。

**建议。** 先在 Page、Run、Workflow/Outline 三处共同改定词汇与图模型：Workflow 展示有序/有路由的 planned Run Specs，并投影出已分配的 Run Instances；Run 内含有界目标、close rule、Steps；必要的路由/gate/controller 数据放在列表之外作为控制信息。删改 live Phase 工作单位定义、phase producer roster 和 phase 表行，但保留并明确标注当前序列化字段/路径兼容层，例如 `workflow/phase.yaml`、`phase`、`start_phase`、`next_cycle`、`--phase`，直到读写方迁移完成。不要把每个 PREPARE、SHAPE、tool call 或审批点击变成独立 Run。

### P1 — 活跃 Studio prompt 仍强制五阶段派发

**证据。** `servers/workbench-studio/chat.py:702-725` 以五个 indexed phases 和 cycle 组织回复，要求每次答复显示 phase/cycle，并规定 WRITE、重复 phase 与 per-commissioned-paragraph Run。插件引用 `haipipe-workbench-studio/ref/chat.md:112-153` 同样称 chat 是 interactive RUN controller、把动词派给 phase，并把每个 pass 称为 Run；而前文 `:25-30` 又说 chat 本身不构成 Run。新 interactive writing 契约把普通反馈定义为现有 Writing Run 内的 Step。

**问题与影响。** 这段是会作用于现场 agent 的 system prompt，不是纯历史措辞。它可能导致每条回复强行带阶段标签、把用户的反馈误当新 phase/pass、过度派单，或将普通段落反馈错误地建成一次 Run。

**建议。** Studio/Board prompt 一起改：助手先定位现有开放 Run 和当前 Step，普通反馈续写在其内；仅当用户选择/直接委托一个可独立关闭的新目标时提议/分配 Run；Workflow 展示 Runs。若旧控制器仍收 `phase`，仅把该字段当兼容 dispatch 坐标，不在用户话术中称它为 Run 或当前工作单位。

### P1 — Outline Shape 批准与 CONTENT 发布授权有冲突

**证据。** `page-workflows/haipipe-page-content/SKILL.md:69-73` 与 `page-workflows/haipipe-page-workflow/SKILL.md:514` 认为用户明确要求继续 CONTENT 足够，即使历史 `approved:` 为空；`page-workflows/haipipe-page-outline/SKILL.md:573-600` 则规定未勾选 Content-release gate 必须 HOLD，且要求批准的 G>=1 Shape。`haipipe-workbench-page/ref/plan-grammar.md:276-280` 把明确批准描述为 promotion/release 事件，`review-packet.md:74-82` 说泛泛聊天反应不等于批准。

**问题与影响。** 用户会被告知“已授权进入 CONTENT”，同时流程又要求 HOLD。Agent 可能擅自把“go ahead”当成对特定 Shape 的批准，也可能重复要求用户对已经接受的 Shape 再授权。

**建议。** 由 Outline 与 Content owner 明确唯一规则，并区分两个可能不同的决定：对某个 Shape 版本的批准，以及明确采用已批准 Shape/启动 Content Run。每种决定都说明接受的对象、用户可见确认语和被记录的字段；同一回复是否可同时作两种决定也要写清。

### P1 — 共享 roster 提供了当前界面不存在或明确禁止的动作

**证据。** `page/haipipe-plugin/ref/roster.md:43` 说 Draft Space 有 note composer，会将反馈追加到待处理 Step；但 Outline SKILL `:325-343,453-470,610-615` 规定只有 Scratch 可写，Draft Table/Reading 只读，无 feedback composer，且当前 `servers/workbench-page/outline.py:3278-3299` 只有 `action:scratch` 并拒绝旧 feedback action。roster `:41` 说 Run Space 有 Scripts 区域；`haipipe-workbench-page/ref/run-space.md:163-167,344-368` 明确禁止在 Run Space 展示 Scripts tree/summary。roster `:35` 仍描述人类 Adopt 决定，当前 Design SKILL `:413,419-426` 说 Verify 后没有此类 decision Run/门槛，`servers/workbench-design/design.py:1659-1660` 拒绝 adopt 等旧 action。

**问题与影响。** roster 被 Studio、Delivery、Runs、Folder 多个技能共同引用，是跨页面的权威清单。它会让用户/agent寻找不存在的 composer、Scripts 区域或 Adopt 控件，或对旧写入路径发请求。

**建议。** 以当前 presenter 与 action handler 为准更新共享 roster，一处删掉已退役控件；若要记录旧路径，在单独的历史/兼容说明中标清“不在当前 UI”。同时审阅依赖 roster 的插件说明，避免它们复制旧行为。

### P2 — Design 与 Delivery 对同一 Render manifest 定义了互不兼容的格式

**证据。** Design SKILL `../design/haipipe-workbench-design/SKILL.md:261-268,419-427` 把 `delivery/render/manifest.json` 绑定到确切 Generate candidate，并称 Verify 是 readiness gate。当前 `servers/workbench-design/design_actions.py:525-538` 把它当按 item/candidate/version 递增的 JSON list，复制候选字节并写 `render`、`sha256`、`version`；`servers/workbench-design/design.py:651-654` 也按该列表读图。Delivery `haipipe-workbench-page/ref/delivery.md:15-21,23-39,57-59` 却定义一个带 design/warrants/render 三个 stamp 的单 artifact/version 文档，并包含人类 accepted 状态。

**问题与影响。** 同路径会被两个插件按不同 schema 读写。Design 可能生成 Delivery 无法读的 list；Delivery 可能覆盖 Design 用于预览的结构。谁负责“ready”也可能从 Verify 门槛漂移成人工 render acceptance。

**建议。** Design owner 与 Page Delivery owner 明确资源归属、路径和 schema。可将 Design 的候选预览/验证清单与 Page 内容的交付 Render 收据分别命名/存放；或统一 schema 并提供迁移/读兼容。单独规定 Design Verify readiness 与交付 artifact acceptance 的关系，避免把 Design 记录错误当作 Page 整页接受。

### P2 — Page reader-facing 内容结构在 Outline 插件中仍是四区

**证据。** `haipipe-workbench-page/SKILL.md:151-166` 把 Page 展示为 Opening、Outline、Content、Aims 四个 reader-facing section；新 Page 主说明 `haipipe-page/SKILL.md:586-633` 和模板 `ref/page-template.md:16-22,29-37` 只定义 Opening 与 Content，Outline/Aims 为 backstage 工作面；`ref/page-checklist.md:46-67` 也保持两部分结构。Outline `:438-445` 还称生成的 compact Outline table 位于 Board page，容易与 Page 正文中的 Outline reader section 混淆。

**问题与影响。** 实施者可能在最终 Page 中多渲染两个流程/计划区，把作者工作台内容暴露给读者，或误删 Board 中的独立投影。

**建议。** 明确区分文章（仅 Opening/Content）与 Outline tab/Board 的工作投影，并更新 Outline 插件的渲染说明和例子。保留后台 Outline 数据，不把它作为第三个 Page 内容区。

### P2 — Outline space mapping 把兼容标签呈现为 Workflow phase

**证据。** `haipipe-workbench-page/ref/space-mapping.md:28-43` 的标题为 `Workflow phase`，并把 SHAPE/SURVEY、LAND/EMBED、CHECK 映射到“工作阶段”，其中 `CHECK` 指向 Delivery Space；紧接着 `:45-78` 的规范表却将单位定义为 Run Specs，并把 Check 描述成跨 Draft/Evidence/Runtime/Delivery 的只读检查。Workflow table `page-workflows/haipipe-page-workflow/ref/workflow-table.md:5` 也说旧 controller labels 不是 Phase authority。

**问题与影响。** 读者会按旧标签把 SHAPE、LAND、CHECK 当成独立 Workflow 单位，或者只检查 Delivery，而不是审查 Page Check 实际要读的多处证据；这与同一文件的 Run Spec 投影表相互矛盾。

**建议。** 将前表标为“legacy controller label → owning Run Spec / routing surface”的兼容映射，明确 label 本身不是 Run；把 CHECK 映射成整体检查规则及所需证据面，不能造一个 Check Run，也不能把它缩成 Delivery-only 工作。

### P2 — Workflow 指令引用已退休 Evidence 路径

**证据。** `page-workflows/haipipe-page-workflow/SKILL.md:280-281` 说可从 `outline/evidence/display/`、`outline/evidence/bibex/` 与 `delivery/latex/` 读取；Outline 当前 evidence refs `haipipe-workbench-page/ref/evidence/displays.md:180-185` 与 `citations.md:107-109` 已退休前两条路径；`user-check-packet.md:239-244` 明确禁止读取/返回这些位置或 fallback；Page Evidence `SKILL.md:369-378` 也称旧 `outline/evidence/` 已归档。

**问题与影响。** Agent 可能引用过时预览/引用来源，让用户检查到 stale artifact，或在未找到文件时走到不安全的 legacy fallback。

**建议。** 将允许读取来源写成当前 RE Result payload/Card 路径与 Page-level `delivery/latex` PDF；display 的 `preview.pdf` 明确来自相应 RE Result payload。将旧路径只列在明确的历史/迁移说明里，不与“eligible current evidence”放在同一句。

**补充冲突。** 这不只出现在 Workflow SKILL：当前 Delivery refs `haipipe-workbench-page/ref/delivery.md:38-39` 和 `word.md:36-37` 仍把 `<page>/outline/evidence/display/` 定义为正在使用的 display 来源，Word `:29-30` 仍从 `bibex/<stem>.bib` 读当前引用。需由 Evidence 与 Delivery owner 共同确认实际兼容边界和当前写入源；仅从 Workflow 文档删除旧路径不足以修复。

### P2 — Run 的 `Held` 状态没有出现在已定义的状态枚举

**证据。** `page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:176-179` 列出 `ready/running/waiting-for-feedback/blocked/complete`；`:187-190` 又要求中断的 Step 必须投影为 `Held`，而不是 `Waiting`。

**问题与影响。** `Held` 未出现在枚举中且大小写不一。恢复逻辑、状态卡和用户无法知道这是 blocked、等待用户反馈，还是另一个合法状态；中断 Run 可能无法一致恢复。

**建议。** 使用既有状态枚举中的一个值（例如 `blocked`），并在独立字段记录 interrupted Step 与原因；或者将 `held` 正式加入 schema、定义它与 waiting/blocked 的转移条件，再同步 Run contract 和用户包。

### P2 — Check 人工决策卡未呈现完整闸门状态

**证据。** `page-workflows/haipipe-page-check/SKILL.md:253-256` 的只读 collecting card 显示 approved/verified/read/accepted，但不显示 owner RULING 或总数；待办 ledger 只能从 CLI 查看。该技能 `:203-220` 又采用 `ACCEPT-BIASED`/“CONFIRMATION, not an inspection”表述。

**问题与影响。** 用户难以知道还差哪个责任人决定、是否所有必需条件都已满足，也难以复核同意的基础。把闸门设计成倾向接受的确认步骤，会弱化真实检查。

**建议。** 卡片列出每个声明的 gate、owner、evidence、状态和 x/n 完成数，并链接到实际写入面。保留预先汇集证据以减少搜索成本，但把问题改成中立的 approve/revise 选择，并展示完整依据。

### P3 — Design 详情把 Run 记录标成 `STEPS`

**证据。** `../design/haipipe-workbench-design/SKILL.md:166-167` 的单项时间线标题为 `STEPS`，例子是 Commission ✓ → Generate ✓ → Verify ✓ → Delivery；但 `:408-417` 把 Commission/Generate/Verify 说明为各自 `rdNN` Run，且 `:413` 明确 Delivery-ready 本身没有 decision Run。`ref/space-mapping.md:6,8-9` 也称这些为 Steps。

**问题与影响。** 用户无法区分显示对象究竟是执行 Run，还是某个 Run 的内部操作；把 ready handoff 当成 Run 还会导致错误计数。Insight 与 Design 是独立 first-class 家族；Page 可以消费它们的 Supporting Runs/Results。`haipipe-workbench-design` 是 Page 展示/接入面，不意味着 Design 从属已退休的 Application 父族。

**建议。** 若时间线记录的是 Commission/Generate/Verify 的独立 `rdNN`，将标题改为 Runs/Run history；将 Delivery-ready 显示为派生状态或 handoff，不增加 Run。对非独立可关闭操作则保留 Step 一词。

### P3 — 页面插件入口和 Folder 排序说明彼此不一致

**证据。** `haipipe-plugin/SKILL.md:89-91` 把“Page phases stepper”列为 Plugin picker 项，但 picker 脚本 `board/assets/js/10-drawer/65-plugin-pageflow.js:1-27` 将其标为 internal lifecycle view/no Plugin row；`page_workspace.py:300-318` 的独立 picker 项是 Outline、Delivery、Folder、可选 Labeling。另 `haipipe-workbench-page/ref/folder.md:37-40` 说 Folder 位于 Outline、Studio、top-level `⚙ Runs`、Delivery 之后，而共享 roster `:34,39-43` 与 Runs `SKILL.md:21-26` 把 Runs 放在 Outline 内。

**问题与影响。** 新上下文中的 agent 可能寻找不存在的 picker 行，或把 Runs 作为顶层插件误放进导航。

**建议。** 以当前各运行时 picker 为准，分别写 Board 与 standalone UI 的有效项；将 Run Workspace 明确说成 Outline 内的区域，而非顶层 Plugin；把 lifecycle stepper 只写作内部/只读状态投影。

### P3 — 用户检查包仍用 Phase 表示下一状态

**证据。** `page/haipipe-page/ref/user-check-packet.md:208-216` 在无内容时显示 `no Content yet · phase <PHASE>`；同一文件 `:1-26` 还称之为 phase receipt。当前协议中有明确 Run 状态和下一动作可展示。

**问题与影响。** 即使只是一行状态，用户也被引导继续按 Phase 理解后续工作。

**建议。** 改为当前 Run 状态与下一步，例如 `no Content yet · next Run: <Run name/status>`；若需要保留历史 phase receipt，标注为 controller compatibility receipt，而非下一工作单位。

## 5. 代表性交互桌面推演

以下是根据指令、模板与可见字段做的桌面推演，用于判断用户能否理解下一步；**不是实际点击/运行结果，也不是观察到的用户测试**。

1. **段落改动：**用户说“把 S2 的分母说清楚”。若已有匹配 open RP，合理路径是续用同一 Run，先展示该 Step 的范围与原文，原样保存反馈，形成受限候选及窄范围检查，然后返回完整段落。应报告“已保存/已应用，等待你验收”，不能把保存、应用或模型判断说成用户已接受。当前 Run 模型有支持；Studio prompt 的 phase-by-phase 回复要求是干扰。
2. **“我现在需要做什么？”：**展示只读候选及每项范围/阻塞，不预先分配 typed ID；用户选择后续用匹配的 Run；外派 Discovery/段落产物仍留在其 Task/owner。`fn/runs.md` 做法明确，值得保留。
3. **Shape 到 Content：**给用户看绑定具体 Shape 版本的审阅包、未解决事项和明确批准目标。当前规则同时可能把“go ahead to CONTENT”解释为充分授权、又要求 release gate 与 Shape 批准；必须先统一。CONTENT 只采用符合规则且获接受的候选，不把模糊的“looks good”扩展成全页接受。
4. **Evidence、Check 与发布：**针对冻结版本列出当前 Evidence Result 链接、缺项与每个 gate 的责任人；展示 page-level PDF。Check 只报告判断和路由回产生该问题的 owning Run Spec，不自行修补自己的判断。当前 Workflow 引用旧 display/bibex lane 的句子可能把人带往归档路径；Check 卡目前也缺完整 gate ledger。
5. **Design 到 Delivery：**设计人员创建/更新相应独立 Design Run，完成 Generate 与 Verify 后呈现准确 candidate 和 ready 状态，再交给 Page Delivery 展示/打包。不能把每次点击或 handoff 新建 Run；不能默认两边同路径 manifest schema 一样。Design 可作为引用的 first-class 支持工作，Application 不是其父族。
6. **Draft 与 Scratch：**用户编辑 Draft 表格/阅读视图时只读；需要反馈则从显式 Scratch 写入口提交，保存但不自动关闭，Finish 按说明要求有效 AI Summary 后关闭。当前 presenter 与 Outline skill 一致，roster 的 note composer 描述会造成误导。
7. **Standalone 与部署：**先区分导入/宿主 workspace 和静态构建输出，按交付技能记录 artifact/build receipt；只有被授权且明确的宿主写回/部署动作才改变线上状态。页面交付 Run 不等于 Page 全文验收，整页 Check 仍是独立的人类决定。

## 6. 英文原文建议改写

以下改写只针对明确指出的英语源文，保留原本的步骤/兼容数据含义，并不建议在本审查阶段实施。

1. `page/haipipe-page/ref/glossary.md:174-181` 当前将 workflow 与 phase 分工为“which LOOP / which AUTHORITY”。建议替换为：

   **Before:** `workflow — which LOOP this is. Never repeats.` / `phase — which AUTHORITY is acting ... REPEATS`

   **After:** `Workflow — the declared list of Run Specs for this Page goal, with each Run's route and close rule. A Workflow may be reopened; reopening does not create a new workflow unit.` `Run — one bounded, addressable attempt instantiated from a Run Spec. Steps, feedback turns, controller dispatches, and tool calls stay inside a Run or in routing metadata unless they independently meet the Run contract.` `Compatibility fields such as phase, cycle, and start_phase may remain in serialized controller receipts; they do not name Workflow units.`

2. 对 `servers/workbench-studio/chat.py:702-725` 的活跃 prompt，建议改为：

   **Before:** `Announce the current phase and cycle in every reply.`

   **After:** `Resume the matching open Run when the request fits its commissioned target. Show the Run's current state and the next user decision. Keep ordinary feedback and revisions as Steps inside that Run; create a new Run only for a selected or directly commissioned goal that can close independently. Treat legacy phase/cycle fields as routing metadata, not user-facing work units.`

3. 对 `page/haipipe-plugin/ref/roster.md:43`，建议改为：

   **Before:** `Draft Space note composer appends pending-Step feedback.`

   **After:** `Draft Table and Reading views are read-only. Submit browser feedback through Scratch Mode, or continue the matching Page Writing Run; both preserve scope and do not imply acceptance.`

4. 对 `interactive-writing-run.md:176-190` 的状态句，建议改为：

   **Before:** `An interrupted Step projects the Run as Held, never Waiting.`

   **After:** `If a Step is interrupted, keep the Run in the defined blocked state and record the interrupted Step and reason separately. Use waiting-for-feedback only when the next action is explicitly owed by the person.`

5. 对 `page-workflows/haipipe-page-workflow/SKILL.md:280-281` 的 Evidence 来源句，建议改为：

   **Before:** `Eligible source lanes include outline/evidence/display/, outline/evidence/bibex/, and delivery/latex/.`

   **After:** `Read current Evidence from its referenced RE Result payload and Card. A display preview PDF is inside that current Result payload; the Page-level delivery/latex PDF is a delivery artifact. Do not fall back to retired outline/evidence/display/ or outline/evidence/bibex/ paths.`

6. 对 Design timeline (`haipipe-workbench-design/SKILL.md:166-167`)，建议改为：

   **Before:** `STEPS — Commission ✓ → Generate ✓ → Verify ✓ → Delivery`

   **After:** `RUNS — Commission ✓ → Generate ✓ → Verify ✓ · Delivery readiness: ready`，并说明 readiness 是当前验证/交付状态，不是另一 Run。

## 7. 跨家族责任边界与修正顺序

- **Page Workflow / Run contract owner：**协调 Page glossary、workflow SKILL、neutral Run contract 对 Workflow 结构的统一解释。Route/gate 信息可以保留，但不得再把重复 Phase 定义成 Workflow 单位，也不得把整个 controller pass 自动算作 Run。
- **Page 插件 roster owner：**共享 roster 是陈旧 UI 行为的集中来源。先以当前 Outline/Run/Design presenter 及其有效 action 为准，更新 roster，再改 Studio、Folder、Delivery 中引用它的副本。
- **Design 与 Page Delivery owners：**共同解决 `delivery/render/manifest.json` 的路径、格式及 acceptance/readiness 所有权；Insight 与 Design 是独立家族，Page 插件只投影/消费它们的交付结果，不以 Application 为共同父级。
- **Outline 与 Page article owners：**统一“文章正文”和“Outline工作区/Board投影”的边界，保持文章两部分结构。
- **Evidence workflow 与 Outline Evidence owners：**把已退休来源路径从当前可读清单撤掉，并为当前 RE Result 路径提供统一引用。
- **Outline、Content 与 Board gate owners：**决定 Shape 批准、Content release、owner ruling 的唯一语义和 UI 收据；确保同一用户话语不会在一处被当成批准、另一处被判 HOLD。
- **纠正顺序建议：**(1) 先定 Workflow=Runs 列表及 Run/Step/dispatch 边界；(2) 清理活跃 Chat prompt 与共享 roster；(3) 解决 Shape→Content gate；(4) 对齐 Render manifest owner/schema 和 Evidence 当前路径；(5) 改 Page reader-facing 结构及所有可见 Phase/Steps label；(6) 补齐状态枚举、Check gate 卡片、picker/Folder 导航；(7) 做术语、模板和示例的最终一致性复核。

本审查不实施以上修改。
