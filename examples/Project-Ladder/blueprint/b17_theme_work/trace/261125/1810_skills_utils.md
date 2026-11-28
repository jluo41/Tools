---
title: skills utils
date: 2026-11-25 18:10
topic: s31-files-pane
aim: The Files pane's Skills part also lists the shared skills every page works by, hai-trace (traces) and haistack (rules), so they show under skills/0_utils/ beside 1_base and 3_theme.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1810_skills_utils.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: own_skills adds hai-trace and haistack
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_work_frame.py
  what: the Skills part holds 0_utils/hai-trace and haistack
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1810_skills_utils.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_work_frame.py
---

# skills utils

## Prompts

- **18:10** I think you can put the 0_utils to in the 3. SKILLS as well, what is your thoughts?
- **18:19** yes, yes, pleasego ahead and do it

## Check

- 5623 b17 Files: 3 · Skills now opens with 0_utils › hai-trace, haistack, then 1_base and 3_theme.
- workbench tests: 242 passed (own_skills on b17 holds hai-trace and haistack).

## Summary

The Skills part lists the two shared skills every page works by, hai-trace and haistack, under skills/0_utils/.

