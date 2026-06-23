# Research Agent Skills vs haipipe-paper

## 外部库定位

`research-agent-skills` 是一组研究论文审稿和编辑 Markdown skill。它覆盖 writing editor、structural editor、abstract checker、statistical reviewer、top3 reviewer、bibliography checker、research code review、replication archive、R refactor。它不是一个统一 orchestrator, 更像多个可直接调用的 reviewer/editor tools。

## 与 haipipe-paper 的重叠

| 维度 | Research Agent Skills | haipipe-paper |
|---|---|---|
| Writing edit | writing/structural editor | edit-content, edit-weaving, section playbooks |
| Abstract check | bidirectional abstract-body checker | proof/submission/reviewer audit可覆盖, 但未单独成型 |
| Statistics | statistical reviewer | edit-reviewer, manual-review-values |
| Citation | bibliography checker | citation components |
| Code/repro | review-paper-code, replication-archive | paper routes evidence/code issues to task/probe |
| Review | top3 reviewer | edit-reviewer |

## 关键差异

| 差异 | 判断 |
|---|---|
| 外部库以独立 reviewer/editor 为单位 | 我们以 lifecycle stage 和 paper folder 为单位 |
| 外部库有很清楚的单点 audit names | 我们同类能力较多, 但命名更内部化 |
| 外部库的 abstract checker 很具体 | 我们可补一个抽象层面强 audit |
| 外部库包含 replication archive builder | 我们更倾向把复现交给 evidence/task worker |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 新增 `haipipe-paper-edit-abstract-checker` 或并入 proof-checker | `3-write-edit` |
| structural editor 的 given-new flow, paragraph unity, section handoff 维度可写入 weaving | `haipipe-paper-edit-weaving` |
| statistical reviewer 的 perspective mode 可增强 manual values review | `edit-manual-review-values` |
| replication archive checklist 可作为 submission audit 的 reproducibility 子模块 | `edit-submission-audit` |
| R refactor 可交给 task/code review 层, 不进入 paper core | task skill |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 把所有 editor tools 平铺进 paper skill 命令空间 | 我们已有 cluster, 应合并为 review profiles |
| 让 code review 直接改 manuscript | 代码 verdict 应回填 claim/display, paper 再改 prose |

## 结论

Research Agent Skills 的价值是 reviewer/editor 检查维度非常清楚。它适合作为 haipipe `3-write-edit` audit cluster 的维度补丁, 尤其 abstract-body consistency、structural edit、statistics review 和 replication archive readiness。

