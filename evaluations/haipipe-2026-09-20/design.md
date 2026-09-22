# Design 家族技能评估

## 快照、范围与限制

- 审阅日：2026-09-20；基线提交：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。
- 开始与结束核对时，工作树都有其他会话留下的 `references/*` 修改和共享 `evaluations/` 未跟踪文件；指定 Design、page-design、board-design 技能路径未见改动。本报告是本会话唯一写入的文件。
- 主要范围与初始清单一致：Design 主目录有 4 个当前 `SKILL.md`。按用户要求另加 page-level 和 board-level Design 插件 2 个，共审阅 **6/6 个当前技能**。Venue 目录没有独立 `SKILL.md`，作为 Design 的当前支持指令整体审阅。
- 这是静态文档评估。没有调用这些技能、打开实时网页、运行脚本或测试，也没有执行外部服务。代表性场景是文档桌面推演，不是真实用户测试；少量读取实现代码只用于核对文档声称的路由和兼容行为。

## 覆盖清单

| 范围 | 覆盖 | 检视材料与限制 |
|---|---:|---|
| Design 主技能 | 4/4 | `haipipe-design`、`haipipe-design-brief`、`haipipe-design-unit`、`haipipe-design-workflow` 的完整 `SKILL.md`。 |
| 主技能支持材料 | 全部当前说明材料 | Designer agent、Brief 的 `agents/openai.yaml`、Unit 的 `modes.md` 与 `unit-contract.md`、Workflow 的 `run-profile.md`、venue `_SCHEMA.md`、8 个 venue README、8 个 `style-profile.md`。另检查 Design 四技能变更记录的当前段落。 |
| Field-test 记录 | 7/7 | VERSION-NOTE、两份 expectation、两份 prompt、两份 settlement；按历史记录阅读，不当成当前行为证据。 |
| Page-level Design 插件 | 1/1 | 完整 `SKILL.md`、`ref/space-mapping.md`、当前 changelog 条目；只读查看实际 action dispatcher 和状态投影。 |
| Board-level Design 插件 | 1/1 | 完整 `SKILL.md`、`ref/space-mapping.md`、当前 changelog 条目；只读查看当前 Board 投影代码。 |
| 有意排除 | — | 未逐份审阅其它 Page、Board、Task、Run、Insight 技能；它们仅在交叉边界核对时引用。Unit 脚本与测试文件没有完整逐行审阅或执行；venue 示例素材目录不存在。 |

初始 Design 清单与磁盘当前清单相同；没有发现第五个 Design 技能。新增的 page/board 插件是评估要求中的两项，不计入 Design 主目录清单。

## 总体判断

Design 主体已经有清楚的边界和强约束：Design Item 与 Run 分开；Run 记录包含 `item:`；Commission 固定配置与来源哈希；Generate 与 Verify 由不同责任方关闭；工具调用、意见和点击不会自动生成 Run；Page Run 与 Design Run 的编号及权限分离。新人可沿着状态、责任人与下一步操作推演工作，也能理解“Verify 通过即可 ready for Delivery”。这些内容值得保留。

整体评估仍为 **不通过**：当前主技能已转到 Commission → Generate → Verify，Delivery 是 Verify 后的只读投影；但 venue 支持材料、Unit 合约和 Board 插件还残留上一代的 Adopt 流程。一名只读了核心 Workflow 的 agent 与一名按 venue README 行事的 agent，会给同一份设计画出不同的完成边界。另有多个文件仍用 `Phase` 指工作阶段，Page UI 把非 Run 的 Delivery 放进 Run 链，核心定义仍称 Workflow 是 Run Spec 图，而不是用户要求的 Run 列表。

## 优先发现

### P1 · Venue schema 和八套说明仍要求旧的 Phase/Adopt 生命周期

