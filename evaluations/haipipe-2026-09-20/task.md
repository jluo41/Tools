# Task 家族写作与交互评估

日期：2026-09-20  
评估根目录：`plugins/haipipe-toolkit/skills/task/`  
基线：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`

## 总体判断

本家族当前有 49 个 `SKILL.md`，与提供的 `inventory.json` 完全相符。所有 49 个当前技能均已完整阅读。主要问题是 Task 创建与报告流程仍以 `phases:` 为计划行，而当前 Workflow schema 已规定 `run_specs` 是唯一 Workflow 行 roster。此冲突同时存在于 Task 主指引、计划/报告程序和 12 份子类型计划样例中，会让新上下文生成不符合其引用 schema 的计划。另有数据责任人路由、Endpoint payload 契约、Individual 预测安全输入和 Stata/Task 目录结构等直接影响执行的矛盾。

当前 Run 判定为：**2 PASS、10 PARTIAL、8 FAIL、29 N/A**。PASS 是 `haipipe-workflow` 与 `haipipe-task-gpu`。FAIL 集中在 Workflow 计划结构及 Task 生命周期模板；N/A 表示技能本身不定义 Task Workflow roster，不代表其内容整体无问题。

**后续归属更新（2026-09-21）：** `haipipe-task-gpu` 与
`haipipe-task-gpu-training` 已移入
`task/5_fit/haipipe-task-for-fit/`，公开 Skill 名称保持不变。GPU 现在是
Fit Task 的执行修饰；独立 `gpu` Task type 路由已收回，评估、serving 和
engine 的 GPU 工作继续由各自 owner 负责。原始评分数字保留为评估快照，
当前路径和归属以本更新为准。

**后续归属更新（2026-09-21，Insight Page）：** `haipipe-page-insight` 原先
误放在 Task 的 `page-types/` 下，现已移到
`skills/insight/haipipe-page-insight/`。它仍是 Task 路由使用的
consumer-neutral topic/data Page 合同，公开 Skill 名称和调用方式不变；当前
清单按 Insight 归类为 9 个、Task 归类为 48 个。原先的 49 个 Task 统计保留
为本评估快照。

评估遵守“Workflow 是 Runs 的列表”这一边界：有独立输入、关闭条件和 Result/receipt 的工作可成为 Run；脚本内操作、检查、工具调用、Gate、数据拆分、Page controller pass 不会自动成为 Run。兼容用的低层 `phase`/`stages` 字段与当前语义冲突的指令分开处理，没有建议盲目全局替换。

## 快照、方法与限制

- 基线与当前 HEAD 均为 `f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。任务目录之外有 8 个子模块引用修改：`references/{cite-guard,grant-writer-skills,paper-rag-skill,paperspine,reprorun,research-agent-skills,research-co-pilot,scipilot-figure-skill}`；`evaluations/` 原先未跟踪且含本次既有 brief/inventory/session 文件。本报告原始评估阶段没有修改 Task 技能目录；后续归属调整见上方更新。
- 逐篇阅读 49 个当前 `SKILL.md`；并阅读各组所链接的当前 README、references、procedures/functions、模板、例子、agents 和可见交互文案。覆盖明细见下文。
- 只在核实文档描述含义时读少量源码或脚本，如 Individual payload / builder、Task raw 的 Databricks shell 模板。没有运行技能、服务、代码、checker 或测试；以下 walkthrough 均为桌面推演，不是运行时观察。
- 历史 `CHANGELOG.md` 与历史审查文件不作为当前行为的证明。相关历史材料仅用于确认某条修复记录或说明其过期；第三方 skill 实现、未分配家族、Task checker/tests、未检出的 `platforms/` 资料和大部分可执行资产没有全面审阅。逐组未读内容与代码审阅限制列在覆盖说明中。

## 高优先级发现

### P1 — 当前 Task 生命周期继续产出 schema 明确禁止的 `phases:` roster

证据：`haipipe-task/SKILL.md:123-139` 将 Plan、Build、Execute、Report 标为 “Four phases”；共享模板 `haipipe-task/ref/workflow-template.yaml:29-34` 用 `phases:` 包含 `Run`、Gate1、Gate2；计划程序 `haipipe-task/fn/stage-plan.md:36-40,95-112,133-182` 教作者按 “Phases → Steps” 分组并生成 `phases:`；报告程序 `haipipe-task/fn/stage-report.md:7,25-29,91-133,137-199` 要求镜像相同 phases 并记录 `phases_completed`。相反，当前共享 schema `haipipe-workflow/ref/plan-schema.md:19-34,120-129` 规定 `run_specs` 是唯一 Workflow 行 roster，并写明 “Do not add `phases:`”。

影响：一个按 Task 主程序工作的 agent 会生成自己所引用 schema 判为无效的计划；审查/报告还会继续把旧行结构传播到后续阶段。这不是历史字段或纯措辞差异，而是活动文档、样例和结构约束之间的直接冲突。

建议：保留 `/haipipe-task plan|build|execute|report` 作为命令/操作；在 WorkFlow 中用 `run_specs` 表达每个真正可单独验收的 Run。把 Configure/Train/Checkpoint/Validate、Gate1/2、Plan/Build/Execute/Report 留作 Run 内的 Steps/Gates，除非某项有独立输入、关闭条件和 Result/receipt。同步主模板、`stage-plan`、`stage-report`、lifecycle prompt、agents README 与对子类样例的引导。

### P1 — 12 份任务类型计划样例及主模板都沿用旧 roster

