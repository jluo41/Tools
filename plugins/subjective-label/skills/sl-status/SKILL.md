---
name: sl-status
description: "Show current state of a subjective-label project: iteration count, gallery size, panel-internal κ, public-dataset κ trajectory, disagreement category breakdown, suggested next step. Read-only. Use when the researcher says /sl-status or wants to check progress."
---

Skill: sl-status
================

Read-only status dashboard.

Protocol
--------

Step 1. Resolve project_dir (from arg or cwd).

Step 2. Read:
  - {project_dir}/.state.json
  - {project_dir}/gallery/gallery.json
  - {project_dir}/gallery/guideline.md (first 30 lines for preview)
  - {project_dir}/validation/trajectory.jsonl (if exists)
  - {project_dir}/gallery/history/*.diff (last 3 for preview)

Step 3. Print status block:

  ============================================================
  Project:    {project_dir}
  Topic:      {config.topic}
  Labels:     {config.label_values}
  Iteration:  {state.iteration}
  Status:     {state.status}  (initialized / iterating / converged / scaled)
  ------------------------------------------------------------
  Gallery:    {N} entries across {K} label values
  Guideline:  {M} rules, last updated iter {state.last_guideline_update}
  ------------------------------------------------------------
  Panel κ (latest iter): {value}
  Public-κ trajectory (last 5 iters):
    iter 1  GoEmotions  κ=0.31
    iter 2  GoEmotions  κ=0.42
    iter 3  GoEmotions  κ=0.48  ← ceiling 0.46, CONVERGED
  ------------------------------------------------------------
  Disagreement profile (latest iter):
    A boundary:  12 cases
    B ambiguity: 3 cases
    C novel:     1 case
    D noise:     8 cases
  ------------------------------------------------------------
  Next step:
    {contextual recommendation based on state}
  ============================================================
