# Design 家族：修复实施与测试结果

日期：2026-09-20。依据 [发现与修复计划](design-findings-and-fix-plan.md)，本轮已修改技能、支持文档、执行/展示实现和测试，并完成真实运行验证。

## 结果

**F01–F12 与共享入口 X01/X02 已处理。最终 121 项自动化测试通过：Unit/renderer 50，Design Page/Board 71；零失败、零跳过。** 此外，6 个技能入口通过格式校验，8 套 venue 导航可解析，新上下文 Workflow 验证通过 20/20 项。SMS 与 UI card 分别完成真实 Generate 和独立新上下文 Verify，均通过 4/4 个委托标准。

测试过程中发现并修复了两个实际运行缺陷：浏览器视口与请求尺寸不一致却报告一屏可容纳；已审核文件被改动后仍被标记 ready 并导出。两者都有原始失败证据、修复后的验证和新增回归测试。

四个 Design 技能保持 **0.4.0**；Page Design 插件为 **0.11.1**，Board Design 插件为 **0.7.1**。更新当前日期和修订记录，保留旧 changelog 作为历史。

## 1. 逐项完成情况

| 发现 | 已实施的修复 | 验证依据 |
|---|---|---|
| F01 venue 生命周期 | schema、8 README 统一 Commission/Generate/Verify；移除当前 Adopt/Phase 执行指令，Delivery 为投影 | 8 venue 新上下文阅读、20 项 Workflow 检查、SMS/UI 完整主路径 |
| F02 Board 与 CSV | 更新 ready 数量、动作、交付过滤和 mapping；交付前重新验证精确候选及独立 Verify | Page/Board/CSV 混合状态回归，内容改动反例复验 |
| F03 Unit/共享 Run 边界 | 当前 caller 负责释放、排队、关闭和投影；历史 Adopt 只读；旧 `adopt()` 写入口明确拒绝 | 历史记录完整保留、直接调用拒绝且写入差集为零 |
| F04 Runs/Steps/Delivery | Workflow 首先定义为 Runs 列表；三类 Run Spec；图表示 Route；卡片用 Runs，Run 表保留真实身份 | 三条真实 Run 的 SMS/UI 路径、Page/Board HTML 和截图 |
| F05 路径与 profile | 修复 Unit 到 venue 的相对路径；8 profile 改用 Item、Commission、输入、Result/hash；UI 视觉判断读取真实渲染 | 8/8 路径解析、真实 UI Generate/Verify |
| F06 held/blocked | 区分 `commission held`、`blocked` 和 worker hold 诊断；显示阻塞 Run、原因、负责人，不提供 Commission release | Generate/Verify blocked 回归；Hold→新 Release 保留旧决定 |
| F07 Unit 粒度 | 标题为 one Ticket, one inspectable Result | 独立 Generate/Verify 分别写入自己的 Result |
| F08 render 范围 | 新图片、计量、manifest 写在当前 Result/render；manifest 绑定 source/image hash、Item、候选和版本；检查器和 presenter 支持 | 7 项新增完整性测试、11 项 renderer 测试、实际浏览器与独立 reviewer |
| F09 历史身份 | Page/Board/tooltip 保留 `rdNN_adopt_*`，标注 Adopt (historical)，不改写为虚构 Delivery id | 历史 fixture 在各视图一致；无磁盘迁移 |
| F10 Commission 计数 | `C Commission + N Generate + J Verify`；计入 held/failed/blocked/superseded；最多一次 release | Hold、Release、Generate、Verify 共 4 条；第二次 release 被拒绝 |
| F11 Verify 重试 | 已完成且有效的独立 review 阻止重复审核；invalid/unresolved 可重试；完成 verdict fail 走新 Generate | 三类结果的实际排队/状态回归，旧候选字节不变 |
| F12 冻结字段 | 继承已释放配置，仅派生 mode/review_mode；revision 根据冻结 stance 判断 challenge，不读取后来改动的 register stance | 普通/challenge 双向 register 改动回归，其他字段逐项相等 |
| X01 家族目录 | STRUCTURE 移除旧 Application 家族行，Design 链补齐 Generate；保留并发任务已修正的 Board 父级说明 | 当前目录/入口复核 |
| X02 共享定义 | 共享 Run/Workflow 入口明确 Workflow 是 Runs 列表，路线图不新增执行身份 | 当前入口与 Design Workflow 交叉阅读 |

主要实现位于：

