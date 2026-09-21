# Board 修复与验收结果 · 2026-09-20

已按用户批准的[补充修复计划](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/board-findings-and-fix-plan.md)落实 F01–F13，并补修独立验证发现的 `new-folder` 登记缺口与已验证内容被修改后仍可交付的问题。最终 **105 项相关 unittest、10 项原生 Task Board pytest、4 个技能格式验证通过**。Board 范围的 Workflow/Run 文案与受测行为已对齐；全库 Folder 集成审计仍有一项 Discovery 元数据问题，见下文。

## 范围与并行改动

- 修改前检查了工作树，并保存相关文件的修复前快照。保留已有修改、未跟踪文件与脏 submodule；没有修改 installer、marketplace 或 `references/`，没有提交 Git commit。
- Folder 的 Run Spec/资源身份迁移在本轮开始前已经存在，沿用它；本轮没有重复迁移 Phase schema。
- 与 Design 任务协调共享文件：Design 负责 ready/Delivery 状态、历史 Run ID 修复、对应核心回归和 Insight 绑定 fixture；本轮负责 Board 入口、Routing、Folder 示例、审批材料、代理术语、参数说明、队列/Run 表头、Board 插件版本，以及新发现的展示登记缺口。共享差异不能全部归为本任务所写。
- 原评估与计划保留为历史快照；本文件记录批准实施后的结果。

## 逐项完成情况

| 项目 | 修复结果 | 主要落点 |
|---|---|---|
| F01 · 机器检查与人工放行 | `checked:` 只记录机器结论；owner/mode 决定允许继续的工作。checked v0 可做获准的证据工作，Content 仍须有持久的人类授权。缺 owner 上下文时完成检查，放行相关字段报告未评估；保留人的 🛑。 | [审批规则](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/approve-rules/README.md:77)、[approver](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/haipipe-page-approver-agent.md) |
| F02 · Design 交付状态 | 当前状态和 CSV 均按 exact Verify-passed 的 ready draft，并重新校验候选与独立 Verify 的当前文件；文件变化后显示 records invalid、清除 ready/CSV。Delivery 是投影，Commission/Generate/Verify 才是当前 Run 类型。历史 Adopt 仍可读。 | [DesignBoard](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/SKILL.md:48) |
| F03 · Page Run ID | 新例子采用 `rp-struct-*`、`rp-sec-*`、`rp-para-*`、`rp-scratch-*`；旧 compact ID 仅作为历史兼容。 | [Board Run 定义](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:43) |
| F04 · Run、Runtime 与 controller | Workflow 按 owner Run Specs 定义；controller 坐标、快照和 gate 不自动增加 Run。补充 Board `_runs/page/<page-id>/`，明确 adapter `run_id` 的 Runtime 含义；同步 creator/reviewer/auditor/roster。 | [Board 树](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:84)、[agent roster](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/README.md) |
| F05 · 类型与 owner | 补齐 generic、task-block、discovery-block、design-board、insight-board。Insight 路由到真实 family door/workflow，Design 路由到既有 Board plugin；移除 Application 父家族归属。 | [kind 表](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:68)、[家族 README](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/README.md) |
| F06 · 原生成员路由 | 先查 Board kind 和实际成员树，再找 Folder/Page owner。`## Pages` 是展示注册表；未列 Task 不代表 Task 不存在，未登记 generic Page 不应重建。 | [Routing](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md:146)、[operations](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/operations.md:62) |
| F07 · regroup 范围 | 明确只 folderize 匹配 group key 的根 Pages；nested、unmatched 和已有目标分别说明。重命名/拆分的 moves、aliases、当前引用须另行处理；未扩大脚本功能。 | [Routing regroup](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md:123) |
| F08 · 模板路径 | Board、operations 和 creator 指向 canonical Page template。同步当前 generic Page 的 Opening/Content 阅读面，过程记录按 owner 放后台；native/legacy 表面依 owner 保留。 | [Page template](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/haipipe-page/ref/page-template.md)、[creator](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/agents/haipipe-page-creator-agent.md) |
| F09 · 状态示例/help | 状态行明确是 readiness/controller 汇总，示例用 EVIDENCE；CLI 帮助说明 Board/Group 三行、Page 四行，实际 Run 从 Run Space 查询。 | [状态说明](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/SKILL.md:218)、[status.py](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/status.py:337) |
| F10 · Ticket dialect | `.sh` 是 shell 示例；提供 Page Markdown 与 Design YAML Run Profile 链接，扩展名与 Result 路径由 owner 定义。空 Run lanes 不应自动创建。 | [Folder runtime](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md:81) |
| F11 · 路由反馈 | 减少当前流程中的历史解释；区分 Board Map/Structure，复用已给的结构批准。LANDED/PROPOSED/REPORTED 都报告实际写入或 none，并指明需要的下一位执行者。 | [Routing 返回](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board-routing/SKILL.md:234) |
| F12 · Brief row key | `{row}` 明确是解析后的 key，例如 `R3`，不使用标题或整数位置。独立验证额外发现无 `## Pages` 时登记被跳过，已修补并覆盖 section 保留与重复请求。 | [动作参数](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/board-plugins/haipipe-plugin-design-board/SKILL.md:149)、[_list_page](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/designboard.py:703) |
| F13 · 历史 Design ID | Board/Page 链接文字与 tooltip 保留真实 `rdNN_adopt_*`；Run type 显示 `Adopt (historical)`。队列用 next action，Run 表用 Run type，不制造 `_delivery_` ID。 | [Page Run renderer](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py)、[Board Run 表](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board/haipipe-board/live/designboard.py:392) |

