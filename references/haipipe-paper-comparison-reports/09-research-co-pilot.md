# Research Co-Pilot vs haipipe-paper

## 外部库定位

`research-co-pilot` 是整个 research lifecycle 的 Claude co-pilot。它覆盖 research-brainstorm、literature-review、methodology-advisor、ethics-committee、survey-design、data-analysis、qualitative-coding、manuscript-drafter、replication-designer、grant-writer、talk-builder、reviewer-response、citation-formatter、peer-review。它用 project vault 管理 `research/<project>/` 文件夹和 knowledge, decisions, bibliography, glossary, open questions。

## 与 haipipe-paper 的重叠

| 维度 | Research Co-Pilot | haipipe-paper |
|---|---|---|
| Lifecycle | research-wide lifecycle | paper-specific lifecycle |
| State | research vault + manifest + knowledge | paper folder + STATUS + lifecycle + rounds |
| Manuscript | manuscript-drafter | write/edit |
| Peer review | peer-review | edit-reviewer/audit cluster |
| Reviewer response | reviewer-response | 5-respond |
| Citation | citation-formatter | citation components |
| Survey | survey-design | outside paper core, maybe project/data skill |

## 关键差异

| 差异 | 判断 |
|---|---|
| Research Co-Pilot 明确把 data collection/IRB 等人类步骤作为 gates | haipipe-paper 的 gates 更关注 paper maturity |
| Vault 是 project-level | 我们刻意不让 project-level narrative layer 拥有 paper story |
| Survey/design/ethics/data/qual coding 是 project能力 | paper 只应接收其输出 |
| 它的 `/vault audit` 防 drift 很有参考价值 | 我们 `enter/status` 可加强 cross-file drift audit |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 借鉴 project vault 的 knowledge/decisions/open questions, 但保持在 paper `1-rounds` 和 `STATUS` 内 | `haipipe-paper-enter`, `1-rounds` |
| Survey Builder 对应的 `survey-design` 应接入 haipipe data/application skill, paper 接收 instrument description 和 validity evidence | data/application skills |
| `/vault audit` 思想可做成 paper folder drift audit | `haipipe-paper-enter` 或 `edit-consistency` |
| manuscript-drafter 的 voice profile 可增强 write/edit | `haipipe-paper-edit-weaving` |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 用 research vault 取代 paper folder contract | paper lifecycle 需要 TeX-first source-of-truth |
| 让 paper skill 管 IRB、data collection、survey authoring | 这些是 project/data/application 层, 非 manuscript owner |

## 结论

Research Co-Pilot 是 project lifecycle 层面的强参考, 尤其 survey-design、vault audit、human gates 和 manuscript voice profile。对 haipipe-paper 来说, 它不是同层竞品, 而是上游 project orchestration 的参考。paper skill 应接收其 artifacts, 不接管其全生命周期。

