# haipipe diagrams / board work — Feedback Inbox

Capture preferences, corrections, and defects observed while doing board and Q-page work, then fix
them in a later revision pass. Schema and workflow follow the house convention in
`../../display/skills/figure-to-svg/feedback/` (see its `../fn/feedback.md`).

Two extra fields on each file, so a digest can route without re-reading the body:

- `kind:` preference (how JL wants the work done) · convention (a rule about artifacts) ·
  defect (something that broke, usually a missing enforcer)
- `lands_in:` where the fix belongs

## Files in this batch

Captured 2026-07-28 from the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle).
Sixteen topics: 8 preferences · 5 defects · 3 conventions.

**Second capture, rows 17-22.** Added later the same day from the §4/§5 + PROBE tail of the same
session, after rows 1-16 already existed. Each was checked against rows 1-16 AND against
`260727-misq-s3-s4-session.md` before being written; fourteen further candidates were dropped as
restatements rather than added, which is row 7's own rule applied to this file. Row 17 is kept
DESPITE duplicating their P8, because it carries evidence P8 could not have.

| # | topic | kind | lands in |
|---|-------|------|----------|
| 1 | [make-the-decision-yourself](2026-07-28_make-the-decision-yourself.md) | preference | ref/writing-rules.md + the board skill's operating notes |
| 2 | [the-page-is-the-record-not-the-chat](2026-07-28_the-page-is-the-record-not-the-chat.md) | preference | ref/writing-rules.md |
| 3 | [repair-what-your-own-work-invalidated](2026-07-28_repair-what-your-own-work-invalidated.md) | defect | check.py (mechanical half) + ref/writing-rules.md |
| 4 | [copy-the-sibling-pages-shape](2026-07-28_copy-the-sibling-pages-shape.md) | preference | ref/q-template.md |
| 5 | [cross-check-another-agents-analysis](2026-07-28_cross-check-another-agents-analysis.md) | preference | ref/writing-rules.md |
| 6 | [a-decision-row-is-not-an-argument](2026-07-28_a-decision-row-is-not-an-argument.md) | defect | ref/q-template.md + ref/writing-rules.md |
| 7 | [own-or-point-never-restate](2026-07-28_own-or-point-never-restate.md) | defect | check.py + ref/writing-rules.md |
| 8 | [verify-in-a-generated-block-dont-assert-in-prose](2026-07-28_verify-in-a-generated-block-dont-assert-in-prose.md) | preference | check.py + build.py |
| 9 | [checker-blind-spot-markdown-ref-vs-label](2026-07-28_checker-blind-spot-markdown-ref-vs-label.md) | defect | build.py |
| 10 | [assets-is-the-selected-versions-is-the-lineage](2026-07-28_assets-is-the-selected-versions-is-the-lineage.md) | convention | the display skills + asset-manifest.py |
| 11 | [provenance-must-be-measurable](2026-07-28_provenance-must-be-measurable.md) | preference | asset-manifest.py + the display skills |
| 12 | [name-the-unit-the-same-everywhere](2026-07-28_name-the-unit-the-same-everywhere.md) | convention | the display skills |
| 13 | [no-disclaimer-that-denies-an-unmade-claim](2026-07-28_no-disclaimer-that-denies-an-unmade-claim.md) | convention | the display skills |
| 14 | [outcome-wording-must-match-the-ledgers-variable-type](2026-07-28_outcome-wording-must-match-the-ledgers-variable-type.md) | defect | the display skills + haipipe-paper-draft-values |
| 15 | [benchmark-against-the-venue-with-numbers](2026-07-28_benchmark-against-the-venue-with-numbers.md) | preference | haipipe-paper-stage + section-stats.py |
| 16 | [milestone-commits-across-nested-submodules](2026-07-28_milestone-commits-across-nested-submodules.md) | preference | the board skill's operating notes |
| 17 | [use-the-owning-skill-not-hand-work](2026-07-28_use-the-owning-skill-not-hand-work.md) | preference | the paper family's entry rules + ref/writing-rules.md |
| 18 | [fix-everything-fixable-dont-scope-shed](2026-07-28_fix-everything-fixable-dont-scope-shed.md) | preference | ref/writing-rules.md + haipipe-paper-probe step 5 |
| 19 | [resolve-citations-actively-check-after](2026-07-28_resolve-citations-actively-check-after.md) | preference | haipipe-paper-probe harvest + .bib conventions |
| 20 | [checkpoint-before-the-user-asks](2026-07-28_checkpoint-before-the-user-asks.md) | preference | ref/writing-rules.md |
| 21 | [read-a-ruling-narrowly-then-offer-the-wider](2026-07-28_read-a-ruling-narrowly-then-offer-the-wider.md) | preference | ref/writing-rules.md |
| 22 | [probe-answered-vs-read-has-no-enforcer](2026-07-28_probe-answered-vs-read-has-no-enforcer.md) | defect | check-probe-cards.sh + haipipe-probe SKILL.md |

