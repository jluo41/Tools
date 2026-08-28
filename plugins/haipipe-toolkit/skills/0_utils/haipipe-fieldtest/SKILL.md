---
name: haipipe-fieldtest
description: >-
  The field-test method for a skill family: run a REAL task through the skills as shipped, against a PRE-REGISTERED expectation of how the run should go, and learn from every place actual and expected diverge. A 🛠 DESIGN desk authors the skills, writes the commission AND an expectation ledger (per step: which law is exercised, what should happen, what should land on disk); a 🏃 FIELD desk — a separate session holding the shipped files and none of the design conversation — executes the real work under the skills' own human gates, keeping a numbered FRICTION LOG; a 📡 monitor watches transcript and disk read-only. Afterward the desks' two halves are joined: each expectation row settles as MATCH, SKILL GAP (reality right, law unclear/wrong/missing), or EXPECTATION GAP (law fine, the designer's model was wrong — also learning). Gaps become law patches and checker teeth (each proven to FAIL first); loop with a fresh slice of real work until a run returns zero new gaps. Use when a new or reworked skill family needs proof it runs, or when deciding whether a skill set is good enough to trust. Trigger: fieldtest, field test, field run, expectation ledger, friction log, commission packet, expected vs actual, does the run match the skill, two desks, skill conformance, 实测, 试跑, 对表, /haipipe-fieldtest.
metadata:
  version: "0.2.1"
  last_updated: "2026-08-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-fieldtest · run the real task, against a written expectation

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
```

## The expectation ledger · what the design desk writes, before

One row per commission step, written before the run and frozen with the baseline:

```text
step · law exercised · EXPECTED behavior            · EXPECTED artifacts
  3    lap ①-⑥        one lap per cell, present      12 mirror pages, slugs
                      each settle, flip nothing        mirroring F, CHECK-closed
```

After the run, each row settles three ways:

```text
✅ MATCH             actual = expected · the law held and the model was right
🔧 SKILL GAP         reality was reasonable, the law was unclear, wrong,
                    contradictory or missing · joins the friction log · patch + tooth
💭 EXPECTATION GAP   the law is fine, the designer's model was wrong (batching
                    twelve mints was legal; the designer expected strict one-per-lap)
                    · corrects the designer, sometimes becomes an example in the law
```

## Laws

1. **Expectation before run.** A prediction written after seeing the outcome is not a prediction — the same rule the direction card enforces on design bets. The ledger freezes with the baseline.
2. **Freeze the baseline.** No edits to the skills under test while a run is live: the field desk resolves files at read time, and a mid-run edit makes every finding ambiguous between "the skill was wrong" and "the skill changed."
3. **The designer never grades.** Behavioral verdicts come off the transcript and the disk, mechanically; content verdicts belong to the run's own CHECK machinery and the human, not to the desk that wrote the law.
4. **Friction is four-valued.** Unclear, wrong, self-contradictory, missing — an entry needs a file and the sentence (or absence) that caused it. "It felt awkward" is not an entry; "no skill names the field a signature goes in" is.
5. **Behavior pass ≠ done.** A run can hold every gate and still expose that a gate is untestable as written. The joined ledger outranks the green run.
6. **Triage into exactly three bins.** ① infra, fix now; ② false positive, explain and drop (a stale read); ③ law gap, patch the law THEN grow a checker tooth for the mechanical ones — each tooth proven to FAIL on an artifact broken exactly that way before it is trusted.
7. **Loop until dry, on fresh slices.** Patch, re-commission a DIFFERENT slice of real work, run again. Converged when a run settles every expectation row MATCH and returns zero new frictions; a run that only re-finds known ones means the patches did not land.
8. **The monitor never intervenes.** Drift is reported to the human, who may stop the field desk in its own session. An agent whispering corrections mid-run contaminates the test.

## The automated loop · charter in, signatures out

Full automation does not remove the human gates; it BATCHES them to the run's two ends, under the family's auto-charter law (`haipipe-insight` §The auto charter):

```text
before the run   the person signs a CHARTER: which decision classes are
                 pre-authorized for this run (vocabulary re-marks under a ruled
                 grammar · 🟡-final flips whose licensing sentence the receipt
                 QUOTES · header re-derivations citing their Queue) — signatures
                 and new-computation releases are never charterable
during the run   the design desk spawns the field desk as a subagent; the
                 monitor's events become task notifications; charterable
                 decisions execute against the charter, quoting it in each
                 receipt; anything outside its classes stops at the gate
after the run    the person's two remaining acts: the batched signatures the
                 run queued, and the run-close review of the joined ledger
```

Quality is preserved by the same four guards the manual form uses, none of which the charter touches: the expectation ledger is still written before and joined after; refusal-is-convergence still legalizes 🚫; receipts still land on the pages; and every friction still becomes a law patch and, where mechanical, a checker tooth proven to FAIL first. The charter automates the PERSON'S ATTENTION, never the person's authority.

## What this method is not

Not a unit test (the checker owns mechanical assertions), not a review (CHECK owns content judgment), not pair programming (the desks never converse), not a dry run (the task is real and its outputs are kept). It tests exactly one thing nothing else tests: **whether the skill as written produces the run as expected in a stranger's hands** — and its unit of progress is one settled divergence.