- [check_unit.py](../../plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/check_unit.py)：可选 render 证据的范围、身份和 hash 校验，图片不计入内容数量。
- [render_screen.py](../../plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/render_screen.py)：Result 写入边界、版本不可覆盖、精确视口及双轴溢出检查。
- [design.py](../../plugins/haipipe-toolkit/servers/workbench-design/design.py)：状态、历史 ID、Result 图片读取、交付时重新校验。
- [design_actions.py](../../plugins/haipipe-toolkit/servers/workbench-design/design_actions.py)：冻结 stance 派生、退役 Adopt 写入拒绝。
- [test_design_repairs.py](../../plugins/haipipe-toolkit/skills/board/haipipe-board/tests/test_design_repairs.py) 与 [test_render_screen.py](../../plugins/haipipe-toolkit/skills/design/haipipe-design-unit/tests/test_render_screen.py)：新增行为回归。

### 新上下文验证后的补充修正

Brief 原来只列出 4 个 venue，容易被读作完整枚举；现明确列出 8 个。提醒的 3–5 个变体是旋转集合默认值，实际数量服从冻结的 `unit.shape/count`；Report 的完整报告字数区间与短篇 audience 默认值在 Commission 前归并为一个明确预算。brief-only 规格必须标明样例值和缺失来源，不得由示例推导出真实发现或在线刷新能力。

合成 fixture 的 `config.goal` 现使用目标句 `spec.goal`。历史 demo 默认 `stage=adopted` 保留并标注；当前验证明确选择 `verified`，避免删除历史兼容覆盖。

## 2. 两个真实失败与修复

### 2.1 浏览器视口和裁切

第一次真实 UI 生成请求 390×844、scale=2。旧 Chrome 调用输出 780×1688 PNG，但页面实际按宽 500、高 757 布局；右侧被裁切，而旧检查仅考虑高度并返回 `fits_one_screen=true`。producer 查看图片后拒绝据此通过。

