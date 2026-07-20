haipipe-paper-draft-citation — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 1.1.0 — 2026-07-19 — READ-ONLY: the lane reports, the hub writes

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` finding N2 (JL: "我以为draft会call draft-citaton, draft-values, ... 最后之后haipipe-paper-draft 再改 draft.md 和Q-consumers").

**Two writers, and a race.** This lane edited the manuscript prose directly, and claimed the right to RAISE a `## Q-<Stage>-<n>` and author its ENTRY in `1-probes/` — while `haipipe-paper-draft` said IT folded the new questions in. Both files claimed the pen. Worse, `Step 4a` dispatches all three lanes "in one batch": citation and values both edit the same working `.md`, and a sentence missing both a citation and a number is the common case, not the corner one.

The lane is now READ-ONLY. It walks and REPORTS one row per hole — where it is, what it owes (`\\cite{TOADD}`), and which `Q-<Stage>-<n>` will produce it, or `UNOWNED`. `haipipe-paper-draft` takes the three reports and writes: the prose placeholders, the Q-consumer, and the probe entries. One writer per file — the same rule the bank's QA files enforce with ONE WRITER + `set -C`. `allowed-tools` drops `Edit` and `Write` accordingly.

## 1.0.0 — 2026-07-19 — created, from the DRAFT half of the retired `haipipe-paper-probe-citation`

From the `paper/2-phase` skillset review (118 findings, 5 parallel auditors, 22/22 spot-checks passed).

The old `haipipe-paper-probe-citation` was named a probe lane worker, but an audit of all five of its numbered phases found NONE of them was PROBE work (③DISPATCH / ④POINT / ⑤INTERPRET). Its phases straddled four phases: AUDIT + ROUTE/PLAN were ①ORGANIZE (DRAFT), CANDIDATE wrote to a sidecar that no longer exists, PLACE edited manuscript prose (REVISE), and REVIEW was a human-paced pre-submission walk (CHECK). Its own text proved it — it declared itself "fully automatic" while instructing "Wait for explicit user approval before any edit."

### Changed (JL: "I think we can do A" — three separate lane skills, not one folded hub)
"For each topic, they should be aware how to check the values and citations and displays, and raise the questions." The three lanes stay three skills because the CHECKING METHOD is distinct expertise per lane — bibliographic verification, numeric re-derivation, and unit correctness are not interchangeable — and folding them into the draft hub would blend that expertise away.

### Changed (JL: "\\cite{TOADD} [Q-XXX-N] So I want something like this.")
A hole this lane cannot fill leaves a placeholder carrying the id of the question that will settle it, two markers side by side and never fused. A placeholder with no bracket is a defect: nobody owns it, so nobody will ever fill it. When no existing question would produce it, this lane RAISES one — JL: "feel free to add more questions … the Q-consumer is as many as possible … if there's no one here, I think you should propose a new question."

This skill carries the DRAFT half only. Placement moved to `haipipe-paper-revise-place`; pre-submission verification to `haipipe-paper-check-evidence`; harvest folded into `haipipe-paper-probe`'s ⑤ INTERPRET.
