haipipe-paper-revise-place — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.1.2] — 2026-07-27 — a VALUE keeps its bracket; only a CITATION discharges

- **The discharge rule was wrong for values and it was making verified numbers
  unverifiable.** `\citep{key}` is self-checking against the `.bib` forever, so its bracket is
  genuinely redundant once the key is placed. A bare `12.9` has no such property: the bracket is
  the ONLY thing tying it to the run, and `body.py` checks a prose number only on a bracketed
  sentence. Discharging it did not tidy a finished sentence, it blinded the board to it.
- A placed value now reads `12.9 [Q-X-n]` plus a `> Value:` lane naming the entry, the run and
  `state=verified`. This is not new design — it is `QC0@paper`'s S4, which has been the worked
  example of a FINISHED sentence since 260726, and is why `QC0` reports 3 numbers `ok`.
- Measured on MISQ: `S-Main-0`'s headline `12.90` was placed under the old rule and its page
  reports 0 markers, while `S-Main-6`, still carrying its brackets, reports 41. The board was
  brightest where least was finished.

## [0.1.1] — 2026-07-26

- Open-placeholder flags now land in the owning S page's `[REVISE]` log entry.
- Preserved the invocation hint under `metadata.argument_hint`, which conforms to
  the current Skill frontmatter schema.

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