`plugins/haipipe-toolkit/skills/design/venue/_SCHEMA.md:12` 说 venue pack“不是 workflow”，`:47` 却要求每份 README 提供 `Phase use`；`:26` 把 `terminal: adopted` 固定为必填字段；`:52` 到 `:57` 把 Preview、Adopt 列成共用过程；`:60` 到 `:62` 又称 `adopted` 是“Application terminal”。同一文件既说 venue 不拥有生命周期，又给它声明了终点。SMS 示例把矛盾写得更直接：`venue-sms/README.md:28` 将 `Commission → Generate → Verify → Adopt` 称为唯一 Design workflow，`:57` 仍有 `Phase use`，`:72` 到 `:76` 要求审核、预览后 adopt/decline。其余七个 README 也沿用 `Phase use`、`terminal: adopted` 和 Verify 后 adopt/decline。

这不是兼容字段的单独出现：Unit 明确要求在需要时加载所选 venue pack；因此 agent 会收到仍然有效语气的旧操作指令。它可能在 Verify 通过后等待一项当前没有的人工 Adopt Run，也会误把 `adopted` 当作 Design 终态。`Application terminal` 还重新引入了用户已退休的 Application 父级词义。

**建议：**统一改造 schema 与八个 README：把章节叫 `Run guidance`；明确 Design Workflow 的 Run 清单为 Commission、Generate、Verify，允许路线规则决定是否创建新的 Generate/Verify Run；Render/Preview 若需要，写成现有 Run 内的 Step 或 Delivery 投影内容；删除 `terminal: adopted`。Verify 通过后用 `ready for Delivery` 表达结果。对历史 `adopt` 文件/API 字段，只保留明确标注的兼容说明。

**英文改写示例：**

```text
Run guidance (required in every venue README)
Commission  freeze the audience, job, venue and acceptance rules
Generate    create the commissioned content or screen
Verify      independently check the exact Result against the rules

An optional render is a Step that presents an immutable Result; it does not
create another Run. A passed Verify makes the design ready for Delivery.
```

### P1 · Board 插件仍把 Adopt 当作当前 Run 和用户待办

`plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/SKILL.md:48` 到 `:49` 写“Steps are Commission, Generate, Verify, Adopt”；`:108` 到 `:110` 说 Run Space 的等待队列包含 `JL · adopt`；`:113` 到 `:124` 用 adopted 状态选择交付和 CSV 行；`:163` 到 `:164` 把 adopt 路由到 Page-level；`:195` 到 `:196` 还称 checker 会审计只有 Commission 与 Adopt Runs 的目录。

这些是当前正文与用户看到的列表、待办相连，不是历史数据描述。对照之下，page 插件的 action 表 `haipipe-workbench-design/SKILL.md:408` 到 `:417` 只有 Commission、Generate、Verify、重试、添加 Design Item 和补充草稿请求；`:413` 明说 ready-for-Delivery 没有决策 Run。当前 Page changelog `design/haipipe-workbench-design/CHANGELOG.md:5` 到 `:9` 也明确：Verify 通过即进入 Delivery；live surface 不创建 Adopt action/state/counter/batch button。只读代码核对确认 `servers/workbench-design/design.py:1659` 到 `:1660` 会把 adopt/decline 请求拒绝为 unknown action，而 `:355` 到 `:357` 将旧 adoption 记录作为已 ready 的 Delivery 读取。也就是说，Board 文档告诉人去做一个当前控制器拒绝的动作。

**影响：**Board 读者可能停在不存在的人工队列，或误以为 CSV 里只有 `state=adopted` 才能供下游使用。当前 projection 的 ready 状态与 Board 文档的 adopted 总数不能作为同一份状态解释。

**建议：**Board 当前说明、表格、队列与 CSV 叙述统一使用 `ready` / `verified`；删除 live `JL · adopt`、`Adopt` Run 和 adopted 行筛选。旧 `rdNN_adopt_*` 可继续映射为 Delivery 历史记录，但必须明确为兼容数据，不作为新队列或交付门槛。Board `CHANGELOG.md` 的当前段落仍说 adopted CSV 和 Adopt Runs，应同步修正。

**英文改写示例：**

```text
Run Space shows only current waits and current Runs. A passed Verify is ready
for Delivery. Historical rdNN_adopt_* records may appear as legacy delivery
evidence; the current writer does not create them.
```

