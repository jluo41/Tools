# Task 全家族：问题复核与修复计划

复核日期：2026-09-20。原报告：[task.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/task.md)。

本次重新核对了当前 49 个 Task 技能的清单、原报告各问题对应的现行材料，以及原评估以来的 Task 目录差异。最重要的未解决问题仍是：共享 Workflow schema 要求 `run_specs`，Task 计划生成器、报告程序和 12 份类型样例却继续要求 `phases:`。此外，六类旧脚手架与当前目录规范不一致；Endpoint 的平台 payload 规则相互矛盾；Individual 数据构建、缓存更新与 safety judge 输入仍有缺口。

本报告也更正原评估中证据不足或口径不一致的结论。Insight 的旧 Phase 表已在现有工作区改动中修正；`scripts/config/` 是当前 Task 的正确配置目录；`bNNjNNtNNrNN` 是完整的 Task Run 标识。以下修复计划以本次复核结论为准。

本消息授权的是问题说明和计划。本会话没有另一项独立获批的实施任务；本次只新建本补充报告，保留原报告和所有已有工作区改动，没有开始修复技能、代码或执行运维流程。

## 后续归属更新（2026-09-21）

随后已按当前 Task domain 结构落地一个范围收窄：
`haipipe-task-gpu` 和 `haipipe-task-gpu-training` 现在位于
`T/5_fit/haipipe-task-for-fit/` 下，公开 `name:` 保持不变，因此按名称
调用仍兼容。GPU 是 Fit Task 的执行修饰，不再作为独立 Task type；通用
GPU companion 只负责 Fit 的队列、卡占用、teardown 和 receipt，训练
companion 负责 checkpoint/resume、preemption 与训练专属 fallback。评估、
serving 和 engine 的 GPU 工作仍由各自 owner 负责。原文中这两项的旧路径
以本节为准；Run 边界结论保持不变。

## 1. 当前快照与复核范围

- HEAD 仍是 `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`；但工作区已不等于该 commit。根 README、多个其他家族、8 个 `references/*` 子模块工作树均有预存改动，另有未跟踪的 `AGENTS.md`、`evaluations/` 和 Insight 新目录。
- Task 下 49 个 `SKILL.md` 与原 `inventory.json` 的集合完全相同，没有新增或缺失。48 个 SKILL 相对基线没有差异，`page-types/haipipe-page-insight/SKILL.md` 有预存修改。
- Task 共有 4 个预存修改文件：`haipipe-task/fn/insight.md`、`haipipe-workflow/ref/workflow-runtime.md`、`page-types/haipipe-page-insight/SKILL.md`、其 `ref/workflow-table.md`。这些修改不是本次实施成果，本计划不覆盖它们已完成的工作。
- 在原评估完整阅读 49 个技能的基础上，本轮重读原报告，检查全家族清单和差异，逐项重查现行证据段落。特别补读了原来未完整检查的 `haipipe-task/ref/databricks-execution.md`，并核对了 Individual 的相关实现、共享 Run identity 和 Page controller 契约。
- 本轮是静态复核，没有调用技能、外部服务、训练/部署任务或测试。`platforms/` 不在本 checkout 中，NN/Data 的实际用户项目运行库也未在本轮验证；这些限制在对应问题和验收条件中保留。
- 下文 `T/` 表示 `/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/`。其他家族引用以 `skills/` 为共同根；行号对应本次核查的工作区内容。

## 2. 原报告需要更正或关闭的结论

| 原结论 | 本次证据与处理 |
|---|---|
| Insight 仍使用 “Phase × Run Map” | **这一点已修正。** `T/page-types/haipipe-page-insight/ref/workflow-table.md:25-28` 现为 “Workflow activities × Run ownership”，明确 actual workflow nodes 是 owner-native Runs；`:37-46` 保留 checkpoint/LLM call/review 不自动新建 Run 的边界。不要重复进行该修改。 |
| Task config 应从 `scripts/config/` 改为 `configs/` | **撤回该迁移建议。** 当前权威 `T/haipipe-task/ref/hierarchy.md:16,83-92`、`ref/task-structure.md:75-95`、`fn/run.md:13,23` 均使用 `scripts/config/`；Data Task 自身 `SKILL.md:25-38` 也如此。原报告把历史 Data review 的 `configs/` 修复记录误当作当前权威。Data reviewer 的路径本身正确，快捷清单缺项仍成立（F07）。 |
| Display seed 中 `b01j01t01r01` 不是完整 Run id | **撤回该判断。** `skills/run/haipipe-run/SKILL.md:354-358` 明确它是 Task 的完整 owner-native identity。仍需解决的是 source_runs 与最终 provenance 没有一致保留同一组来源字段（F20）。 |
| Raw 所在家族没有远端 receipt 规则，应默认单独建 conversion Run | **收窄。** `T/haipipe-task/ref/databricks-execution.md:24-33,206-211` 已定义同一 Ticket 的 deploy/run/fetch 和 cluster receipt。Raw specialist 的 convert-only 流程没有清楚接上这一契约（F04）。默认可让转换留在 extraction Run 内，不应机械多建一个 Run。 |
| GPU training 的 train/validation/test phases 构成 Workflow 错误 | **仅保留 P3 用词建议，已随 Fit 归属更新。** `T/5_fit/haipipe-task-for-fit/haipipe-task-gpu-training/SKILL.md:113-120` 的语境是指标覆盖的数据划分，不是 Workflow 行；现行文字使用 “data splits”。不能把三种数据集升级为三个 Runs。 |
| Remote pull plan 没有 Run specs，所以判 PARTIAL | **改为 N/A。** `T/1_data/haipipe-data-remote/fn/fn-plan.md:4-8,105-131` 描述一次 transport 操作内的多个 pull，并返回操作摘要；它没有声明自己是 Task Workflow definition。CLI 调用列表不能仅因是有序计划就被强制变成 Run roster。 |
| Fit/Eval/Display/Agent 用 `phases:` 样例，却只判 PARTIAL | **统一为 FAIL。** 它们与 Data/Algo/Endpoint/Individual 使用同一个被明文禁止的顶层 roster，不能因其他段落写得好而减轻这一指标。 |
| 所有四步生命周期说法都必须废除 | **收窄为 Workflow 单位问题。** Plan/Build/Execute/Report 可保留为操作或命令；错误是把它们作为 domain Phases、计划 rows 或独立身份权威。Task-for-page 的本地问题因此列 PARTIAL；它未直接给出 `phases:` YAML。 |
| Patient report 与 judge 必然互相矛盾，judge 无法做任何阈值检查 | **收窄。** persona 禁的是医疗处方，通用活动建议是否越界尚未定义；这属于交互范围不清（F18）。Report 含 `pred_min/max/mean`，所以能做部分内部一致性检查；缺失 raw forecast 的真正问题是不能独立对照原始预测核实最近窗口（F17）。 |

