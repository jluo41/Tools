# Paper 家族写作与交互评估

## 快照与边界

- 审读日期：2026-09-20；基线提交：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`，与 brief 一致。
- 当前工作区在审读前后均显示 8 个 `references/` 子模块指针修改、未跟踪的 `evaluations/` 目录；没有 Paper 技能或 Paper UI 的已跟踪改动。`evaluations/` 当前只含 brief、inventory、sessions；本报告是本次唯一新增文件。
- 当前 Paper 范围共有 9 份 `SKILL.md`，与初始清单逐项一致，共 3,743 行，未发现额外 Paper 技能。以下覆盖表记录了技能全文及其活动支援材料。
- 审阅包含文档与代码静态核对；未运行被审阅技能、外部服务、测试或 build。交互场景是桌面推演，不是现场用户测试。
- venue 资产范围：检查了当前模板、README、部分完整 desk pages 和其实际链接的 PNAS/MISQ/UTD-IS 指引，并对 17 份当前 QBv desk Markdown 页面检查了合同字段是否存在。未逐页通读其余全部 QBv 正文，也未穷尽阅读来源 PDF、原始 `.bin`、论文范例 PDF；这些是背景证据，不作为技能指令审查。未完整审读 Page、Run、Insight、Design 家族，仅查看了判定边界所需的现行段落。

## 总评

Paper 家族有可保留的治理骨架：G0–G5 为每个人类决定列出可检查的记录；工作结果留在 Discovery/Task/Run 等原生负责人处；Story 解释证据含义，Section 持有稿件文字，Round 逐条登记意见，编译产物必须区分 `DRAFT` 与可提交状态。早期编译不能假装为已就绪，Venue bank 也明确不代替作者选择目标。这些边界写得很认真。

按指定模型衡量，当前仍是**结构性不通过**。活动 Paper 叙事用 P0–P4 定义“journey phase / position”；Paper 插件则把 `paper.*` Run-Type 当成待分配的工作行，并称 Workflow map 不是 Run inventory；共享 Run 合约要求 Workflow 由受控的 Run Spec/Run 节点和路由组成。Story、Section、Round 等长期 Page 身份又明确不是 Run。单纯把 `Phase` 替换成 `Run` 会把容器和工作实例混为一谈。应先定义实际 Run 列表、每个 Run 的 owner/target/input/output/acceptance/route，再把页面、证据、关卡和展示地图分别放回其正确位置。

## 完整覆盖

| 当前技能 | 全文审读 | 活动支援材料 | Workflow/Run 判定 |
|---|---|---|---|
| `paper/haipipe-paper/SKILL.md` | 是，510 行；含完整入口、路由、交互和维护部分 | `paper/README.md`、`ref/page-integration.md`、`ref/run-naming.md`、`ref/submission-readiness.md`；对照当前 Page/Run 合约 | **失败**：`:28–40,54–86,227–246` 显式使用 `[phase]` 路由、Page phase 和 P0–P4；未以 Runs 定义 Paper Workflow。 |
| `paper/haipipe-paper-assemble/SKILL.md` | 是，532 行 | CHANGELOG、TOML 示例、wrapper、JAMA IM/MISQ profiles、`build_delivery.py` 与 DOCX 转换代码（只读检查，未执行） | **部分**：`:359–408` 是清楚的有界编译操作；`:457` 仍称 `CHECK phase`，也未说明 Workflow Run 身份/收据。 |
| `paper/haipipe-paper-venue/SKILL.md` | 是，210 行 | CHANGELOG、`template.md`、`venue/README.md`；当前 QBv 页面及 playbook 检查见下文 | **失败**：`:21–24` 仍称 Page phase；Venue 本身是 PageType/参考资产，不应变成 Run，且模板/实例不能满足 `:93–121,199–207` 的合同门槛。 |
| `paper/haipipe-paper-workflow/SKILL.md` | 是，281 行 | CHANGELOG、`paper/README.md`、Run naming、Paper–Page integration；Paper Plugin 的 Run-Type map | **失败**：`:21–30,40–79,225–247` 把 P0–P4 作为当前活动位置；Workflow 没有被定义成 Runs 清单。 |
| `paper/haipipe-workbench-paper/SKILL.md` | 是，448 行 | CHANGELOG、`ref/space-mapping.md`、当前 `servers/workbench-paper/paper.py`、drawer JS、共享 Plugin/Outline/Run 页面契约 | **失败**：`:370–399` 不把计划行冒充已执行 Run，但把 Workflow 定义为记录移动和关卡测试，展示的也是 Run-Type × Space 投影，不是 Run 清单。 |
| `paper/workflow-phases/haipipe-paper-ideation/SKILL.md` | 是，512 行 | CHANGELOG、`agents/openai.yaml`、Ideation manifest/sync/receipt/workflow-table 支援文档、Ideation 入口 | **部分**：`:29–47,64–116` 能力、人类选择与非 Run 同步边界清楚；P0 journey phase 和 phase 收据文案仍活动。 |
| `paper/workflow-phases/haipipe-paper-round/SKILL.md` | 是，383 行 | CHANGELOG、`agents/openai.yaml`、Paper–Page 集成与 Page receipt 边界 | **部分**：`:26–38,60–63` 一方面明确 Page/Run 边界，一方面仍有 P4 phase 和含义不明的 Page “round” 计数。 |
| `paper/workflow-phases/haipipe-paper-section/SKILL.md` | 是，401 行 | CHANGELOG、generic template、resolver/stat 脚本、Venue Page 与 Story 关联 | **部分**：`:25–44,96–114` 有 Section Page/内部 Runs 区分，但 P3 phase、“Section Page RUN”和 Paper-local Run owner 指示冲突。 |
| `paper/workflow-phases/haipipe-paper-story/SKILL.md` | 是，466 行 | CHANGELOG、`ref/integration.md`、`agents/openai.yaml`、Page CHECK 规则 | **部分**：`:65–95` 将 Story 定义为前瞻蓝图而非 Run；但仍将其放在 P1，`:415–417` 称 CHECK 为 shared Page phase。 |

**新增并核对的当前支援材料：**运行编译代码、Paper board 页面、Paper 插件抽屉 JS、共享 Page Workflow 的 ontology/compatibility 段落、共享 Run Run-Type/Run Spec 段落、Venue bank/模板与所链接 playbook。历史 changelog 只用来判定文件迁移和旧说法，不视为现行行为。老 MISQ abstract template 含 `0-lifecycle`/`stages/5-section-edit` 等旧路径；Section skill 将原始 pack 内容界定为参考材料，因此不将其本身误判为当前 Phase 概念。

## 优先发现

### P1 — Paper 的活动工作流仍以 P0–P4 阶段位置为权威模型

**证据。** `paper/haipipe-paper-workflow/SKILL.md:21–30` 定义：“A **journey phase** is one position in the paper journey below. A **Page phase** is one step of the shared Page lifecycle”，并列出 `P0 Ideation → P1 Story → P2 Evidence/Execution → P3 Section → Compile → P4 Round`。同文件 `:40–79,225–247,257–280` 重复位置表、流程图、“phase reading”和 P0–P4 完成检查。Umbrella `haipipe-paper/SKILL.md:54–86` 将相同旅程作为路由图，当前路径名 `paper/workflow-phases/` 仍承载四个活动技能；`paper/README.md:40–47,99–105` 还称 workflow receipt 为 phase receipt。P0/P1/P3/P4 也在 Paper UI `servers/workbench-paper/paper.py:219–235` 显示为 “the idea pool / one prospective Story / named Section Pages / one RD page per feedback batch”。

**影响。** 人和新上下文代理会把 P0–P4 当作进度单位，汇报“当前阶段”，却找不到该位置对应的实际 Run、Run owner、输入输出或完成收据。且这些位置混有持久 Page（Ideation、Story、Section、Round）、工作通道（P2）与动作（Compile），本身并不都是 Run 实例。

**建议。** 由 Paper Workflow owner 改写成明确的 Run 列表；每个 Run 有 bounded target、owner、input、expected Result、进入条件、acceptance/receipt 和下一路由。可把 ideation generate/test/select、Story shape/review/route、owner-native Discovery/Task work、Section writing/evidence、compile、Round response 定义成恰当的 Run Spec/owner-native Run。G0–G5 保持关卡/人类决定记录，Story/Section/Round 保持 Page 身份，Page controller 的 CONTEXT/OUTLINE/EVIDENCE/CONTENT/CHECK 保持内部控制步骤。`run-naming.md:128–132` 已明说这些 Page identity/owner “not additional Run families”。在路径、P0 等既有标识完成兼容迁移前，保留它们作内部地址，不继续当用户可见的流程阶段。

**英文改写示例（语义示例，非实现）：**

> A Paper Workflow lists its declared Runs and the routes between them. Each Run Spec names its owner, bounded target, authoritative inputs, expected Result, entry and exit rules, and receipt. Runs operate on Idea, Story, Section, evidence, delivery, and Round records; those records remain with their owning skills. G0–G5 are decision gates. The Workflow may route work back to an earlier owner when a Result changes the Story.

### P1 — 编译配置示例既不能按新合约读取，也可能删除旧 room

**证据。** 当前范例 `paper/haipipe-paper-assemble/ref/paper-build.toml.example:1–12` 没有 `[pages]`，并将 `source.room = "../1-<desk><year>"`。技能新合约 `haipipe-paper-assemble/SKILL.md:284–323` 要求 `[pages] main/order`、`source.room = "latex"`（appendix 可按需要）；代码在 `scripts/build_delivery.py:139–142,845–849` 读取 `CFG["pages"]["order"]`，把 `source.room` 相对 delivery 解析为 `LATEX`（`:55–61`），再于每次 build 前执行 `shutil.rmtree(LATEX)`（`:842–850`）。

**影响。** 直接复制示例会因缺少 `pages` 而在读取 compile order 时失败。作者若只补新字段、忘了把旧 `room` 换成 `latex`，build 会递归删除那个示例指向的旧目录，而不只是清理本次生成的 `delivery/latex/`。

**建议。** 让示例与 canonical config 完全同源，限定生成目录位于本 Paper 的 `delivery/` 下，并在 builder 侧拒绝根目录之外的 `source.room`。将源 Page group 与生成 room 明确分开标注。审读未实际运行 build。

**Before / after（关键 TOML）：**

```toml
# Before: ref/paper-build.toml.example
[paper]
source_format = "latex-room"
[source]
room = "../1-<desk><year>"
```

```toml
# After: 与 SKILL.md 的 canonical configuration 对齐
[pages]
main = "../Ba-<desk>-Main"
order = "../A1-Story/<Story>.md"

