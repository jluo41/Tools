# Question Book：版本工作台设计

2026-11-12 · 可交互设计提案；未接入生产写入。原型入口为 index.html，默认进入第二版 Job 的 Plan + Results。

## 范围和事实边界

Question Book Block 管问题体系及其演进；每个 Job 制作一版问题集；Task 定义一个问题、它的证据需求及方法。Insight Job 才把签定的问题集版本应用到固定数据版本。

本次只新增独立设计文件，不修改现有 server、问题文件或签名。已有工作树有大量其他改动，全部保留。原型的内容基于 InsightQuestionBook-Example 的 I02、K02 和第二版 release.yaml，采用中文摘要；进度、计划、Findings 和第三版草稿都是展示用样例。实际第二版还包含其他问题，原型没有把两个展示条目冒充完整清单。

## 必须遵守的原则

- 层级表示范围，view 表示角度；不能让不同 view 重复列相同内容。
- 每个 Job 有动机、证据、目标和范围；Task 追溯到版本计划。
- Plan + Results 一起展示，每项计划旁边有实际结果、进度、阻碍和完成标准。
- Results 是产出，Findings 是基于产出形成的认识。发现不能成为无依据的摘要。
- 同一逻辑记录只有一个权威源；上层引用并展开它，不创建展示副本。
- 跨层级汇集保留归属、版本和来源；新综合判断单独记录并引用原发现。
- 已发布版本保持固定。未改变的问题沿用旧 Task；真正改变的问题建立新版本定义，并保留旧定义。这与“一份记录不为展示复制”不矛盾。
- 用户操作名称描述工作，不要求先理解路径和脚本。默认折叠条目，展开后可直接看证据、结果和下一步。

## 各层视图

| 层级 | View | 主要内容 | 用户下一步 | 上层如何展示 |
|---|---|---|---|---|
| Block | Overview | 整本书的目标、边界、当前版本 | 进入当前版本 | 更上层引用 Book 摘要 |
| Block | Questions | 选择版本后的问题目录、关系 | 打开问题定义 | 不另存问题文本 |
| Block | Ideas | 建议、来源、理由、采纳状态 | 讨论、选入版本计划 | 引用 proposals 源记录 |
| Block | Plan + Results | 每个版本的目标、进度、成果 | 展开并进入版本 Job | 直接读取各 Job |
| Block | Findings | 各 Job/Task 的发现、跨版本综合判断 | 查依据、回到归属层 | 按 ID 去重 |
| Job | Overview | 升级动机、证据、目标和范围 | 查看来源、转到计划 | Block 摘要引用 |
| Job | Questions | 本版清单、沿用/新增/修改/退出、依赖 | 对照前版、进入 Task | release.yaml 引用 Task |
| Job | Plan + Results | 改进项→Task→产出与进度；整版评审和发布 | 查看结果、推进下一项、审查 | Block 展开同一内容 |
| Job | Findings | 本版下属发现和整体认识 | 查看依据及对计划的影响 | Block 引用同一 ID |
| Task | Question | 定义、动机、适用范围 | 修订问题草稿 | 上层引用问题定义 |
| Task | Method | needs、方法、输出约定、解释边界 | 准备或审查证据计划 | 上层展示方法状态 |
| Task | Plan + Results | 定义→计划审查→脚本→脚本审查及各自产出 | 查看产物、审查、继续执行 | Job 计划引用成果 |
| Task | Findings | 本问题准备过程中形成的认识 | 查依据、提出改进建议 | Job/Block 同源展开 |

共享 MindMap、Studio、Interactions、Decisions、Timeline、Skills、Files 等外框能力继续由共享框架提供；本原型不重复制作这些侧栏。重点验证题书内容视图，不建立另一个独立产品框架。

## 版本升级示例