所有以下当前样例声明或链接共享 Workflow schema，却顶层使用 `phases:`：`1_data/haipipe-task-for-data/ref/workflow-plan-sample.yaml`、`2_nn/haipipe-task-for-algo/ref/workflow-plan-sample.yaml`、`3_end/haipipe-task-for-endpoint/ref/workflow-plan-sample.yaml`、`4_individual/haipipe-task-for-individual/ref/workflow-plan-sample.yaml`、`5_fit/haipipe-task-for-fit/ref/workflow-plan-sample.yaml`、`6_eval/haipipe-task-for-eval/ref/workflow-plan-sample.yaml`、`7_display/haipipe-task-for-display/ref/workflow-plan-sample.yaml`、Stata 的 `workflow-plan-sample-{case,cms,data,reg}.yaml`，以及 `9_agent/haipipe-task-for-agent/ref/workflow-plan-sample.yaml`。共享 `haipipe-task/ref/workflow-template.yaml:29-34,48-50,69-72` 也如此。schema 的相反要求见 `haipipe-workflow/ref/plan-schema.md:126-129`。

影响：每个子类型都把自己的旧例子作为 fresh-context 作者的模板；一致传播了错误结构，不能靠只改 umbrella 文案解决。样例中 Setup/SmokeTest/Verify、Load/Score/Compare、训练或包装顺序多是某一个 bounded Run 的内部步骤。

建议：先修共享 schema 主模板，再逐个修 12 份样例，让每个 `run_specs` 行都含独立边界、actor/action、entry/exit gate、route、result receipt、cardinality 和所需 Cells。若子步骤只是内部操作，就把它保留在 Run 的 action/steps 说明内。

### P1 — Raw Task 把跨系统手动交接写成一个 Workflow，但本地 Run 只回执“已转换”

证据：`1_data/haipipe-task-for-raw/SKILL.md:147-163` 将转换、用户上传、Databricks 集群执行、parquet 落地、可选本地同步连成 “Workflow”。但 `ref/run-databricks-sh-template.sh:43-54,67-84` 仅生成本地 `runtime.yaml`，结束状态是 `converted`/`failed`，明确标注 “Convert-only — upload notebook to Databricks to execute”。

影响：自动 Run 完成状态可能被误读为 extraction 已完成；执行结果缺少 Databricks 端运行回执和最终数据落地证据。这里不是每个交接都要成为 Run；问题在于目前一个 `converted` 回执覆盖不了远端执行的完成声明。

建议：把本地转换定义为一个有自己 Result 的 Run；Databricks 上传/运行列为明确的人类交接及外部执行状态，并要求 run URL/ID、结束状态、输出位置等可核验 receipt 后，才能报告 extraction 成功。若整个远端 extraction 由同一独立 Ticket 驱动，再把远端执行建成有独立 Result 的 Run；不要把上传动作或每个 cluster 操作自动拆 Run。

### P1 — SourceFn / HumanFn 责任分配矛盾会使 Data builder 路由错人

证据：`1_data/haipipe-data-source/SKILL.md:15,114-118`、Data umbrella `haipipe-data/SKILL.md:35-38`、Record `haipipe-data-record/SKILL.md:15,30` 把 HumanFn 放在 Record/Stage 2；但 `haipipe-data-source/SKILL.md:31` 将 SourceFn 与 HumanFn 一并交给 Source 的 design-chef。共享指南 `haipipe-data/fn/fn-3-design-chef.md:178,272-293,795-800` 也同时把 SourceFn 放 Stage 1、HumanFn 放 Stage 2。历史 `1_data/SKILLSET_REVIEW.md:48` 曾记过修复，但当前说明仍互相打架。

影响：用户要编辑 HumanFn 时，agent 可能生成 Stage 1 Source，而非 Record 侧 HumanFn，并误判已有资产或调用错 specialist。

建议：明确 Stage 1 仅拥有 SourceFn；Stage 2 由 RecordFn/HumanFn 负责。修改 Source skill 的分派语句及共享 design-chef 的类型路由清单，补一条 HumanFn 请求到 Record specialist 的例子。

### P1 — Endpoint 的部署平台与 wire-format 契约互相冲突

证据：`3_end/haipipe-end/ref/0-overview.md:222-240` 说 Fn pair 按平台选用，并分别列 SageMaker flat JSON 与 Databricks `dataframe_records`；同文件 `:298-324` 又说两个格式都由所有 Fn 透明处理且“不存在 platform-specific Fn”。`haipipe-end-input2src/ref/concepts.md:37-44` 要求 parser 只读目标平台 shape，但 `:126-132` 的示例、`haipipe-end/fn/fn-design.md:296-304` 及 `haipipe-end-endpointset/fn/fn-review.md:144-149` 都要求/生成双格式 parser。`haipipe-end/ref/0-overview.md:245` 还把目标平台的 `.tar.gz` 写成 “same artifact!”。Individual inference `4_individual/haipipe-individual-inference/SKILL.md:39-40` 声称一个 payload 可同时供两种平台使用；源码 `src/build_payload.py:63-90` 固定生成 `dataframe_records`。

影响：作者无法确定应该部署哪对 Fn、parser 要接受哪种 shape、包是否可以跨平台共用。Individual 实际请求也不能满足一个只接受 SageMaker flat JSON 的 Endpoint。

建议：按目标平台选择一对 Src2InputFn/Input2SrcFn，parser 只接受该平台的 wire shape；统一 overview、设计指南、审核 checklist、样例和 Individual consumer。明确 Local 格式；说明相同之处指压缩/产物组织还是内容完全兼容。保留同一打包工具也不等于跨平台 payload 契约相同。

### P1 — Individual 构建文档描述的操作与实际 builder 不符，缓存可忽略输入变化

证据：`4_individual/haipipe-individual/SKILL.md:131-154` 说构建会运行 `fn_source.run()` 与 `fn_record.run()`；`:184-195` 说依据清单新鲜度跳过。实际 `fn/build_sample_individuals.py:1-5,260-303` 过滤已有的全局 Source/Record parquet 并复制个人切片，没有运行这两个 pipeline；缓存检查 `:238-247` 只看 `built_at` 是否在一小时内。

影响：agent 会预期或调用不存在的构建步骤；输入刚更新时也可能复用旧切片。

