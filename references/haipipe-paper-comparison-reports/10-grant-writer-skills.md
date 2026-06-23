# Grant Writer Skills vs haipipe-paper

## 外部库定位

`grant-writer-skills` 是完整 grant proposal pipeline, 面向 EU Horizon/ERC/MSCA 和 Romanian UEFISCDI/PNRR。它从 FOA analysis、document import、landscape、aims、literature、preliminary data、proposal writing、risk、budget、supporting docs、compliance、fact-check、review、revision 到 resubmission。输出以 Markdown 为主, 无 LaTeX 依赖。

## 与 haipipe-paper 的重叠

| 维度 | Grant Writer Skills | haipipe-paper |
|---|---|---|
| Target | funding proposal | academic manuscript |
| Venue/agency | agency templates and scoring | venue playbooks |
| Aims/claims | aims refinement | pitch/claims ledger |
| Evidence | preliminary data, literature, landscape | probe/discover/task/insight |
| Compliance | word counts, required sections, budget | submission audit, build-check |
| Review | Claude/Codex panel | reviewer/audit cluster |
| State | proposal state/tools | paper STATUS/lifecycle/rounds |

## 关键差异

| 差异 | 判断 |
|---|---|
| grant pipeline has budget/supporting docs/FOA parsing | paper skill should not carry these |
| grant output Markdown, agency sections | paper output TeX-first manuscript |
| grant checkpoints tied to PI decisions | paper gates tied to manuscript maturity and evidence |
| grant fact-check is journalism-grade, multi-pass | useful pattern for paper submission audit |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| Strengthen `_venue/playbook-grant` using this pipeline's agency/checkpoint ideas | `_venue/playbook-grant` |
| Add FOA/call analysis as an upstream grant-specific route, not generic paper route | application/grant or venue-grant |
| Borrow fact-check pass structure: citations, external facts, claim-source alignment, consistency | `edit-submission-audit` |
| Borrow agency-calibrated panel review as venue-calibrated reviewer profiles | `edit-reviewer` |
| Budget/timeline consistency analog can inspire methods/timeline/data availability consistency checks | submission audit |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| Fold grant budget/supporting docs into paper core | grant is a different artifact class |
| Make Markdown output the paper default | haipipe-paper relies on TeX folder and compile contract |
| Generalize FOA parsing to all papers | only grant/policy calls need this |

## 结论

Grant Writer Skills is a strong adjacent artifact workflow, not a paper workflow replacement. It should inform `_venue/playbook-grant`, fact-checking, agency/venue-calibrated review, and checkpoint discipline. The grant-specific budget/FOA/supporting-docs machinery should remain outside haipipe-paper core.

