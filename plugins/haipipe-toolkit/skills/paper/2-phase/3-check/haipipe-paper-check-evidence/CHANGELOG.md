haipipe-paper-check-evidence — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 1.0.0 — 2026-07-19 — created; the pre-submission evidence walk gets a home

From the `paper/2-phase` review (`../../../_console/260719-02-PHASE-BOUNDARY-REFACTOR.md`), ruling D11.

### Changed (JL: "I think check should be in executor side." → confirmed as the NARROW reading, "我 agree with this")
Two readings were on the table. NARROW: the verification work belongs to the CHECK PHASE rather than to DRAFT. BROAD: verification belongs to the executor side entirely, so the paper never re-verifies what came across the wall and this skill should not exist. JL confirmed the narrow one — the broad reading changes the task/discovery `qa` gate contract, which is a different bucket and needs its own run.

### Where the content came from
The three `1-probe/haipipe-paper-probe-{citation,values,display}` skills each carried a `Phase 5 REVIEW` that was a human-paced, pre-submission verification walk — inside skills that declared themselves "fully automatic" and sat in a phase (PROBE = ③DISPATCH ④POINT ⑤INTERPRET) that does no verification at all. `probe-citation` proved the point against itself: line 100 said "All five phases run automatically without stopping for human input" while line 364 said "Wait for explicit user approval before any edit", and line 104 named the destination outright — "Human review happens ONLY in the CHECK phase".

### Why CONDITIONAL dispatch, not a fold into haipipe-paper-check
An audit of the landing zone found DUPLICATE at the shallow layer, GAP at the deep layer, and a CONFLICT on CADENCE. `haipipe-paper-check` is a per-stage, per-section gate; all three incoming REVIEWs are explicitly pre-submission ("run before a top-tier submission when one wrong-context cite is a desk-reject risk"). Folding them in means resolving every DOI at every section gate — unaffordable — or the pass silently never running. So it mirrors `haipipe-paper-proof-checker`: dispatched only when the run is pre-submission, exactly as the proof-checker fires only when a section carries `\begin{proof}`, and never running alone as the gate.

### Preserved verbatim, because it is not derivable
The three-axis citation decomposition (existence / metadata / context) with its named failure modes; the source-of-truth hierarchy (Google Scholar is a discovery aid, never the verification source — its metadata is scraped and often wrong); the wrong-context hunting patterns; the lit-review/intro asymmetry (the intro's citations were drafted from memory and are the suspicious ones); revise-drift as the #1 citation regression; the value verification recipes, especially NEVER trust a claimed delta; the value failure taxonomy (rounding_drift / unit_error / stale_snapshot / config_mismatch / figure_drift_from_body); method claims as values; the closed-format figure rule.

### Report-only
It seeds `> CHECK:` comments and never edits prose — CHECK verifies, the human decides, REVISE changes. This is deliberate: `haipipe-paper-proof-checker` currently edits the `.tex` from inside CHECK while `haipipe-paper-check` expects only "verdict PASS or WARN" from it, and this skill does not repeat that. A finding the human declines to fix becomes a `{CONCERN:}` entry rather than evaporating.
