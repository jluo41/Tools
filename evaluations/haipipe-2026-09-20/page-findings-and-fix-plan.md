# Page 家族问题复核与修复计划

复核日期：2026-09-20。范围为 Page 家族全部 **15 份当前 SKILL.md**，以原报告 `evaluations/haipipe-2026-09-20/page.md` 为线索，核对当前文件、相关引用和必要的运行时代码。本报告只列问题与计划；本次唯一新增文件为本报告，没有实施技能或代码修复，也没有执行工作流、导出或测试。

**当前结论：Workflow/Run 指标仍未通过，原报告的大部分文档矛盾仍存在，但需要更正两处过强判断。** `Held` 已是实现中的显示状态，并非运行时无法理解的值；Render 的旧 `adopt()` 写入分支也不能当作当前 UI 可达的写入路径。另有 LaTeX 来源路径等修正已在工作树中，不能重复算作待改原文。

## 1. 当前快照、已有改动和判定方法

HEAD 仍为 `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`，但工作树已明显变化。初读时 Page 下有 9 个已修改文件，收尾时为 10 个；此外还有其他家族、README、未跟踪的评估文件及 8 个 dirty reference 子模块。本次保留这些已有改动，不将其归因于本任务，也不认定它们已验证或完成。

| 当前已有改动 | 对本次计划的影响 |
|---|---|
| `haipipe-page/SKILL.md`、`ref/glossary.md`、Context/Workflow SKILL 将 Folder 身份来源改到 `workflow/folder.yaml` | 这是资源身份迁移。后续不可继续把 `workflow/phase.yaml` 统称为当前 Folder 身份权威；但它没有修复 glossary 中 phase 作为工作单位的定义。 |
| `haipipe-page/src/folder_contract.py`、`src/page_phase.py`、`src/plan_shape.py` 已有修改 | 应由已有改动的负责人继续处理；实施前重新取 diff，避免重复修改其 resolver 和状态逻辑。 |
| Delivery `ref/latex.md:38` 已改用 `<page>/results/<re-run>/payload/<unit>/` | 原报告指向该句的旧路径问题已在文本层修正；Workflow、Word、roster 与 exporter 的剩余问题见 F08。 |
| 写报告期间，Outline `ref/evidence/displays.md:16-30` 的 payload 树补充 `intake/`、README、wrapper 和 preview | 收尾对 75 个相关源文件比对发现此变化，已重读；退休目录规则未改变，F08 的相关引用更新为 `:184-189`。 |
| `interactive-writing-run.md:267` 改为正确的相邻引用链接；Workflow receipt 文字明确 `phase` 是 adapter dispatch label | 保留这些修正，不再提出同一链接修复；它们尚未解决 F01、F09。 |

本会话没有另一个独立获批的修复任务正在实施。这里只能确认工作树中已有改动，无法从 diff 判断其他会话的完成状态或授权范围。

文件引用采用下列明确前缀，行号均来自本次工作树读取：

- `P/` = `/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/`
- `B/` = `/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/`
- `R/` = `/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/`
- `BA/` = `/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/`

“已确认”表示当前文档或源码存在该差异，不表示已做端到端复现。“待确认”表示需要 owner 决策或运行验证。原审查已逐份阅读 15 份技能；本次核对完整清单、全族差异、每个问题的当前源文，以及相关调用/显示路径。未重新对所有未改动材料逐行做一次同规模审计。

## 2. 全族覆盖及 Workflow/Run 指标

强制标准是：**A Workflow is a list of Runs. Use Run, not Phase, for workflow units.** Run Spec 表示计划中的 Run 定义，Run Instance 表示已委托的执行。列表中的 Run 可以有依赖、分支和返回路由；“存在有向图”本身不是错误。错误在于当前有多套竞争定义，并把 Phase 或非 Run 的 dispatch 行混入工作单位。

不得为满足术语规则而把每个反馈、工具调用、gate 或 retry 建成独立 Run。serialized `phase`、`cycle`、历史 receipt 和兼容文件名可以保留，但必须明确它们不定义 Workflow 单位。也不能凭旧字段名删除已有运行数据。

