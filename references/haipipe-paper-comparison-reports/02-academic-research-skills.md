# Academic Research Skills vs haipipe-paper

## 外部库定位

`academic-research-skills` 是一个大而全的研究到发表套件。它包含 `deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`。其 full pipeline 是 research -> write -> integrity -> review -> revise -> re-review -> final integrity -> finalize -> process summary。它强调 human-in-the-loop、mandatory checkpoints、material passport、citation integrity、multi-agent review。

## 与 haipipe-paper 的重叠

| 维度 | Academic Research Skills | haipipe-paper |
|---|---|---|
| 全流程 | 10-stage research/publication pipeline | paper lifecycle + handoff 到 probe/discover/task/insight |
| 写作 | 12-agent academic-paper | `3-write-edit` 写作/编辑/audit cluster |
| Review | 7-agent reviewer panel | reviewer, claim-audit, proof-checker, submission-audit |
| Citation | claim-faithfulness audit, citation-check | citation components + DBLP/CrossRef hygiene |
| State | Material Passport + checkpoints | `STATUS.md`, `1-rounds`, lifecycle TeX files |
| Integrity gate | Stage 2.5/4.5 mandatory | maturity/checks, but gate policy较分散 |

## 关键差异

| 差异 | 判断 |
|---|---|
| ARS 从 research 起步, paper 只是其中一段 | haipipe-paper 明确只拥有 manuscript story, evidence 在外部 |
| ARS 多 agent 人设丰富 | haipipe-paper 更文件契约和路由驱动 |
| ARS checkpoint 很强 | haipipe-paper 有 stage gate, 但还可更 formal |
| ARS 支持多 citation/output 格式 | haipipe-paper 以 TeX paper folder 为中心 |
| ARS 是 Claude Code-first 插件生态 | haipipe-toolkit 是 OpenClaw/本仓库工作流生态的一部分 |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 借鉴 Stage 2.5/4.5 的 mandatory integrity gate, 明确成 haipipe maturity gate | `ref/paper-lifecycle.md`, `edit-submission-audit` |
| 引入 Material Passport 的思想, 但命名为 Paper Evidence Passport | `STATUS.md` 或 `0-lifecycle/2-claims` 附属文件 |
| reviewer panel 可扩展为 EIC + methodology + domain + devil advocate | `haipipe-paper-edit-reviewer` |
| checkpoint adaptive FULL/SLIM/MANDATORY 可用于 long-running paper sessions | `haipipe-paper-enter` |
| claim-reference alignment audit 可加强 citation component | `components/citation` |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 把 research pipeline 直接并入 paper skill | 会破坏我们“project evidence outside paper”的边界 |
| 让 paper skill 自动跑完整 research/writing/review chain | 对 PHI/Stata/server-blocked 项目风险太高 |
| 默认 DOCX/PDF/Pandoc 多格式中心化 | 我们当前最稳定资产是 TeX-first paper folder |

## 结论

ARS 是这批外部库中最完整的 peer workflow 参考。它比我们强在 checkpoints、多 agent reviewer、integrity gate 和 artifact passport。我们比它强在 paper-specific disk contract、evidence worker handoff、display units 和 venue playbook 与 claim ledger 的耦合。建议吸收 gate/reviewer/passport 机制, 不吸收其 research mega-pipeline 边界。

