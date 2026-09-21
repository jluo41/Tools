# Task 修复结果 · 2026-09-20

已按 `task-findings-and-fix-plan.md` 落地仓库内的代码、模板和说明修复。原评审报告保留为历史记录，不把本次静态检查当作实际训练、部署或临床验收。

本仓库另有并行工作和既有修改；本轮未 reset、clean、提交，也未修改 references 子模块。下表描述本轮 Task 修复，不把整个工作区 diff 都归为本轮产物。

## 修复对应表

| 项 | 已落地内容 | 验收边界 |
|---|---|---|
| F01 | 共享 plan/report、生命周期 prompts、agents 和 12 份领域样例使用 Run Specs / 实际 Runs。保留内部 Steps；审核关卡不自动分配 Run。`task.execute` 对接当前共享 catalogue。 | 静态语法和 fresh-context 规划复核通过；未运行 Workflow 引擎。 |
| F02 | Algo、Individual、Fit、Eval、Agent、Stata 的新脚手架改为 bNN/jNN/tNN/rNN；Task scripts/config、Job src、同名 Page/Ticket 配对。Stata 保留四种 stage 的领域结构。 | 受控规划复核通过；未在真实项目生成或执行工作负载。 |
| F03 | Page/Display 样例和共享 Run 引用统一为 OUTPUT_ROOT/<task>/results/<run>；澄清 self-serving 的物理投影。 | 未搬迁既有产物。 |
| F04 | Raw conversion 使用同一 extraction Run 的完整回执框架；转换完成保持等待外部执行，失败如实记录。接上 Databricks 外部 id、日志、hash、manifest 和 Result gate。 | Shell 静态语法通过；未上传或运行 notebook。 |
| F05 | SourceFn 归 Source；HumanFn/RecordFn 归 Record；TriggerFn/CaseFn 归 Case。 | 入口和交叉路由已对齐。 |
| F06 | Data/NN 的当前 AIData 示例统一 ParentSetName/@vNAIData-name；要求从 manifest/config/inventory 解析。 | 未假设用户项目存在新 resolver 字段。 |
| F07 | Data 快捷清单覆盖 SF1–15、RF1–17、CF1–13；保留 CGM 条件项。 | 文档核对。 |
| F08 | Remote auth 提示区分 GDrive/rclone 与 S3/AWS。 | 未进行登录或传输。 |
| F09 | ModelSet 版本及 manifest 示例与 Instance 的 @v 约定对齐。 | 实际 hainn/haipipe 库不在本仓库；API 默认值、旧版本归一化与 round trip 尚未验收。 |
| F10 | NN Task 配置使用 scripts/config/rNN；独立开发 harness 的 config 路径明确为项目条件。 | 实际项目 harness 未验收。 |
| F11 | 保留显式 run→smoke alias；自然语言按 smoke/inference/训练产物分流。 | 静态路由核对。 |
| F12 | Endpoint 平台 wire pair、生成例子、reviewer 与 Individual payload 对齐；共享 Trig unwrap 保留。CLI 可选 platform 和 endpoint-model。 | 静态数据流复核通过；未调用真实 Endpoint 或做 round trip。 |
| F13 | Local 默认采用现有 FastAPI 模板；Flask/Docker 和远端部署显式检查项目 adapter、依赖、配置及权限。 | 两个平台 repo 不在本仓库，真实部署未验收。 |
| F14 | Individual 文档准确说明筛选已有 global Source/Record，而非重跑生成 pipeline；同步读取来源与 provenance。 | 静态源代码核对。 |
| F15 | 缓存使用 spec/builder/输入 stat inventory 指纹；staging 重建、失败保留旧缓存、同轮去重、--force、输出 inventory。批次失败退出非零，raw_materialized 反映实际复制。 | 指纹用于失效判断，不是全数据内容 hash；未读真实 parquet 或运行缓存行为测试。 |
| F16 | 去除硬编码个人 Linux root；支持 workspace 参数/env/cwd 发现、绝对 Subject 路径和歧义错误；参数贯通 CLI。 | 静态接口复核通过。 |
| F17 | report/forecast 文件 hash 和窗口选择绑定；judge 校验实际传入文件，接收原始 forecast 与确定性比较。绑定缺失/不符分支明确，legacy 不声称独立核验。原始阈值先于展示舍入计算；时间锚未证实则明确说明。 | 软件证据链静态复核通过；不声称验证了预测准确性或窗口真实时间。 |
| F18 | report 与 safety persona 统一既有边界：解释预测、联系 care team、引用已提供的 clinician plan；不由预测生成新的治疗/运动/饮食/饮水指令。 | 未新增临床政策或完成临床/产品内容验收。 |
| F19 | scaffold 返回统一 status/summary/artifacts/next；生命周期 schema 接受 artifacts 并保留旧 files alias。 | 静态 caller/返回说明核对。 |
| F20 | Display source_runs 和 derived_from 贯通完整 Run id、确切 artifact 与 SHA-256。 | 未读取实际来源数据。 |
| F21 | Page 使用 controller/command 术语和 owner-native 引用；Discovery 重排仅在明确请求时进入，依从 Discovery owner，去除自动提交要求。 | 未改写任何真实 Page。 |
| F22 | Task README 补齐 10_page，Display 范围准确，Insight/Design 为独立家族；DESIGN 标记历史，TODO 保留四个命令而非 Workflow Phase。 | 既有 Insight/Workflow 改动保留。 |

## 检查记录

- 本轮结束时，对 Task 已修改文件集合进行 Python AST、YAML/JSON 和 SKILL frontmatter 静态解析，无解析错误；Raw Shell `bash -n`、Workflow JavaScript 函数体解析、`git diff --check` 通过。
- `skill-creator` 的 `quick_validate` 检查了 32 个相关技能：16 通过；16 仅因既有 `argument-hint` 被该通用 validator 拒绝，与 HEAD 基线相同，保留兼容字段。详情：`task-fix-skill-validator.json`。
- fresh-context 规划复核：`task-fix-validation-core.md`。临时 Algo/Stata 计划和脚手架说明已人工复核；最终无遗留的已报告范围内冲突。
- fresh-context Individual/Endpoint 数据流复核：`task-fix-validation-individual.md`。最终无遗留的已报告范围内冲突。
- 未新增或运行测试套件，未运行实际 Workflow、Python 工作负载、Stata/PowerShell、训练、云端部署、模型报告调用或患者数据处理。验证代理只读仓库，在临时目录产生说明/草案。

## 后续环境验收

需要消费项目的 `code/hainn`、`code/haipipe` 和相应 `platforms/` 才能验证 NN API、Endpoint pair round trip、真实运行回执与部署行为；这些路径当前不存在于 Tools-SPACE。Windows PowerShell 5.1/Stata 与真实数据行为也未在本轮执行。上述限制不以文档修改或静态解析结果替代。