## 3. 问题清单：现行证据、影响、修复和验收

P1 表示会造成错误契约、错误路径、错误输入或不可信完成判断；P2 表示明确的一致性/交互缺口；P3 表示需要改进的表述或路由建议。标为“待确认”的内容不得在实施时当作已经证明的运行故障。

### F01 · P1 · 仍存在：Workflow 主契约与生成/报告链条使用两套结构

**范围与证据：** `T/haipipe-workflow/ref/plan-schema.md:126-129` 写明 “`run_specs` is the only workflow row roster. Do not add `phases:`”。但 `T/haipipe-task/ref/workflow-template.yaml:29-34` 生成 `phases:`，`fn/stage-plan.md:39,134,203` 教 “Phases → Steps”，`fn/stage-report.md:7,92,124,148,189,220` 要求 same phases / `phases_completed`。`haipipe-task/SKILL.md:112,123` 也使用 `<phase>` / “Four phases”。`ref/task-lifecycle.workflow.js:80-99,114-116` 将旧格式嵌入作者和 reviewer 的实际 prompt，`:42` 继续返回 phase 数。

**人或 agent 会遇到什么：** 同时遵守 schema 和作者/审核程序不可能；旧样例会成为新计划，reviewer 还可能按旧格式放行。这里已确认的是文档/生成指令冲突，没有声称已观察某个 validator 的运行失败。

**拟修：** 以现有 Run Spec schema 为定义权威、report 中 `runs` 为实际实例列表。同步主模板、plan/report 程序、lifecycle prompt、agents 指引和全部 12 份样例；将 internal Steps 保留在相应 Run 里。`meta.phases`、`opts.phase`、`stages` 如仍被底层 API 消费，可作为有文档说明的兼容 dispatch 参数保留；它们不得决定 Run identity、routes 或计数。不得把 Gate1/Gate2 自动升级为 Runs。

**验收：** 新 plan 只有 `run_specs` 作为 Workflow roster，每行具有 bounded target、actor/action、close rule、receipt、cardinality 和有效 bindings；新 report 按 `run_spec_id` 对应实际 Runs。旧格式样例不会被新建入口读取。现有已冻结计划的兼容/迁移有显式版本规则，不能原地重写历史证据。

12 份仍含 `phases:` 的类型样例如下；它们属于 9 类 Task，另加 1 份共享主模板，不能误报为 12 个技能：

| 相对 T 的文件 | `phases:` 行 |
|---|---:|
| `1_data/haipipe-task-for-data/ref/workflow-plan-sample.yaml` | 25 |
| `2_nn/haipipe-task-for-algo/ref/workflow-plan-sample.yaml` | 24 |
| `3_end/haipipe-task-for-endpoint/ref/workflow-plan-sample.yaml` | 24 |
| `4_individual/haipipe-task-for-individual/ref/workflow-plan-sample.yaml` | 25 |
| `5_fit/haipipe-task-for-fit/ref/workflow-plan-sample.yaml` | 25 |
| `6_eval/haipipe-task-for-eval/ref/workflow-plan-sample.yaml` | 26 |
| `7_display/haipipe-task-for-display/ref/workflow-plan-sample.yaml` | 25 |
| `8_stata/haipipe-task-for-stata/ref/workflow-plan-sample-cms.yaml` | 50 |
| `8_stata/haipipe-task-for-stata/ref/workflow-plan-sample-case.yaml` | 56 |
| `8_stata/haipipe-task-for-stata/ref/workflow-plan-sample-data.yaml` | 45 |
| `8_stata/haipipe-task-for-stata/ref/workflow-plan-sample-reg.yaml` | 53 |
| `9_agent/haipipe-task-for-agent/ref/workflow-plan-sample.yaml` | 24 |

Endpoint SKILL 的当前 80–88 行是 config 字段，原报告对此处的 phase 引用不准确；该样例仍会由通用 lifecycle 的 glob（`:83`）发现，因此问题仍成立，证据应改用样例和通用调用者。

### F02 · P1 · 仍存在：六类脚手架仍新建旧 Job 布局

**范围与证据：** 当前 Task hierarchy `T/haipipe-task/ref/hierarchy.md:11-17,76-97` 规定 `bNN/jNN/tNN`，Task code 在 `scripts/`、config 在 `scripts/config/`。Algo `2_nn/haipipe-task-for-algo/SKILL.md:43-51`、Individual Task `4_individual/haipipe-task-for-individual/SKILL.md:27-36`、Fit `5_fit/haipipe-task-for-fit/SKILL.md:45-55`、Eval `6_eval/haipipe-task-for-eval/SKILL.md:27-37`、Agent `9_agent/haipipe-task-for-agent/SKILL.md:29-41` 仍新建字母组下的平铺 `.py/configs/runs`。Stata `8_stata/haipipe-task-for-stata/fn/scaffold.md:7,43-65` 同样如此，但自己的 `ref/stata-dialect.md:104-129` 已称 nested 为当前形状、flat “do not scaffold it”。

**影响：** 用户从不同 specialist 创建的同类 Task 会落在不同层级，通用 Run 命令要求的 Page/config/Ticket 路径无法一致解析。Stata 还让同一个 `scripts/` 在旧 Job 和新 Task 中代表不同职责。

