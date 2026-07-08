---
name: haipipe-run-timeline
description: "Rebuild a multi-lane flight-record timeline of any Claude Code session (paper runs, probe/discovery chains, replication tests) from its transcript + subagent transcripts. Lanes = spawn depth (session / probe agent / discovery agent / creator / reviewer); events = Skill calls, Agent dispatches, file Writes/Edits, with mm:ss offsets. No instrumentation needed -- transcripts already carry timestamps. Trigger: run timeline, flight record, session overview, 复盘, audit the run, what happened in session X."
argument-hint: "<session>.jsonl path (find via grep -l '<session-name>' ~/.claude/projects/<project-dir>/*.jsonl)"
allowed-tools: Bash, Read
metadata:
  version: "1.0.0"
  last_updated: "2026-07-05"
  summary: "One-command flight recorder: python3 run_timeline.py <session>.jsonl. Born during the test-2-2222 replication audit (JL: 'how could you log the process... so we can have an overview')."
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
  L0 = 🎬 d0 paper-session
  L1 = 🕵️ d1 probe-orchestrator
  L2 = 📚 d2 discovery-orchestrator
  L3 = ✍️ d3 discovery-creator
  L4 = 🔍 d3 discovery-reviewer

00:00 [L0] 🎯 Skill(haipipe-paper-enter)
03:42 [L0] 🤖 dispatch haipipe-probe-orchestrator-agent (bg=False)
07:33     [L1] 📝 Write 0705_silicon-physician-novelty/probe.yaml
10:10             [L3] 🎯 Skill(arxiv)
17:34             [L3] 📝 Write 01_novelty-verdict-three-axes/sources.md
19:39         [L2] 🤖 dispatch haipipe-discovery-reviewer-agent (bg=False)
```

Read it for: where time went (per-layer spans), whether dispatches took the mandated doors, sync-vs-background choices (`bg=`), and which files were born when. Complements the on-disk coarse trail (_LOG [PHASE] entries carry date + HH:MM per wiki/02); this is the fine-grained view.