[source]
# Generated room; validated as Paper/delivery/latex
room = "latex"
```

### P1 — Venue 的活动范例和模板无法满足 Venue 自己的 versioned contract 门槛

**证据。** `haipipe-paper-venue/SKILL.md:93–121,199–207` 要求 `versioned_contract`，且当前状态需通过 CHECK、目标/类别匹配、官方来源和无阻塞未知项。相邻 `template.md:1–84` 没有该 block。对 `venue/bank/1-QBv-desks/` 下全部 17 份当前 `QBv*.md` 做字段检查，没有一份含 `versioned_contract`、`contract_version` 或 `schema_version`。Venue skill 还把 QBv1-MISQ / QBv17-WISE 称为参考实现（`:55–67`）；QBv1 的头部/状态仍写 one-sentence test “unread by any skill”/“no run reads it”（`QBv1-misq.md:1–3,1090`），而 WISE 虽如实标为 CfP-only/partial（`QBv17-wise.md:3,11–13`），也没有新机器合同。

**影响。** 作者依照技能要求维护新 contract block，却在可复制的当前模板和全部 desk 页面里都找不到可遵守范例；目标选择、deep-fit 和 G0 读取到的合同状态无法形成可解析、可核验的统一交接。这比个别文案过期更直接地阻断 gate。

**建议。** 将 template 与全部当前 QBv 页面纳入一个迁移清单：为每页补 schema/version/state/verified/source/unknowns；把尚未完成者诚实标成 `partial`/`stale`，不要用旧 `taste ✓` 暗示当前有效。同步修订或取消旧参考实现称谓。Template 还应按技能的七种内容角色（`:123–152`）示范结构，而不是保留旧的固定图表/文件三分法（`template.md:19–27,44–63`）。此处仅检查字段有无及抽样正文，不声称已审计每条 venue 事实。

### P1 — Paper–Page reference 对 Evidence/Display Run 的 owner 分类互相矛盾

**证据。** `paper/haipipe-paper/ref/page-integration.md:59–64` 说 `pm-`/`pa-`/`pr-` “remain Task-lane Runs”。但 `ref/run-naming.md:12–15,164–177` 将它们列为 Paper-local typed Runs，示例还用 `family: page`；Section skill `:96–114` 也把 Page interaction、Paper-local evidence/display、owner-native Task 分开。

**影响。** 代理可能将本地证据工作派到 Task owner、错误填 `family`，或者把一条本地证据结果误当作满足 Task/Page 写作前置条件。

**建议。** 与 Page/Run owner 先统一这三类 Run 的 owner、schema、前置条件，再让 integration、run-naming、Section skill 用同一名字。不要借术语清理改变已落盘的 identity。

**英文改写示例：**

> Paper-local typed Evidence/Display work uses `pm-`, `pa-`, or `pr-` IDs under its declared Page Evidence/Display owner. It is separate from Page interaction Runs and does not satisfy a Page-writing prerequisite. Delegated computation remains with its owner-native Task or Discovery Run.

### P2 — 活动 Paper 文案将共享 Page controller 的 dispatch label 重新称作 Phase

**证据。** `haipipe-paper/ref/page-integration.md:10–18,34–47,112–127` 称 “Page phases” 并列出 Paper P0–P4 与 Page 00–04；`haipipe-paper/SKILL.md:28–40` 和 Venue `SKILL.md:21–24` 要求加载“current Page phase”。但现行 Page owner 在 `page/page-workflows/haipipe-page-workflow/SKILL.md:23–35` 将 Workflow 定义为 Run Spec route graph，Step 是 Run 内动作；`:57–61,111–119` 将序列化 `phase/cycle/next_cycle` 与 `workflow/phase.yaml` 限定为 controller/API compatibility labels，没有 Phase 的语义权限。`haipipe-run/SKILL.md:492–515,526–538` 区分 Run Spec 与内部 Steps。

**影响。** Paper adapter 让读者把共享 Page 生命周期理解成第二套 workflow unit；反过来若盲目将 00–04 都改名 Runs，又会把 Step 误建成 Run。

**建议。** Paper 当前 prose 改称 Page controller label、Page workflow step 或对应 Run receipt；兼容字段和文件名由 Page owner 决定何时迁移。避免直接重命名 schema。

**Before / after：**

```text
Before: The Paper journey and the Page lifecycle are different axes:
        Paper: P0 ... P4; Page: 00 CONTEXT → ... → 04 CHECK