**拟修与验收：** 六类 SKILL、scaffold 和种子路径统一到 BJTR；共享代码归 Job `src/`，Task 自有代码归 `scripts/`，配置保留 `scripts/config/`。旧树仅提供显式读取兼容说明。用每种类型一个临时新建例子检查同名 Page、config/Ticket stem、输出路径及 Task checker；Stata 需覆盖四种 stage，但不执行服务器计算。

### F03 · P1 · 仍存在，并补充证据：Result 路径规则连共享入口内部也不一致

**证据：** `T/haipipe-task/fn/run.md:23-31` 规定 `$OUTPUT_ROOT/<task>/results/<run>`，默认 OUTPUT_ROOT 为 Job；但 `:48` 又一概说 “Do not create generated Results in the Task Folder”，与默认解析结果冲突。Page Task `10_page/haipipe-task-for-page/SKILL.md:40` 用正确路径，`:63,105` 和 `ref/specimen-page-values.md:31` 却使用 `results/<task>/<run>`。Display `7_display/haipipe-task-for-display/ref/config-seed.yaml:13` 与 `ref/provenance-template.json:10` 也分别使用这两种顺序。Page Task 目录图 `SKILL.md:62` 还把 workflow 放在 Job 层，而共享 Task tree 将其放在 Task 内。

**影响：** 同一 artifact 有两个目的地；人能看见文件却不能按 receipt 或 Task audit 稳定找回。共享禁止句使作者无法判断 self-serving Result 是否合法。

**拟修：** 统一按已解析 output root 计算路径；明确 self-serving 时物理路径可以位于 Task 内，consumer-serving 时位于配置的外部 projection。分别说明 authored files 与 generated Results 的写入规则。修正所有示例和 provenance 输出地址，不以简单搬文件代替迁移说明。

**验收：** self-serving 和显式 RESULT_STORE 两个例子中，scaffold、Ticket、report、values、provenance 指向同一个 `<task>/<run>`；没有同时允许和禁止该目标的句子。旧 Result 不自动搬迁。

### F04 · P1 · 结论收窄：Raw convert-only 流程缺少与共享远端完成契约的接线

**证据：** `T/1_data/haipipe-task-for-raw/SKILL.md:147-163` 的 Workflow 为转换→人工上传→cluster 运行→落地→可选 sync；其 `ref/run-databricks-sh-template.sh:43-54,67-84` 结束于 `converted`，并明确说没有执行。共享 `T/haipipe-task/ref/databricks-execution.md:24-33,190-193,206-211` 已有完整 Ticket loop、resume 和 cluster `runtime.yaml` 规则。

**影响：** 转换完成后，用户虽然知道还要上传，却缺少在同一 Run 上登记远端结果、恢复和报告完成的明确做法。未观察到虚假成功；本问题是接续契约不完整。

**拟修：** 默认将转换/上传作为 extraction Run 内的 Steps。Raw specialist 采用共享 Databricks 契约；自动执行与人工交接各说明 pending、still-running、failed、complete 如何映射到同一 Ticket/Result。仅在用户独立委托 notebook conversion 时另建转换 Run。

**验收：** 只有 converted 时 extraction 不被报告为 complete；有匹配 cluster Run/输出门证据时才能关闭；超时后恢复观察而不默认启动第二份计算；PHI/server-resident 情况继续遵守现行产物边界。

### F05 · P1 · 仍存在：HumanFn 的创建入口分给两个 owner

**证据：** `T/1_data/haipipe-data-source/SKILL.md:31` 写 “SourceFn / HumanFn via builder”，而 Record `haipipe-data-record/SKILL.md:15,30` 明确拥有 HumanFn / RecordFn。Data Task `haipipe-task-for-data/SKILL.md:144-145` 仍写 SourceFn/HumanFn 属 Source。Source 自己的范围 `:114-118` 又只有 SourceFn。

**影响与拟修：** 用户要求修改 HumanFn 时可能被送往错误的 stage。统一 Stage 1 SourceFn、Stage 2 HumanFn/RecordFn 的 owner，并更新 umbrella、交叉引用及 design-chef routing；不要将 Data stage 改名为 Run。

**验收：** “create a HumanFn” 和 “review HumanFn” 从 umbrella、Source 入口或 Task 创建入口都转到同一个 Record owner，输出目录一致。

### F06 · P2 · 仍存在：AIData 的共享读写例子仍用旧目录

**证据：** `T/1_data/haipipe-data-aidata/SKILL.md:131` 输出为 `4-AIDataStore/{ParentSetName}/@v{N}AIData-{aidata_name}/`。共享 Data `fn/fn-0-dashboard.md:536,544`、`fn/fn-1-load.md:264,281,287`、`fn/fn-2-cook.md:480,532,599` 仍写 `{aidata_name}/@{version}`；NN `2_nn/haipipe-nn/fn/fn-test.md:218,233` 也保留旧例子。

**影响与拟修：** 用户按 load/dashboard 指引可能寻找另一个路径。让 specialist/store-map 成为当前布局的单一说明，其他调用处统一引用；若实际 loader 仍兼容旧布局，应明确 legacy discovery 顺序。实际库的兼容能力尚未验证。

**验收：** 同一个 ParentSet/AIData 例子从生成、dashboard、load、NN 使用均解析成同一目标；兼容例子标注为旧数据，而不是另一种默认布局。

### F07 · P2 · 仍存在：Data reviewer 的快捷清单遗漏新增检查

**证据：** `T/1_data/haipipe-data/fn/fn-review.md:206-213,255-260,301-304` 已新增 Source SF-11..15、Record RF-15..17、Case CF-12..13；quick reference `:410,412,414` 却分别停在 SF-10、RF-14、CF-11。该文件 `:50,87` 的 `scripts/config/` 路径正确，不再列作缺陷。

**影响与拟修：** 只按快捷表工作的 reviewer 会漏掉 external release、向量顺序、时点安全或 serving parity 检查。让快捷表与完整清单共享 ID 范围，并保留 CGM-only 条件。