### P1 · Venue 与 Unit 参考合约仍给 agent 不同的完成边界

`design/haipipe-design-unit/references/unit-contract.md:37` 说 Commission 和 Adopt Tickets 都带 `item`；`:46` 把上游验证责任叫作 “Application callers”；`:155` 保留“Human adoption is a separate version-bound receipt”；`:170` 到 `:172` 把 Commission 与 Adopt Runs 并列为当前文件夹审计对象。Unit 的 `SKILL.md:112` 甚至说 Verify 的任一结果都不代表“adopted”，`:121` 又让 caller 承担 adoption。与此相反，当前 `haipipe-design-workflow/SKILL.md:41` 规划的 Run 总数是 `1 Commission + N Generate + J Verify`，`:61` 到 `:64` 将 Commission 指为唯一人工决策 Run，并明确 Delivery 不是 Run；Design 主技能 `haipipe-design/SKILL.md:267` 到 `:273` 也说 Verify 通过后无需第二个人工决定。

**影响：**刚从当前 Workflow 进入 Unit 合约的 agent 会把过时的 Adopt 当成 v2 必需步骤；人类读者无法确认 adoption 是一个独立 receipt、独立 Run，还是已经移除的旧流程。实现代码 `check_unit.py` 仍识别旧 Adopt 配对，所以这里尤其需要把“当前写入”与“历史读取”写清楚，而不是贸然删掉兼容校验。

**建议：**在 `unit-contract.md` 增加一条明确的 current/legacy 切线：新 v2 写入只允许 Commission/Generate/Verify；Adopt-shaped records 仅供历史审计读取。把 caller 写成实际拥有边界的 `Design caller` 或“调用方”，删除当前 worker 指令中的 adoption 决策职责。

### P1 · Page 的 `Steps` 示例把 Delivery 错放进 Run 链

Page 插件先规定 `haipipe-workbench-design/SKILL.md:63` 到 `:65` 里步骤要用 Run 名称，然后在示例卡 `:166` 显示 `STEPS Commission ✓ JL → Generate ✓ → Verify ✓ → Delivery`；`:205` 到 `:207` 又称“item's Runs”作为 Steps 芯片。可是 Workflow `haipipe-design-workflow/SKILL.md:59` 与 `:63` 已明确 Delivery projection 不是 Run。

**影响：**人在唯一面板上看见一个 Run 清单，但无法判断 Delivery 是否有记录、编号、结果或关闭条件。当前文档把正确的概念定义与实际示例做成了互相矛盾的界面。

**建议：**面板把三种实际 Run 放入 `RUNS`；将 Delivery 显示为通过 Verify 后的状态/只读交接字段，不要作为第四个 Run chip。保留 `Step` 表示 Run 内部动作，不把渲染或评论升成 Run。

**英文改写示例：**

```text
RUNS             Commission ✓ JL → Generate ✓ → Verify ✓
READY FOR DELIVERY · draft hash <hash> · verified by <reviewer>
```

### P1 · `Phase` 仍出现在当前说明中，Workflow 定义也没有落到用户要求的列表模型

用户要求的是 “A Workflow is a list of Runs.” 当前主技能把实际单位大多正确地叫 Run，也明确工具调用不是 Run；但仍有活的 `Phase` 用法：`haipipe-design/SKILL.md:65` 与 `:248` 写 “the design phase judges”；`haipipe-design-brief/SKILL.md:38` 用 “not a Design workflow phase”说明前置关系；`haipipe-design-workflow/SKILL.md:48` 写“There is no Design Phase layer”。Venue schema 的 `Phase use` 以及八个 README 同样是当前章节名。

