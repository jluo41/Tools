# PaperSpine vs haipipe-paper

## 外部库定位

`PaperSpine` 是 motivation-driven paper/report writing suite, 支持 Codex、Claude Code、OpenClaw。它面向 journal paper、conference paper、course/technical report、review、competition paper。核心流程是先学习 target scene 和强样例, 再建立 rationale matrix, 然后 rewrite/build, LaTeX/PDF/Word, translation, audit。

## 与 haipipe-paper 的重叠

| 维度 | PaperSpine | haipipe-paper |
|---|---|---|
| Orchestrator | `paper-spine` routes branch skills | `haipipe-paper` routes lifecycle stages |
| 前期学习 | target-scene examples + recent papers + requirements | venue playbook + seed/pitch/claims |
| Citation | citation support bank | claim ledger + citation components |
| Build/rewrite | rewrite existing 或 build from materials | write/edit/weaving sections |
| LaTeX | `paper-spine-latex` | TeX-first folder + compile/build tools |
| Audit | artifact/rationale/citation/translation audit | review cluster + submission audit |

## 关键差异

| 差异 | 判断 |
|---|---|
| PaperSpine 的入口更产品化, 安装和多平台分发完整 | 我们更像内部研究工程系统 |
| PaperSpine 强制 target scene learning | 我们通过 `_venue/playbook-*` 做 venue knowledge, 但 exemplar learning 不够显式 |
| PaperSpine 有 UI/intake/config | 我们靠 paper console 和 folder state |
| PaperSpine 支持 translation package | 我们 paper skill 没有系统化 bilingual/translation package |
| PaperSpine 面向 report/competition 也可用 | 我们更聚焦 manuscript lifecycle |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 增加 "target scene examples" intake, 要求 venue pack 绑定 exemplars | `_venue/playbook-*` |
| 给每个重大改写生成 rationale matrix: 为什么改、对应 claim/display/venue rule | `1-rounds/*/decisions.md` 或 `applied.md` |
| 增加 installable dist/checklist 思维, 降低新 agent 进入成本 | `Tools/plugins/haipipe-toolkit` docs |
| 引入 `paper-spine-update` 风格的 reference update checker | `Tools/references` 管理脚本 |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 将 target-scene research 变成每次写作的必选前置 | 对已有 venue-pinned paper 会浪费 |
| 把 Word/translation package 作为核心完成标准 | 会稀释 TeX-first submission contract |

## 结论

PaperSpine 是最接近我们“写作流程产品化”的外部库。它给我们的启发不是 lifecycle 结构, 而是 intake、rationale matrix、target-scene exemplar learning 和多平台分发。haipipe-paper 应吸收其用户体验和 rationale 可审计性, 保持自己的 claim/evidence/display lifecycle。

