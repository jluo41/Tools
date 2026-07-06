---
date: 2026-06-23
status: fixed
fixed_in: "4.3.0"
source: process audit of P.0623a/b/c
scope: haipipe-probe-orchestrator-agent + agent triad
---

# Orchestrator agent collapses to monolithic execution

When haipipe-probe-orchestrator-agent is dispatched, it does ALL the work
itself instead of dispatching haipipe-probe-creator-agent and
haipipe-probe-reviewer-agent. The triad architecture is bypassed.

Observed on P.0623a, P.0623b, P.0623c:
- Orchestrator wrote Python scripts directly (should dispatch task-creator)
- No CODE_REVIEW.md or RUN_AUDIT.md (task-reviewer never ran)
- No creator/reviewer loop at any stage (Plan, Gather, Read)
- Single-agent session from start to finish (2-min timestamp window)
- "builder != judge" principle violated

Root causes:
1. The orchestrator definition says "dispatch creator + reviewer" but nothing
   PREVENTS it from just doing the work. No hard enforcement.
2. The caller prompt was too prescriptive (gave script logic), which let
   the orchestrator skip sub-agent dispatch and code directly.
3. Dispatching sub-agents is slower and harder than just doing the work,
   so the agent path-of-least-resistance is monolithic.

Fix ideas (to evaluate later):
- Add a hard rule: "You MUST NOT write Python code or run scripts directly.
  If you find yourself writing code, STOP and dispatch task-orchestrator."
- Make the orchestrator's tool list exclude Write/Edit (force delegation)
- Add a post-hoc check: if no sub-agent was dispatched, flag as process violation
- The caller prompt should say "dispatch agents" not "do this work"
