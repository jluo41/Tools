---
date: 2026-06-23
status: open
source: process audit of P.0623b/c
scope: fn/gather.md + agent triad
---

# Gather needs a "link+extract" lightweight variant

The current Gather procedure has two modes: "call" (create new task/discovery)
and "link" (attach existing artifact). But P.0623b and P.0623c needed a THIRD
mode: extract a subset from an existing result (e.g., filter per_arm_interaction.csv
for gender concordance rows, or rank physician dimensions on a specific arm).

This is heavier than "link" (needs a script) but lighter than "call task"
(doesn't need Plan/Build/Execute/Report). The orchestrator collapsed to
monolithic because the extraction was too small to justify a full task lifecycle
but too complex for a plain link.

Proposed: a "link+extract" Gather action:
- Creator writes a small extraction script (no config, no IPO contract)
- Reviewer spot-checks the output (abbreviated Gate 2, no full RUN_AUDIT)
- Results land alongside the source data (not in a separate task folder)
- Sanctioned lightweight path that still gets reviewer eyes

This avoids the false choice between "full task lifecycle for 30-line script"
and "monolithic orchestrator does everything."
