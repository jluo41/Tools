# haipipe-paper 外部 Skill 库对比报告索引

## 基准: 我们的 haipipe-paper skill set

本轮比较把 `Tools/plugins/haipipe-toolkit/skills/paper` 作为基准。它的核心不是一个写作 prompt，而是一个 TeX-first paper delivery lifecycle:

```text
enter/status
  -> seed
  -> pitch
  -> venue
  -> claims
  -> narrative
  -> display
  -> minimap
  -> write/edit
  -> review
  -> respond/present
```

关键设计:

| 维度 | haipipe-paper 基准 |
|---|---|
| 状态模型 | `STATUS.md` + `0-lifecycle/` + `1-rounds/` + `.paper-console.yaml` |
| 文件契约 | `0-lifecycle`, `0-sections`, `0-displays/displayNN-*`, `1-rounds` |
| 论证核心 | claim ledger, evidence needs, venue-coupled claims |
| 证据接口 | paper GAP -> delivery need -> probe/discover/task/insight -> backfill |
| 写作方式 | 从 minimap 和 display units 生成/编辑 TeX sections |
| 审查方式 | claim audit, citation audit, reviewer, proof checker, submission audit |
| Venue 处理 | `_venue/playbook-*` 是知识层, 不是流程层 |
| 强项 | 可恢复、可审计、可路由、适合长期 paper project |
| 短板 | 对新用户重, setup 成本高, 外部检索/多模型面板/专门工具链可继续增强 |

## 报告列表

| # | 外部库 | 报告 |
|---|---|---|
| 1 | Nature-Paper-Skills | [01-nature-paper-skills.md](01-nature-paper-skills.md) |
| 2 | Academic Research Skills | [02-academic-research-skills.md](02-academic-research-skills.md) |
| 3 | PaperSpine | [03-paperspine.md](03-paperspine.md) |
| 4 | PaperRAG Skill | [04-paper-rag-skill.md](04-paper-rag-skill.md) |
| 5 | Cite-Guard | [05-cite-guard.md](05-cite-guard.md) |
| 6 | IEEE LaTeX Writer | [06-ieee-latex-writer.md](06-ieee-latex-writer.md) |
| 7 | Research Agent Skills | [07-research-agent-skills.md](07-research-agent-skills.md) |
| 8 | ReproRun | [08-reprorun.md](08-reprorun.md) |
| 9 | Research Co-Pilot | [09-research-co-pilot.md](09-research-co-pilot.md) |
| 10 | Grant Writer Skills | [10-grant-writer-skills.md](10-grant-writer-skills.md) |

## 总体结论

| 外部库类型 | 对我们的价值 | 建议 |
|---|---|---|
| Venue/journal-first 写作库 | 补 venue playbook、submission audit、rebuttal 素材 | 选择性吸收到 `_venue/` 和 review cluster |
| 全流程研究/写作套件 | 提供 agent-team、checkpoint、integrity gate 设计参考 | 不替换 lifecycle, 吸收 gating 和 multi-review |
| 单点工具库 | RAG、citation grounding、IEEE audit、reproduction | 作为 evidence worker 或 component, 不并入核心 lifecycle |
| grant/survey/research lifecycle | 对 paper 之外的 project lifecycle 有参考价值 | 放在 application/research planning 层, paper 只接收其输出 |

最重要的产品判断: haipipe-paper 应继续保持“paper owns story, evidence workers own verdicts”的架构。外部库的强项不应把 paper skill 变成一个无边界 research mega-pipeline, 而应作为:

```text
external capability -> delivery need route -> verdict/artifact -> paper backfill
```