| 当前技能（相对 P/） | 本次核对结果 | Workflow/Run 判定与对应问题 |
|---|---|---|
| `haipipe-page/SKILL.md` | 对读改动、glossary、reader sections、用户包 | **失败**：F01、F06、F13；Folder 身份迁移只修正其中一个边界。 |
| `haipipe-plugin/SKILL.md` | 对读 roster、picker 与子插件现行约定 | **部分**：F04、F12；旧 phase/pass 语言仍通过共享 roster 扩散。 |
| `haipipe-sentence/SKILL.md` | 反馈 rail 与 Draft Run 路由一致；badge 文案有小歧义 | **不适用**：不定义 Workflow；局部反馈进入当前 Run 的边界正确。F15 为文案问题。 |
| `haipipe-workbench-page/ref/delivery.md` | 对读四类交付引用中的问题点及 exporter | **局部通过，整体依赖 F01**：RD 单位清楚；F05、F08 是交付契约/来源问题，不应误算为 Run 计数错误。 |
| `../design/haipipe-workbench-design/SKILL.md` | 对读 action 表、manifest reader、当前 action 拒绝逻辑与真实显示标签 | **部分**：Commission/Generate/Verify 为独立 Runs；F11 将它们显示为 Steps；F04、F05 涉及旧 Adopt/Render。 |
| `haipipe-workbench-page/ref/folder.md` | 对读 tab 顺序与当前 picker | **不适用**：材料/导航面，不定义 Workflow；F12 是入口说明过时。 |
| `haipipe-workbench-page/SKILL.md` | 对读正文两区/四区、Scratch、space mapping、现行 Evidence 引用 | **部分**：Run 核心清楚，F04、F06、F07、F08 仍在。 |
| `haipipe-workbench-page/ref/run-space.md` | `:50-90` 区分计划 Run Specs、实际 Run inventory 和内部动作；对读 live 状态映射 | **局部通过**：保留不为 Step/gate/call 建 Run 的规则；F04 是共享 roster 误述，F09 是状态投影问题。 |
| `haipipe-workbench-studio/SKILL.md` | 对读 chat ref 与实际 boot prompt | **失败**：F02 的活跃指令按 phase 派发；Draw lane 的 owner 边界没有发现同类问题。 |
| `page-workflows/haipipe-page-context/SKILL.md` | `:27-49` 同时说非 Run adapter 又给出 PHASE Brief；对读身份来源迁移 | **部分**：F01；资源身份变更保留，不能把 PREPARE 自动更名成独立 Run。 |
| `page-workflows/haipipe-page-outline/SKILL.md` | 对读 SHAPE/SURVEY 内部边界和发布 gate | **部分**：F01、F03；SHAPE/SURVEY 共享 Structure Run 的设计保留。 |
| `page-workflows/haipipe-page-evidence/SKILL.md` | `:23-30` 正确区分 RE 与 EMBED Step；`:369-378` 明确退休来源 | **部分**：活跃 trigger 仍写 EVIDENCE phase；F01、F08。 |
| `page-workflows/haipipe-page-content/SKILL.md` | `:27-34,54-87` release owner、内部 movements 与 profile 例外 | **部分**：F01、F03；不能因一次 build/revise 就另建 Run。 |
| `page-workflows/haipipe-page-check/SKILL.md` | gate、人类决定摘要、owner 路由和 Application 引用 | **部分**：F01、F10、F14；独立只读判断的边界保留。 |
| `page-workflows/haipipe-page-workflow/SKILL.md` | 对读 canonical ontology、混合行表、兼容契约、写作状态引用 | **失败**：F01、F03、F08、F09；部分 adapter 文案修正尚未统一全族。 |

保留的质量基础包括：先提议后分配 Run、同目标续用 open Run、原始反馈和完成 Step 不可覆盖、`applied` 不等于 accepted、发布正文与候选文字分开、Check 不修改自己判断的版本。

## 3. 问题、证据与具体修复建议

### F01 · P1 · Workflow 的工作单位与 Phase/控制记录混在一起——仍存在

**文件和证据：** `P/haipipe-page/ref/glossary.md:174-181,215-218` 写 `workflow — which LOOP this is. Never repeats.`、`phase — which AUTHORITY is acting ... REPEATS`。`P/page-workflows/haipipe-page-workflow/SKILL.md:23-30` 采用 Run Spec graph 定义，而 `:334-343` 在同一表混列 `rp-struct-01` 与 `controller/context`、`controller/check`，后二者明确 `no Run Instance`。Context `SKILL.md:39-49` 又同时称其 Run Spec/dispatch adapter，并打印 `PHASE 00 CONTEXT`。`P/page-workflows/agents/README.md:3-12` 仍说每个 phase 对应一个 actor。共享 `R/SKILL.md:35-58` 使用 graph 表达，需要共同对齐。

**影响：** 同一读者可能把 Workflow 理解成五个 Phase、若干 Run Specs，或包含非 Run 节点的调度表。用户很难知道“下一单位”是什么，agent 也可能错误计数、重复建单或按旧阶段接管不属于自己的写入。

