haipipe-paper-revise-place — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## 1.0.0 — 2026-07-19 — created; placement is REVISE's first step

From the `paper/2-phase` skillset review.

### Changed (JL: "Follow your recommendation." — D7)
Placement — substituting a landed key, number, or display link into the prose — becomes a REVISE worker. It had been buried as "Phase 4 PLACE" inside three skills that lived under `1-probe/` and were named probe lane workers, even though editing manuscript prose is the definition of REVISE, not of ③④⑤.

The ruling was already half-made: `haipipe-paper-revise/CHANGELOG.md [1.5.1]`, 2026-07-10, recorded "REVISE resolves `\cite{TOADD}` slots whose keys have landed in .bib" — but only the first half of that entry ever reached the SKILL body, so a worker reading the skill would place nothing.

### Changed — the order is binding: place → content → humanizer → results
Placement runs FIRST. Running the prose workers before substitution means every landed key and number lands in sentences those workers had already closed, so the text that ships was never reviewed in its final form. Running de-AI over `{VAL:? held-out accuracy}` and swapping in the number afterwards reviews a sentence that does not exist.

### Changed — two same-commit reconciliations in the landing zone
`haipipe-paper-revise-content/SKILL.md:19` forbade exactly this work ("does not verify numbers or citations… that is haipipe-paper-probe-values / -citation"); rewritten to point at this worker and at the evidence check. `haipipe-paper-revise/SKILL.md:121` stated REVISE's precondition as "reads PROBE outputs (citations placed…)", which is self-referential once placement IS a REVISE step; rewritten to say REVISE reads what PROBE landed in each `### a-executor` and places it.
Also fixed in the same pass: `haipipe-paper-revise-content/ref/content-edit.md` opened with a comment-first instruction ("you change no prose… fixes happen only in Round 2, after the human replies") that contradicted the skill's own "fully automatic, no human gate". A worker loading that ref would refuse to substitute anything.

### Discharge rule
A bracket comes off only when the hole is actually filled. A placeholder whose answer has not landed keeps its bracket and is flagged — that is an accurate statement, not a failure. Removing the bracket while leaving the placeholder is the failure: the hole becomes unowned and nothing will ever fill it.
