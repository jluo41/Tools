---
name: field-test
description: >-
  Validate a shipped skill family on a real task from a separate context.
  Freeze expectations before execution, collect a friction log and receipts,
  and compare behavior with the skill's own gates. Use for field tests,
  skill conformance checks, or proof that a revised skill works in a new context.
metadata:
  version: "0.4.2"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /field-test · run the real task, against a written expectation

A skill is a claim about how work will go. A field test checks the claim the only way it can be checked: give the skills to a desk that holds nothing but the shipped files, hand it a REAL task, and compare what actually happens with what the designer wrote down IN ADVANCE that should happen. Both sides can lose: a divergence may mean the law is wrong, or that the designer's model of the work was — and the second kind is learning too, which is why the expectation is written before the run and never after.

Born 260827 from the insight-family validation: one field run on a live board returned 14 frictions, including a gate no contract made testable — a gap three design passes had not seen. Generalizes the board family's fresh-agent-run (QF2) from "does the route work once" to a convergence loop.

## The three desks

```text
🛠 DESIGN desk   authors/patches the skills · writes the commission AND the
                expectation ledger BEFORE the run · joins the two halves after ·
                grows the teeth. NEVER executes its own commission.
🏃 FIELD desk    a SEPARATE context — what matters is that the design conversation
                is not in it, so the shipped files are its only instruction.
                Two forms: a second human-driven session (the manual form), or a
                SPAWNED SUBAGENT, cold by construction (the automated form) —
                the commission is its prompt, the report is its return, and the
                human message-bus disappears. Either form loads the skills by
                name, works the real target, and keeps the friction log as it
                goes. It is never shown the expectation ledger: an executor who
                knows the prediction performs the prediction.
📡 MONITOR       runs on the design desk, READ-ONLY: polls the field desk's
                transcript (reply sections, friction rows) and the target's git
                status (which files appear, which pen wrote). It reports drift
                to the human and never messages the field desk mid-run. The
                human is the only channel between desks, by copy-paste — a
                feature: every instruction the field desk received is on its
                transcript.
```

## The commission packet · what the field desk receives

One pasteable block. Its anatomy, each part load-bearing:

```text
① LOAD lines        name the exact skills under test, by slash name
② REAL target       a live artifact with history and debt — never a toy fixture;
                    divergences live in the debt (stale headers, backlog cells,
                    legacy names), and a clean fixture has none
③ ORDERED steps     each step exercises ONE named law or gate; a step that tests
                    nothing is ballast · use the TARGET FAMILY'S own vocabulary —
                    round 3's commission said `proposed` where the probe ladder
                    says `planned`, and the field desk had to correct the designer
④ GATES pinned      mode: copilot · the human releases and signs · present, then wait
⑤ SCOPE fences      what NOT to touch, WITH the reason (cascade, ownership,
                    mid-test freeze) — a fence without a reason reads as arbitrary
                    and gets reported as friction instead of respected
⑥ THE deliverable   "keep a numbered FRICTION LOG: every place a skill was unclear,
                    wrong, self-contradictory, or missing a rule you needed. That
                    log matters more than the work." Say this sentence; without it
                    the field desk optimizes for the work and swallows the friction
⑦ STOP line        report after the last step; no self-directed continuation
⑧ THE clock        every friction-log stamp comes from the `date` command, never
                    estimated (a 260828 run caught itself fabricating stamps and
                    confessed in its own log); the log's header records start,
                    its Close block records end — the scorecard reads both
```

## The expectation ledger · what the design desk writes, before

One row per commission step, written before the run and frozen with the baseline:

```text
step · law exercised · EXPECTED behavior            · EXPECTED artifacts
  3    lap ①-⑥        one lap per cell, present      12 mirror pages, slugs
                      each settle, flip nothing        mirroring F, CHECK-closed
```

After the run, record two independent judgments for each row: whether the
observed behavior met the frozen expectation, and what caused any difference.
The first axis is `met`, `not_met`, or `not_verifiable`; the second is
`skill_gap`, `executor_nonconformance`, `expectation_error`, `infrastructure`,
`mixed`, or `unresolved`. Keep the transcript/disk evidence pointer with both.
Do not infer a skill defect from a failed expectation alone.

Examples of the independent axes:

```text
met + expectation_error       the law allowed batching; the desk expected one per lap
not_met + skill_gap           a clear instruction conflicts with the required artifact
not_met + executor_nonconformance  the shipped instruction was clear but not followed
not_verifiable + unresolved   available receipts cannot determine what happened
not_met + mixed               evidence supports more than one contributing cause
```

Assign friction severity on its own consequence scale. `blocking` means the
uncertainty or defect prevents a trustworthy run/decision and must be resolved
before dependent work; `material` means it could change a result or gate and
must be resolved by the responsible owner before close; `local` means it affects
clarity or maintenance without changing the current result. This scale is
specific to field-test triage and is not comparable to another owner's labels.

## The scorecard · what every run costs and what it bought

Recorded at settle, one block on the settlement file, all of it read off receipts and stamps — never reconstructed from memory:

```text
⏱ time       field-desk start→end from the log's date stamps · design-desk
              overhead (commission + ledger + settle) counted separately ·
              serialized judge time named, since it usually drives wall clock
🎫 tokens     field session: the operator runs /cost at close and pastes it
              into the log's Close block (a session cannot read its own meter) ·
              every dispatched judge or subagent: exact usage from its task
              receipt · a number without a receipt is labeled estimate
📐 format     mechanical quality: checker findings before → after · independent
              CHECK rounds to CLOSE (1 = first-pass clean) · reworks the
              producer's own misses forced
🧠 semantic   expectation tally (n met · n not_met · n not_verifiable) plus
              attribution tally (skill gap · executor nonconformance ·
              expectation error · infrastructure · mixed · unresolved) ·
              frictions by severity · the independent CHECK's cold-read verdict
              — never the designer's opinion (law 3)
💸 tax line   every avoidable spend named with its lesson: a judge dispatched
              against a version whose own state line still registered a debt ·
              a rework a skipped exit-sweep forced · a re-run a dead executor
              forced. The tax line is where the next law patch comes from.
📏 rate       units ÷ time and units ÷ tokens, with the UNIT and the GRADE
              named — repair-grade and close-grade are different products and
              never share a rate row
```

Calibration from the two 260828 runs, so a new scorecard has something to stand beside: repair-grade ran 13 pages in 14 minutes with 12 frictions (the page-family run); close-grade ran 1 page in 30 minutes with 213k tokens across three serialized judges, of which ~128k (~27%) settled as tax — one judge bought against a known-dirty version, one rework a skipped exit-sweep forced.

## Laws

1. **Expectation before run.** A prediction written after seeing the outcome is not a prediction — the same rule the design card enforces on design bets. The ledger freezes with the baseline.
2. **Freeze the baseline.** No edits to the skills under test while a run is live: the field desk resolves files at read time, and a mid-run edit makes every finding ambiguous between "the skill was wrong" and "the skill changed."
3. **The designer never grades.** Behavioral verdicts come off the transcript and the disk, mechanically; content verdicts belong to the run's own CHECK machinery and the human, not to the desk that wrote the law.
4. **Friction is four-valued.** Unclear, wrong, self-contradictory, missing — an entry needs a file and the sentence (or absence) that caused it. "It felt awkward" is not an entry; "no skill names the field a signature goes in" is.
5. **Behavior pass ≠ done.** A run can hold every gate and still expose that a gate is untestable as written. The joined ledger outranks the green run.
6. **Triage after evidence.** First settle expectation status; then classify
   attribution. Infrastructure failures may be repaired and rerun. A false
   positive is closed only with its stale or incorrect evidence identified. A
   skill gap goes to the skill owner; executor nonconformance goes to the
   execution path; an expectation error updates the design desk's model; mixed
   and unresolved cases retain their evidence and named resolver. Add a
   checker only for a mechanically decidable rule, and prove it rejects an
   artifact broken in that exact way before relying on it.
7. **Loop until dry, on fresh slices.** Patch, re-commission a DIFFERENT slice of real work, run again. Converged when a fresh run settles every expectation row `met`, has no unresolved attribution, and returns zero new frictions; a run that only re-finds known ones means the patches did not land.
8. **The monitor never intervenes.** Drift is reported to the human, who may stop the field desk in its own session. An agent whispering corrections mid-run contaminates the test.
9. **Metrics are recorded, never recalled.** Time from `date` stamps, tokens from task receipts and a pasted `/cost`, quality from the checker, the ledger and the independent CHECK. A scorecard rebuilt from memory after the fact is the same defect as an expectation written after the run.

## The automated loop · bounded authorization

Use the target family's current authorization contract. For Insight, read
[`../../insight/haipipe-insight-workflow/ref/authorization.md`](../../insight/haipipe-insight-workflow/ref/authorization.md).
It permits only explicitly granted mechanical register operations. Record an
existing instruction as its source; do not ask the person to repeat approval
already given for the same scope.

Before dispatch, record the exact person, source, board/runtime, targets,
permitted actions, and expiry. Empty `run_ids` do not authorize Run execution.
During execution each covered action records the grant and licensing evidence;
the ordinary owner and gate still apply. A missing, expired, revoked, or
out-of-scope grant cannot authorize the action. Handoff signatures and release
of new computation remain person-reserved; automation does not batch them away.

The design desk may dispatch a FIELD subagent with the commission and shipped
skills, but not the expectation ledger or design discussion. The monitor stays
read-only and does not coach it. After execution, join the ledger with the
friction log and receipts. Requests outside the existing grant go to the
normal gate; run-close review does not retroactively authorize them.

For another family, use its own available authorization rules. Do not copy
Insight's register schema into an unrelated project. Keep the baseline frozen,
expectations written beforehand, independent judgment, and receipt-backed
metrics in both manual and automated forms.

## What this method is not

Not a unit test (the checker owns mechanical assertions), not a review (CHECK owns content judgment), not pair programming (the desks never converse), not a dry run (the task is real and its outputs are kept). It tests exactly one thing nothing else tests: **whether the skill as written produces the run as expected in a stranger's hands** — and its unit of progress is one settled divergence.