**修复：** 写一份简短、唯一的上位定义：“Workflow is a list of Runs”，说明定义视图为计划 Run Specs，执行视图为已委托 Run Instances。依赖与 routes 属于这些单位的属性；adapter dispatch 和未独立委托的 Context/Check gate 单列为控制信息。明确 Content adoption 落在哪个已有 Run/Step，或者何时满足独立 Run 契约；不要仅为改名创造 release/check Run。随后同步 glossary、六个 workflow SKILL、agents、workflow-table、phase cards 与 Run 插件。

**验收：** 一张 Workflow 表的每个工作单位都能解释目标、owner、close rule 和实例化条件；控制信息不冒充 Run 行。SHAPE/SURVEY、LAND/EMBED 的改名不会增加 Run 数。历史字段仍可读，现行指令不再把 Phase 定义为单位。

**对原报告的收敛：** “有向图”与“Runs 列表附带 routes”可以兼容；独立 controller receipt 也可以合理存在。不能仅因出现 graph 或 controller pass 就认定模型失败。

### F02 · P1 · Studio 活跃 prompt 仍按五个 Phase 组织普通反馈——仍存在

**文件和证据：** `P/haipipe-workbench-studio/ref/chat.md:114-153` 写 `interactive RUN controller`、`performs a phase`、`agent-per-phase RUN`。`B/live/chat.py:702-725` 实际注入 `Five indexed phases`，并要求 `Announce the phase/cycle on every reply`，末尾还写 `WRITE runs without asking`。同一 prompt `:681,686-693` 保留四区 Page 与直接替换正文的旧路由；与 persistent Writing Run 指令发生竞争。

**影响：** “把这句改清楚”可能被派成一个新的 phase pass，或者修改已发布 Content，而不是保存在现有 Writing Run 的候选 Step。每次都播报 phase/cycle 也挤占用户需要的候选、改动说明和下一决定。

**修复：** 同步修改 ref 与真实注入 prompt。先识别用户是在评阅候选、编辑已发布句子，还是委托新目标；候选反馈续用匹配 Run 并追加 Step。回复显示当前范围、已保存内容与下一决定。已有授权继续有效；只有不在当前范围内的新重操作才按相应政策处理。旧 phase 字段仅在 adapter 中翻译。

**验收：** 新上下文处理“修改当前 P02 第二句”时复用相同 Run；不发布正文、不新建 phase Run、不重复请求已经给过的授权。用户明确编辑已发布句子时才按 Sentence rail 的契约处理。

### F03 · P1 · Interactive profile 与通用 Shape 发布规则缺少清楚的优先级——仍存在，影响需按 profile 判断

**文件和证据：** Content `P/page-workflows/haipipe-page-content/SKILL.md:69-73` 允许所有必要 Runs/Results 完成后，用明确的“go ahead to the content and delivery”作为 release decision，即使历史 `approved:` 仍空白。Workflow `SKILL.md:514` 认可此例外。Outline `SKILL.md:573-600` 则要求人类 Content-release gate 和已批准的 G>=1 Shape；`ref/plan-grammar.md:272-280` 不允许 v0 发布；`ref/review-packet.md:79-82` 要求对指定 Shape 明确批准。`BA/approve-rules/approve-rules.md:79-84` 又说 `approved:` optional，RUN 可据 `checked:` 继续。

**影响：** 它们可能意在描述不同 profile，但交叉加载时没有足够明确的判定顺序。agent 会让用户重复批准已有决定，或把一个 release 指令错误扩大成对尚未接受内容的批准。

**修复：** 定义一张 profile/decision 权威表。推荐保留 interactive profile 的现行便利：若指定版本的 Structure/Writing Run 接受证据与依赖齐全，复用该证据并记录明确 release 指令，不因旧字段空白再次要求批准；非 interactive 或未迁移页面沿用明确的 Shape gate。`checked` 仅代表机器检查，不能代替 owner 声明的人类决定。原话、目标版本与适用范围必须可追溯。

**验收：** “全部 Runs 完成但旧 approved 空白”“有段落尚未接受”“对另一版本说 looks good”“明确拒绝/暂停”四种输入得到唯一一致的行为。前一种不重复索要同一批准；其余输入不越过真实欠缺的 gate。

**不确定性：** 已确认源文差异；未证明当前运行时实际越权发布。修复先解决 profile 优先级，不凭审查意见取消用户保留的决定。