After:  Paper Workflow lists declared Runs and routes; Paper Pages own their content.
        The Page controller exposes CONTEXT, OUTLINE, EVIDENCE, CONTENT, CHECK
        labels; its owner defines these dispatch steps and any serialized aliases.
```

### P2 — Paper Plugin 的 Workflow 名称与映射图没有表达 Run 清单；drawer 提示也过期

**证据。** `haipipe-workbench-paper/SKILL.md:370–399` 定义 Workflow 为 “how owned records move and which gate is tested”，另列 Run-Type 和 Run；`ref/space-mapping.md:1,7–17` 是 Run-Type/record × Space 投影，单元格给 `read/action/review/route/run`。当前 UI `servers/workbench-paper/paper.py:2589–2592` 明称这是定义图、“not a Run inventory”，因此它不等于 Workflow Runs 清单。它正确提醒 planned row 不代表 actual Run（skill `:398–399`），这一条要保留。另，`haipipe-workbench-paper/SKILL.md:94–98` 称 plugin 自有 hint 都在 `servers/workbench-paper/paper.py`；实际 drawer 位于 `servers/workbench-paper/assets/js/10-drawer/09-plugin-paper.js:40–42`，hint 只列 Setup/Ideation/Story/Run，漏 Delivery，注释 `:7–8` 仍说四个 Spaces；实际 Python `servers/workbench-paper/paper.py:2801–2804` 渲染五个。

**影响。** 第一处会让用户把类型/负责人地图当成实际执行图；第二处会漏掉 Delivery，或让贡献者在错误源文件修改提示。

**建议。** 将本图明确命名为 Run Specs by Space/Folder 投影；唯一 Workflow 清单单独列 Run Spec 与 route，actual Run/receipt 保持原生 owner。同步五个 Space 的 UI 提示和源文件说明。

**英文改写示例：**

> Workflow: the list of declared Run Specs and their routes. A Run Spec defines bounded work; a Run instance records work that occurred. This map projects Run Specs by Space and folder. It neither allocates Runs nor proves execution.

### P2 — CfP-only Venue 模板仍要求作者填写不存在的 pack 观察

**证据。** Venue skill 区分 `PACK-BACKED` 与 `CfP-ONLY`，后者只能使用 DESK RULE 与显式 OWN ESTIMATE（`haipipe-paper-venue/SKILL.md:49–67`）。模板却无条件提供 `### 4 · ... what the pack found`、`The moves, as slots`、`What the pack refuses`、style.md/exemplar 引用（`venue/template.md:44–58`）。模板前面的说明只在 `:21–23` 说无 pack 时改为 target document units，并没有关闭后面的 pack 栏。