此外，`haipipe-design-workflow/SKILL.md:13` 叫“一张 directed graph of Design Runs”，`:22` 叫 `Run Spec graph`；`haipipe-design/SKILL.md:146` 也定义 “canonical Workflow” 为有向 Run Spec 图。路线图本身可用来表达分支和重复次数，但现在没有一句把 Workflow 定义为 Run 清单，并指出 Delivery 不在清单中。全局 Task Workflow 也继续在 `task/haipipe-workflow/SKILL.md:19` 到 `:26` 将 Workflow 定义为图，因此这需要与共享 Run/Workflow owner 协调，不能只改 Design 图上的标题。

**建议：**正文和可见说明统一使用 `Run` 描述工作单位；“Workflow”说明可写成清楚的 Run 清单，并保留每个 Run 的路线与重复规则。明确 “一条评论、点击、模型调用或渲染动作仅在 Run 有自己的闭合条件与记录时才构成 Run；否则是 Step。” `Phase` 可仅在解释已退役目录/历史接口时留作原始标记；query 参数 `workflow` 已明示为旧别名，属于兼容字段，不代表当前工作模型，不应机械改名。

**英文改写示例：**

```text
The Design Workflow lists Commission, Generate and Verify Runs. Route rules
say when another Generate or Verify Run is created. Comments, clicks and tool
calls stay Steps inside their Run. Delivery is the read-only status of a
passed Verify, not another Run.
```

以及：

```text
These Runs judge design quality only. Keep experiment terms (arm, allocation,
power, winner, field) out of `expected` and `falsified`.
```

### P2 · Venue 导航指向旧目录，Style Profile 仍假设旧 Card/DU/grant 数据结构

Unit 说“只加载被选中的 venue pack”，但 `design/haipipe-design-unit/references/modes.md:35` 指示去 `application/venue/venue-<kind>/`；当前 pack 实际位于 `design/venue/venue-<kind>/`。新上下文按字面读会找错目录。

Style Profile 又重复要求 `[ ] Card id, grant, and exact render version resolve in the Design Folder`，例如 `venue-checklist/style-profile.md:46`；SMS `venue-sms/style-profile.md:80` 到 `:93` 仍给出 `unit: DU<NN>-<slug>`、`division-id`、`draft | judged` 与 `card.md`。当前 Design 使用 `ITEM01` register、Commission 固定配置与 Result；主技能 `haipipe-design/SKILL.md:116` 还明令屏幕不应显示 DU。所有八份 Style Profile 都有 Card/grant 检查项。

**影响：**这些文件虽然是 venue 参考资料，仍会在需要时作为生成/自检依据；agent 会寻找不存在的 Card/grant 文件，或照旧格式命名内容，验收清单也无法对应当前 Run/Result。

**建议：**把 venue 目录写成相对明确的 Design skill 路径；把旧检查项换成 `item id`、已发布的 Commission 配置、被固定的 Result/artifact hash 与适用的 render manifest。将 SMS `DU` 示例改为当前 `ITEM` / `rdNN` 术语，并声明屏幕可以显示的字与仅存在于记录内的字段。

### P2 · `blocked` 和人为暂缓的 `hold` 汇成同一个用户状态

Page 的状态折叠 `design/haipipe-workbench-design/ref/space-mapping.md:45` 用 `hold` 表示人暂不发布 Commission，且表单回到 Release；`:57` 又把任意 Run 的 `blocked` 状态折叠成相同的 `hold`，等待人处理 `failure:`。`haipipe-design/SKILL.md:83` 也只有一个 `hold` 状态。

**影响：**列表中的“hold”可能让人以为可以重新发布 Commission，即使实际是某个 Run 因缺少来源或损坏记录而 blocked；期望的负责人和按钮不同。

**建议：**分成 `commission held` 与 `blocked · <reason>`；前者提供 Release 决定，后者说明失败归属并给出真实的重试/解除动作。若某种 blocked 状态没有按钮，要标明具体等待谁和原因。

### P2 · Unit 标题让人误以为一个 Commission 只产生一个结果

`design/haipipe-design-unit/SKILL.md:13` 标题为“one commission, one inspectable result”，但这个 worker 的 Entry `:35` 到 `:39` 接收的是 Generate 或 Verify Ticket；Workflow `haipipe-design-workflow/SKILL.md:41` 明确一个 Commission 后可有 N 个 Generate、J 个 Verify。正文足够具体，但第一屏标题把不同层级的 Run 与 Result 并列，会给刚接手的 agent 一个错误的基数暗示。