技能版本已更新：Board 1.0.11、Routing 0.11.1、Folder 0.7.1、DesignBoard 0.7.1。相关 family/skill/agent changelog 已同步。

## 实际验收

| 检查 | 结果与边界 |
|---|---|
| `quick_validate.py` | 4/4 技能通过。只验证技能格式，不当作行为证明。 |
| 相关 unittest | **105 passed**：`test_design_board_plugin`、`test_design_plugin`、`test_design_run_gate`、`test_status`、`test_pageruns`、`test_page_phase_ledger`、`test_folder_contract`、`test_design_repairs`。最终运行中 8 个关键实现/fixture 文件哈希保持不变。 |
| 原生 Task Board | **10 passed**：`pytest tests/test_task_block_board.py`，覆盖原生发现、注册顺序、歧义与构建。 |
| regroup dry-run | 根 Page 产生正确 move；nested 不动；unmatched/collision 分别跳过；dry-run 前后文件字节不变。 |
| 实际 status 输出 | Board 3 行、Group 3 行、Page 4 行；Page 示例实际输出 CONTEXT readiness。文档 EVIDENCE 例子使用同一 formatter 结构。 |
| 新 canonical 链接 | 新增或修正的 12 个相对文件链接均可解析；历史 changelog 的示意链接不作为现行路径。 |
| 空白检查 | Board 范围 `git diff --check` 通过。 |
| Folder owner 审计 | Insight 范围 **6 contracts / 0 findings**；全库 **7 contracts / 1 finding**，见下一节。 |

测试使用现有 Python 3.11 与已有 PyYAML/pytest。系统 Python 3.9 无法导入现有 `list | None` 类型注解；其它独立解释器缺 PyYAML。最终测试通过临时 `PYTHONPATH` 使用已安装依赖，没有修改仓库依赖或全局环境。pytest 关闭了与本测试无关的自动插件加载。

关键复跑命令（在 `skills/board/haipipe-board/` 下）：

```bash
PYTHONPATH=/Users/jluo41/Library/Python/3.9/lib/python/site-packages PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.11 -m unittest tests.test_design_board_plugin tests.test_design_plugin tests.test_design_run_gate tests.test_status tests.test_pageruns tests.test_page_phase_ledger tests.test_folder_contract tests.test_design_repairs
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/Users/jluo41/Library/Python/3.9/lib/python/site-packages PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.11 -m pytest -q -p no:cacheprovider tests/test_task_block_board.py
python3 cli/foldercontracts.py --check --workflow haipipe-insight-workflow
```

## Fresh-context 场景

