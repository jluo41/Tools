# Shared prose rubric · haipipe-draft-review/base-v1

Writing self-review and Page CHECK use this one base. Resolve applicable host,
venue, user and target-job requirements before judging. Page CHECK adds its
whole-Page mechanics and independent actor rules; it does not transfer those
release responsibilities to the writing worker.

| Axis | Base question | Evidence needed |
|---|---|---|
| Mechanics | Is the required structure present, ordered, addressable and consistent? | Target/format contract and observed structure; relevant mechanical checks |
| Function | Does the paragraph/Section answer its assigned reader question and perform its job? | Job/requirements mapped to actual sentences; Section coverage and joins |
| Evidence | Is every factual claim supported, and are claims, numbers, citations and uncertainty preserved within the authorized change? | Baseline comparison and exact supplied sources/Results; no invented premises |
| Readability | Can the intended reader follow the text without supplying an unstated premise or decoding unnecessary jargon? | Located prose, explanation of the reading problem, necessary context/seams |

Use these verdicts per applicable criterion:

- MEETS: observed text and available evidence satisfy the criterion.
- NEEDS WORK: a demonstrated defect, with the smallest authorized repair.
- N/A: the criterion does not apply; explain why.
- NOT VERIFIABLE: required evidence/authority is unavailable or conflicts;
  name the missing source or unresolved decision. It is never a pass.

Add resolved venue requirements and specialist findings as sourced criteria;
do not change the rubric after seeing a low result. For a local edit, assess
the changed span, preservation and affected seam. Unreviewed criteria remain
explicitly outside this check's coverage; do not mark them MEETS or N/A merely
because they were not reviewed. A Section draft needs paragraph and aggregate
coverage. Formal Page CHECK reviews every required Page unit.

Hard content findings are never averaged away by style: changed causal
strength, missing citations/numbers, unsupported factual additions and edits
outside scope require repair or an upstream decision. Token comparison can
find lost values/keys; it cannot establish semantic equivalence or truth.

Readability findings should explain how a reader gets lost. Long sentences,
passive voice, technical terms or repeated words can be appropriate. Statistics
and pattern hits suggest spans to inspect; no word blacklist, numeric-density
floor, AI-origin verdict, detector score or undetectability promise establishes
acceptance. For a batch of related sections, also check whether noun swaps
leave interchangeable boilerplate instead of each section's own argument.

Each row records criterion id/source, target/quote, verdict, evidence/reason,
smallest fix and owner. Report unresolved conflicts and coverage separately.
Self-review readiness, independent review and the person's acceptance are
distinct records. No evaluation alone changes the Run's human gate.

## Scores, 0 to 10, a reading aid

A review may give each row a score out of 10 beside its verdict, so a person sees at a glance where a draft is weakest
(JL 261021: "我觉得还是用十分制吧"). The verdict still decides; the score never turns NEEDS WORK into a pass, and the
mean of the rows is shown as a reading aid, never as a pass mark.

| Score | When |
|---|---|
| 9-10 | MEETS, nothing to change |
| 7-8 | MEETS, or NEEDS WORK on one or two local spans |
| 5-6 | NEEDS WORK across several sentences, or one join that breaks the argument |
| 3-4 | NEEDS WORK in the paragraph plan, or a claim its source does not hold |
| 0-2 | the criterion fails throughout |

NOT VERIFIABLE scores at most 4: what cannot be checked is not yet good. N/A has no score.

## The Revise review overlay

A draft Task's Revise review report (haipipe-draft-writing `ref/revise.md`) adds two rows to the four axes, each with
the same verdicts, score, evidence and smallest fix (JL 261021: "句子连贯性、反 AI 写法 ... 你有没有拿那个来测试"):

- **Coherence**: each join from one sentence to the next. A join carries when the second sentence's subject or first
  words connect to what the first said; it breaks when a pronoun or "the same" points further back than one sentence,
  a turn word ("However") turns from nothing, or a new topic arrives without a link. Report the count of joins that
  carry and name each one that breaks. The row sums up the per-sentence lines of `ref/sentence-logic.md`
  (a logic and a read score for each sentence, its link and its specific problem), which a Revise review
  report lists under `Sentences:`.
- **Anti-AI writing**: run `cli/anti_slop.py audit` on the text (its score out of 100, its findings), then read the
  text against `ref/ai-tells.md`. Name each cluster of tells; a finding inside a placeholder mark (⟦…⟧) is not prose.
  When the reviewer also proposes text, audit that text too and say how it scores against the draft.

## Specialized overlays

Host workflows may add sourced criterion rows without changing this base
rubric. The Paper submission-readiness overlay is the canonical example:
`2_theme/paper/haipipe-paper/ref/submission-readiness.md` defines the `SUB-*` rows for
the final Introduction, Methods, Results, Discussion, cover-letter and
whole-manuscript checks. Those rows still use these four axes and four verdicts;
they are recorded with the same target, evidence, smallest-fix and owner
fields. An overlay is not a replacement for Page CHECK, or a venue rule unless the current venue contract
says so; its score, when given, is the reading aid above.
