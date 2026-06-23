# Cite-Guard vs haipipe-paper

## 外部库定位

`Cite-Guard` 是 LaTeX/BibTeX paper 的 citation and claim-grounding pipeline。它有 audit, resolve, ground, venue, ml, review_critiques 六类阶段, 通过 OpenAlex/Crossref/arXiv/DBLP resolution、evidence fetching、claim grounding、venue/ML lens、blocker rules 生成 per-reference audit table 和 ranked critique。

## 与 haipipe-paper 的重叠

| 维度 | Cite-Guard | haipipe-paper |
|---|---|---|
| BibTeX hygiene | audit + corrected bib | edit-write DBLP/CrossRef hygiene + citation components |
| Canonical resolution | OpenAlex/Crossref/arXiv/DBLP | DBLP/CrossRef fallback, local checks |
| Claim grounding | citation evidence support | claims ledger + citation audit |
| Venue lens | policy + ML/NeurIPS profile | `_venue/playbook-*` |
| Blocker rules | configurable default/profile blockers | submission audit gates, less centralized |
| Output | CSV/MD reports, corrected bib, rewrites | review notes, rounds todo, sections backfill |

## 关键差异

| 差异 | 判断 |
|---|---|
| Cite-Guard 是 deterministic-ish CLI pipeline | 我们的 citation checks 更分散在 writing/review skills |
| Cite-Guard 输出 per-reference score | 我们更关注 claim slot status 和 manuscript readiness |
| Cite-Guard 有 profile blockers | 我们 venue-specific blockers 可以更明确 |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 增加 `audit_references.csv` 风格的 per-reference table | `components/citation` |
| 把 citation check 拆成 audit/resolve/ground/venue/profile/review stages | `haipipe-paper-edit-check-reference` |
| 增加 blocker rules schema: unresolved, year/venue mismatch, unsupported abstract/conclusion claim | submission audit + citation component |
| 支持 OpenAlex/arXiv 作为 DBLP/CrossRef 之外的 resolution backend | citation scripts |
| 将 `rewrites.tex` 思路映射到 paper backfill todo | `1-rounds/<round>/todo.md` |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 把 citation score 当作 paper acceptability score | citation 是必要条件, 不是故事/claim/display 的充分条件 |
| 将 NeurIPS profile 作为默认 | 我们需要 venue pack 驱动, 非 ML paper 不能套用 |

## 结论

Cite-Guard 是 citation component 的强参考。haipipe-paper 应吸收它的 staged citation pipeline 和 blocker rules, 并把结果接入 `1-rounds/todo.md` 与 `2-claims` backfill, 而不是只输出独立报告。