建议：按实际构建行为重写说明，指出 raw 文件仅在可用时物化、个人 Source/Record 从共享 store 过滤。用输入、配置和 builder 版本指纹判定缓存，并给出明确的强制重建选项。

### P1 — Individual inference 将 Workspace 固定到一台机器的绝对路径

证据：`4_individual/haipipe-individual-inference/src/load_patient.py:21-22` 写死 `WORKSPACE_ROOT = Path("/home/jluo41/WellDoc-SPACE")`；resolver `:27-37` 支持 Subject shorthand/路径，却没有 workspace 参数。Inference SKILL quickstart 使用 `Subject-18`，没有说明固定根路径。

影响：不同机器或新 checkout 上，即使传入有效 Subject ID 也可能读不到数据。

建议：以配置项或环境变量注入 workspace root，并在 SKILL 中说明 shorthand 的解析规则及默认值；无显式配置时，检查当前 repo/workspace 而不是硬编码个人路径。

### P1 — Stata 说明的 Task 目录布局与当前 Run 层级冲突

证据：`8_stata/haipipe-task-for-stata/SKILL.md:75-90` 与脚手架 `fn/scaffold.md:7,43-53` 使用平铺 Task 目录；新 Stata 说明 `ref/stata-dialect.md:96-135` 则说当前形状是嵌套结构、平铺形状只属 legacy。Task 的 canonical hierarchy `haipipe-task/ref/hierarchy.md:11-17,58-97,229-239` 要求 Block/Job/Task/Run 四层结构。Stata 的 plan/report 程序仍要求 `phases:`，例如 `fn/plan-stata.md:50-108,110-175,182,197`、`fn/report-stata.md:41-68,75-117,132-150`。

影响：新脚手架可能产出无法被当前 Task audit/Run 机制发现的路径，同时计划程序还与共享 WorkFlow schema 冲突。State/CMS/Case/Data/Reg 等 Stata 阶段是 domain pipeline 分段，也不应自动提升为 Runs。

建议：先决定 Stata 当前 canonical path，并与 Task hierarchy/audit 对齐；再把 plan/report 用 `run_specs` 表达可独立验收的 Stata Ticket，Stage/SQL 步骤留在 Run 内。废弃平铺布局应标成 legacy 示例，而非现行 scaffold。

### P1 — Patient-facing report 的行动语气与安全审核规则冲突，默认 judge 缺少阈值输入

证据：`4_individual/haipipe-individual-inference-report/personas/patient-friendly/system.md:11,19-26` 要求解释 “what to do about it”，偏好 “drink some water and walk for 10 minutes”，同时又说不要替医生提供行动建议；`4_individual/haipipe-individual-inference-judge/personas/safety-review/system.md:5,9-16,23-26` 要按原始预测核对 `<70`、`>300` 并禁止医疗行动建议。报告 CLI 写 `forecast.json`（`...report/scripts/make_report_cli.py:87-99`），但 Report SKILL 输出清单 `:86-92` 未列此文件；judge CLI `...judge/scripts/judge_report_cli.py:46-65` 只加载 `report.json`，没有把 `forecast.json`/`extra_context` 传给 judge。底层函数虽支持 context（`...judge/src/judge_report.py:37-54,176-182`），默认 CLI 未连通。

影响：患者文案可能越过模型解释边界给出生活/治疗建议，而默认 judge 无法按 persona 要求核对阈值事实。

建议：把文案限定为预测说明、遵循现有 care plan 或联系 care team；不建议新的治疗行动。让 judge CLI 读取必要 forecast 窗口并传入 context，或明确缺少 ground truth 时不做阈值判断。

### P2 — AIData 新路径已进入专用技能，但共享 Data/NN 指南仍指向旧资产布局

证据：`haipipe-data-aidata/SKILL.md:127-131` 及其 `ref/concepts.md:64-67`、模板 `:168-175` 使用 `_WorkSpace/4-AIDataStore/{ParentSet}/@v{N}AIData-{name}/`。共享 Data `fn/fn-0-dashboard.md:536,544`、`fn/fn-1-load.md:264,281,287`、`fn/fn-2-cook.md:480,532,599` 仍使用 `{aidata_name}/@{version}`；NN 测试 `2_nn/haipipe-nn/fn/fn-test.md:218,233` 也保留旧路径。

影响：dashboard/load/cook/test 指引会找不到已经按新规则保存的 AIData。

建议：将路径规则集中在一个 live reference 中，其余指南都链接或引用该规则；在迁移期明确兼容查找顺序，不要同时把两种结构说成当前布局。

### P2 — Data reviewer 的快捷检查漏掉新规则并寻找旧 config 目录

证据：`haipipe-data/fn/fn-review.md:50,87,357,365,376,386` 仍扫描 `**/scripts/config/**/*.yaml` 或 `<task>/scripts/config/<name>.yaml`；当前 Data 任务配置使用 Task `configs/`。完整检查清单已有 Source SF-15 `:212-213`、Record RF-15..17 `:255-260`、Case CF-12..13 `:301-304`，但 quick reference `:410,412,414` 仅列到 SF-10、RF-14、CF-11。

影响：合法 configs 可能不进入 review，新加入的 external source、时点安全和 parity 检查也可能因快捷清单未同步而跳过。

建议：按当前目录布局更新扫描规则；从完整检查 ID 生成 quick reference，避免两份清单手工漂移。不要仅凭历史 `SKILLSET_REVIEW.md` 中的“已修复”记录判定当前实现已一致。

### P2 — Remote 凭据提示与其 backend 分支规则不一致

证据：`1_data/haipipe-data-remote/ref/concepts.md:137-152` 区分 GDrive/rclone token 与 S3/AWS SSO，但 `:176` 将 auth error 的建议概括成 surface SSO URL；`SKILL.md:123-126` 又按 gdrive 和 s3 分支提供不同恢复动作。