依据根 README，由独立上下文实际读取技能和 owner 合约，在 `/private/tmp/board-validation-20260920/` 使用合成数据。

- **原生 Task 路由**：仅列 Job headings 的 Board 找到现有 `b03j01t01`，更新获准的 `Now:` 事实并写 dated log；未新建重复 Task，未改人工 gate。重建后 0 errors，保留 fixture 原有 16 warnings/8 template gaps。第二个独立 reviewer 确认局部写入 PASS，整个 Task 仍因缺输入和 READING 而 HOLD。
- **无写入提案**：家庭搬迁 Board 只在回复给 proposal；明确 `Writes: none`、`State: PROPOSED` 和人的结构审阅动作，没有 materialize。
- **审批**：checked v0 缺人工批准时，允许 owner 定义的证据准备，Content HOLD；已持久记录明确授权且其它条件满足时继续 adoption，不重复索取旧式 tick；人的 🛑 保留并重新打开受影响检查。缺 owner/mode 不阻塞 artifact check，但 allowed work/gate 未评估。发现并统一了一处 README/返回字段措辞。
- **Design/Folder**：按任务标题从 Brief 找到 key `R3`，创建目标 Folder，导出一个 ready ITEM01；其 Generate/Verify 分别是 `rd02_generate_item01` / `rd03_verify_item01`。失败项与未验证项未导出。历史 `rd04_adopt_item01` 保留。既有 Run/Result 哈希不变，新 Folder 没有创建 Run lanes。根据 owner 正确选出 YAML Design 与 Markdown Page Ticket。
- **额外登记缺口复验**：第二个新 fixture 确认创建缺失的 `## Pages` 和准确入口，保留原 Board 文字、Brief 非目标内容与 owner；重复请求拒绝且字节不变。新 Page 检查 0 errors，仍有 title-too-long/hard-wrap 两个原有生成器警告。
- **交付版本追加验证**：Design 的独立 walkthrough 发现已验证 artifact 被修改后仍进入 ready/CSV。Design owner 修正 exact target 解析及 Generate/Verify 重新校验，Board 合并复验通过；新增参数化回归覆盖 artifact、checks、result、config 和 render 变化。失效记录显示修复指引，ready 计数为零且 CSV 不含该项。

临时证据：[测试摘要](/private/tmp/board-validation-20260920/focused-tests-summary.json)、[测试日志](/private/tmp/board-validation-20260920/focused-tests-final.log)、[Design 场景报告](/private/tmp/board-validation-20260920/design/DesignPlugin-Demo-260916-DesignBoard/validation-report.md)、[新建 Folder 复验](/private/tmp/board-validation-20260920/design/DesignFolder-NoPages-DesignBoard/validation-fixed-writer.json)。临时目录可能被系统清理，本文保留结论。未声称完成真实服务的 HTTP/browser 端到端验收。

## 留给跨家族集成的事项

全库 `foldercontracts.py --check` 唯一 finding 是 [Discovery inquiry 的 metadata.workflow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/discovery/workflow-phases/haipipe-discovery-inquiry/SKILL.md:12) 为 `haipipe-discovery-inquiry`，不符合当前要求的 `*-workflow` owner。已交给主协调任务归属 Discovery；本轮未修改该源，也未放宽 Folder validator。

并行 Insight 更新曾使 Design 合成 fixture 的当前绑定失效；相应 owner 补齐真实 hash-bound receipts 与 Wisdom register 后，最终相关测试已恢复通过。早期失败不是最终状态。

随后同步保留了 Design fixture 的两处修正：config goal 取 `spec.goal`，以及明确 `adopted` 默认值只为历史兼容案例。同步后再次运行上述 105 项 unittest，仍为 0 failures/errors，关键文件在运行期间保持稳定。Design 任务另外报告独立 walkthrough 的原有 20 条断言全部通过；该结果未并入本报告的 115 项测试计数。

Page RD 与 native Design rdNN 的跨 owner 命名关系仍是原计划的架构确认项；本轮没有发现实际碰撞，也没有改写历史 ID 或发起全库重命名。上述 Board 修复完成不代表其它家族或整个仓库均已通过验收。
