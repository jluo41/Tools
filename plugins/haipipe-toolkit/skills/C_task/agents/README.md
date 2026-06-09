C_task — Agent Roster
=====================

Two agents, separated by role. The split is the whole point:

```
haipipe-task-builder-agent   🔨 BUILD  — author code for any task type
haipipe-task-reviewer-agent  🔍 REVIEW — Gate 1 (pre-run) + Gate 2 (post-run)
```

builder ≠ judge. One agent authors, a different agent (with independent
context) reviews it.

The C_task lifecycle
--------------------

```
human/agent → haipipe-task skill ──(detect type)
                    │
   ▼ BUILD          │
   haipipe-task-builder-agent
     calls Skill("haipipe-task-for-<type>")   scaffold 4 sister files
     authors <TASK>.py/.do body + config       type-specific code
                    │
   ▼ 🚦 GATE 1     │
   haipipe-task-reviewer-agent (gate=1)
     Python: intent vs code, two-stage (Claude + Codex)
     Stata: structure + server-runnability + readability + correctness
     → CODE_REVIEW.md
                    │
   ▼ EXECUTE        bash runs/<RUN>.sh or powershell runs/<RUN>.ps1
                    │
   ▼ 🚦 GATE 2     │
   haipipe-task-reviewer-agent (gate=2)
     per-run trustworthiness checklist
     → RUN_AUDIT.md
                    │
                    ▼  (run is now linkable as a D_probe arm)
```


Agent details
--------------

| Agent | Role | Detects | Deliverable |
|-------|------|---------|-------------|
| `haipipe-task-builder-agent` | BUILD | task type → calls right skill | `<TASK>.py/.do` + config |
| `haipipe-task-reviewer-agent` | GATE 1 + 2 | gate mode + dialect (Python/Stata) | `CODE_REVIEW.md` or `RUN_AUDIT.md` |


Invocation from SKILL.md
--------------------------

The haipipe-task SKILL.md Step 3c wires these agents into the workflow
lifecycle:

```
(4) REVIEW  → Agent(agentType="haipipe-task-reviewer-agent",
                    prompt="gate 1: review <task-folder>")
(6) AUDIT   → Agent(agentType="haipipe-task-reviewer-agent",
                    prompt="gate 2: audit results of <task-folder>")
```

For the BUILD step (when creating new tasks):
```
Agent(agentType="haipipe-task-builder-agent",
      prompt="build <type> task from spec: <spec>")
```


Legacy agents (creators/ and reviewers/)
------------------------------------------

The per-type `code-creator-for-<type>-agent` family (9 agents) and the
separate `run-script-reviewer-agent` + `run-result-auditor-agent` +
`stata-script-reviewer-agent` (3 agents) are **superseded** by the two
unified agents above. The legacy files remain under `creators/` and
`reviewers/` for reference but should not be used for new work.

Consolidation rationale:
- Per-type creators were thin wrappers — type knowledge lives in the
  skills, not the agents. One builder agent routes to the right skill.
- Three reviewers did the same job with dialect variations. One reviewer
  agent detects the dialect internally.
- 12 agents → 2 agents. Zero duplication, same coverage.
