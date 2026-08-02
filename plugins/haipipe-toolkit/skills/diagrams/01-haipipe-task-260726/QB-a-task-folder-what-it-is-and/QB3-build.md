# BUILD: what Gate 1 catches that a test cannot
state: 🔴 OPEN
owner: JL
method: review code that has never run, against the intent it was supposed to implement

## Opening
What is a pre-run code review for, when the code has not run and no test has been written? Gate 1 sits between BUILD and EXECUTE and produces `CODE_REVIEW.md`. Its whole value rests on catching something that running the code would not reveal, and if it cannot name that class of defect it is a delay rather than a gate.

It can, and the family already names it: an intent-versus-implementation mismatch. Code that runs cleanly, produces plausible numbers, and measures something other than what the author meant. No test catches that, because a test encodes the same misunderstanding; the run does not catch it, because there is nothing to crash; and the author does not catch it, because they wrote both halves.

That is why the author convention exists: every task script must carry an `Intent` section in its docstring. Gate 1 is the comparison between that paragraph and the code beneath it, and it is the only place in the lifecycle where those two are read against each other by something that did not write either.

**Covered elsewhere**: Why the reviewer is a separate agent is `QB6`; the post-run audit is `QB5`; the four sister files this phase creates are `QC1`; who presses the run button is `QB4`.

## Diagram
```
   BUILD                     creates  <NN>_<task>.py · configs/<run>.yaml
                                       runs/<run>.sh · notebooks/
                                       CODE_REVIEW.md            ← GATE 1

    creator writes ────▶ reviewer reads ────▶ CODE_REVIEW.md ────▶ ↺
                                                    │
                                          then a HUMAN: bash runs/<run>.sh

   ── the ONE defect class this gate exists for ──────────────
      INTENT vs IMPLEMENTATION.
        the code runs. the numbers look fine. it measures
        something the author did not mean.

      no TEST finds it     a test encodes the same misunderstanding
      no RUN finds it      nothing crashes
      the AUTHOR misses it they wrote both halves

      so the gate reads the docstring `Intent` paragraph against
      the code beneath it, with fresh eyes that wrote neither.

   ── which is why the Intent docstring is MANDATORY ─────────
      ref/intent-docstring-template.py
      no Intent section = nothing to compare against = the gate
      degrades into a style review.

   ── the two skip mechanisms, and what they cost ────────────
      _meta.skip_review: true        in the config
      HAIPIPE_SKIP_REVIEW=1          in the environment

      both are legitimate and both are invisible afterwards:
      nothing records that a run skipped its gate. A result whose
      gate was skipped reads identically to one that passed. → Items
```

## Content
### The gate's value is exactly one defect class
Stating it narrowly is what keeps the gate cheap. It is not a style review, not a performance
review, and not a second opinion on the experiment. It is one comparison: does this code do what
its `Intent` says it does.

Everything else a reviewer might say at this point is either caught later for free, by the code
failing to run, or is the researcher's call and not the reviewer's.

### The skip is silent, and that is the real gap
Both skip mechanisms exist for good reasons: a trivial rerun does not need a review, and an
automated sweep cannot wait for one. What neither does is leave a trace. After the fact, a
`results/<run>/` produced with the gate skipped is indistinguishable from one produced with the
gate passed, so the strongest thing anyone can say about a number is that it probably had a
review.

A one-line record in `runtime.yaml` would close that, and it is the smallest possible change:
the snapshot is already written by the run script.

### File ownership
BUILD touches only code, configs and runs. It does not write `results/`, which belongs to EXECUTE,
and it does not touch `workflow/plan*.yaml`, which is the contract it is being judged against.

## Aims
- [ ] 📝 Record when the gate was skipped
      One key in `runtime.yaml`. Today a skipped gate and a passed gate leave identical evidence, so nothing downstream can weigh a number by whether it was reviewed.
- [ ] 🎯 State the gate's single defect class in the reviewer's contract
      Intent versus implementation. Written in `SKILL.md`'s prose and not in the reviewer agent's own instructions, which is where it would actually bind.
- [ ] 📏 Rule what happens when there is no `Intent` docstring
      The convention says MUST. If the gate proceeds anyway it silently becomes a style review, and if it blocks, every legacy script fails. Neither is written.

## States
The gate runs and produces `CODE_REVIEW.md`. Its purpose is stated in `SKILL.md` prose. Nothing is
ruled here, and the skip is unrecorded.

- 260726 CC · 🎯 Named the defect class as the gate's whole justification
      Taken from `SKILL.md`'s own description of what the reviewer catches. Written down here because a gate that cannot name what it uniquely catches gets skipped by default within a month.

## Files
- `ref/intent-docstring-template.py`
  The `Intent` section the gate reads against.
- `ref/run-sh-template.sh`
  The pre-flight gate, and the `runtime.yaml` snapshot where a skip record would live.
- `agents/haipipe-task-reviewer-agent.md`
  The reviewer's own contract, which does not yet name the defect class.

## Log
260726 · Created with the board.
