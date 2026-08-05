---
name: haipipe-run-timeline
description: "Rebuild a multi-lane flight-record timeline of any Claude Code session (paper runs, task/discovery dispatch chains, replication tests) from its transcript + subagent transcripts. Lanes = spawn depth (session / task or discovery orchestrator / creator / reviewer); events = Skill calls, Agent dispatches, file Writes/Edits, with mm:ss offsets. No instrumentation needed -- transcripts already carry timestamps. Trigger: run timeline, flight record, session overview, 复盘, audit the run, what happened in session X."
argument-hint: "<session>.jsonl path (find via grep -l '<session-name>' ~/.claude/projects/<project-dir>/*.jsonl)"
allowed-tools: Bash, Read
metadata:
  version: "0.1.4"
  last_updated: "2026-08-05"
  summary: "One-command flight recorder: python3 run_timeline.py <session>.jsonl. Born during the test-2-2222 replication audit (JL: 'how could you log the process... so we can have an overview'). v1.1: the worked example re-cut to the live dispatch doors — the probe gateway agent was retired 2026-07-14, so a paper session now dispatches DIRECT to haipipe-task-orchestrator-agent / haipipe-discovery-orchestrator-agent, which write <task-folder>/QA/<n>-<slug>.md."
---

Skill: haipipe-run-timeline
===========================

Rebuild the timeline of a run after the fact. Every session transcript line carries a `timestamp`; every subagent has `subagents/agent-*.jsonl` + `.meta.json` (agentType, spawnDepth). This script merges them into one chronological, depth-indented flight record.

## Usage

```bash
# 1. locate the transcript (session names live inside the jsonl)
grep -l "<session-name>" ~/.claude/projects/<project-dir>/*.jsonl

# 2. rebuild
python3 run_timeline.py /path/to/<session-id>.jsonl
```

## Output shape

```
LANES:
  L0 = 🎬 d0 paper-session          (consumer — holds the stake, dispatches, never executes)
  L1 = 📚 d1 discovery-orchestrator (executor — clean context, runs the qa gate)
  L2 = ✍️ d2 discovery-creator
  L3 = 🔍 d2 discovery-reviewer

00:00 [L0] 🎯 Skill(haipipe-paper)   # enter verb
02:15 [L0] 📝 Write papers/Paper-X/1-probes/PP02_novelty/      ← the probe file (paper-side)
03:42 [L0] 🤖 dispatch haipipe-discovery-orchestrator-agent (bg=False)   ← the commission, verbatim
10:10     [L1] 🎯 Skill(haipipe-discovery)
17:34         [L2] 📝 Write L01_novelty/01_three-axes/sources.md
19:39     [L1] 🤖 dispatch haipipe-discovery-reviewer-agent (bg=False)
26:04     [L1] 📝 Write L01_novelty/01_three-axes/QA/1-three-axis-novelty.md   ← the ANSWER
27:10 [L0] ✏️  Edit  papers/Paper-X/1-probes/PP02_novelty/      ← target: + ### a-executor
```

Read it for: where time went (per-layer spans), sync-vs-background choices (`bg=`), which files
were born when, and — the audit that matters most — **whether dispatches took the mandated doors**:

```
✅ the consumer lane (L0) touches ONLY papers/ and applications/.
✅ every tasks/ or discoveries/ Write happens in an EXECUTOR lane (L1+), under a
   haipipe-task-orchestrator-agent / haipipe-discovery-orchestrator-agent dispatch.
❌ a Write into tasks/ or discoveries/ FROM LANE L0 = LAW 1 broken. The paper session did bank
   work inline, with the stake in its context. That is the leak this timeline exists to catch.
✅ dispatch goes DIRECT from the consumer lane to the two executor orchestrators — no
   intermediate hop between them.
```

Complements the on-disk coarse trail (_LOG [PHASE] entries carry date + HH:MM per wiki/02); this
is the fine-grained view.