**影响。** 无 exemplars 的期刊/基金/专利 desk 的作者可能编造 pack pattern，或留下看似必填的空章节，违背模板声称的 authority 分类。

**建议及英文改写：**

> For PACK-BACKED desks, create one unit record from the linked `style.md` and named exemplars. For CfP-ONLY desks, use the target's own document units; mark exemplar observations “not available” and include only sourced DESK RULEs or clearly labelled OWN ESTIMATEs. Do not create pack-observation sections.

### P2 — Venue 示例 README 越权建议选刊，且实际 desk 页面仍是旧结构

**证据。** `paper/venue/README.md:31–32` 说 “The venue stage … reads these packs to recommend a venue and derive a structural blueprint”。当前 Venue skill `:29–47` 明确 Venue Page 不选择目标也不写 Story Section Narrative；目标决定由 Ideation/Story 持有。QBv1-MISQ 仍把自身称为通用 template，并要求 `## Diagram`/旧 Files 组（`QBv1-misq.md:38–60,93`），而当前 Venue template `:19–27` 把 Diagram 排除为 Page section。QBv17-WISE 又以 QBv1 为 reference，尽管它是没有 exemplar pack 的 CfP-only page。UTD-IS playbook README `:45–61,125,165–195,231–232` 仍引导作者经 Claims/Display/Minimap “stages” 与 `STATUS.md`，和当前 Page-first Story/C8 入口不同。

