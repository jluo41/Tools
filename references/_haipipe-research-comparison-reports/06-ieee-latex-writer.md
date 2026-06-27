# IEEE LaTeX Writer vs haipipe-paper

## 外部库定位

`ieee-latex-writer` 是 IEEE 论文写作和 LaTeX submission readiness skill。它覆盖 IEEEtran drafting/revision, narrative framing, experimental rigor, double-blind anonymity, reviewer responses, DOI/publication lookup, BibTeX cleanup, static LaTeX audit。它包含 `scripts/audit_ieee_latex.py` 和 `scripts/clean_ieee_bib.py`。

## 与 haipipe-paper 的重叠

| 维度 | IEEE LaTeX Writer | haipipe-paper |
|---|---|---|
| Venue | IEEE journals/conferences | `_venue/playbook-*`, 当前 IEEE 不是主 venue |
| LaTeX | IEEEtran-specific | TeX-first generic paper folder |
| Audit | static IEEE LaTeX audit | build-check, typeset, submission audit |
| BibTeX | IEEEtran cleanup | citation components, DBLP/CrossRef hygiene |
| Blind review | anonymity checks | submission audit可做, 但不够 IEEE-specific |
| Rebuttal | response letter workflow | `5-respond` |

## 关键差异

| 差异 | 判断 |
|---|---|
| IEEE 库是 venue-specific formatting + static scripts | 我们是 lifecycle and claim system |
| IEEE 库有可运行脚本 | 我们的 checks 还可更多 deterministic scripts |
| IEEE 库重视 official template/assets | 我们 venue packs 可补 template artifacts |

## 我们可吸收的点

| 建议 | 放置位置 |
|---|---|
| 新增 IEEE venue pack | `_venue/playbook-ieee` |
| 引入 static LaTeX audit script pattern | `4-build-submit/haipipe-paper-build-check/scripts` |
| 加 double-blind identity leak check | `edit-submission-audit` |
| 加 BibTeX cleanup script, 保留 DOI, 清除导出噪声字段 | `components/citation/scripts` |
| 给 venue pack 绑定 official templates | `_venue/playbook-ieee/templates` |

## 不建议吸收的点

| 不建议 | 原因 |
|---|---|
| 把 IEEEtran 逻辑写进 generic write skill | 应由 venue pack 和 build-check 条件触发 |
| 让 formatting checks 覆盖 claim/display checks | 格式合规不能替代论文论证质量 |

## 结论

IEEE LaTeX Writer 是 venue-specific static audit 的优秀样板。haipipe-paper 应把它作为新增 IEEE venue pack 和 deterministic build/citation scripts 的参考, 不应改变核心 lifecycle。