**验收：** 每个当前 check ID 都能从对应类型的快捷入口到达；SF-8/9/10 不被误施于非 CGM 数据。

### F08 · P2 · 仍存在：Remote 的统一 SSO 指令覆盖了 backend 分支

**证据：** `T/1_data/haipipe-data-remote/ref/concepts.md:137-152` 区分 GDrive token 与 S3 SSO；`:176` 又无条件要求 “Surface SSO URL on credential errors”。SKILL `:123-126` 已有正确的按 backend 提示。

**影响、拟修与验收：** GDrive 用户可能收到无关的 AWS 登录建议。把 MUST DO 及 status/pull/push 的同类文案统一为 backend-appropriate recovery；以 GDrive 和 S3 两个失败例子确认提示正确，不实际刷新凭据。

### F09 · P2 · 文档冲突已确认，API 行为待核实：NN 版本是否包含 `@`

**证据：** `T/2_nn/haipipe-nn-instance/ref/concepts.md:225,264-266` 要求 `modelinstance_version='@v0001'`，甚至写 “never bare `v0001`”；ModelSet `haipipe-nn-modelset/ref/concepts.md:149,353,418` 却使用裸 `v0001` 和 `MyModel/v0001`。

**影响与拟修：** 用户无法知道 config 值还是 loader 负责加前缀；可能得到不同模型目录。先读取实际目标项目的 parser/normalizer，确认接受/输出形式，再统一 Instance、ModelSet、overview 和 Task seed。不能依据 Tools 仓库缺少某个目录直接认定运行 API 已坏。

**验收：** 同一模型版本经生成、保存和重载保持相同 canonical identity；支持的旧输入有显式 normalization，unsupported 输入给清楚错误。资产版本不计为额外 Workflow Run。

### F10 · P2 · 待确认范围：NN 的配置示例缺少 workspace/dialect 限定

**证据：** `T/2_nn/haipipe-nn/fn/fn-generate.md:239-246` 的 WHERE to write 是 `config/test-haistep-...`；`fn/fn-dashboard.md:210-220` 的 YAML_FILE 也用 `config/.../my_model.yaml`。Task-owned Run 的当前配置位置则是 `scripts/config/`。

**影响与拟修：** 文档没有说明这是独立 NN 开发 workspace 的配置还是 Task config。保留确有支持的 NN 独立开发模式并标明适用环境；在 Task 模式用已解析 Task config path。实际 NN workspace 可能合法拥有根 `config/`，因此原报告“这个路径必不存在”的推断不能保留。

**验收：** fresh-context 用户能从一次调用知道自己处于 NN development 还是 Task execution 模式，生成与 review 使用同一文件；不得默认将所有 `config/` 全局替换成 `configs/`。

### F11 · P3 · 交互建议：自然语言“run model”需要结果导向的消歧

**证据：** `T/2_nn/haipipe-nn/SKILL.md:66-74` 明文将 `test, smoke, run` 映射到 test；Algo Task `haipipe-task-for-algo/SKILL.md:15-17,61-68` 区分 smoke test 和 Fit。这个明确 alias 本身不是代码错误，也不能推出 `train` 一定会被误派。

**拟修与验收：** 保留明确的 test alias；自然语言说明若要新 checkpoint/完整训练则用 Fit，检查既有模型则用 test/eval/inference。只在预期产物不明时问一次。以“run the smoke test”和“train and save a checkpoint”两个请求确认路径不同。

### F12 · P1 · 仍存在：Endpoint 的 wire pair 规范与 builder/reviewer/consumer 相反

**证据：** `T/3_end/haipipe-end/ref/0-overview.md:222-240` 标注 owner decision 2026-07-05：Src2InputFn/Input2SrcFn 按平台各一对；`:298-324` 却说所有 Fn 接受两种格式、没有 platform-specific Fn。`haipipe-end-input2src/ref/concepts.md:37-44` 明说只读本平台 shape，`:126-132` 示例却 unwrap both；`haipipe-end-endpointset/fn/fn-review.md:144` 要求 “Handles BOTH”。Individual inference `4_individual/haipipe-individual-inference/SKILL.md:39-40` 宣称跨平台同 payload，`src/build_payload.py:90-98` 固定输出 `dataframe_records`。

**影响：** 同一实现可能被一个检查要求接受、另一个要求拒绝；用户也不知道同一 Endpoint_Set 包可否直接跨目标部署。

**拟修：** 采用已有明确 owner decision：wire pair 按部署目标匹配，builder、concepts、review、sample payload、Individual consumer 一起对齐。特别保留 `0-overview.md:225-237` 所说共享 MetaFn/TrigFn/PostFn，以及 TrigFn 合法的 unwrap；不能对所有 Fn 做同样删除。“same artifact!”（`:245`）须改成明确的压缩格式/目标内容说明。Local contract 需随本地 wrapper 确认。

**验收：** 每个支持平台的 Src2Input/Input2Src 能同平台 round trip；错误平台的 payload 被明示拒绝或由明确适配层转换；Individual 选定目标后输出匹配 shape；shared TrigFn 的行为不被意外破坏。外部平台真实部署另需对应仓库与环境。

### F13 · P2 · 仍存在：部署默认路径和“可用”状态缺少一致前提

**证据：** Local `T/3_end/haipipe-end-deploy-local/SKILL.md:19-29,41-43` 说 FastAPI fully specified、Flask/Docker placeholders，却将 Flask 设为默认。Databricks `haipipe-end-deploy-databricks/SKILL.md:22-23` 标 active/tested，`:93-110` 的 procedure 仍标 placeholder；SageMaker `haipipe-end-deploy-sagemaker/SKILL.md:87-104` 同样依赖项目实际约定。

**影响与拟修：** 默认命令把用户带进尚未具体定义的 Local 路径。将 Local 默认与完整实现对齐；远端 skill 区分“外部平台实现已知存在”与“本环境已满足 prerequisites”，把必需 repo/config/credential 的缺失作为明确状态。当前 checkout 没有 `platforms/`，不能据此声称外部脚本本身不可用。