影响：GDrive 用户遇到认证失败时可能被引导去找并不适用的 AWS SSO URL。

建议：让所有状态/pull/push/error 文案读取 backend 并给出匹配的 token-refresh 或 SSO 操作；通用 error 说明只说“显示后端对应的认证恢复提示”。

### P2 — NN 的“run model”路由可能把训练误派成 smoke test

证据：`2_nn/haipipe-nn/SKILL.md:66-74` 将 `run` 动词映射到 `test`；但 `2_nn/haipipe-task-for-algo/SKILL.md:15-18,61-68` 明确 smoke test 不是训练，训练归 `/haipipe-task-for-fit`。

影响：用户说 “run/train model” 时可能只得到 smoke test，而不是训练结果。

建议：按用户表达的结果区分 test/inference 与 fit/train；当用户要生成新的模型参数或 checkpoint 时路由 Fit，当验证既有模型行为时路由 test。无需把 model test 的每个内部 Step 都拆成 Run。

### P2 — NN / Fit / Eval / Agent 的配置与产物路径示例没有和 canonical Task 路径对齐

证据：Data 的旧 review 记录 Task config 已从 `scripts/config/` 移到 `configs/`（`1_data/SKILLSET_REVIEW.md:31`），但 Data 设计指南 `fn-3-design-chef.md:158-162`、`fn-4-design-kitchen.md:78-84` 和 reviewer 仍保留 `scripts/config/`。NN 共享 `fn-generate.md:242-247`、`fn-dashboard.md:210-221` 使用 repo-root `config/...`；AIData test 又有旧目录（P2 path finding）。Fit/Eval/Agent 仍示例平铺 `{NN}_job` 路径（Fit `SKILL.md:44-55`、Eval `:27-37`、Agent `:29-41`），与 Task hierarchy 的 Block/Job/Task/Run 层级不符。NN workspace config 的目标目录尚需核实，不应盲目套用 Task `configs/` 迁移。

影响：脚手架、dashboard 和 run command 可能找不到配置或把 Job/Task/Run 写入不兼容的目录。

建议：分别确认 Data、NN 的当前 config owner/path；将 Task 类型共享样例与 hierarchy 对齐，再让各 specialist 引用该单一权威路径。若平铺结构只为 legacy 文件，标明迁移读取兼容规则但不要把它作为新建模板。

### P2 — Fit/Eval/Stata 初始返回 schema 与实际报告字段不一致；Display provenance 不能唯一定位 Run

证据：Fit `5_fit/haipipe-task-for-fit/SKILL.md:19,89-97`、Eval `6_eval/haipipe-task-for-eval/SKILL.md:19,66-74`、Stata `8_stata/haipipe-task-for-stata/SKILL.md:22,367-375` 的 initial output 示例为 `{status, task_folder, run_name, files}`，后续返回合同又使用 `{status, summary, artifacts, next}`。Display scaffold `7_display/haipipe-task-for-display/fn/scaffold.md:25-31` 要求 provenance full Run id/path/hash，但 seed config `:25-28` 只有 compact `b01j01t01r01`，provenance JSON `:16-21` 只有 `derived_from`，没有 `run_id`。

影响：调用方不能稳定解析状态/下一步；展示产物只能保留不完整的短路径，无法唯一回溯其源 Run。

建议：区分 scaffold acknowledgement 与执行完成返回，并统一公共必需字段与 type-specific optional fields；Display provenance 明确写入完整源 Run id 和路径/hash，旧 compact id 只作为便于查看的 display key。

### P2 — Page Task 的 Result 示例落在 canonical Run Result 目录之外

证据：`10_page/haipipe-task-for-page/SKILL.md:40` 写 `$OUTPUT_ROOT/<task>/results/<run>/values.yaml`，但目录树 `:63` 和示例 `:105` 写 `$OUTPUT_ROOT/results/t01_collect_values/r01_.../values.yaml`；`ref/specimen-page-values.md:31` 重复后者。canonical Run contract `haipipe-task/fn/run.md:23` 要求 `$OUTPUT_ROOT/<task>/results/<run>`。

影响：照抄 specimen 会让 Task audit 或 Page 的 Result binding 找不到输出。

建议：将目录树和 specimen 修正为 canonical Task/Run path；若 Page 只引用 Result 而不复制 Task Folder，在图中显式标记路径为链接/引用。

### P2 — Insight 图仍使用“Phase × Run”，Task 架构图仍将 Insight/Design 归到 Application

证据：`page-types/haipipe-page-insight/SKILL.md:149-153` 指向 “Phase × Run Map”；`ref/workflow-table.md:8-23,25-43` 用 Phase 列分组 Scope/Plan、Bind/Evidence、Reason/Publish、Synthesize。该文档正确写明 checkpoint 不等于 Run、避免重复 episode Runs，但 `Phase` 标题仍将 Run roster 和过程 checkpoint 混在一起。

另外 `task/DESIGN.md:28-40` 把 `applications/` 映射到 `/haipipe-insight, /haipipe-design`；当前 Insight 与 Design 是 `skills/insight/` 和 `skills/design/` 两个独立一等家族，且用户 brief 明确规定不存在 Application parent family。相反，`task/TODO.md:14-16` 已在 2026-09-20 标记 Application bucket 退休。

影响：Insight workflow 使用者可能误把 checkpoint/analysis stage 当成 Runs；维护者可能继续按已退休的 family hierarchy 放置责任。

建议：将表命名为 Activity / Run allocation map，保留 checkpoints、Steps 与 Runs 的边界；把 Task DESIGN family map 画为 Task、Discovery、Insight、Design 等独立 siblings。区分项目产物目录 `applications/` 与 skill-family ownership。

### P2 — Task README 的“无消费者”边界表述过宽且其生命周期仍落后