renderer 改为 Playwright 的显式 browser context，在同一页面测量并截图，检查实际 viewport/device scale，增加页面宽度和左边缘检查。仍使用本机 Chrome，不下载浏览器；页面脚本关闭、网络离线。API 依据：[browser.new_context](https://playwright.dev/python/docs/api/class-browser#browser-new-context)、[page.screenshot](https://playwright.dev/python/docs/api/class-page#page-screenshot)。

修复后 Generate v2 与独立 Verify 新图的实测一致：

| 指标 | 结果 |
|---|---:|
| 实际 viewport / 页面尺寸 | 390×844 / 390×844 |
| PNG / scale | 780×1688 / 2 |
| 最后内容块底部 | 623 px |
| select / button 高度 | 52 / 52 px |
| 最低文字对比度 | 8.38:1 |
| 控件边框对比度 | 7.58:1 |
| button 文字对比度 | 11.04:1 |

保留 [旧图](design-validation/screen-before.png)、[修复图](design-validation/screen-after.png) 和 [计量](design-validation/screen-metrics.json)。v1 未覆盖；v2 使用新版本。对比度计量是静态样例的检查辅助，不等于完整无障碍认证。

### 2.2 审核后的内容改动仍可交付

新上下文 walkthrough 修改已 Verify-passed 的 SMS。原 presenter 一边报告 hash mismatch，一边返回 `ready` 和改动后的文字，CSV 仍附着旧 hash。问题由真实 `design_snapshot`、`bundle_rows`、`bundle_csv` 调用复现。

现在交付读取精确的目标 `result.yaml`，重新校验 Generate 与 Verify 的绑定、内容、checks、config 和可选 render，并要求 independent review。失败时显示 `records invalid`、受影响 Run 和修复负责人，ready 为 null，交付和 CSV 排除该候选；只读展示不改 runtime 或历史文件。

独立 validator 用同一反例重验：损坏项导出 0 行；未改动的 8 个 venue fixture 仍为 8 ready、8 CSV 行、24 条 Run、零审计问题。见 [修复后证据](design-validation/delivery-repair.json)。

## 3. 最终测试

| 检查 | 最终结果 | 持久化记录 |
|---|---:|---|
| Unit + renderer 完整 suite（含真实 Chrome） | 50/50，0 skipped | [unit-tests.log](design-validation/unit-tests.log) |
| Design Page/Board suite | 71/71 | [board-tests.log](design-validation/board-tests.log) |
| 6 个技能 quick_validate | 6/6 | 4 个 Design + Page/Board 插件 |
| Unit 指引到 venue README/profile | 8/8 | 每个相对路径均解析为现有文件 |
| 新上下文 Workflow/Brief/插件 | 20/20 | [workflow-checks.json](design-validation/workflow-checks.json) |
| SMS / UI Generate | 各 4/4 | [producer](design-validation/producer-validation.md) |
| SMS / UI 独立 Verify | 各 4/4 | [reviewer](design-validation/reviewer-validation.md) |
| Page/Board 投影不写源文件 | 0 个文件变化 | [完整案例](design-validation/completed-cases.json) |
| presenter 浏览器检查 | 4 个视图/尺寸通过图片加载和宽度检查 | [presenter-checks.json](design-validation/presenter-checks.json) |
| 本次相关 diff 空白检查 | 通过 | `git diff --check` |

Unit 原有 32 项测试通过后，新增 render 完整性 7 项及 renderer 11 项，合计 50。Design 原有 62 项基础上，新增本任务 8 项 repair tests，加并发 Board 任务 1 项页面登记回归，合计 71。参数化分支不另作测试数量膨胀。

初期 Board suite 使用系统 Python 3.9 时不能加载既有 `list | None` 注解；Homebrew Python 本身又缺 PyYAML。最终使用 Python 3.13，并显式引用本机已装的 PyYAML 路径。并发 Insight 修复引入当前 handoff eligibility 后，旧签名 fixture 不再充分；补齐合成的 hash-bound GI5/GI6、dependency 和 Wisdom register，更新 eligible 文案断言，未放宽生产 gate。

### 可复跑命令

在 Design Unit 目录运行（需 PyYAML、Playwright Python 包和本机 Chrome/Chromium；可用 `CHROME` 指定路径）：

```sh
DESIGN_RENDER_BROWSER=1 PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

不设 `DESIGN_RENDER_BROWSER=1` 时，4 个真实浏览器测试明确 skip，其余 46 项仍运行。本次最终执行设置了该变量，零 skip。此 macOS 环境中的 Chrome 启动需经自动批准后在 sandbox 外运行；测试只读取/生成临时合成文件。

在 Board engine 目录运行（以下依赖路径是本机配置，不是可移植安装命令）：

```sh
PYTHONPATH=/Users/jluo41/Library/Python/3.9/lib/python/site-packages PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.13 -m unittest discover -s tests -p 'test_design*.py' -v
```

技能格式检查使用系统 skill-creator 的 `scripts/quick_validate.py <skill-folder>`。新上下文验证按根 README 要求分配给独立 subagent；producer 与 reviewer 使用不同上下文，非仅改 actor 名称。

## 4. 完整案例与界面检查

两个库取书示例都使用明确的合成 Commission。最终各有：

```text
rd01_commission_item01 → rd02_generate_item01 → rd03_verify_item01
```

caller 通过真实 `complete_run` 关闭 worker Run。Page、Board 和 CSV 都只交付 `rd02_generate_item01`，每个案例 1 ready、1 行导出，零审计问题；无新增 Adopt/Delivery Run。屏幕 Generate 与 Verify 各自保存自己的 render 证据，源候选保持不变。

检查了实际 presenter 的桌面 Design/Run/Board Delivery 与 430px 手机 Design 截图：图片正确加载、无页面横向溢出；桌面清楚列出三个真实 Run、操作者及独立审核。手机卡片沿用现有内部滚动布局。本次是 agent 浏览器检查，**没有真人可用性测试**。

额外的 8 venue walkthrough 验证 Brief、输出契约、状态和只读投影；它的 proposal 保持未委托状态（8 Items、0 Runs），另行合成的普通/异常 fixture 测试记录行为。不能把这些合成 verdict 当成另外 8 个真实内容生成或独立质量审核。

保留其 [Brief](design-validation/workflow-brief.md)、[walkthrough](design-validation/workflow-walkthrough.md) 和 [最终 observations](design-validation/workflow-observations.md)。最后的指令复读确认无未解决发现；提醒的起草属于 Generate，Verify 只检查冻结数量与内容。

## 5. 保存与范围

原 [design.md](design.md) 未修改，SHA-256 仍为：

```text
d1f910e2075d699802f0af335612c6383f9b6abd6986d0e2f967af71ffe4edc6
```

共享 Board 文件存在并发修复；已协调保留另一任务的 parsed Brief key、queue/Run type 文案、稀疏 Board 的 `## Pages` 登记和插件版本记录。共享 Insight fixture 改动按当前契约合并。没有重置工作树、改写 dirty submodule、提交或推送。

历史 Adopt、旧 Delivery render manifest 的既有只读支持保留；v1、DU、D0–D5、PageX 等已拒绝形状没有恢复。新 render 写入需要 Result-local manifest，旧显示文件不被迁移为新授权。

验证覆盖当前 macOS/Python/Chrome 环境；未运行 Windows/Linux 浏览器矩阵、真实部署、发送或效果实验。其他六种 venue 的检查集中于契约和 fixture；真实内容端到端覆盖 SMS 与 UI card。原始临时执行树位于 `/tmp/design-skill-validation-20260920` 和 `/tmp/design-workflow-validation-20260920`；关键日志、失败/修复图和结果已复制到本报告的 `design-validation/` 目录以留存。

相关 Design 文件的最终内容指纹记录于 [source-hashes.json](design-validation/source-hashes.json)；它是共享工作树当时的快照，不代表其他并发任务停止修改。
