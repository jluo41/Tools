---
date: 2026-06-23
status: open
source: user
scope: orchestrator / probe routing
---

# Probe dispatch from paper skipped the 1-probe-plans/ buffer

When the user asked to create a probe for per-arm theory fit from within a paper
session, the orchestrator called /haipipe-probe directly instead of going through
the paper's probe buffer (1-probe-plans/).

The correct flow per the orchestrator's routing logic:
1. /haipipe-paper probe "<need>" → BUFFER mode: create PP file in 1-probe-plans/
2. /haipipe-paper probe run [PPNN] → DISPATCH mode: call /haipipe-probe and
   update the PP file status to dispatched + link the active probe ref

What actually happened:
- Skipped step 1 entirely
- Called /haipipe-probe plan directly
- Created the probe in probes/0623_per_arm_theory_fit/ but the paper's
  1-probe-plans/ folder has no record of it
- The paper console (enter/status) won't surface this probe as a dispatched need

The problem: the paper loses awareness of its own evidence pipeline. When
/haipipe-paper enter runs, it won't know that P.0623a was dispatched from
claims and needs backfill.

Fix: the orchestrator must ALWAYS buffer first (create the PP file), then
dispatch. The PP file is the paper's record of "I asked for this evidence."
Direct /haipipe-probe calls bypass the paper's awareness.