证据：`task/README.md:24-41` 仍称 Plan→Build→Execute→Report 是 four-stage lifecycle；`:99` 说 Tasks “tracks no consumers, names none”，但 `:116-121` 接着列出 Insight、Paper、Application 等消费者及其职责；`:45-64` 的 Task domain 清单只覆盖 1–9，而当前 tree 有 10_page，dispatcher `haipipe-task/SKILL.md:197` 已路由 `page`。

影响：文档意图是 Task Result 保持 consumer-neutral，但字面上否定了它自己列出的消费者；新维护者还会漏掉 Page 类型。

建议：改成 “Task Results remain consumer-neutral; a consumer records its own Supporting Run and any Local Run.” 更新 domain 清单。Plan/Build/Execute/Report 可保留为命令/操作，但不要继续宣称它们是 WorkFlow Phases。

### P2 — Endpoint / Agent 子流程状态与实际可执行程度不一致

证据：Databricks deploy `3_end/haipipe-end-deploy-databricks/SKILL.md:22-24` 标 active、tested，但 `:93-110` 把 procedure 标为 placeholder；SageMaker `haipipe-end-deploy-sagemaker/SKILL.md:87-104` 同样是 placeholder。Local deploy `haipipe-end-deploy-local/SKILL.md:19-30,38-43` 说 FastAPI 路径完整，但默认 framework/quick command 指向 Flask。`task/agents/README.md:19-27,56-60` 仍称 four-phase lifecycle；`task/DESIGN.md:4,323-335,440-467` 仍描述 4-phase engine，而 `TODO.md:45-47` 指示保留该 engine。

影响：fresh-context 操作者看到 active/tested 后可能找不到下一条可执行命令；Local 默认流程指向未完成路径；agent roster 文档会继续教旧 lifecycle。DESIGN 属于旧架构材料，但页面没有将它明确标成历史，因此不能作为当前架构权威。

建议：按真正可运行的程序更新状态标签/命令；Local 默认切到完整路径或补齐 Flask；当前 README/agent prompts 改用 Run/Step 模型，并将历史 DESIGN 生命周期明确标为 dated archive 或迁移背景。

## 值得保留的做法

- `haipipe-workflow/SKILL.md` 与 `ref/plan-schema.md` 把 Run Spec、Run Instance、Step 区分清楚；schema 将 `run_specs` 设为唯一 roster。低层 `phase`/`stages` API 作为 progress/compatibility metadata 的边界也写得清楚，可保留字段但不应继续教作者将它们当 domain Workflow rows。
- `5_fit/haipipe-task-for-fit/haipipe-task-gpu/SKILL.md` 用 Ticket、Run、配置、Result/receipt 配对表达 Fit 队列，明确 supervisor 不会隐式创建 Run。
- `5_fit/haipipe-task-for-fit/haipipe-task-gpu-training/SKILL.md` 对实际训练 Run 的责任表达清楚；数据 splits 不是 Workflow Runs。
- `haipipe-task/fn/run.md` 的输入/输出约束、精确路径和 Run receipt 检查有助于 agent 收尾；Task 的 fail/block 处理在 `fn/block.md` 里也能让人知道待解决事项。
- `haipipe-data-remote/SKILL.md:21-27,93-100` 先 dry-run、向人展示计划再确认，对远程复制有清楚的人类控制点；不可删除/镜像的边界易懂。凭据错误按 backend 提示的原则正确，但 concepts 文档另有通用 SSO 说法，见 P2。
- Data umbrella 的用户确认点只在多项匹配时出现；Endpoint 显式选择目标平台、ModelInstance 和 payload；GPU queue 保留可审计 Ticket/Result。应继续保留这些明确可见的输入与下一步。
- Insight 文档明确说 checkpoint、LLM call 与单个表格行不是 Run，并提醒只保留真正的 Run 边界。应保留这条边界，修正旧 map 标题而非把 checkpoint 升格。

## Workflow / Run 逐技能判定

PASS = 当前表达与 Run roster 契约一致；PARTIAL = 核心边界大体对，但有活跃歧义/用词；FAIL = 明确结构或语义冲突；N/A = 不拥有 Task Workflow roster，也未把内部工具步骤错当成独立 Run。Remote 的 dependency pull plan 因其将多个 pull 组成一条可确认执行序列，暂列 PARTIAL：需明确它是一项有 receipt 的 bounded pull-plan operation，还是一个正式 WorkFlow；不得把每条 CLI 调用自动当 Run。

