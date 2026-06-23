# PaperRAG Skill vs haipipe-paper

## 外部库定位

`paper-rag-skill` 是一个单点工具型 skill: 把 academic PDFs 转成 text, chunk 后写入 ChromaDB, 通过 `query_for_agent()` 给 agent 检索上下文。它的核心是 PDF -> text -> embeddings -> local query。

## 与 haipipe-paper 的重叠

| 维度 | PaperRAG | haipipe-paper |
|---|---|---|
| 目标 | 建论文知识库 | 写/修/审一篇 manuscript |
| 证据 | retrieval chunks | probe/discover/task/insight verdicts |
| 状态 | `PaperRAG/papers`, `texts`, `chroma_db` | `STATUS.md`, lifecycle, rounds |
| 输出 | retrieved context | claim ledger, display units, sections |
| 自动化 | 增量索引和查询 | evidence need routing and backfill |

## 关键差异

| 差异 | 判断 |
|---|---|
| PaperRAG 是 retrieval substrate, 不是 paper workflow | 应作为 discover/evidence backend |
| PaperRAG 不做 claim-faithfulness 判断 | 不能直接替代 citation verifier 或 probe |
| PaperRAG 依赖 embeddings/API key/Chroma | 我们目前没有强制本地向量库依赖 |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 为 `/haipipe-discover` 增加可选 local paper RAG backend | discovery skill, not paper core |
| 在 paper delivery need 中允许 `kind: context` route 到 PaperRAG query | `ref/delivery-need.md` |
| 为 claim ledger 的 citation/context need 保存 retrieval provenance | `0-lifecycle/2-claims` |
| 用 `expand_neighbors` 思想改善上下文完整性 | discover/query helper |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 在 haipipe-paper core 中强依赖 ChromaDB | 会提高 setup 成本, 且 paper skill 应能离线读现有证据 |
| 把 retrieved chunks 当作 verdict | 检索只是证据候选, verdict 仍需 probe/discover 判断 |

## 结论

PaperRAG 对我们是 evidence retrieval backend, 不是 paper workflow 竞品。最合适的集成方式是 `paper GAP -> /haipipe-discover -> PaperRAG query -> context report -> claim backfill`, 而不是让 paper skill 自己维护向量库。