**验收：** 不带 framework 的 Local 命令能解析到一条文档完整的入口；缺平台依赖时明确返回 required input/blocked，不能宣称已部署。平台资源创建不属于本计划编写阶段。

### F14 · P1 · 仍存在：Individual 的构建说明与指定 builder 做不同工作

**证据：** `T/4_individual/haipipe-individual/SKILL.md:145-154,184-195` 说 builder 运行 `fn_source.run()`、`fn_record.run()`，并称 raw store 加脚本为 source of truth。指定实现 `fn/build_sample_individuals.py:1-5,260-303` 实际过滤已有全局 Source/Record parquet；不会重新生成这两个全局资产。

**影响与拟修：** 用户可能以为修改 raw 后即可重建，实际仍在消费旧的全局派生数据。优先让技能描述反映实际 extract-and-copy 行为，列出 Source/Record 前置资产和 provenance；若想新增 pipeline rebuild 模式，应另列实施范围，不悄悄改变已有 build 行为。

**验收：** 文档列出的 reads/writes 与 builder 一致；缺全局 Source/Record 时明确缺什么，不报已从 raw 重算。

### F15 · P1 · 仍存在，并补充证据：缓存过期后也可能继续保留旧个人切片

**证据：** `T/4_individual/haipipe-individual/fn/build_sample_individuals.py:238-247` 仅用一小时 `built_at` 判 fresh；`:268-269,294-295` 又对已存在目标直接 continue。因此过了 TTL 重新进入 build，也不等于已有文件得到刷新。

**影响：** 更新输入或过滤参数后仍可能看到旧数据，但 manifest/构建摘要已进入新一轮，降低结果可解释性和重现性。这是源码分支推导，尚未运行复现。

**拟修：** 用数据源版本/指纹、过滤参数和 builder 版本决定缓存是否可复用；分清同轮去重与跨轮刷新。重建使用临时目标和完整替换/原子发布策略，失败时保留原可用 Result；显式处理不再属于该个人的旧切片和强制重建语义。

**验收：** 同输入可复用；一小时内输入变化触发更新；TTL 过期后已有目标可刷新；失败不产生半新半旧的“成功”目录；删除或变更筛选条件不会留下被误当当前结果的旧切片。

### F16 · P1 · 仍存在：Individual shorthand 解析固定到个人 Linux 路径

**证据：** `T/4_individual/haipipe-individual-inference/src/load_patient.py:21-22` 固定 `/home/jluo41/WellDoc-SPACE`；`:32-40` 基于该 USER_STORE 解析 Subject shorthand。`:29-31` 已支持有效绝对路径，因此原报告不应说所有输入形式都失败。

**影响、拟修与验收：** 用户在其他工作区照 quickstart 传 `Subject-18` 可能找不到数据。把 workspace root 注入配置/参数或已有环境规则，文档写清优先级；继续支持绝对路径。两个临时 workspace 的同名 Subject 必须按显式 root 解析，歧义保持报错，不静默读另一个人的数据。

### F17 · P1 · 结论收窄：Safety judge 无法独立核对最新预测窗口

**证据：** `T/4_individual/haipipe-individual-inference-judge/personas/safety-review/system.md:5,9-16` 称 raw forecast 可在提供时用于核对，rubric 针对 most-recent forecast window。CLI `scripts/judge_report_cli.py:46-65` 只传 report，底层 `src/judge_report.py:37-54,176-182` 支持但未收到 extra_context。Report CLI `haipipe-individual-inference-report/scripts/make_report_cli.py:96` 已保存 `forecast.json`，但 SKILL `:86-92` 没列它。Report schema `src/report_schema.py:58-64` 有 min/max/mean，可供摘要内部检查，不能替代独立对照。

**影响与拟修：** safety verdict 没说明哪些维度真实核对过、哪些只信任待审报告。显式绑定匹配该报告的 forecast/window，传入 judge 或由确定性的检查先产生事实结果；缺 forecast 时把依赖它的维度标 unavailable/blocked，不能制造 pass。输出清单应列 forecast 及其对应关系。

**验收：** 用项目既有阈值和边界样例核对 safety_flag；错误窗口/不匹配输入不能通过；缺原始预测时仍能做文案检查，但必须清楚标注事实核对范围。这里不评估模型的临床有效性。

### F18 · P2 · 边界待内容 owner 确认：患者文案中的“行动建议”范围不清

**证据：** `T/4_individual/haipipe-individual-inference-report/personas/patient-friendly/system.md:11,19-26` 要求 “what to do about it” 和具体饮水/步行建议，并禁止特定胰岛素剂量/替代医生；judge persona `safety-review/system.md:18-26` 禁止剂量和 medical action prescription。通用活动建议是否落入禁区并未定义，所以不能简单断言两者字面完全矛盾。

**拟修：** 由内容 owner 确认该产品只解释预测，还是允许经审定的行动提示；将允许/禁止示例写成 reporter 和 judge 共享规则。若职责仅为解释，移除主动行动例子并采用现有 care-plan/care-team 表达。不能只修 judge 使它迁就不清楚的文案。

**验收：** 同一组被批准的正反例在两个 persona 中得到一致边界；不把“措辞安全”说成“预测有临床保证”。这个政策选择不阻塞 F17 输入绑定。

### F19 · P2 · 仍存在：同一 scaffold 调用的返回字段有两份答案

**证据：** Fit `T/5_fit/haipipe-task-for-fit/SKILL.md:19` 要求 `status/task_folder/run_name/files`，`:89-97` 的 Return contract 却是 `status/summary/artifacts/next`；Eval `6_eval/haipipe-task-for-eval/SKILL.md:19,66-74`、Stata `8_stata/haipipe-task-for-stata/SKILL.md:22,367-375` 同样如此。Fit/Eval 后一段也在描述“what was scaffolded”，不能未经核实解释成另一个 execution 模式。