| 当前 skill（相对 `skills/task/`） | Verdict | 依据 / 相关问题 |
|---|---|---|
| `haipipe-task` | FAIL | 四个 phases 和 `phases:` 模板冲突于 `run_specs` schema（P1）。 |
| `haipipe-workflow` | PASS | `run_specs` 唯一 roster；Run Instance / Step / progress metadata 边界清楚。 |
| `5_fit/haipipe-task-for-fit/haipipe-task-gpu` | PASS | Fit queue item 是可配对 Ticket、Run、Result 和 receipt；无隐藏 Run。 |
| `5_fit/haipipe-task-for-fit/haipipe-task-gpu-training` | PASS | Fit training Run 所属清楚；data splits 不会被升级为额外 Run。 |
| `haipipe-page-task` | PARTIAL | Page evidence 有 Run 边界；“current Page workflow phase”应为 controller label/route。 |
| `10_page/haipipe-task-for-page` | FAIL | 四阶段/旧计划结构；Page Result specimen 路径偏离 canonical Run 路径。 |
| `page-types/haipipe-page-insight` | PARTIAL | 正确区分 Run 与 checkpoint，但仍有 “Phase × Run Map”。 |
| `1_data/haipipe-data` | N/A | 域/Store 介绍，无 Task Workflow roster。 |
| `1_data/haipipe-data-aidata` | N/A | AIData 资产操作；自身不创建 Task WorkFlow。路径支持文档有旧值。 |
| `1_data/haipipe-data-case` | N/A | Case 资产逻辑；配置字段 `phase='all'` 是 API 值，不是 Workflow unit。 |
| `1_data/haipipe-data-external` | N/A | External 资产操作；Phase 1/2 是成熟度/实现状态描述。 |
| `1_data/haipipe-data-raw` | N/A | Raw domain 操作，不定义 Task Workflow。 |
| `1_data/haipipe-data-record` | N/A | Record/HumanFn 资产逻辑；不是 Task Workflow owner。 |
| `1_data/haipipe-data-remote` | PARTIAL | dependency-aware 多资产 pull plan 需说明是一项有 receipt 的 operation，或按 Run specs 建模；CLI calls 不自动成为 Runs。 |
| `1_data/haipipe-data-source` | N/A | SourceFn 资产工作；HumanFn 路由矛盾是职责问题，不是 Run roster。 |
| `1_data/haipipe-task-for-data` | FAIL | 样例使用顶层 `phases:`，缺少共享 schema 要求的 Run Spec 边界。 |
| `1_data/haipipe-task-for-raw` | FAIL | numbered Workflow 包含外部 Databricks 执行，但本地 Run 只回执 converted，没有远端执行 receipt。 |
| `2_nn/haipipe-nn` | N/A | NN 领域编排/脚本，无用户 Workflow roster；若单独测试需另行确定 Run 边界。 |
| `2_nn/haipipe-nn-algo` | N/A | 模型算法/代码逻辑，无 Task Workflow roster。 |
| `2_nn/haipipe-nn-instance` | N/A | resolver phases 是配置解析检查，不是 Workflow rows。 |
| `2_nn/haipipe-nn-modelset` | N/A | pipeline 与模型资产版本历史；`@run-v000X` / `run_versions` 不是 Task Workflow Runs。 |
| `2_nn/haipipe-nn-tuner` | N/A | 调参操作技能，无正式 Workflow row schema。 |
| `2_nn/haipipe-task-for-algo` | FAIL | Setup/SmokeTest/Verify 用旧 `phases:` 样例表达。 |
| `3_end/haipipe-end` | PARTIAL | 目标平台部署阶段 Phase 0–2 语义不明确；确认是 Run 内操作还是独立可验收 Run。 |
| `3_end/haipipe-end-deploy-databricks` | N/A | 平台部署步骤 / execution id，不创建 Task Workflow roster；另有 procedure placeholder 问题。 |
| `3_end/haipipe-end-deploy-local` | N/A | deploy/test/monitor 操作，无 Workflow row roster；默认 Flask 与可用 FastAPI 不一致。 |
| `3_end/haipipe-end-deploy-mlflow` | N/A | deferred，无当前 Workflow roster。 |
| `3_end/haipipe-end-deploy-sagemaker` | N/A | 部署操作和 endpoint execution id，不定义 Task Workflow rows。 |
| `3_end/haipipe-end-develop-databricks` | N/A | service Job `run_id` 是实际执行标识，不是 Workflow roster。 |
| `3_end/haipipe-end-develop-local` | N/A | 对 NN/EndpointSet 的内部调用，不定义用户 Workflow。 |
| `3_end/haipipe-end-develop-sagemaker` | N/A | SageMaker pipeline 子步骤属服务内部执行，不是 Task Workflow roster。 |
| `3_end/haipipe-end-endpointset` | N/A | package/test/profile/review 是操作面；内部步骤未升为 Runs。 |
| `3_end/haipipe-end-input2src` | N/A | Step 2 of 7 是一次 inference 内部步骤。 |
| `3_end/haipipe-end-meta` | N/A | 单个 Fn 的 packaging-time 行为，不是 Workflow。 |
| `3_end/haipipe-end-post` | N/A | 单个 response-format Fn，不是 Workflow。 |
| `3_end/haipipe-end-src2input` | PARTIAL | packaging 内部动作仍称 Phase 1–3；应称 Step 并留在一个 bounded package Run。 |
| `3_end/haipipe-end-trig` | N/A | 单次 inference trigger 逻辑，无 Workflow rows。 |
| `3_end/haipipe-task-for-endpoint` | FAIL | Phase 2: Build 旧生命周期术语，计划样例又用 `phases:`。 |
| `4_individual/haipipe-individual` | N/A | Build Logic Step 1–5 为构建过程步骤，无 Workflow roster。 |
| `4_individual/haipipe-individual-inference` | N/A | load→payload→POST 是一次预测请求内部流程，不是多 Runs。 |
| `4_individual/haipipe-individual-inference-judge` | N/A | 单份报告的 judge 操作，无 Workflow rows。 |
| `4_individual/haipipe-individual-inference-report` | N/A | 单份报告生成步骤，无 Task Workflow roster。 |
| `4_individual/haipipe-task-for-individual` | FAIL | Phase 2: Build 术语与 `phases:` workflow-plan sample 均冲突。 |
| `5_fit/haipipe-task-for-fit` | PARTIAL | Task Run 本身可对应每个训练 Ticket/variant；样例把 Configure/Train/Checkpoint/Validate 写入 `phases:`。 |
| `6_eval/haipipe-task-for-eval` | PARTIAL | 每个模型/split 的评估可做一个 Run；Load/Score/Compare/Emit 样例仍为 `phases:`。 |
| `7_display/haipipe-task-for-display` | PARTIAL | upstream Run/来源关系表达较好，但计划样例使用 `phases:`。 |
| `8_stata/haipipe-task-for-stata` | FAIL | planner/report 要求 phases；目录 hierarchy 也与 canonical Task 层级不符。 |
| `9_agent/haipipe-task-for-agent` | PARTIAL | 单个 prompt-ticket Run 边界可成立；Setup/Execute/Parse 样例仍为 `phases:`。 |
| `9_agent/haipipe-task-llm-engine` | N/A | engine/LLMRec ticket 与 receipt 能表达 Run，但不创建 Task Workflow roster；内部调用是步骤。 |

## 子组覆盖与全量清单