**影响。** 读者可能要求 Venue 技能做它不拥有的决定，或新写一份与当前 Page resolver / Venue 检查规则不兼容的银行页面。Section skill 明确 `:225–227` 将旧 pack `style.md` 和 stage-era playbooks 限为参考材料；PNAS README/template 中仍有 claims/display/minimap 与旧 `0-lifecycle` 的路线（`playbook-pnas/README.md:28–34,101–112`；Significance template `:1–4`），这些必须标明 reference-only，不能与当前 Paper Page 路由混用。

**建议。** 改 README 为“venue bank 保存 desk 的出处规则与 pack observations；Ideation/Story 用版本化 contract 作 fit 与 retarget 决定”。将仍活动引用的 QBv 示例迁移至现行 template；对阶段时代 playbook 明标 historical/reference-only，或重写其入口路径。

### P2 — 活动 MISQ/PNAS 样式说明之间有互相矛盾或断开的路由

**证据。** `playbook-utd-is/MISQ/MISQ-abstract/style.md:52–58` 禁止数值结果、建议不超过约 160 词；后文 `:84–102` 又允许 health-policy effect size，并说约 185 词可能出现。Assembly 的 MISQ profile `profiles/misq.toml:27–30` 也有 120–160 目标、185 上限，风格文件自身没有将“行为研究常态”和“政策论文例外”说清。PNAS 的 QBv13 当前状态 `QBv13-pnas.md:1–5,9–10,26–28` 标 PARTIAL，并直接写：“Neither file names the other, so a writer who opens one never learns the second exists. Which one comes first?” `playbook-pnas/taste.md` 与 Significance style/template 未互链。