### F04 · P1 · 共享 roster 仍描述已移除的控件和动作——仍存在

**文件和证据：** `P/haipipe-plugin/ref/roster.md:43` 称 Draft note composer 会追加反馈；当前 Outline `SKILL.md:320-329,453-463` 明确 Table/Reading 只读、只有 Scratch 写入口，`P/servers/workbench-page/outline.py:3291-3299` 拒绝 `feedback`、`edit-preview` 等动作。roster `:41` 称 Run Space 有 Scripts 区，但 Runs `SKILL.md:344-368` 禁止该区。roster `:35` 仍列 Adopt 按钮/Run；Design `SKILL.md:413,419-426` 不再需要它，`B/live/design.py:1659-1660` 拒绝旧 Adopt 等动作。

**影响：** 被多个插件引用的“唯一清单”告诉人和 agent 去找不存在的界面，甚至发出当前服务明确拒绝的写请求。仅修子技能无法阻止旧说明再次传播。

**修复：** 以当前产品契约及有效 action 为准更新 roster，再同步消费者。普通写作反馈进入现有 Page Run，浏览器 Scratch 保持其限定用途；脚本可从 Folder 查看；成功 Verify 后 ready，不新增 Adopt 决策。旧数据读取能力标为历史兼容，不能列成可操作按钮。

**验收：** roster 中每个当前动作都有真实入口与允许的 writer；任何已拒绝动作都不会被现行引导推荐。保留历史 Adopt 记录的读取和审计，不重新开放它的写按钮。

### F05 · P2 · Render 的对象身份、来源与接受规则缺少统一契约——保留，但撤回“已证实当前两写入方覆盖”的判断

**文件和证据：** Design `P/../design/haipipe-workbench-design/SKILL.md:261-268` 和 `B/live/design.py:650-662` 按 `item`、`candidate`、`render` 读取 `delivery/render/manifest.json`，要求图片对应确切 Generate Run。Delivery `ref/render.md:15-21,23-43,59` 则按 Page division/render version、`design/warrants/render` 三类 stamp 和 division `accepted:` 描述相同路径。它没有给出完整 JSON schema 或明确 profile 适用范围。

**影响：** 新 writer 无法从现有文档确定要保存哪些字段，以及 Design Verify readiness、division acceptance 和真正分发之间的关系。两种记录可能可以兼容，也可能用于不同 Folder profile；目前契约没有讲清。

**修复：** Design 与 Delivery owner 共同定义版本化 schema 和适用 profile，明确 `candidate` 来源、渲染版本、证据 stamp、readiness/acceptance 的作用域。优先统一公共字段并显式区分 profile；确实是不同对象时再分开路径。新 writer 保留已知历史记录，reader 对不支持的格式给出明确说明。

**验收：** 同一 Generate 候选的图片不会被另一候选替代；Render 不修改 Verify verdict；需要人工接受的交付仍保留该 gate。给出两种 profile 的可读样例，并说明是否允许共享 manifest。

**更正原报告：** `B/live/design_actions.py:503-538` 的 JSON list 写入位于旧 `adopt()`；当前 UI 已拒绝该动作，定向检索仅找到同模块的旧 `adopt_all()` 调用。Delivery 文档也未规定 JSON 顶层必须是单 object。因此不能把“list 与 object 必然不兼容”或“当前 UI 两 writer 会互相覆盖”作为已确认缺陷。

### F06 · P2 · 同一 Page 被定义成两区和四区——仍存在

**文件和证据：** Outline 插件 `P/haipipe-workbench-page/SKILL.md:151-153` 写 `four on-stage sections`：Opening/Outline/Content/Aims。主 Page `SKILL.md:586-632` 与 `ref/page-template.md:16-22,29-37` 只允许 reader-facing Opening/Content。`B/live/chat.py:681` 仍注入四区旧模型。

**影响：** 作者和实现者会把工作过程、计划表或 Aims 塞进最终文章，或误以为后台 Outline 工作区该删除。

**修复：** 统一文章两区；把 Outline、Aims、Discussion 等指向各自的工作区/后台记录。对旧 Page source 的兼容读取单列说明，同步 Chat prompt 和创建示例。

**验收：** 新 Page 只形成 Opening/Content 正文；Outline 仍可从其工作区访问；旧数据不会因隐藏读者区而被删除。

### F07 · P2 · Space mapping 把旧 dispatch 当成 Workflow 单位，并缩窄 Check 范围——仍存在