每个表项对应一个已完整阅读的当前 `SKILL.md`。支持材料列是本次逐项阅读的当前材料集合；共享 Task/Workflow 文件及其引用已在前文注明，具体支持发现均给出逐文件行号。

| 子组与完整技能清单（路径相对 `plugins/haipipe-toolkit/skills/task/`） | 已查的当前支持材料 | 排除 / 缺口 |
|---|---|---|
| **Core / Page / Insight：5** — `haipipe-task`、`haipipe-workflow`、`haipipe-page-task`、`10_page/haipipe-task-for-page`、`page-types/haipipe-page-insight` | Task README、Task agents README 与 agent instructions、`haipipe-task/fn/` 全部程序文档及引用的 hierarchy/task structure/authoring convention/workflow/page/schema 文档、workflow template、Task lifecycle workflow JS、Workflow concepts/plan-schema/template/API/runtime references、Page task 模板与 specimen、Insight 的 instance-items/workflow-table/task-calls/migration、Insight agent manifest、Page owner 的路由/Workflow 兼容语义。 | 未逐行读 `config-meta-template.yaml`、`databricks-execution.md`、`intent-docstring-template.py`、`metrics-json-schema.md`、`run-sh-template.sh`、`runtime-yaml-schema.md`、`running-process.txt`；未读 Task checker 实现/tests、Insight scripts/tests。未运行 skill、checker 或 tests。 |
| **Data / NN：16** — `1_data/haipipe-data`、`haipipe-data-aidata`、`haipipe-data-case`、`haipipe-data-external`、`haipipe-data-raw`、`haipipe-data-record`、`haipipe-data-remote`、`haipipe-data-source`、`haipipe-task-for-data`、`haipipe-task-for-raw`；`2_nn/haipipe-nn`、`haipipe-nn-algo`、`haipipe-nn-instance`、`haipipe-nn-modelset`、`haipipe-nn-tuner`、`haipipe-task-for-algo` | Data umbrella README/overview/7 个共享 fn 文档；Data specialist 的链接 refs、templates、examples；External/Remote references 与 live fn 文档；两个 Task 的 scaffold/config/workflow 样例。NN README、overview、4 个 layer concepts、4 个共享 fn 文档。历史 subgroup review 仅用来核对先前修复陈述。 | 没有读 Data/NN 可执行源码与资产；CHANGELOG 排除。未发现 NN subgroup review。历史 review 不是当前行为证明。 |
| **Endpoint / Individual：20** — `3_end/haipipe-end`、`haipipe-end-deploy-databricks`、`haipipe-end-deploy-local`、`haipipe-end-deploy-mlflow`、`haipipe-end-deploy-sagemaker`、`haipipe-end-develop-databricks`、`haipipe-end-develop-local`、`haipipe-end-develop-sagemaker`、`haipipe-end-endpointset`、`haipipe-end-input2src`、`haipipe-end-meta`、`haipipe-end-post`、`haipipe-end-src2input`、`haipipe-end-trig`、`haipipe-task-for-endpoint`；`4_individual/haipipe-individual`、`haipipe-individual-inference`、`haipipe-individual-inference-report`、`haipipe-individual-inference-judge`、`haipipe-task-for-individual` | Endpoint README/overview/deploy overview/fn design、各 Fn concepts、EndpointSet 五份 fn、各 target develop concepts、Task scaffold/config/workflow/performance notes、相关 builder 与 Local serving 脚本。Individual Task scaffold/config/workflow sample、individual builder、inference source/CLI、report/judge scripts/schemas/personas；共享 Workflow schema/template/creator/reviewer agents。 | CHANGELOG 排除；LESSON 只读当前矛盾相关段落；历史 SKILLSET_REVIEW 作为历史材料。当前 checkout 没有 `platforms/`，故未核对平台仓库 CLAUDE/docs。未运行代码/服务/skills/tests。 |
| **Fit / Eval / Display / Stata / Agent：8** — `5_fit/haipipe-task-for-fit`、`5_fit/haipipe-task-for-fit/haipipe-task-gpu`、`5_fit/haipipe-task-for-fit/haipipe-task-gpu-training`、`6_eval/haipipe-task-for-eval`、`7_display/haipipe-task-for-display`、`8_stata/haipipe-task-for-stata`、`9_agent/haipipe-task-for-agent`、`9_agent/haipipe-task-llm-engine` | 逐个当前 SKILL、相关 refs/templates/changelogs、全部 26 份 Stata 文件中的相关 planner/report/dialect 资料；Fit-owned GPU companions 的交叉材料；LLM engine 文档；Task schema 与 run contract。 | LLM engine Python 仅做关键词层面检查，未完整审代码；未运行 skill/tests。历史 changelog 仅用于语境，不作为当前语义依据。 |

总计：**49/49 个当前 Task SKILL.md 已完整阅读**，覆盖分组与 `inventory.json` 相符。未审第三方工具行为、Task runtime 实际执行、平台外部仓库或未分配的其他 skill family；这不是那些内容正确与否的判断。

## 桌面推演（非运行时测试）

### 1. Task / GPU：两个独立配置的训练请求

用户说：“Fit these two model configs, compare validation metrics, and report the better one.” 合理路由是为每个可独立训练/验收的 Ticket 建一个 Run，输入分别绑定 config、输出分别有 Result/receipt；training、checkpoint、validation 属于各 Run 内部操作。比较结果可是一项有独立输入/结论的后续 Run，若只是同一报告操作则留作 Report Step。当前四阶段主模板会误导作者创建 Configure/Train/Validate phases。改后先显示识别出的两个 config/Ticket 与预期输出，只在模型或验证集无法唯一确定时提问。

### 2. Data / NN：用户要生成 HumanFn 并验证模型