**影响。** MISQ 作者只看 style 文档时不知某个 effect size 算不算违例；PNAS 作者无法确定从何处做 eligibility check 和如何使用 Significance 模板。

**建议及 MISQ 英文改写示例：**

> Behavioral-paper abstracts should normally avoid raw coefficients and p values. A health-policy paper may include an effect size when the number is itself a central finding. Target 120–160 words; treat approximately 185 as an observed exceptional ceiling, not a desk rule.

为 PNAS 写一个明确的入口次序：先适用性判断（taste），再选择正文/意义段模板，并从一处互链到另一处。

## 代表性交互桌面推演

以下只是按当前说明做的桌面推演，不是运行时测试。

1. **“我有审稿人意见，帮我回复。”** Round 的流程总体可执行：固定收到意见所对应的 sent build → 每项 concern 建一条 ledger entry（跨 reviewers 汇总，不按每条意见新建 Round）→ 作者逐条决定接受/拒绝/延期 → 转给 Story、Section 或证据 owner → 读取检查后的版本 → 组装 response package → 人类批准 response/close。清晰输出应摘要覆盖和待作者决定，例如：

   > 已按 build hash `…` 登记 14 项意见：9 项已回复并对应改动，3 项需要你确认 Story/Section 的实质性调整，2 项建议延期。当前没有提交回复包；请先决定这 5 项的处置，之后我会重检差异并请求你批准最终 response。

   这保留了 `round/SKILL.md:85–115,231–260,332–360` 的冻结、逐项路由与 human approval；不得将“已起草”写成“已采纳”。

2. **“稿子当前在哪？能不能编译？”** 按当前 skill 容易回答“在 P2 / P3”；这并未说明哪些工作实际有 Run receipt，也没有直接报 G4 的 ready/DRAFT 状态。更好的答复是列出尚未闭合的 Run Spec、owner、最新 Result 和具体 gate，再报 build 结果与所需的人类决定：

   > 当前有 2 个 Discovery/Task Runs 尚无可接受 Result；Main Section X 已有人释放并完成 Page CHECK。最近 build 是 `DRAFT`，因为 Section Y 尚未过 G4；现在可以继续读草稿，但不能称为 submission-ready。下一决定由你确认 Y 是否纳入本轮 ready set。

   G4 的 ready 规则及早编译政策本身很清楚（`paper-workflow/SKILL.md:163–177`），应把它放到首屏状态里，取代 P-number 阶段。

3. **“我有一批想法，选一个来投 MISQ。”** Ideation 正确将 I3 人类选择作为唯一选中 receipt（`ideation/SKILL.md:64–97,187–194`），但同步部分说“三个状态”后列出语义源 + working/release/delivery 四行（`:99–108`）。应先告诉作者哪份是 source、哪三份是 Page surface，再提出 I3 决定：

   > 当前工作投影是 rev 4；人类批准的 release 与 delivery 仍是 rev 3。尚无 Idea 被选中。MISQ fit 与 pilot 记录已就绪；下一步是由你在 I3 明确 select、defer 或 abandon。

4. **“这篇没有 exemplar pack，照模板新建 Venue Page。”** 当前 Venue 两 profile 的说明可防止虚构来源；但模板仍有强制语气的 pack 分栏。助手应明确走 CfP-only 分支、只提取有来源的规则、标出 OWN ESTIMATE/UNKNOWN，并报告 contract 状态为 partial/stale，而不是填造 observations。一个没有 pack observation 的字段应显示“not available”，而不是由模型补出风格数值。

5. **“请比较 MISQ 和 JAMA，然后替我决定目标。”** `paper/venue/README.md` 暗示 bank 会 recommend target，但 Venue skill 明确不拥有选目标权。更清楚的交互是：

   > 我可以汇总每个 desk 的当前 contract、fit 证据、限制和未知项；目标由你决定。选定后我会把该 contract version 绑定到 Story 的 Section rows。