**文件和证据：** `P/haipipe-workbench-page/ref/space-mapping.md:34-39` 的 `Workflow phase` 表含 SHAPE/SURVEY、LAND、EMBED、CHECK，且 CHECK 仅指向 Delivery；同文件 `:57-78` 的 canonical Run Spec 表把 Check 投影到 Draft、Evidence、Runtime、Delivery。Context/Check 又没有相应实例，需和 F01 一起梳理。

**影响：** agent 可能把一次 EMBED 当成新 Run，或仅看交付文件就声称完成全页检查。

**修复：** 将旧表改成明确的兼容 dispatch → owning Run/控制规则映射，并以规范 Run 列表为主。Check 的证据清单覆盖确切版本的全文、计划、Evidence、收据和交付。若今后独立委托一个可关闭的检查 Run，按完整 Run 契约定义，不能靠改名产生它。

**验收：** 两张表不再给出不同工作单位或 Check 范围；每个可见单位能追溯到规范 Run/控制规则；内部动作不增加 inventory 行。

### F08 · P1 · 当前 Evidence 来源与兼容目录读取规则冲突——部分文本已修正，问题仍在

**文件和证据：** Workflow `P/page-workflows/haipipe-page-workflow/SKILL.md:280-281` 仍把旧 `outline/evidence/display/`、`outline/evidence/bibex/` 叫作 eligible lanes；Word `P/haipipe-workbench-page/ref/delivery.md:29-36` 仍读旧 bib/display。`P/haipipe-plugin/ref/roster.md:29-30` 仍列这些为当前 lane。相反，`P/haipipe-page/ref/user-check-packet.md:239-244` 禁止旧来源/fallback，Outline evidence `displays.md:184-189`、`citations.md:107-109` 及 Evidence `SKILL.md:369-378` 声明退休。

这也不只是文字遗漏：`B/live/export.py:205-239` 先读取 DISPLAY Results，再无条件枚举 legacy display fallback；`:478-484,701-713` 仍读取 `evidence_lane_dir(..., "bibex")`。`P/haipipe-page/src/common.py:45-78` 的 helper 将 Outline Evidence 或旧目录作为当前/兼容来源。当前 LaTeX `ref/latex.md:38` 已修为 RE payload，应保留。

**影响：** 用户检查包展示当前 RE Result，导出器却可能将旧 display/bib 文件作为来源。这样“用户刚看过的证据”和“交付带出的证据”可能不是同一版本；本次未做实际导出复现，风险由可见读路径确认。

**修复：** 明确 v4 当前来源只能来自 Evidence Item 绑定的 Result/payload；如保留迁移读取，必须有独立且可识别的 legacy profile，不能在当前 Page 缺材料时静默 fallback。同步 Workflow、Word、roster、shared resolver 和 Board exporter；CITE 的导出来源也应绑定当前 Result。当前 exporter 会扫描多个 Result manifest，还需确保未选中的旧 Result 不因目录排序变成当前来源。不要重新修改已经正确的 LaTeX 路径句子。

**验收：** 同时存在当前 RE 与旧 display/bib 的样例中，v4 只采用指定 Result；当前 Result 缺失时返回 named blocker；迁移模式明确标识，且不会把历史文件写成当前证据。LaTeX/Word 与用户检查包指向同一来源与版本。

### F09 · P2 · 需要明确存储状态与显示状态；真正可见的缺口是 `ready` 映射——修正原判断

**文件和证据：** `P/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md:176-190` 给出存储状态 `ready/running/waiting-for-feedback/blocked/complete`，又要求中断时投影为 `Held`。但 `P/servers/workbench-page/runs.py:1190-1191` 已实现 `blocked/held/... → Held`，所以 Held 本身不是未实现的状态。

另一方面，`servers/workbench-page/runs.py:1175-1209` 的 `_status()` 将 `planned/ticket/queued` 映射为 Ready，却没有处理契约中的 `ready`；未知值最终落到 Held。当前本地 Run 行在 `:1392` 使用此函数。因此，在已有 runtime、无其他审计错误并且写入 `status: ready` 的路径上，会显示 Held。这是源码判读，未运行端到端用例。

**影响：** 用户可能被错误告知正常待开始的 Run “Needs attention”。文档混用存储字段和显示名也容易让 writer 写入错误层的词汇。

**修复：** 增加一张 canonical runtime status → UI label → next action 表；明确 `blocked → Held`，补齐合法 `ready → Ready` 的处理。保留未知/损坏状态的保守 Held 和 audit 提示，不能为使 UI 变绿而绕过有效性检查。