**建议：**改成“one Ticket, one inspectable Result”或“one bounded operation, one Result”，将 Commission 描述为该 Ticket 的上游授权，而不是 Unit 的运行粒度。

**英文改写示例：**

```text
# /haipipe-design-unit · one Ticket, one inspectable Result
```

## Workflow/Run 逐技能判定

| 技能 | 判定 | 证据与解释 |
|---|---|---|
| `haipipe-design` | 部分 | 有 `Design Item`/Run 分界和 Page/Design 两套 Run identity；但仍用“design phase”，且把 Workflow 定义为 Run Spec 图，没有明确 Run 列表。 |
| `haipipe-design-brief` | 部分 | Brief 是 Design Commission 的前置条件，不是执行 Run；其 Page Workflow 委托给 Page owner。但“not a Design workflow phase”仍使用禁用词，也没有直接用 Run 描述这个依赖。 |
| `haipipe-design-unit` | 不适用（Workflow 定义）/部分（Run 边界） | 它是单次 Generate/Verify worker，正确区分调用与 Run，并指出内部草拟不是额外 Run；但 Unit 合约仍含当前 Adopt 模型和历史术语。 |
| `haipipe-design-workflow` | 部分 | Run Spec/Run instance、Route 和内部 Step 边界写得清楚；但规范名称仍为 `directed graph`，且“no Design Phase layer”保留旧术语。 |
| `haipipe-workbench-design` | 部分 | 核心按钮对应实际 Commission/Generate/Verify Run；卡片将 Delivery 放进 Steps/Run chips，偏离该 Run 清单。 |
| `haipipe-workbench-design` | 不通过 | 当前文档仍把 Adopt 当作步骤、等待项、Run 与 CSV 决策状态，和 Page 的新 writer / ready projection 冲突。 |
| Venue schema + 8 README（支持材料） | 不通过 | 强制 `Phase use` 和 `terminal: adopted`，要求 Verify 后 adopt/decline；不是独立技能，但会实际被 Unit 读取。 |

**整个 Design 范围：不通过。** 合规边界有明显优点（内部 Step 不自动扩成 Run、交付投影不需要新 Run），但当前所有使用路径还没有统一执行用户指定的 Workflow/Run 定义。

## 人类交互桌面推演（非用户测试）

### 1. 在 Board 上提交五个群组、每组十条 SMS

假设请求是：“为五个受众群组各准备十条短信，使用 Insight board X，并打开文件夹。” Board skill 的 `add-tasks` 能生成每群组一条 Brief line，并由 `open=yes` 同时开文件夹；缺少 subgroup/job/venue 或 Insight board 解析不到时会以一句话拒绝且不写入。然后每个 folder 可在 Design Space 注册 Items、在 Commission 决定 Release，agent 只执行已排队 Run。这个流程的责任分界清楚。

更明确的答复可先确认对象数：“我会在 Brief 中新增 5 条设计任务，每条 `10 wanted`，并为这 5 条打开 Design Folder。接下来需在各 Folder 登记 Design Items，再决定要 Release 哪些 Commission。”这能避免把“5 个 Brief line”和“50 个 Design Item”混为一谈。

### 2. 用户要求修订 Verify 未通过的 SMS

Page action 表会要求输入 feedback 并把 `base` 与 `feedback` 固定到新的 Generate Run；旧 Result 保留，agent 不会原位覆盖候选；重生成后再排新的 Verify。它能解释等待在人还是 agent、运行失败还是 verdict fail。建议界面持续显示被修订的 draft 标题/hash，减少用户在长列表里认错目标。

一个清楚答复示例：“该 Verify 的结论是 fail，draft 保留在 Run Space。请写下要改的地方；我会基于这个 draft 建一个新的 revise Run，然后需要一次新的独立 Verify。”

### 3. UI Card 中引用数据且需要可视验证

