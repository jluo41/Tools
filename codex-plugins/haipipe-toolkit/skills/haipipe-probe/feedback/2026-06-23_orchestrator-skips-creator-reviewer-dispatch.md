---
status: open
created: 2026-06-23
context: PP01/PP02/PP05/PP06 dispatch from /haipipe-paper probe run (JAMANO session)
fixed_in: ""
---

When /haipipe-paper dispatched 4 probe-orchestrator agents in parallel (PP01 persistently low, PP02 robustness, PP05 drug class, PP06 clinical funnel), every orchestrator did ALL the work itself — writing Python analysis code, running it, writing evidence.md, AND self-assessing the verdict — instead of dispatching creator and reviewer agents in the designed triad loop.

The orchestrator agent definition (haipipe-probe-orchestrator-agent.md) clearly says:
- Step 2: dispatch haipipe-probe-creator-agent → dispatch haipipe-probe-reviewer-agent → loop if revise
- Step 3: dispatch haipipe-task-orchestrator-agent for task work
- Step 5: dispatch haipipe-probe-reviewer-agent for Judge G1/G2/G3

In practice, none of these sub-agent dispatches happened. The orchestrator acted as a monolithic agent.

Two contributing causes:

1. PROMPT OVERRIDE: the caller (/haipipe-paper) gave the orchestrator a comprehensive prompt ("build the script, run it, read results, judge") that told it WHAT to do rather than WHO to dispatch. The prompt made the orchestrator self-sufficient, so it never needed to call Agent().

2. NESTING DEPTH: the designed chain is 3-4 levels deep (me → probe-orch → probe-creator → task-orch → task-creator). Each Agent() call is a fresh context with no memory. At level 4, the task-creator needs the full chain of context (paper claim → probe hypothesis → task config → code) from its prompt alone. Context fidelity degrades with each hop.

Result: builder=judge violation in all 4 probes. The agent that wrote the analysis code also judged whether the results supported the claim. PP02 and PP05 at least wrote verdict.md with G1/G2/G3 sections; PP01 and PP06 only embedded verdicts in probe.yaml.

Fix candidates:
(a) Make the orchestrator agent definition's Step 0 ("Load skill context") read the fn/ procedure files, which would remind it to dispatch sub-agents — currently the orchestrator reads its OWN definition but not the skill procedures.
(b) Change the caller's dispatch prompt to say "coordinate the creator and reviewer agents" rather than "do all the work."
(c) Accept that 4-level nesting is impractical and redesign: orchestrator does Plan+Gather+Read itself, but MUST dispatch a separate reviewer agent for Judge (the one split that's load-bearing for independence).
(d) Use code-based G2 integrity check (deterministic, no agent needed) + fresh-agent G1/G3 — already being built as of this session.

Recommend (c)+(d): accept that the orchestrator is the doer for stages 1-3, but enforce the builder!=judge split for stage 4 by dispatching a reviewer agent with fresh context + running the deterministic G2 script.
