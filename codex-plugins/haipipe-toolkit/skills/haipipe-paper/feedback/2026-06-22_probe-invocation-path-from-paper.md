---
status: fixed
created: 2026-06-22
context: Paper-SMSforSubgroup-IS prospectus; 6 open evidence needs in 0-seed all route to probe/task/discover but no clear invocation path from the paper session
fixed_in: "SKILL.md v1.4.0 (2026-06-22)"
---
User asks: "I want to know in the skills what is the tool to call the probe? or should we give /haipipe-paper a probe command and it can work on the probes folder in this project folder?"

Two questions embedded:

1. DISCOVERABILITY: When the paper seed lists "NEED-1 (probe): ..." and "NEED-2 (task): ...", how does the user actually trigger those? The current routing hints in the orchestrator SKILL.md say "claim needs a verdict -> /haipipe-probe plan from-need <need>", but there is no `/haipipe-paper probe` verb in the routing table. The user has to leave the paper session and invoke /haipipe-probe directly. Is that the right UX, or should the paper orchestrator accept `probe` as a positional verb and dispatch?

2. FOLDER STRUCTURE: Should probes live inside the paper folder (e.g., `<paper>/probes/`) or at the project level (e.g., `examples/<Project>/probes/`)? Currently the delivery-need reference says evidence lives outside the paper ("Project-level evidence lives outside the paper in probes, discoveries, tasks, and insights"), but for a submodule paper repo, the project-level probes folder is in a different git repo. This creates a friction: the paper seed names a need, but the probe lives elsewhere.

Design options to evaluate:
A. Paper orchestrator gains a `probe` verb that dispatches to /haipipe-probe with the paper's project context pre-loaded. Paper stays a story layer; probe does the work; the verb is just a convenience shortcut.
B. Paper folder gets a `probes/` subfolder for paper-scoped probes (lightweight; keeps evidence close to the paper). Project-level probes remain separate for cross-paper evidence.
C. Status quo: user manually invokes /haipipe-probe. Paper only records needs and backfills verdicts.

Related: 2026-06-22_paper-evidence-gap-route-to-probe.md (covers the layer boundary: paper should NOT do evidence work, only trigger it).

Fix: Implemented Option A. Added `probe`, `discover`, and `task` as first-class verbs in the paper orchestrator (SKILL.md v1.4.0). The paper resolves the project root from the paper path (walk up from paper/ to examples/<Project>/) and dispatches to the evidence worker with project context. Probes stay at the project level; the paper verb is a convenience dispatcher. Updated keyword map, positional aliases, routing logic Step 2 + Step 4, no-arg dashboard, and the Composing diagram.