## The one-line summary

Most of these are not new knowledge. `ref/writing-rules.md` already says "Clear out stale text",
and that was the session's dominant failure mode with six instances in a day. It is the only hard
rule with no enforcer. The two genuinely new editorial rules are
[a-decision-row-is-not-an-argument](2026-07-28_a-decision-row-is-not-an-argument.md) and
[own-or-point-never-restate](2026-07-28_own-or-point-never-restate.md); the highest-value mechanical fix is
[checker-blind-spot-markdown-ref-vs-label](2026-07-28_checker-blind-spot-markdown-ref-vs-label.md).

## Relationship to `260727-misq-s3-s4-session.md`

A parallel session wrote its own reflection into this folder at the same time, as ONE file with 20
topics, covering §3 Theory AND §4 Measurement. This batch is one file per topic and covers §3 plus
the display registry only. Neither is wrong; they were written blind to each other, which is itself
topic M6 in that file. Read them together and expect overlap. A digest should merge, not pick.

**The same topic, found twice and independently.** Convergence here is signal, so these are the
ones to graduate first.

| this batch | their file |
|---|---|
| copy-the-sibling-pages-shape | P2 convention propagates by copying a NAMED sibling |
| a-decision-row-is-not-an-argument | P3 a decision row carries real metadata inline · P4 one short sentence per line |
| assets-is-the-selected-versions-is-the-lineage | P5 |
| provenance-must-be-measurable | P6 provenance answerable from the folder itself |
| repair-what-your-own-work-invalidated | M3 state mirrors rot, and they rot fast |
| name-the-unit-the-same-everywhere | M4 renumbering a registry silently breaks every consumer |
| use-the-owning-skill-not-hand-work (row 17) | P8 call the skill, do not hand-roll its work |

Note that P3 and P4 sit on opposite sides of the tension this batch names in
`a-decision-row-is-not-an-argument`: P3 says a row needs real metadata inline, P4 says keep the lines
short. Both are true and neither alone prevents the 33-line row JL rejected. The missing piece is the
decision-versus-argument split plus a row-length cap.

**Only in their file** (do not re-derive these; §4 and the skill-dispatch topics were outside this
batch's scope): P1 answer at the size of the question · P7 prefer the published source over
recomputation · P8 call the skill, do not hand-roll its work · P9 retire settled apparatus to the Log ·
P10 delete what is superseded · P11 the section title belongs inside Content · P12 a methods section
opens with study design · P13 the Log belongs on the Section Page, in order · P14 ask for the explicit
finish-list · M1 depth-0 closes more than the records assume · M2 two numbers that looked verified were
wrong · M5 `section-stats.py` counts `%%` comments as prose.

**Only in this batch**: make-the-decision-yourself · the-page-is-the-record-not-the-chat ·
cross-check-another-agents-analysis · own-or-point-never-restate ·
verify-in-a-generated-block-dont-assert-in-prose · checker-blind-spot-markdown-ref-vs-label ·
no-disclaimer-that-denies-an-unmade-claim · outcome-wording-must-match-the-ledgers-variable-type ·
benchmark-against-the-venue-with-numbers · milestone-commits-across-nested-submodules ·
and from the second capture: fix-everything-fixable-dont-scope-shed ·
resolve-citations-actively-check-after · checkpoint-before-the-user-asks ·
read-a-ruling-narrowly-then-offer-the-wider · probe-answered-vs-read-has-no-enforcer.

Combined, after merging the six duplicates and counting row 17 once with their P8:
**35 distinct topics** from the one session.

## What the second capture adds that the first two could not

Rows 17, 18 and 22 are one finding from three sides, and it only became visible once the phase skill
was finally run. A checker that was never invoked had eight harvest debts and one unowned placeholder
sitting green for days. Row 22 is the mechanical half and the cheapest fix in the file: six of those
eight needed ONE WORD changed, not a re-harvest, because the interpretation had already been written
and only the `state:` field was stale.

Row 19 is the one live grant to carry forward: JL released citation resolution to the agent with
review afterwards, which changes a standing "human-only" rule on at least two S pages.
