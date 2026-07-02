---
status: open
created: 2026-06-23
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
---
"display is so [off], it should make the plan about how to create the figures,
and then think about what is the probe and task to generate this plots, but
currently it just doesn't work as expected. Please think about it."

What went wrong: at the display stage I hand-plotted a figure with ad-hoc
matplotlib INSIDE the paper folder (0-display/Figure/Figure-DiscretionGradient.py).
That is the wrong layer. The paper layer does not generate artifacts; it PLANS the
display set and ROUTES generation to a probe (claim settled?) + task (render the
artifact, with configs/runs/results, PHI-aware on the server). Figures are
materialized outputs OWNED BY DISPLAY TASKS (e.g. Z01_Display_PhyTraitOpioid), then
backfilled into the paper's 0-display.

Correct display flow (what the skill should enforce):
  1. PLAN the display set (4-display.tex): each display = what it shows, which
     claim, what FORM (figure/table/diagram), what data it needs.
  2. For each display, route:
       - claim/data already settled by a probe?  -> LINK it (no new probe)
       - data exists but no rendered plot?        -> TASK (haipipe-task-for-display / Z01)
       - underlying claim not settled?            -> PROBE (which calls task to compute)
       - concept figure (no data)?                -> display-diagram/illustration task
  3. DISPATCH the task/probe to GENERATE the plot in the TASK folder.
  4. BACKFILL the rendered artifact into 0-display + the display map.
  5. The paper layer NEVER ad-hoc plots.

FIX (proposed): haipipe-paper-display Step 0/1 must produce the figure PLAN +
the per-display probe/task routing table FIRST, and only dispatch generation to
tasks; forbid in-paper ad-hoc plotting. The ad-hoc Figure-DiscretionGradient.py
should be promoted to a Z01 cross-cohort display task.

Fix:
