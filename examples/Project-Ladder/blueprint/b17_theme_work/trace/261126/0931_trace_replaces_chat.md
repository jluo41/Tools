---
title: Trace replaces the cNN chat
date: 2026-11-26 09:31
aim: A Block keeps jNN, sNN and trace/; the cNN chat folder and hai-chat are retired, c01 becomes a trace.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0931_trace_replaces_chat.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261121/0046_plugin_principle.md
  what: c01's six prompts and files as a closed trace
- do: delete
  path: examples/Project-Ladder/work/b10_project_workbench/c01_plugin_principle_and_chat
  what: now a trace
- do: delete
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-chat
  what: skill, scripts, tests, hook; and its ~/.claude/skills link
- do: edit
  path: PRINCIPLE.md
  what: Block = jNN, sNN, trace; ui/ to delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_sessions.py
  what: stop reading cNN chat faces
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/ref/board-contract.md
  what: 'tree: trace/ instead of cNN'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/chat.md
  what: cNN paragraph points to hai-trace
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/ideation/hai-ideation/references/idea-block.md
  what: cNN rows to trace/
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-project/scripts/audit_projects.py
  what: drop CHAT_ITEM skip
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-project/scripts/ladder.py
  what: drop CHAT_ITEM skip
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-report/scripts/check_report.py
  what: drop CHAT_ITEM skip
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-job/scripts/new_job.py
  what: drop CHAT_ITEM skip
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0931_trace_replaces_chat.md
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261121/0046_plugin_principle.md
- PRINCIPLE.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_sessions.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-block/ref/board-contract.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/chat.md
- plugins/haipipe-toolkit/skills/1_base/ideation/hai-ideation/references/idea-block.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-project/scripts/audit_projects.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-project/scripts/ladder.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-report/scripts/check_report.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-job/scripts/new_job.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-block/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A07-trace-plan-and-states.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
- plugins/haipipe-toolkit/servers/workbench/ref/three-views.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/test_frame_sessions.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-project/ref/ladder.md
---

# Trace replaces the cNN chat

## Prompts

- **09:31** go

## Check

- c01's 12 prompts kept in trace/261121/0046_plugin_principle.md; trace check 0 problems
- hai-chat and its skill link removed; no live mention left outside history notes
- workbench 306 passed (6 old draft-reader failures); hai-project 19, hai-job 13, hai-report 17 passed
- ladder audit of b17 no longer flags trace/

## Summary

A Block keeps jNN, sNN and trace/; the cNN chat and hai-chat are retired, c01 lives on as a trace.

