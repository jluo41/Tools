---
date: 2026-06-23
status: open
source: user feedback during claims stage walkthrough
severity: design
affects: haipipe-paper orchestrator, all lifecycle stage skills, claims skill
---

Probe plans should be created automatically during lifecycle work
==================================================================

Problem
-------

When working through lifecycle stages (seed, pitch, claims), evidence gaps
surface naturally — e.g. "we need to check persistently low engagement
subgroups" or "robustness checks are missing." Currently the user must
explicitly call `/haipipe-paper probe "<need>"` to buffer these. The user
expected the skill to do this automatically.

Desired behavior
-----------------

1. Every lifecycle stage skill should detect evidence needs as they arise
   (GAP/weak claims, \needprobe{} macros, open evidence needs in seed,
   "still fragile" items in pitch) and AUTO-CREATE probe plan files in
   `1-probe-plans/` without requiring a separate `/haipipe-paper probe` call.

2. At the end of each stage's output, the skill should report any new probe
   plans it buffered: "Buffered PP03: <slug> (from <stage>)".

3. The user still controls DISPATCH — auto-buffer does not auto-run. The
   user calls `/haipipe-paper probe run` when ready.

4. The claims skill is the primary source: every GAP row and every
   \needprobe{} macro should generate a probe plan automatically when
   the claims ledger is written or updated.

Implementation sketch
----------------------

- In each lifecycle stage skill's workflow, after writing the .tex, scan for
  evidence needs (GAP status, \needprobe{} macros, open needs in seed,
  fragile items in pitch).
- For each need, check if a matching PP file already exists in 1-probe-plans/
  (match on claim text or source_ref to avoid duplicates).
- If not, create PPNN_<slug>.md with status: planned.
- Update 1-probe-plans/README.md index.
- Report the new probe plans in the stage's output.

Why it matters
--------------

The probe buffer is the right design (separates need-surfacing from
evidence-running), but requiring the user to manually buffer each need
defeats the purpose. The lifecycle stages ALREADY know what evidence is
missing — they should write the probe plans as a side effect of their
normal work.