**验收：** 五个声明状态均有确定映射；正常 waiting 仍显示等待用户，中断/不完整 Step 显示 Held 并给原因；`ready` 在审计通过时显示 Ready。原报告“Held 无法恢复/必须加新枚举”的结论撤回。

### F10 · P2 · Check 的人类 gate 摘要不完整，文案也容易把复核弱化为确认——仍存在，属于交互改善

**文件和证据：** `P/page-workflows/haipipe-page-check/SKILL.md:253-256` 自述 collecting card `omits the RULING`、无总数；`:223-247` 却列出 owner ruling。`:203-220` 采用 `ACCEPT-BIASED`、`CONFIRMATION, not an inspection`，但也明确 silence 不是 consent，不能据 timeout 通过。

**影响：** 用户可能看不见还欠哪个 owner 的决定，或将机器已备齐证据误解为自己只需要点击接受。现有界面里的 Evidence/aim 计数不能自动等同完整 gate 完成数。

**修复：** 从实际 owner 契约派生必需 gate 列表，展示目标版本、责任人、证据、状态和下一动作；可用 x/n 总数作辅助，不因多数已通过就让缺失 gate 失效。保留“先整理证据再请人决定”的目的，把决定写成可接受、要求修改或保留问题的中立选择。

**验收：** 存在 owner ruling 时摘要必有对应项；缺证据/拒绝/待定不会展示整体完成；用户能直接到正确的决定写入面。所有通过均有明确证据，继续保持 silence≠consent。

**不确定性：** 本次确认的是技能自述与数据需求，未做浏览器观察；不能称已经复现“漏 gate 导致错误 CLOSE”。

### F11 · P3 · Design Run 历史被标为 Steps——仍存在

**文件和证据：** `P/../design/haipipe-workbench-design/SKILL.md:166` 显示 `STEPS Commission → Generate → Verify → Delivery`；`:408-413` 明确前三者为独立 `rdNN`，ready 后没有 decision Run。`ref/space-mapping.md:6,8` 也混用 Steps。实际 `B/live/design.py:1091-1107` 遍历 `item["runs"]`，`:1129` 将这一列表标为 Steps。

**影响：** 使用同一系统的人会分不清 Run 是完整委托还是内部动作；Delivery-ready 还可能被误当另一 Run。

**修复：** 将独立记录列表标为 `Runs` 或 `Run history`；行中另列 Run type/action。Delivery readiness 作为派生 handoff 状态展示。保留真正位于 Run 内的 Steps，以及明确标为历史的 Adopt 记录。

**验收：** 一个 Commission/Generate/Verify Run 各占一个历史项；ready handoff 不增加 Run；文档与真实 UI 同时修正。

### F12 · P3 · Plugin picker 与 Folder tab 顺序说明过时——仍存在

**文件和证据：** `P/haipipe-plugin/SKILL.md:88-91` 说 Page phases stepper 也在唯一 picker 中；`B/assets/js/10-drawer/65-plugin-pageflow.js:1-27` 将其定义为 internal lifecycle view/no Plugin row。Folder `SKILL.md:37-40` 将 Runs 列成顶层 tab，但 Runs SKILL `:50-90` 将其放在 Outline 内。Standalone 实际配置 `P/haipipe-page/src/page_workspace.py:300-318` 只有 Outline、Delivery、Folder、可选 Labeling。

**影响：** 用户和 agent 找不到文档指定入口；实现者可能增加重复 tab。Board 和 standalone 的能力差异也被模糊了。

**修复：** 分别列出 Board、standalone 的当前入口；Runs 明确为 Outline 的 Space。内部 controller 历史面只写作调试/兼容投影，不作为新的工作单位 picker。

**验收：** 每个文档入口都能对应到相应运行模式的真实 registry；没有两个顶层 Runs 入口，也不会要求 standalone 拥有未实现的 Studio 能力。

### F13 · P3 · 用户完成包仍用 phase 描述下一状态——仍存在

**文件和证据：** `P/haipipe-page/ref/user-check-packet.md:213-216` 在无 Content 时要求 `no Content yet · phase <PHASE>`。

**影响：** 即使其它地方采用 Run，用户最常见的回复末尾仍把 Phase 当作当前单位；它也没说明下一步需要谁做什么。

**修复：** 有当前 Run 时显示其名字、状态与下一决定；只有候选时显示“next: select a Run”，不要制造已分配 ID；没有 Content/PDF 时如实说明并给唯一相关阻塞。

**验收：** “未选 Run”“Run 正等待反馈”“缺当前 Evidence”“导出失败”四个包都提供真实状态和明确下一动作；无 active Phase 标签，无虚构的 Run/PDF 链接。

