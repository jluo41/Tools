haipipe-paper-draft-display — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 1.0.0 — 2026-07-19 — created, from the DRAFT half of the retired `haipipe-paper-probe-display`

From the `paper/2-phase` skillset review (118 findings, 5 parallel auditors, 22/22 spot-checks passed).

The old `haipipe-paper-probe-display` was named a probe lane worker, but an audit of all five of its numbered phases found NONE of them was PROBE work (③DISPATCH / ④POINT / ⑤INTERPRET). Its phases straddled four phases: AUDIT + ROUTE/PLAN were ①ORGANIZE (DRAFT), CANDIDATE wrote to a sidecar that no longer exists, PLACE edited manuscript prose (REVISE), and REVIEW was a human-paced pre-submission walk (CHECK). Its own text proved it — it declared itself "fully automatic" while instructing "Wait for explicit user approval before any edit."

### Changed (JL: "I think we can do A" — three separate lane skills, not one folded hub)
"For each topic, they should be aware how to check the values and citations and displays, and raise the questions." The three lanes stay three skills because the CHECKING METHOD is distinct expertise per lane — bibliographic verification, numeric re-derivation, and unit correctness are not interchangeable — and folding them into the draft hub would blend that expertise away.

### Changed (JL: "\\cite{TOADD} [Q-XXX-N] So I want something like this.")
A hole this lane cannot fill leaves a placeholder carrying the id of the question that will settle it, two markers side by side and never fused. A placeholder with no bracket is a defect: nobody owns it, so nobody will ever fill it. When no existing question would produce it, this lane RAISES one — JL: "feel free to add more questions … the Q-consumer is as many as possible … if there's no one here, I think you should propose a new question."

This skill carries the DRAFT half only. Placement moved to `haipipe-paper-revise-place`; pre-submission verification to `haipipe-paper-check-evidence`; harvest folded into `haipipe-paper-probe`'s ⑤ INTERPRET.
