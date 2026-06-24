---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: display stage, ProjB Paper-Personality-Opioid-MedJournal (JAMA); reviewing the display plan / worklist
fixed_in: ""
---
"I feel a lot of things in Display Unit Rule, and Current Display plan or things before Render Worklist they might not necessary to keep."

The display stage's plan artifact carries too much boilerplate. JL finds the
"Display Unit Rule", the "Current Display plan", and the scaffolding before the
"Render Worklist" largely unnecessary to keep around: it adds noise without
earning its place. The display plan should be trimmed to what actually drives the
figures/tables, not a heavy templated preamble.

How to apply (haipipe-paper-display revision): slim the display-plan / worklist
template. Drop or fold the "Display Unit Rule" + "Current Display plan" boilerplate
and keep only the per-unit Render Worklist that maps each display to a claim/beat
and its build route. Related: [[feedback_display_plan_then_route_to_task]].

Fix:
