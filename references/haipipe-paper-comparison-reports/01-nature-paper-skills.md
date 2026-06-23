# Nature-Paper-Skills vs haipipe-paper

## 外部库定位

`Nature-Paper-Skills` 是 Nature 系列期刊优先的论文技能栈。它强调 claim-driven manuscript、figure-led storytelling、Nature-series pre-submission discipline。核心 skill 包括 `paper-workflow`, `paper-bootstrap`, `nature-portfolio-playbook`, `scientific-writing`, `manuscript-optimizer`, `figure-planner`, `citation-verifier`, `data-availability`, `submission-audit`, `rebuttal-response`。

## 与 haipipe-paper 的重叠

| 维度 | Nature-Paper-Skills | haipipe-paper |
|---|---|---|
| 核心哲学 | journal-first, claim-driven, figure-led | lifecycle-first, claim/evidence contract, TeX-first |
| Venue | Nature Portfolio 是中心 | `_venue/playbook-nature-portfolio` 是一个 venue pack |
| Figure | `figure-planner` 强调 one main claim per figure | `4-display` + display units + figure/table/diagram/illustration renderers |
| Citation | `citation-verifier` | `components/citation`, `edit-citation`, `edit-check-reference` |
| Submission | `submission-audit`, `data-availability` | `edit-submission-audit`, build/check, venue playbooks |
| Rebuttal | `rebuttal-response` | `5-respond/haipipe-paper-rebuttal` |

## 关键差异

| 差异 | 判断 |
|---|---|
| Nature 库是明确 journal-first | 我们是 venue-aware, 但不是 Nature-only |
| Nature 库的 skill 名更用户友好 | 我们的 `haipipe-paper-*` 更工程化, 可路由性强但学习成本高 |
| Nature 库更像安装式 skill suite | 我们更像长期 paper folder state machine |
| Nature 库强调 manuscript optimizer | 我们把 optimizer 拆成 claims, narrative, display, minimap, edit audits |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 把 Nature 的 "figure legends are second layer of result narration" 写入 Nature venue playbook | `_venue/playbook-nature-portfolio` |
| 增强 `data-availability` 和 source-data coverage checklist | `3-write-edit/haipipe-paper-edit-submission-audit` |
| 给 `4-display` 加一条更明确的 "one display, one claim unless justified" gate | `1-lifecycle/haipipe-paper-display/ref/` |
| 把 Nature pre-submission audit 拆成 policy, data, figure, claim 四类 blocker | submission audit cluster |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 把 workflow 默认锁定为 Nature | 我们还服务 MISQ, ISR, MS-IS, PNAS, JAMA, clinical, grant, patent |
| 把 figure-planner 独立成中心流程 | 我们已经用 `4-display` 作为 lifecycle stage, 更利于 backfill |

## 结论

Nature-Paper-Skills 对 haipipe-paper 最有价值的是 Nature venue knowledge 和 pre-submission discipline。它不应替代我们的 lifecycle, 但应作为 `_venue/playbook-nature-portfolio` 和 submission audit 的增强参考。