Unit Skill 明确样例数据与 `data-bind`、真实输入控件、HTML screen、Render 计量和人工查看图片的分工；Renderer 自己不裁定 Pass。这里实际 Run 是 Generate/Verify，Render 是 Run 内工具步骤。这个范例正确体现“不是每个工具动作都另建 Run”，但 UI venue README 的 Adopt 与 ASCII wireframe 旧指引需按新 `ready for Delivery` 结构校正。

### 4. Verify 通过后把确切稿件交给下游

按 Design Workflow，用户可看到准确的 draft hash、哪个 Generate 产出、由哪个 Verify 确认；结果直接进入 Delivery Space。Board Skill 却仍要求“adopt”，显示 `JL · adopt` 并只从 CSV 取 `adopted` 行。桌面推演在此停止，因为文档给出了互不兼容的下一步；如果用户根据 Board Skill 操作，当前 Page writer 会拒绝该操作。

建议当前答复：“独立 Verify 已通过。这个确切版本已 ready for Delivery，可连同 hash 和 Verify 记录交给下游；当前 Design Workflow 没有额外的 Adopt 决定。”

## 交叉家庭边界

- **Design 与 Application：**四份 Design 主技能的 metadata/所有权声明把 Design 作为直接家族，Brief 中的 “Application” 可合理理解为要建设的产品/项目对象，不等于父级 skill family。但 Design 支持材料仍有 `Application terminal`（venue `_SCHEMA.md:61`）与 “Application callers”（Unit `unit-contract.md:46`）。此外，范围外的 `skills/board/README.md:19` 到 `:21` 仍说 Application Pages 属于 Application family；当前工作树没有 `skills/application/` 目录。请 Board/结构 owner 将该树状描述改为 Design、Insight 等独立家族的直接所有权。
- **Insight 与 Application：**范围外 `skills/insight/haipipe-insight/SKILL.md:32` 到 `:38` 仍把 Task-side 与 Application Insight 描述为双路入口，并说技能物理位置在 `skills/application/`；当前文件实际上在 `skills/insight/`。这是 Insight owner 与全局目录/Board owner 的交叉修订，不是本次 Design 范围内的工作。
- **通用 Workflow 术语：**范围外 `skills/task/haipipe-workflow/SKILL.md:19` 到 `:26` 同样给 Workflow 下“有向图”定义。若用户的新规定适用于整个 Toolkit，应由通用 Workflow/Run owner 与本次各家族一并统一；只改 Design 会让同一产品里仍有两套定义。
- **Page 与 Design Run 边界：**`haipipe-design/SKILL.md:122` 到 `:142` 的两张 Run 图与 `:179` 到 `:183` 的变更路由是好例子：改变候选内容走 Generate Run，解释不变候选的 Page 文本留在 Page Writing Step，固定决策中的评论也不新开 Run。应保留这一边界。

## 建议修订顺序

1. 先由共享 Workflow/Run owner 明确最终定义，并解决 Board README 与 Insight 入口中的 Application 家族树残留。
2. 修正 venue `_SCHEMA.md` 与八套 README：取消 `Phase use`、`terminal: adopted` 和当前 Adopt 流程；保留 Run 内 Step 与 Delivery projection。
3. 对齐 Page/Board 插件与其映射文件：Board 当前队列、计数和 CSV 全面改为 ready/verified；旧 Adopt 记录显式标为 legacy；Page 卡片将 Delivery 从 Run/Steps 列表移出。
4. 对齐 Unit SKILL、`unit-contract.md`、checker 合约说明和 `modes.md` 路径；保留必要的旧记录读取校验，但在说明中标明只有历史读取。
5. 修正八套 Style Profile 的 Card/grant/DU 示例，并拆分 commission-held 与 blocked 状态；更新 Unit 标题。
6. 用更新后的文档重新做相同场景的 desk walkthrough，再单独安排真实用户测试或运行时验证。本报告没有执行这些验证。

本轮未修改任何技能、实现、测试、分支或其他评估报告。
