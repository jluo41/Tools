# Ideation 修复与验证记录

日期：2026-09-20。依据 [问题与修复计划](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/ideation-findings-and-fix-plan.md) 实施。原评估和计划文档保持原样。

## 已实施

| 问题 | 修复 |
|---|---|
| F01 Workflow/Run 归属 | 新增 [workflow-runs.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/workflow-runs.md)：列出 Discovery source、Task pilot、Task portfolio Run Specs，以及目标、owner、依赖、内部 Steps、门禁、关闭与恢复规则。I1/I2/I3 保持能力标签；P0 同步不分配额外 Run。 |
| F02 逐候选决策 | [receipts.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/references/receipts.md:93) 新增 v3：每个 reviewed card 分别记录 disposition、理由，入选卡分别绑定 posture、risks、assertions、target/category/contract version 和 Story。未回答保持 open。 |
| F03 人类权威 | Generate/Test 只能建议 defer/abandon；非 open 卡状态必须指向可归属的 I3 人类收据。Card、Venue Fit、sync、manifest 和 Paper 显示字段由决定投影。 |
| F04 未入选候选阻塞 | 全体 Test 完成检查保持严格；Select/Handoff 对实际入选集合检查完成与资格，未入选 HOLD 可保留。全体候选仍需满足结构、广筛和投影一致性要求。 |
| F05 交接一致性 | [selection_contract.py](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/scripts/selection_contract.py) 逐卡连接选择、目标、Story 和 handoff；检查实际 Venue contract 块、目标/category/version、当前性字段及来源路径；拒绝错卡、空选择、重复 Story、错误 claim/evidence/feasibility 引用、旧同步及不匹配快照。机器 next_route 不再决定所选卡是否接受完整资格检查。 |
| F06 目标投影与历史 | 定义不可变 selection/handoff 快照和当前视图；严格核对派生字段。证据 revision/hash 变化后旧决定保留为历史，新交接需新决定。G0 intended target 与 Story 后续 operational target 分开。 |
| F07 skipped pilot | skipped 在 pressure receipt 保存理由，不要求虚构 Task Result；矩阵映射 pending，不能代替 pilot 或 waiver。 |
| F08 字段映射 | depth 统一 none/metadata/abstract/full-text，兼容读取 metadata-only；补齐 defer 建议。区分 central novelty 摘要与所有 Core Claims 的选入资格。矩阵收据必须指向本卡的正确记录。 |
| F09 one-off 路由 | 明确复用、Discovery 单次检索、inline 输出和 durable 保存的边界；no-search/read-only 限制下保留 provisional/HOLD。 |
| F10 UI | Select 短描述改为协助比较与准备人的选择。 |
| F11 入口导航 | 增加用户任务、产物、缺证据状态、保存时机和术语简述，保留按需加载。 |

8 个 Ideation 技能及对应 changelog 已更新；端到端示例已改为逐卡 v3 决策。Paper P0 adapter 补充 v3 消费规则。已有的 Paper/Page 入口修改以及其他家族、上游子模块的工作均保留。

## 验证结果

### 定向测试：32 项通过

执行：

~~~sh
python3 -m unittest discover -s plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/tests -q
~~~

结果：32 tests，OK。覆盖：

- 成熟入选卡与未入选 HOLD 共存；全体 Test 仍拒绝未完成状态。
- 多卡分别 proceed/caution/defer/abandon/open；风险与目标不串用。
- 错卡但等长的路由、重复物理 Story、preempted/未验证卡的选择。
- 目标/category/contract version、stale contract、官方来源路径和 Markdown 中的 contract 块。
- selection/handoff 快照漂移、错 claim/evidence/feasibility、旧 sync、manifest 漂移。
- v3 对实际 P0 工作视图及其 receipt 的要求；工作、release、delivery 状态仍分开。
- skipped 理由与无 Task Result、supporting claim 未解决、depth 兼容映射。
- 重选保存旧快照；早期 defer 无需先完成 Venue 工作；全 open 草稿不算已决策。

另外，8 个技能均通过 skill-creator 的 quick_validate.py；相关 diff 通过 git diff --check，新增文档链接检查没有发现断链。

### 独立 fresh-context 调用

按根 README 的技能验证要求，使用三个独立 subagent，未提供评估报告或预期答案：

1. **Generate + Novelty + Test + 伞技能**：在禁止检索/落盘、没有已核验文献与 pilot 的输入下，返回两个可检验的临时候选，将 novelty 标记 unverified、reading depth 标记 none，未声称已经执行检索或创建 portfolio。
2. **Select + Paper adapter**：审阅隔离目录中的多卡合成样例，实际调用 select/handoff/sync gates。识别 i01 的明确 caution 选择和 i03 的明确 defer；确认未入选 HOLD 不阻塞选定集合。更新后的样例正确区分 working current、release stale、delivery not-requested。
3. **Pressure + Journal Fit + Nature Review**：在禁止检索/实验/落盘的请求下，保留 skipped→pending，给出最小实验和修复路径；期刊仅作 provisional family screen，Nature 为 HOLD，没有代人选择，也没有编造当前投稿规则。

独立审阅促成了额外修正：矩阵不能串用另一张卡的收据；新版交接不能依赖旧 sync 的一个 current 标记；manifest 不能保留与当前决定冲突的状态。合成样例的 Page receipt 路径和 context 引用也已整理。

## 兼容要求与验证边界

- 新建或改写决策使用 v3。已有 v2 收据可读，但不会从未入选、全局 defer/abandon 或缺字段推断逐卡人类决定；迁移保留原件，缺失决定需补充明确来源。
- 新版 selection/handoff 要求 v2 sync、现存 P0 Page 和 current working projection receipt；不要求 release/delivery 同时 current。
- Page 序列化 phase 字段、能力 stage 字段及历史 Story 路径保留；它们不成为 Run 身份。
- 本次测试使用合成文件，证明机械门禁和技能决策行为，不证明真实科学证据、期刊规则或人的真实意愿。checker 核对记录的 revision/hash、字段与指针；没有重新执行来源库核验、实验或 Page 渲染。
- 未对真实项目数据执行批量迁移，未部署或提交 Git commit。实际 Task/Discovery/Page Run 执行器的整套线上流程不在本轮合成验证范围内。
