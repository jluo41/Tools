---
date: 2026-06-23
status: open
source: P.0623f dispatch failure
scope: haipipe-probe-orchestrator-agent nested dispatch
---

# Nested agent dispatch hangs (orchestrator → task-orchestrator → task-creator)

When probe-orchestrator-agent tried to dispatch task-orchestrator-agent
(which would then dispatch task-creator-agent), the chain hung. The
orchestrator spent its entire runtime deliberating on folder naming
and never actually dispatched.

The 3-level nesting (probe-orch → task-orch → task-creator) appears
to be too deep for reliable execution. The orchestrator agent gets
stuck on planning/deliberation before the first dispatch.

Workaround used: dispatch task-creator-agent directly from the main
conversation, bypassing both orchestrators. Same agents, flat dispatch.

Fix ideas:
- Probe-orchestrator should dispatch task-creator DIRECTLY (skip task-orch)
  for simple "build one script" jobs. Task-orchestrator is for multi-stage
  task lifecycles, not single-script creation.
- Or: flatten to 2 levels max (main → orchestrator → worker). Never
  orchestrator → orchestrator → worker.
- Document the nesting depth limit in agent definitions.