1. 第一版有 I02 每日变化问题。第二版直接引用第一版 I02 的 Task；它没有被复制。
2. 改进建议指出缺少跨时间的差异检验；本版 Overview 呈现这一动机和来源。
3. Plan + Results 中 P02 指向新增 K02。预期是完整问题与方法；当前结果是草稿，不假称分析结果。
4. K02 的 Method 展示 E1–E4，Plan + Results 展示证据计划与脚本审查准备。
5. F01 在 Task 记录一次；在 Task、Job、Block 的 Findings 都读取同一条记录。
6. Job 可另记整版发现 F02，引用相关问题。跨层级显示不是把 F01 改写为 F02。
7. 发布入口列出未满足条件并禁用。演示不产生签名。
8. “起草下一版”预览 v3 的动机和沿用问题引用，只保存在当前页面内存；刷新恢复。真实版本创建必须使用现有 ladder 的流程，不能由 UI 直接复制目录或跳过审查。

## 内容来源与拟议存储

| 内容 | 当前源 | 本次设计的处理 |
|---|---|---|
| Book 目标 | board.md | 直接读取，不另设目标库 |
| 版本身份、签定状态 | Job face、release.yaml | 从现有来源读取 |
| 版本动机、目标 | Job face 的内容区 | 优先扩展现有 face，避免第二份 overview 文件 |
| 改进建议 | proposals/*.md | 保留原记录，计划中只引用 |
| 问题定义、needs、method | Task/question.md | 直接读取；未变问题由 release.yaml 回指旧 Task |
| 计划及实际结果 | 共享 Work UI 的计划/结果读取逻辑、Task 产物和 Run 记录 | 接入前核实共享契约，避免新造独立 plan 状态库 |
| 审查状态 | 现有 Run 卡、passes、agreed、release sign | 从事实推导；不允许前端手动勾成发布就绪 |
| Findings | 需检查现有共享 findings 契约 | 优先复用；若没有，才用归属层 findings/<id>.md，并建立引用索引 |

建议 Findings 最小结构：稳定 id、owner、version、claim、evidence_refs、implication、review_state。全局唯一键包含 Book 与归属路径，不只用 F01。上层索引只存引用，不保存 claim 副本。去重按身份，不能按文字去重。新综合判断引用下层 findings，不改变下层记录。

“同源更新”指所有实时视图重新读取同一源；不意味着覆盖已发布版本历史。真实缓存必须随源变更失效。原型 model.js 是单一展示 fixture，不是新的生产数据库。

## 现有实现与需要补齐之处

已核实文件：

- plugins/haipipe-toolkit/servers/workbench-insight/insight_focus.py：prototype_views 明确 Questions / Ideas / Versions；Job/Task 返回空，回落共享视图。
- plugins/haipipe-toolkit/servers/workbench-insight/insight_prototype.py：已有问题、版本、建议、状态、证据需求与交付读取；可作为新增专属视图的数据基础。
- plugins/haipipe-toolkit/servers/workbench/focus_page.py：装配共享框架和 prototype hooks；Plan + Results 当前已是公共视图名称。
- blueprints/Project-Ladder/insight/InsightQuestionBook-Example/j02_question-v2_example-follow-up/release.yaml：保留问题通过路径引用原 Task，K02 是新增项。

实施顺序：先复用共享的计划/结果和 Findings 源契约，再补 prototype 的 Job 视图；接着让 Block 展开同一内容，最后补 Task 的 Question / Method / Plan + Results / Findings。老 Versions 链接重定向到 Block 的 Plan + Results，旧 view key 保留兼容。实际发布、修改与签定仍经原有 owner 与 gate，不能在渲染层实现副本写入。

## 交互验收

- 默认 Job v2 → 展开 P02 → 同一条目看到计划和结果 → 进入 K02。
- K02 Method → 查看证据来源；定义和数据答案不混淆。
- Task F01 → Job Findings → Block Findings：相同 id、内容、来源，且归属可见。
- Job Questions → 对照前版：I02 沿用原 Task，K02 新增。
- Block Plan + Results → 起草下一版：只生成演示草稿，不写生产状态。
- 窄屏无整页横向溢出；折叠、导航、对话框可用键盘操作。

验证结果另见 VALIDATION.md。
