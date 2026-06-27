# ReproRun vs haipipe-paper

## 外部库定位

`ReproRun` 是论文复现 skill。它从 paper title/PDF 出发, 自动找 code/data, 构建环境, smoke test, full run, 再把实际结果与论文 claims 比较。它包含六个 agent: paper-reader, resource-finder, environment-builder, smoke-tester, full-runner, result-comparator。核心输出是 honest verdict: numbers reproduced, pipeline reproduced, partial, or cannot reproduce.

## 与 haipipe-paper 的重叠

| 维度 | ReproRun | haipipe-paper |
|---|---|---|
| Claim verification | measured vs claimed numbers | `2-claims` GAP -> probe/task verdict |
| Environment | build/repair runtime | outside paper, in task/probe |
| Outputs | reproduction_report, setup/smoke/full reports | backfilled claim slots, rounds, display artifacts |
| Language scope | Python full, R/MATLAB/Julia reduced | Stata/CMS/PHI projects route to task/server |
| State | per-paper output namespace | paper folder + evidence worker artifacts |

## 关键差异

| 差异 | 判断 |
|---|---|
| ReproRun 是 external paper reproduction | 我们更多验证自己的 paper claims |
| ReproRun 自动找 repo/data/build env | 我们把 execution 分给 task/probe, 尤其 server/PHI gated |
| ReproRun 有 explicit honest partial verdict | 我们 claim ledger 有 have/weak/GAP, 但 reproduction verdict 分类可更细 |
| ReproRun agents 用 structured markdown 文件通信 | 与我们 disk-state 思路高度兼容 |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 把 `numbers reproduced / pipeline reproduced / partial / cannot reproduce` 映射为 claim evidence status 子类型 | `2-claims` |
| 为 evidence worker 添加 reproduction mode | `/haipipe-probe` 或 `/haipipe-task` |
| 对每个 claim 保存 measured-vs-claimed comparison table | claim ledger backfill |
| 借鉴 5-round dependency self-healing loop, 但放在 task worker | task/deploy layer |
| 对外部 paper reproducibility review 可作为 reviewer mode | `edit-reviewer` 或 independent insight |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 让 paper skill 自己 clone/build/run 外部代码 | 这属于 evidence/task worker, 也可能触发网络/安全/PHI风险 |
| 把 Python-first 假设引入 haipipe-paper | 本仓库有 Stata/CMS/PHI workflow, 不应偏 Python |

## 结论

ReproRun 与我们的 delivery-need 架构非常互补。它最适合作为 probe/task 的 reproduction backend。haipipe-paper 应只消费其 verdict 和 comparison artifacts, 然后更新 claim ledger、display notes 和 section wording。

