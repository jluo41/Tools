# Rebuttal craft (round stage data; loaded via round/stage.md `craft:`)

The reviewer-response craft for a round that answers external readers: parse reviews,
enforce coverage and grounding, draft a safe text-only reply under venue limits, manage
follow-up exchanges. Venue-agnostic; tuned for text-only rebuttals with strict character
limits, multiple reviewers, and follow-up rounds.

What this craft never does: run new experiments automatically, generate new theorem claims,
edit or upload a revised PDF, or submit to OpenReview / CMT / HotCRP. If the user already
has new results, derivations, or approved commitments, incorporate them as
**user-confirmed evidence**.

Required inputs (stop and ask when missing)
--------------------------------------------

1. **Paper source**: PDF, LaTeX directory, or the Board's section pages
2. **Raw reviews**: pasted text, markdown, or PDF with reviewer ids; landed VERBATIM at the
   round page's Source and intake (or a letter file beside it)
3. **Venue rules**: venue name, character/word limit, text-only or revised PDF allowed
4. **Current stage**: initial rebuttal or follow-up round

If venue rules or the limit are missing, **stop and ask** before drafting.

The three hard gates
---------------------

If any fails, do NOT finalize:

```text
1. PROVENANCE   every factual statement maps to: paper | review | user_confirmed_result |
                user_confirmed_derivation | future_work. No source = blocked.
2. COMMITMENT   every promise maps to: already_done | approved_for_rebuttal |
                future_work_only. Not approved = blocked.
3. COVERAGE     every reviewer concern ends in: answered | deferred_intentionally |
                needs_user_input. No issue disappears.
```

The round page's coverage ledger IS the coverage gate's artifact: one row per atomic
concern, and the response must anchor every row.

Atomize and classify (feeds the round's DRAFT/ledger)
------------------------------------------------------

For each atomic concern, the ledger row carries:

```text
issue_id          R1-C2 grammar: reviewer + concern number
raw_anchor        short verbatim quote
issue_type        assumptions | theorem_rigor | novelty | empirical_support |
                  baseline_comparison | complexity | practical_significance |
                  clarity | reproducibility | other
severity          critical | major | minor
reviewer_stance   positive | swing | negative | unknown
response_mode     direct_clarification | grounded_evidence | nearest_work_delta |
                  assumption_hierarchy | narrow_concession | future_work_boundary
status            open | answered | deferred | needs_user_input
```

Strategy before drafting
-------------------------

1. Identify 2-4 **global themes** resolving shared concerns; they open the reply.
2. Choose a **response mode** per issue.
3. Build a **character budget**: 10-15% opener, 75-80% per-reviewer, 5-10% closing.
4. Identify **blocked claims** (ungrounded or unapproved); pause and present them to the
   user before drafting around them.

A quick pass may stop here: present the ledger + strategy (how many issues per reviewer,
shared vs unique concerns, priorities, evidence gaps) and let the user decide whether to
continue to a full draft or write manually.

Evidence gaps go through PROBE, never inline
---------------------------------------------

An issue tagged `grounded_evidence` with no existing evidence is a question ENTRY in the
round's PROBE phase. MATCH runs first: a reviewer-demanded experiment is often already
answered by an existing task's QA file. Only what MATCH cannot close is a spend decision,
and the ceiling (`probe_depth`, raised per invocation by a human) governs it. If an
experiment fails or is inconclusive: switch the mode to `narrow_concession` or
`future_work_boundary`. Do NOT fabricate positive results. If the estimated compute exceeds
the deadline, skip and flag for manual handling.

Drafting the reply
-------------------

Structure:

1. **Short opener**: thank reviewers + the 2-4 global resolutions
2. **Per-reviewer numbered responses**: answer, then evidence, then implication
3. **Short closing**: resolved / remaining / the acceptance case, addressed to the
   meta-reviewer

Default reply pattern per issue: sentence 1 the direct answer; sentences 2-4 grounded
evidence; last sentence the implication for the paper.

Heuristics (from successful rebuttals):

- Evidence > assertion; concrete numbers for counter-intuitive points
- Global narrative first, per-reviewer detail second
- Name the closest prior work + the exact delta for novelty disputes
- Concede narrowly when the reviewer is right; narrow honest concessions beat broad denials
- For theory: separate core assumptions from technical ones
- Answer friendly reviewers too; reinforce supportive framing
- Don't waste space on unwinnable arguments: answer once, move on

Hard rules:

- NEVER invent experiments, numbers, derivations, citations, or links
- NEVER promise what the user hasn't approved
- If no strong evidence exists, say less, not more
- Any reference added must be verified against a real source before it ships; an unverified
  one carries `[VERIFY]` and blocks finalize

The revision checklist (the commitment gate's artifact)
--------------------------------------------------------

Every paper edit promised (explicitly or implicitly) in the reply becomes ONE atomic
checklist item on the round page (under Applied changes / the ledger), each referencing its
issue_id, its commitment class, and its status. Two-way rule: a promise in the draft with no
item is a commitment-gate violation; an item backed by no promise or evidence is removed.
Keep an out-of-scope log: concerns that will NOT trigger a revision, one-line reason each.
On follow-up rounds, update status in place rather than regenerating.

Safety lints before finalize
-----------------------------

1. **Coverage**: every issue maps to a draft anchor
2. **Provenance**: every factual sentence has a source
3. **Commitment**: promises are approved AND mirrored in the checklist (both directions)
4. **Tone**: flag aggressive, submissive, or evasive phrases
5. **Consistency**: no contradictions across reviewer replies
6. **Limit**: exact character count; compress if over (order: redundancy, friendly padding,
   opener, wording; never drop critical answers)

An independent stress test is worth one pass: hand the raw reviews + ledger + draft + venue
rules to a fresh reviewer agent and ask for unanswered concerns, unsupported statements,
risky promises, tone problems, and the paragraph most likely to backfire with the
meta-reviewer. Grounded fixes only; a hard safety blocker means revise before finalizing.

Finalize: two versions
-----------------------

1. **Paste-ready plain text**: exact character count, fits the venue limit, no markdown,
   ready for OpenReview / CMT / HotCRP. Report the count beside the limit.
2. **Rich draft**: same structure with fuller explanations and optional paragraphs marked
   `[OPTIONAL: cut if over limit]`; the author reads this to understand the reasoning and
   decides what to keep. The extra material is pre-written fuel for follow-up rounds.

Both live in the round page's Response division (or files beside the page when long);
refresh the checklist so it matches the final draft.

Follow-up rounds
-----------------

When new reviewer comments arrive: append them verbatim (new intake on the SAME round page
while the exchange is one batch, or a new round page when the venue opens a new cycle); link
to existing ledger items or create new ones; draft a **delta reply only**, not a full
rewrite; update the checklist in place; re-run the lints. Escalate technically, not
rhetorically; concede if the reviewer is correct; stop arguing when the reviewer is
immovable and no new evidence exists.