### F14 · P2 · Check 的 owner 路由仍引用已退休的 Application 家族——本次确认的补充

**文件和证据：** `P/page-workflows/haipipe-page-check/SKILL.md:19-28` 的加载链末尾写 `family checker, when the Page belongs to paper or application`。

**影响：** 新上下文可能查找已退休 owner，或把独立的 Insight、Design 放回 Application 父级。这不是“style application”等普通英文用法的问题。

**修复：** 按当前 Folder/Page Face 的具体 owner 选择 checker，明确 Insight 与 Design 独立，Paper 保留其自身 owner。使用现行 resolver 的 `workflow/folder.yaml` 资源身份，不再要求 Application 父级；旧身份需要迁移说明而非新调度。

**验收：** 分别给 Paper、Insight、Design Page 的加载示例，均命中真实 owner/checker；找不到 owner 时给明确 blocker，不退回 Application。其他普通 `application` 用词不作盲目替换。

### F15 · P3 · Sentence badge 把类型和等待状态写在同一组——本次确认的轻量文案问题

**文件和证据：** `P/haipipe-sentence/SKILL.md:111` 说 badge 表示 `WHICH KIND`，例子却是 `💬 waiting ▸ ✎ change ▸ ⚑ lane`。

**影响：** 用户不能确定 💬 代表“存在评论”还是“必须等人回复”；这会与 Run 的等待状态混淆。其候选句反馈进入现有 Page Run 的 `:80-85` 规则本身正确。

**修复：** 类型统一写成 `comment / change / typed lane`；仅在实际存在待办决定时另显 waiting。文档示例先修正；是否需要 UI 改动以真实呈现文案复核为准。

**验收：** 类型提示不暗示虚构的未完成决定；真正的 pending 状态能说明等待谁和什么输入。

## 4. 实施顺序与依赖

以下为待实施工作项，不分配新的真实 Run ID，也不构成已经开始修复的声明。由于工作树正在被其它任务修改，每项实施前都应重新核对相关 diff。

| 顺序 | 工作项与范围 | 前置依赖 | 可交付的验收结果 |
|---|---|---|---|
| 1 | 统一 Workflow/Run 定义、Run/控制记录边界和 owner 路由（F01、F14） | Page + Run + Task/Workflow + Board owner 对齐；保留已有 Folder 身份迁移 | 一份唯一术语/单位表与兼容字段表；每个规范 Workflow 行可解释其 Run 契约。 |
| 2 | 统一 interactive 与旧 profile 的 Shape/Content gate 优先级（F03） | 工作项 1；核对已有 Structure/Writing 接受证据及 Board approve-rules | 一张 profile/decision 表与四种边界案例；不重复询问已给出的决定，不跨过真实欠缺的 gate。 |
| 3 | 同步活跃入口和用户说明（F02、F04、F06、F07、F11、F12、F13、F15） | 工作项 1–2；以有效 handler 和产品契约为准 | Chat prompt、roster、子技能、模板、真实 UI label 同一轮同步；用户能定位当前 Run 和有效动作。 |
| 4 | 统一当前 Evidence/导出来源和 Render profile（F08、F05） | F08 依赖 Evidence Result owner；F05 依赖 Design/Delivery 对 schema 和 acceptance 的约定；可与工作项 3 并行实施 | v4 与 migration 读取界限明确；同版本证据贯穿用户包和交付；Render 的候选、版本、来源可验证。 |
| 5 | 修复状态投影并补全决定摘要（F09、F10） | F09 依赖 canonical status 表；F10 依赖工作项 1–2 的 gate 权威 | 所有合法状态正确显示；每个必需 gate 都有 owner、证据、状态和下一动作。 |
| 6 | 做全族一致性与 fresh-context 验收 | 前述改动完成；复核全部 15 份技能及所触及共享文件 | 下列场景通过，记录实际执行的检查与未能运行的环境；对未达标项保持开放。 |

工作项 1、2、4 中的共享契约只应有一个负责定义的 owner，其它家族引用并同步，不各自写一份不同解释。工作项 3 中纯导航或类型文案可以先准备，但涉及行为的 prompt 必须在模型和 gate 规则确定后落地。

## 5. 验收场景与检查方式

根 `README.md:133-136` 要求技能修改完成后在 fresh context 中由 subagent 执行真实任务并检查选择、遵循与结果；这是未来修复的必要验证，本次没有启动该执行。应使用隔离样例和可控依赖，避免用真实用户页面或线上发布作为测试材料。

