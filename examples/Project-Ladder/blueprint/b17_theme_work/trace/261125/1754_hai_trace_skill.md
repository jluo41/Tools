---
title: hai-trace skill
date: 2026-11-25 17:54
topic: s31-files-pane
aim: 'A /hai-trace skill owns the trace: its file, the plan-first loop (plan, show in Files, confirm, change, record, close) and scripts that do each step, so every session writes traces the same way instead of by hand.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1754_hai_trace_skill.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/0_utils/hai-trace/SKILL.md
  what: what a trace is, the loop, when to open and close one, how Files shows it
- do: add
  path: plugins/haipipe-toolkit/skills/0_utils/hai-trace/scripts/trace.py
  what: new (from a plan list), prompt (add one), changed (from git), close (Check, Summary), check (every trace parses)
- do: add
  path: plugins/haipipe-toolkit/skills/0_utils/hai-trace/CONSTITUTION.md
  what: the trace rules moved here from hai-ui's trace article, with JL's words
- do: add
  path: plugins/haipipe-toolkit/skills/0_utils/hai-trace/tests/test_trace_script.py
  what: new, prompt, changed, close and check on a temporary Block
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1754_hai_trace_skill.md
- plugins/haipipe-toolkit/skills/0_utils/hai-trace/SKILL.md
- plugins/haipipe-toolkit/skills/0_utils/hai-trace/scripts/trace.py
- plugins/haipipe-toolkit/skills/0_utils/hai-trace/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/0_utils/hai-trace/tests/test_trace_script.py
---

# hai-trace skill

## Prompts

- **17:52** I think we should have a skill named /haitrace for this, what is your thoughts? ANd go ahead
- **17:58** Could we call it hai-trace? later, we might want to change the skill name to tbe hai-xxxx, instead of hai-xxx
- **18:00** yes, go ahead and do them.

## Check

- hai-trace tests: 3 passed (new, prompt, changed, close, check on a temporary Block; a broken front matter is caught; a plan line needs do, path and what).
- trace.py check over the repo: 46 trace files, 1 problem, another session's 1751_jobs_flat_or_topics.md (no readable front matter).
- this trace was closed by trace.py itself.

## Summary

The hai-trace skill owns the trace file and the plan-first loop; scripts/trace.py makes, updates, closes and checks traces, writing the front matter with a YAML writer so no value can break it. Its constitution holds three rules: plan first, every prompt listed, a closed trace has Check and Summary.

