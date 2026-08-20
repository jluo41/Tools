# q-executor
🧱 STAKE FORBIDDEN · this is the ONLY file that is dispatched.

How many producer agents exist on disk under page-workflows/agents/, which phases do they cover, and which phases lack an agent of their own?

**Where to look**
Tools/plugins/haipipe-toolkit/skills/board/page-workflows/agents/ — one file per agent, README.md and CHANGELOG.md excluded. The controller's PRODUCER_AGENTS table in skills/board/haipipe-board/ref/page-lifecycle.workflow.js maps phases to agents and names the fallback. The support roster lives in skills/board/agents/.

**What a complete answer contains**
The agent-file count, the phase-to-agent mapping including any shared agent, the phases with no agent of their own and why, the fallback agent's name, and the support-agent count.

**How to return it**
Counts with the file or command each came from. A count with no source is not an answer. If a number cannot be produced, say which input is missing rather than estimating it.