**影响与拟修：** 调用者不知道应该从哪个字段取 Task/Run 或下一步。定义每种 operation 的公共 tail 和类型字段；若保留两种返回模式，必须由命令明确选择，并给 caller 映射。不要强制所有 domain-specific fields 消失。

**验收：** 同一个 scaffold 命令的头部承诺、程序尾部和 agent schema 要求相同必需字段；blocked 结果能明确列出 missing input 和下一步。

### F20 · P2 · 收窄后仍存在：Display 来源字段在 config 与 provenance 中断开

**证据：** `T/7_display/haipipe-task-for-display/fn/scaffold.md:29` 要求 source full Run ids、Result paths、hashes。`ref/config-seed.yaml:25-27` 有合法完整 Run id 和 result，但没有 source hash；`ref/provenance-template.json:16-21` 有 upstream artifact/hash/role，却没有其显式 source Run identity。输出地址错误另归 F03。

**影响：** 模板没有说明来源身份在导出中如何保留。绝对 artifact 路径加 hash 可能足以定位数据，因此不再断言“必然无法回溯”。已确认的是承诺字段和模板字段不一致。

**拟修与验收：** 统一 config 到 provenance 的来源映射，保留 owner-native Run id、resolved artifact、内容 hash 和选择规则；能从导出产物还原输入 source_runs。字段可叫 `run` 或 owner 已有名称，不为追求拼写增加一套身份。

### F21 · P2 · 仍存在；部分边界须跨家族确认：Page Task 混合执行、controller 与迁移任务

**证据：** `T/haipipe-page-task/SKILL.md:26` 仍说 “current Page workflow phase”。当前 Page owner `skills/page/page-workflows/haipipe-page-workflow/SKILL.md:57-70` 明确 phase/cycle 是兼容 dispatch metadata，workflow pass 不是 Page Run。`T/10_page/haipipe-task-for-page/SKILL.md:24,93,154` 保留 four phases / phase producer；`:56-57` 图用 `pj...`，而 `skills/run/haipipe-run/SKILL.md:349-358` 已将该 Paper dialect 标为历史。该 skill `:174-194` 又允许一个 Discovery Page 重排例外，含 fan-out/reviewer/commit 行为，超出前文只产 consumer-neutral 数值的主职责。

**影响：** 用户难以判断入口是在执行数字计算、运行 Page controller，还是批量改写 Discovery 页面；照图新建时还可能使用退休 id。

**拟修：** controller 文案用 action/route；P-B-E-R 用命令/操作。Page 图从当前 Page/Paper owner 引用命名规则，不自行分配 id。与 Discovery/Page owner 确认批量重排任务的归属和明确 trigger，至少单列该例外的 inputs、writes、approval/commit 边界；writer/reviewer/fixer 各调用不自动算新 Run。

**验收：** 数值服务调用不意外编辑 consumer Page；显式重排请求只触发声明的例外；新图不 mint `pj...`；同一写作目标的反馈仍属于同一 Run 的 Steps。Task-for-page 的 Run 指标列 PARTIAL，因为其直接缺陷以术语/边界为主，没有独立给出 `phases:` YAML。

### F22 · P2 · 部分已修，仍有残留：Task 家族导航和跨家族职责说明过期

**证据：** `T/README.md:54-64` 的 domain 表漏 `10_page`；`:99` 说 “names none / never route upward”，但 `:82-95,116-121` 又公开写消费者和 Insight 路由。`T/DESIGN.md:28-40` 在 family map 中把 `applications/` 对应 `/haipipe-insight, /haipipe-design`；`T/TODO.md:14-16` 已明确 Application parent family 退休。`T/TODO.md:45-47` 保留历史要求“four equal phases”，容易被当作当前规则。当前 Task Insight map 已修正，见第 2 节。

**影响与拟修：** 维护者可能漏选 Page 类型、误把 consumer-neutral 理解成不能说明消费者、继续套用退休的父家族。补 `10_page`；说明 Task Results 不带 consumer stake，consumer 负责自己的 Supporting/Local Run；将 Insight/Design 画成独立家族，区分 artifact folder 与 skill-family ownership。历史 DESIGN/TODO 保留日期与原意，并标明被哪个当前契约取代，而非全局抹掉历史词。

**验收：** 当前导航能找到全部 49 个技能和 10 个编号 domain；当前规则不把 Insight/Design 放回 Application parent；历史文档有清楚优先级；已修改的 Insight map 不被重写回旧语义。

## 4. Workflow / Run 指标：全家族复核

必须满足：**A Workflow is a list of Runs. Workflow 单位用 Run，不用 Phase。** 定义期以 Run Specs 列表表达计划，routes/dependencies 决定执行关系；执行期记录实际 Run Instances。列表与有向路由图不矛盾。Steps、文件、按钮、反馈回合、controller controls 和 model API calls 不因出现在计划里就获得 Run identity。底层兼容字段和历史材料另行标注。

本轮使用统一口径：**4 PASS、3 PARTIAL、10 FAIL、32 N/A**。数量变化部分来自纠正原评分口径，不能解释为本次修好了若干技能。FAIL 的共同结构证据见 F01；N/A 只针对 Workflow 编写职责，不是整个技能的质量评分。