用户说：“Add a human-readable label for this record and check whether the model still passes its staged tests.” 第一问应路由到 Stage 2 HumanFn/Record owner，而非 Stage 1 SourceFn；目前 source skill 的共同路由会误导。对模型检查，L2/L3/L4 脚本各有独立执行与门控，可作为候选 Run 边界；各脚本内部 7 个步骤及结果表行仍是 Run 内部证据。先找当前配置与已有 Run；只有候选配置/记录不唯一时再向人询问。

### 3. Endpoint：封装 Ohio 模型并部署 SageMaker

用户说：“Package the trained Ohio model and deploy it to SageMaker.” 先定位唯一 ModelInstance、选定目标平台对应 Fn pair，再把 packaging、同目标推理验证和摘要作为有 Result/receipt 的 package Run；deploy 作为目标环境的部署操作，并留存 endpoint/execution id。当前样例把内部过程称四个 Phases，wire-format 文档又冲突。若 ModelInstance 或目标 Fn pair 不唯一才提问；用户已给出目标后不必每一步重复展示完整 YAML 并等无信息确认。

### 4. Individual：生成患者预测并做 safety review

用户说：“Generate a patient-facing forecast for Subject-559 and run safety review.” 首先检查 Subject 能否由配置的 workspace 解析、目标 endpoint 是否明确；目前有固定 workspace 路径和固定 `dataframe_records` payload。Report 应解释预测、避免新治疗动作建议；Judge 必须获得 forecast window 才能按阈值 persona 核对。仅在 subject、endpoint 或数据不唯一/不可解析时询问，而不是要求用户补齐实现细节。

### 5. Fit / Eval / Display / Stata / Agent：一个分析变体从训练到可视化

用户说：“Train variant A, evaluate it on split B, make a figure, and send a reviewer agent to check the result.” 训练 Ticket、评估 Ticket 各形成自己的 Run/receipt；Figure 来源于评估 Run 并保留完整 source Run ID；agent reviewer 若有独立输入、判断、Result 则是单独 Run，否则作为 review Step。Stata 的一个 CMS 2019 Job 可是一个 bounded Run，抽取、benefit 计算、summary 是其内部步骤；年度/Reg/CMS domain stage 不自动成为 Run。当前 Fit/Eval/Display/Agent 样例 phases 与 Stata planner 都会产生另一种模型。

### 6. Page / Insight：带证据的 Page 与综合解释

用户说：“Write an Insight page comparing result A and B, include source evidence, and update the answer after review.” A/B 若来自已有 Run，就引用完整 source Run IDs；Page writer/reviewer checkpoint 是 Page 过程步骤，不要创建 controller-pass Runs。若新增分析有自己的 Ticket/Result，才创建 supporting Run。当前 “Phase × Run” 表可改成 activity/run allocation 表；Page workflow owner 已将 controller `phase/cycle` 限定为兼容 dispatch/progress labels，Task Page skill 应沿用该边界。

## 英文改写示例

### 主 Workflow 计划模板

**Before** — `Four phases: Plan → Build → Execute → Report` / `# P: Phases → Steps`  
**After** — “Plan, Build, Execute, and Report are Task commands. The Workflow roster contains one Run Spec for each independently closable unit of work. Script preparation, execution steps, gates, and reporting operations remain inside the Run that owns them unless they have a separate input, exit gate, durable Result, and receipt.”

### 训练样例

**Before** — `Typical training phases: Configure → Train → Checkpoint → Validate`  
**After** — “Create one Run Spec for each independently requested training Ticket/variant. Configure, train, checkpoint, and validation are operations inside that Run; create another Run only when the validation request has its own scope, close condition, and Result.”

### Task Results 与消费者

**Before** — “Tasks track no consumers and name none.”  
**After** — “Task Results remain consumer-neutral. A consuming skill records its Supporting Run ids and creates a Local Run only when it needs new evidence at its own scope.”

### Page control metadata

**Before** — “current Page workflow phase”  
**After** — “current Page controller route. This low-level label selects the next handler; it is progress metadata, not a Page Run.”

### Raw extraction completion

**Before** — “Workflow: convert → upload → run on Databricks → land parquet → sync locally.”  
**After** — “The local conversion Run ends when the notebook and conversion receipt are written. Databricks upload/execution is a human handoff. Report extraction as complete only after a Databricks execution receipt and the expected catalog output are present; local sync is a separate optional operation.”

### Platform payload contract

**Before** — “All functions transparently handle both wire formats.”  
**After** — “Select the Src2InputFn and Input2SrcFn pair for the deployment target. Each parser accepts only that target's payload shape: flat JSON for SageMaker or a `dataframe_records` envelope for Databricks. Verify the pair with a same-target round trip.”

### Patient-facing forecast wording

**Before** — “Explain what to do about the forecast; suggest drinking water and walking.”  
**After** — “Describe the forecast as a model estimate, not a diagnosis. Encourage the patient to follow their established care plan or contact their care team with concerns; do not recommend a new treatment action.”

## Correction order

1. Repair the shared Workflow authority first: Task plan/report contract, shared template, lifecycle agent prompt and creator/reviewer agent instructions. Preserve command labels and compatibility progress fields while removing them as semantic workflow roster.
2. Update all 12 subtype workflow-plan samples to `run_specs`, with real boundaries and receipts. Include Task-for-raw's external Databricks completion receipt and Task-for-page's canonical Result path.
3. Resolve execution-contract risks: SourceFn/HumanFn ownership, Stata path and phases, Endpoint platform payload contract, Individual workspace/builder/cache behavior, patient report/judge data flow.
4. Fix Data/NN shared paths/config references, reviewer quick-reference coverage, Remote backend-specific auth guidance and NN version field examples against their actual API.
5. Reconcile Page/Insight controller/checkpoint terms, Task README inventory/boundary statements, Agent README and stale DESIGN architecture. Make Insight and Design independent family siblings; mark historical design notes as history.
6. After these writing changes, a later verification pass can inspect current samples and testable contracts. No implementation edits or tests were performed in this review.
