# REPORT: what makes a number trustworthy
state: 🔴 OPEN
owner: JL
method: mirror the plan's IPO shape with evidence, and let the audit compare rather than describe

## Opening
When a run has finished, what has to be true before its numbers may be used? REPORT writes `workflow/report.yaml` mirroring the plan, and `RUN_AUDIT.md` as Gate 2. The mirroring is the whole idea: the same IPO shape holds intent at one end and evidence at the other, so the comparison is mechanical instead of a reading.

What Gate 2 can catch is the opposite of Gate 1's, and the pair only works because they are opposite. Gate 1 reads code that has never run and cannot see numbers. Gate 2 reads numbers and cannot see whether the code that made them meant to. So Gate 2's unique job is the result-level mismatch: an output the plan promised and the run did not produce, a metric whose value is impossible, a file written somewhere the plan did not say.

The blocker is upstream. If a plan may declare `metrics.json` without naming its keys, then "did the run produce what the plan promised" is not a checkable question, and Gate 2 degrades into a reader saying the numbers look reasonable. That is `QB2`'s completeness ruling, and this phase cannot be made rigorous before it lands.

**Covered elsewhere**: The plan it mirrors is `QB2`; the pre-run gate is `QB3`; the digest that may be written at this phase is `QD1`; where outputs were allowed to land is `QC2`.

## Diagram
```
   REPORT          creates  workflow/report.yaml
                            report-script-<name>.yaml
                            RUN_AUDIT.md                      ← GATE 2
                   completes QA/<n>-<slug>.md, when one is due   → QD1

    creator drafts ────▶ reviewer checks accuracy ────▶ ↺

   ── the two gates are OPPOSITE, and that is the design ─────
                    Gate 1 (QB3)              Gate 2 (here)
      reads         code that never ran       numbers that exist
      cannot see    any number                whether the code MEANT it
      catches       intent vs implementation  promise vs production
      ────────────────────────────────────────────────────────
      neither can do the other's job. Two gates, not one twice.

   ── what Gate 2 uniquely catches ───────────────────────
      ✅ the plan promised an output the run did not produce
      ✅ a value that cannot be true (a rate above 1, an empty n)
      ✅ a file written where the plan did not say it would be
      ✅ a heavy artifact sitting in results/            → QC2

   ── the blocker, and it is upstream ────────────────────
      plan says:  output: results/<run>/metrics.json
      run made:   results/<run>/metrics.json
      audit says: ✅ ...and has verified nothing.

      the comparison is only mechanical if the plan named the KEYS.
      Until QB2 rules completeness, this gate reads rather than checks.

   ── the IPO mirror ─────────────────────────────────
      plan.yaml    INTENT     what will go in, happen, come out
      report.yaml  EVIDENCE   what did
      same shape at both ends, on purpose. workflow/ is the task's
      observability surface, and this is the half that is true.
```

## Content
### The mirror is the mechanism, not a formatting choice
Plan and Report share the IPO shape so that a diff between them is meaningful. If Report used a
different structure, checking it against the plan would require a reader to hold both in their
head and decide what corresponds to what, and that reader would be the same person who wrote both.

### This is where the digest may be written, and only sometimes
REPORT is the only phase allowed to complete a `QA/<n>-<slug>.md`, and only for one of three
reasons: a question arrived, results already answered a question that had no digest, or a finding
was judged worth digesting. A `QA/` mirroring every result is noise, which is why 1 of 107 folders
having one is not by itself a problem.

### File ownership
REPORT touches `workflow/report*.yaml`, `RUN_AUDIT.md`, and `QA/` when one is due. It does not
touch `results/`, which is EXECUTE's and is now evidence: a phase that could edit the numbers it is
auditing would make the audit worthless.

## Aims
- [ ] 🔓 Unblock the mechanical check
      Blocked on `QB2`. Until a plan must name its output keys, Gate 2 cannot verify that a promise was kept and can only observe that a file exists.
- [ ] 🚨 List the impossible-value checks worth running
      A rate above 1, an empty `n`, a metric identical across every arm of a sweep. Cheap, mechanical, and none of them are written down.
- [ ] 📦 Check the heavy-artifact rule at this gate
      `QC2` forbids a checkpoint in `results/`. Gate 2 is where a machine would notice, and it does not look.
- [ ] 📋 State the three reasons a digest is due
      They are in `SKILL.md` prose. In the reporter's own contract, where the decision is actually made, they are not.

## Discussion

### From the retired States section (merged 260831)
The phase runs and produces both artifacts. Its rigour is capped by `QB2`: with plans that name
files rather than fields, the audit compares existence rather than content.
- 260726 CC · 🧭 Named the two gates as opposites
      Gate 1 sees code without numbers, Gate 2 sees numbers without intent. Written down because the pair is easy to mistake for one review done twice, and the first thing that happens then is that one of them gets removed as redundant.

## Files
- `fn/stage-report.md`
  The phase contract: what it reads, what it writes.
- `fn/qa.md`
  The digest contract, for the case where one is due.
- `ref/metrics-json-schema.md`
  What a metrics file is expected to contain.

## Log
260726 · Created with the board.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0