## English source 的 Before / after 汇总

**Paper Workflow 定义**

- Before: “A journey phase is one position in the paper journey below. A Page phase is one step of the shared Page lifecycle.”
- After: “A Paper Workflow lists declared Runs and their routes. A Run Spec names an owner, bounded target, authoritative inputs, expected Result, entry/exit rules, and receipt. Page types hold content and route work; controller Steps remain internal.”

**Page 入口说明**

- Before: “For a concrete Venue Page RUN, load ... the current Page phase ... and its phase references.”
- After: “To create or update one Venue Page, load the Page owner and Page Workflow contract, the relevant controller label/receipt, Paper Workflow, this Venue PageType, and its linked references. Allocate a Run only when a declared bounded work unit requires one.”

**Venue target authority**

- Before: “The venue stage ... recommends a venue and derives a structural blueprint.”
- After: “The venue bank records sourced desk rules and exemplar observations. Ideation and Story use a verified contract when evaluating or retargeting a paper; the bank does not select its target.”

## 跨家族事项

- **Page/Run owner：** Paper adapter 应按 Page owner 当前的 Run Spec/Step/dispatch labels 更新 prose；`phase`, `cycle`, `next_cycle`, `workflow/phase.yaml` 作为当前序列化/文件路径兼容项不能由 Paper 局部改名。同步核对 Section/Round 引用的 Page `round:` 计数含义（`round/SKILL.md:60–63` 与 Page receipt schema 不够清楚）。
- **Paper Run naming owner：** 统一 `pm-/pa-/pr-` 的 owner/family（见 P1）；另 `run-naming.md:77–89,183–211` 新增的 `ridea-/rclaim-/rtask-/rnarra-` judgement Run grammar，与 umbrella `haipipe-paper/SKILL.md:152–158` 仅列 `rp00/rpNN` 的表述需要明确：这些是不同 Run Specs，还是既有 Page Run 的内部 Step。
- **Insight/Design owner：** Paper 范围没有把 Insight/Design 放进 Application 家族，未发现 Paper 自称 Application 子类；venue 的 `application category` 和普通动词 application 是业务英语，不应盲目删除。但当前共享 `insight/haipipe-insight-workflow/SKILL.md:48–56` 写 “The Application Insight workflow”，与 Insight/Design 为独立一等家族且不存在 Application 父家族的要求冲突；由 Insight owner 修订。当前 Design Workflow 已显式定义其 Run Spec 图及没有 Design Phase layer（`design/haipipe-design-workflow/SKILL.md:48–64`），可作术语治理的独立家族参照。此处只核对这些段落，不是 Insight/Design 家族的完整评审。

## 建议修正顺序

1. 先让 Paper Workflow owner、Paper Plugin owner、Page/Run owner共同写出活动 Run 清单、owner、输入输出、gate、receipt 和 route，并说明 Page 身份与 Run 实例的边界。
2. 用同一模型改写当前 `workflow-phases/` 命名、P0–P4 用户文案、`[phase]` 参数、Page lifecycle 相关说明；兼容 schema 和旧路径另列迁移项。
3. 先修订 Paper-local evidence Run 的 owner/family 定义，再统一 section/router/ref/plugin 的 ID 规范。
4. **在下一位作者复制或运行示例前**修复 `paper-build.toml.example` 的配置及 room 路径保护。
5. 将 Venue versioned contract 引入模板并给全部 desk 页补状态；让 CfP-only/pack-backed 两种路径在模板中分支；迁移过时 README/示例。
6. 对齐用户看到的 Paper Plugin 五个 Space 与源码位置；修复 MISQ/PNAS 指引、Section Page RUN、Round 计数及 Ideation 三/四行小错误。
7. 再精简重复解释并把 compile/read-only-audit 的最短入口前移；保留当前 G0–G5 的证据、人类审批与 DRAFT/ready 细则。

本轮只完成评审并写入本报告，未修改任何技能、代码或其他 session 报告。