| 场景 | 必须观察到的行为 |
|---|---|
| 已有 RP，用户只改 P02 一句 | 使用同一 Run，原始反馈保存，新增 Step/必要 Version；返回完整选定候选；不自动发布 Content或伪造接受。 |
| 用户问“现在我需要做什么” | 从当前 Run/gate 生成明确待办；提案不生成真实 Ticket/ID；无 Draft composer、Adopt 等失效入口。 |
| 全部必要 Runs/Results 完成，用户明确进入交付，历史 approved 空白 | 按明确 profile 优先级复用已有接受证据、保存本次 release 原话，不重复要求相同批准。 |
| 仍有未接受段落，或批准指向另一 Shape 版本 | 不采用未获接受的候选；给一个具体缺口及对应 owner/版本。 |
| 未开始、执行中、待反馈、中断、完成 | 合法 `ready` 显示 Ready；blocked 显示 Held；等待反馈与中断区分；损坏/未完成记录不会错误显示完成。 |
| 同时有当前 RE 与旧 Outline display/bib | v4 只读当前绑定 Result；迁移入口显式标记；检查包、LaTeX、Word 的来源与版本一致。 |
| Generate A 有图片，Generate B 为当前候选 | 不用 A 的图冒充 B；Verify pass 后为 ready；显示/渲染不改写 Verify 或添加 Adopt gate。 |
| Owner 有额外 ruling，其它 gates 已过 | 摘要仍显示这个欠缺；不能用“多数完成”或 silence 代替明确决定。 |
| 新建 Page、已有旧 Page、standalone Page | 新文章仅 Opening/Content；后台记录可访问；模式对应的真实 picker 正确；不破坏旧内容。 |
| Paper、Insight、Design 三种 owner | 分别路由当前独立 family，不经 Application；找不到权威时报告缺口。 |

静态检查应覆盖当前 SKILL/refs/agents/templates/prompt/UI label 中的 Phase-as-unit 及退休 owner/path；命中列表需要人工分类，不能靠“Phase 命中数量归零”验收。历史词、API 字段、自然语言普通词不计缺陷。

若改动状态/来源/parser，应运行与改动相符的现有定向测试，必要时增加能重现真实边界的最小用例；不为文案改写创建仅复述实现的测试。文档新上下文验证与代码定向验证分别记录。需要 LaTeX、Word 或浏览器环境而无法执行的检查必须明确列出，不能用静态阅读替代成功声明。

## 6. 跨家族协调与仍有不确定性的部分

| 共享问题 | 主责建议 | 需要共同决定的边界 |
|---|---|---|
| F01 单位/生命周期 | Run + Page Workflow；Task Workflow 与 Board 配合 | Workflow Run 列表、Spec/Instance、controller receipts、Context/Check 的控制位置；routes 可以保留图结构。 |
| F02/F04/F06/F12 活跃 prompt/界面/roster | Page Plugin + Board | 同步真正使用的 prompt 与 registry；读取历史动作不等于当前允许写入。 |
| F03/F10 发布与人的决定 | Page Outline + Content + Check；Board approve-rules、具体 owner 配合 | profile 优先级、复用已有接受证据、owner ruling 的显示与持久化。 |
| F05/F11 Render/Design Runs | 独立 Design + Page Delivery | candidate 绑定、manifest profile、Verify readiness、分发 acceptance；保留历史数据。 |
| F08 Evidence 来源 | Page Evidence/Outline + Delivery + Board exporter；Display/Citation owner 配合 | 现行 Result 契约、迁移隔离、导出与检查包的同源性。 |
| F09 状态 | Run contract + Page writing + Runs presenter | 存储状态与显示标签的映射，保留 audit 失败语义。 |
| F14 家族路由 | Page Check + Folder resolver；Insight/Design/Paper owners | Insight、Design 独立，不使用 Application 作为共同父级。 |

需要继续确认的是：Render 两种描述是否对应不同 profile、哪些旧读取只应在 migration 路径启用、各 owner gate 是否能从一个共同结构获得。没有证据证明当前用户已经遇到 manifest 覆盖、错版导出或错误 CLOSE；本报告把这些保留为契约/源码暴露的风险，不称已发生事件。

未覆盖项与原审查一致：未逐行审查全部生成 Page guide、二进制交付物、历史反馈/CHANGELOG、第三方 reference 树或其它家族全部实现；没有浏览器交互、真实导出和新上下文执行结果。原 `page.md` 保留为原始审查记录，本补充报告中的更正应优先用于制定后续修复任务。