| 当前 skill，相对 T；每项对应一个 SKILL.md | Run 指标 | 复核关联 |
|---|---|---|
| `haipipe-task` | FAIL | F01 的定义/生成/报告冲突；F03 路径。 |
| `haipipe-workflow` | PASS | Run Specs/Instances/Steps 明确；现有 runtime 修改保留兼容边界。 |
| `5_fit/haipipe-task-for-fit/haipipe-task-gpu` | PASS | fit-owned companion；queue 只调度有 config/Ticket/Result/receipt 的既有 Runs。 |
| `5_fit/haipipe-task-for-fit/haipipe-task-gpu-training` | PASS | fit-owned companion；fallback、resume、独立配置保持 Run 边界；数据 splits 不创建额外 Runs。 |
| `haipipe-page-task` | PARTIAL | F21：controller 被叫 workflow phase。 |
| `10_page/haipipe-task-for-page` | PARTIAL | F21 命令/例外边界；F03 Result 路径。 |
| `page-types/haipipe-page-insight` | PASS | 现有改动已修 map；ref/workflow-table:25-46 明确活动不分配 Run。 |
| `1_data/haipipe-data` | N/A | 域操作；F05–F07。 |
| `1_data/haipipe-data-aidata` | N/A | 资产操作；F06 的当前路径权威。 |
| `1_data/haipipe-data-case` | N/A | 数据/配置 phase 字段不是 Workflow 行；F07 checklist。 |
| `1_data/haipipe-data-external` | N/A | 构建成熟度 Phase 1/2，不是 Run roster。 |
| `1_data/haipipe-data-raw` | N/A | Raw 资产说明；Task 运行职责在 task-for-raw。 |
| `1_data/haipipe-data-record` | N/A | Record/HumanFn 域职责；F05。 |
| `1_data/haipipe-data-remote` | N/A | 一次 transport 操作内的 pull Steps；F08 凭据文案。 |
| `1_data/haipipe-data-source` | N/A | SourceFn 域职责；F05。 |
| `1_data/haipipe-task-for-data` | FAIL | F01 样例；F05 交叉路由。 |
| `1_data/haipipe-task-for-raw` | PARTIAL | F04：内部 Steps 可以保留，外部执行闭合接续不完整。 |
| `2_nn/haipipe-nn` | N/A | 域路由；F09–F11。 |
| `2_nn/haipipe-nn-algo` | N/A | 算法对象/测试步骤，不定义 Task Workflow。 |
| `2_nn/haipipe-nn-instance` | N/A | resolver 检查步骤；F09 版本字段。 |
| `2_nn/haipipe-nn-modelset` | N/A | 模型 pipeline/资产版本；F09。`@run-v000X` 不作 Task Run 行。 |
| `2_nn/haipipe-nn-tuner` | N/A | 调参/模型职责，不直接定义 Task Workflow roster。 |
| `2_nn/haipipe-task-for-algo` | FAIL | F01 样例、F02 旧脚手架。 |
| `3_end/haipipe-end` | N/A | F12/F13；平台 Phase 0–2 是部署动作标签，建议称 operation。 |
| `3_end/haipipe-end-deploy-databricks` | N/A | 平台操作；F13 的环境前提。 |
| `3_end/haipipe-end-deploy-local` | N/A | 平台操作；F13 默认路径。 |
| `3_end/haipipe-end-deploy-mlflow` | N/A | deferred，没有 Task Workflow 定义。 |
| `3_end/haipipe-end-deploy-sagemaker` | N/A | 平台操作；F12/F13。 |
| `3_end/haipipe-end-develop-databricks` | N/A | 服务 Job execution id 不作 Workflow spec。 |
| `3_end/haipipe-end-develop-local` | N/A | 域内部调用；F12 契约需一并保持。 |
| `3_end/haipipe-end-develop-sagemaker` | N/A | 服务 pipeline Steps 不自动生成 Task Runs。 |
| `3_end/haipipe-end-endpointset` | N/A | package/review 操作；F12。 |
| `3_end/haipipe-end-input2src` | N/A | inference 内部函数；F12。 |
| `3_end/haipipe-end-meta` | N/A | packaging-time 函数，保持共享。 |
| `3_end/haipipe-end-post` | N/A | response 函数，保持共享。 |
| `3_end/haipipe-end-src2input` | N/A | concepts:18-28 的三 Phase 是单次 packaging 内部步骤，建议称 Step；F12。 |
| `3_end/haipipe-end-trig` | N/A | inference trigger；F12 不应删掉其合法双格式 unwrap。 |
| `3_end/haipipe-task-for-endpoint` | FAIL | F01 样例仍被通用 lifecycle glob 发现；F12。 |
| `4_individual/haipipe-individual` | N/A | 一次 build 的内部 Steps；F14/F15。 |
| `4_individual/haipipe-individual-inference` | N/A | load/payload/POST 为请求内部操作；F12/F16。 |
| `4_individual/haipipe-individual-inference-judge` | N/A | judge 操作；F17/F18。 |
| `4_individual/haipipe-individual-inference-report` | N/A | report 操作；F17/F18。 |
| `4_individual/haipipe-task-for-individual` | FAIL | F01 样例；F02 旧脚手架。 |
| `5_fit/haipipe-task-for-fit` | FAIL | F01 样例；F02/F19。 |
| `6_eval/haipipe-task-for-eval` | FAIL | F01 样例；F02/F19。 |
| `7_display/haipipe-task-for-display` | FAIL | F01 样例；F03/F20。 |
| `8_stata/haipipe-task-for-stata` | FAIL | F01 四样例及 plan/report；F02/F19。 |
| `9_agent/haipipe-task-for-agent` | FAIL | F01 样例；F02。 |
| `9_agent/haipipe-task-llm-engine` | N/A | 执行 engine 不建 Workflow roster；其独立 ticket receipts 边界保留。 |

## 5. 实施顺序、依赖与完成标准

以下均为未来实施计划；本次未运行这些检查或部署步骤。

