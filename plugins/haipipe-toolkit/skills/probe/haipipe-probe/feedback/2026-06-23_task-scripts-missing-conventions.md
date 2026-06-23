---
date: 2026-06-23
status: fixed
fixed_in: "4.3.0"
source: process audit of P.0623a/b/c
scope: task conventions in probe-gathered scripts
---

# Task scripts created during probe Gather miss haipipe-task conventions

Scripts created by the probe orchestrator (theory_alignment.py,
permutation_test.py, comm_quality_mechanism.py, gender_concordance.py)
are functional but miss haipipe-task conventions:

- No Intent docstring at top of file
- No cell markers for cell-by-cell review
- Not config-driven (hardcoded dimension categories, arm lists)
- No workflow/plan.yaml
- No runs/ wrapper script
- theory_alignment.py embeds a 43-entry prediction dictionary as a code literal

These scripts were never reviewed by haipipe-task-reviewer-agent (Gate 1)
because the task lifecycle was bypassed (see orchestrator-collapses feedback).

Fix: when the orchestrator enforcement is fixed, these scripts will
naturally go through task-creator (which produces convention-compliant code)
and task-reviewer (which catches missing conventions). The scripts themselves
don't need retroactive fixing — the process fix will prevent recurrence.