| 批次 | 拟做内容与交付物 | 依赖 | 本批验收 |
|---|---|---|---|
| A：确认当前权威和变更边界 | 固定本轮 diff；采用现有 Run schema、BJTR、`scripts/config/`、Result-root 规则；记录需要核实的 NN API 和 persona 边界。列出现有 4 个 Task 修改并保留。 | 无。已有明确权威不需要重新让用户选一次。 | 设计说明不再重复原报告已撤回的迁移；共享字段、兼容读法和新写法各有唯一 owner。 |
| B：共享 Workflow 与路径 | F01 主模板/plan/report/lifecycle prompts；F03 共享 `fn/run` 路径矛盾。增加或复用针对新 plan/report 的结构与语义检查。 | A | 新建、恢复、HOLD、失败和报告均以 Run Spec/Instance 配对；SELF/版本/新 Run 不混淆；self-serving 和外部 Result root 正确。 |
| C：类型样例和脚手架 | F01 的 12 份样例；F02 六类 scaffolds；F03 Page/Display 例子；F04 Raw 接续；F19 返回字段。Stata 的四个 stages 保留 domain 特例。 | B | 每类临时 Task 符合共享 hierarchy 和 plan schema；原有样例不教新作者写 `phases:`；返回字段满足实际 caller。 |
| D：Data 与 NN | F05–F10；F11 路由例子。核实实际 NN parser 后修 version/config 文案。 | 路径事项依赖 B/C；HumanFn、checklist、auth 文案可独立。 | HumanFn 路由唯一；同一 AIData 路径贯通；检查 ID 完整；auth 提示匹配 backend；版本 round trip 在实际库中被证实。 |
| E：Endpoint 到 Individual inference | F12 平台 pair/模板/review/consumer；F13 Local 默认与平台前置条件；F16 workspace 参数。 | 平台规范在 F12 内先定好，consumer 随后对齐；路径依赖 B。 | 本地 fixture 证明两平台 pair contract；支持的 shorthand 可换 workspace；真实云端部署未获授权/无平台环境时明确留作未验收。 |
| F：个人数据与报告可信度 | F14 实际 build 契约、F15 cache/刷新、F17 forecast→judge；F18 由内容 owner 定边界后更新 persona。 | F14 在 F15 前；F17 不依赖 F18 政策决定；配置能力复用 F16。 | 输入变化能刷新；失败不发布混合目录；judge 只对可验证事实给 verdict，缺输入状态可见；report/judge 共享允许行为。 |
| G：跨家族与导航 | F20 provenance、F21 Page/Discovery owner 与现行 ids、F22 README/DESIGN/TODO。 | 共享 Run/path 和 consumer contracts 稳定后。 | 图、samples 和引用与 owning family 一致；历史材料明确失效范围；当前 49 技能可导航；已修 Insight map 保持正确。 |
| H：fresh-context 验收和回归 | 按根 README:133-136 的 fresh-context 流程，让独立上下文在受控任务上实际选择并使用修订技能，记录路由、步骤、结果与 blocker。 | 各批完成后分批做，最后核对全家族清单。 | 不靠关键词零命中代替语义验收；不存在为了消灭 Phase 而多建 Runs 的反例；未具备环境的检查显式列为未完成。 |

可以并行的实施线是 Data/NN 文案、Endpoint contract、Individual cache；但它们应共同等待共享路径决策。Endpoint consumer 必须在平台 pair 规则确定后改。任何新共享返回字段都先核对 caller，再迁移各 specialist。F09/F10 的实际 API 和 F18 的产品文案边界是明确的不确定项，不以时间经过代替决定。

建议保留的验收场景：

1. 一个训练 Ticket 内的配置、训练、checkpoint 和 validation 是内部 Steps；两份独立参数任务形成两个 Runs。重试不自动新增身份，改变实质输入按 owner 规则处理。
2. 同一 Page 写作目标接受多轮反馈；反馈留在同一 Run，接受关闭 gate，改变目标才提出新 Run。controller pass 不伪造 Page Run id。
3. 一个 Raw Run 转换完、cluster 尚未完成；人能看见准确状态和继续方式。导入外部 receipt 后才能通过 Result gate。
4. 用六类旧 scaffold 各生成受控例子，包含 Stata 各 stage；config、Ticket、Page、receipt 使用同一 BJTR 地址和 output root。
5. HumanFn 请求跨三个入口路由一致；AIData 由生成到读取保持同一路径；GDrive auth 不提示 AWS SSO。
6. Endpoint 同平台 pair 能 round trip，错平台输入不静默得到错误结果；Individual consumer 的平台选择与 payload 匹配。
7. Individual 相同输入复用、短时间变化更新、旧目标刷新、失败保留旧完整结果；报告和其 forecast 精确匹配，缺 forecast 时不虚报独立事实检查通过。
8. Display provenance 保留完整来源 identity/path/hash；重新定位 upstream Run 与 source_data 选择规则无需依赖会话记忆。

这些是未来必要的行为检查，而不是为简单措辞改动编写镜像测试。根仓库没有统一 build/test 命令；平台、模型或临床相关运行结论需要实际对应环境，不能由本次文档复核替代。

## 6. 共享问题的负责边界

| 问题 | 主负责家族/组件 | 协调要求 |
|---|---|---|
| F01/F03/F04 | Task 的 `haipipe-workflow`、`haipipe-task`；中立身份由 Run 家族定义 | Task 修生成链和适配器；保留现有 `resource_controls`/兼容 dispatch 边界，不在各 subtype 发明 schema。 |
| F02/F19 | Task core 加对应六类 specialist | owner 先定 path/返回语义；不要把当前 `scripts/config/` 又迁回旧 `configs/`。 |
| F05–F11 | Task 内 Data/NN；实际模型/数据库 API 在用户项目 | 核实真实库版本后才能承诺 API 兼容；历史 review 不作当前事实。 |
| F12/F13/F16 | Task Endpoint、Individual 与目标平台 wrapper | wire pair 改动和 consumer 同批验收；Meta/Trig/Post 的共享角色保留。 |
| F14–F18 | Task Individual；患者文案由产品/内容 owner 决定 | 数据事实、审查能力和文案 policy 分别声明；不可让文案自我充当 ground truth。 |
| F20 | Task display-input 与独立 Display 家族 | Task 产小型数据和来源；Display 决定视觉产物与 intake，不把原始敏感数据交给视觉模板。 |
| F21/F22 | Task、Page、Discovery、Run，以及独立 Insight/Design 家族 | 由 Page/Run owner 定现行 id 和写作边界；Discovery 页迁移的归属需协调；Application 不能恢复为 Insight/Design 的父技能家族。 |

尚未确认的项目级事项：NN version normalizer 与开发 config 家址；外部 Databricks/SageMaker 平台脚本当前行为；patient-friendly 的行动建议政策；Discovery 批量页面重排的最终 owner。补充报告没有把这些不确定事项写成已经完成的修复或验证。
