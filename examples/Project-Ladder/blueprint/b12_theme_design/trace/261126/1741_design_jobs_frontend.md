---
title: Design Jobs in the workbench
date: 2026-11-26 17:41
topic: s12-design-job
aim: Show complete Design Job Main and role-specific Task steps through the shared Jobs navigation, with live Studio examples.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261126/1741_design_jobs_frontend.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  what: Connect Design content to shared navigation
- do: add
  path: plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py
  what: Render two Main contracts and Task steps
- do: add
  path: plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_jobs.py
  what: Guard content, navigation and approval
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
  what: Document implemented operation
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record implementation and acceptance
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/job-views.md
  what: Align live definition and examples
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/task-views.md
  what: Align live definition and examples
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/structure.md
  what: Align live definition and examples
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/view-guide.json
  what: Align live definition and examples
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s12-design-job/s12-design-job.html
  what: Embed live Jobs examples
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s13-design-task/s13-design-task.html
  what: Embed live Task examples
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261126/1741_design_jobs_frontend.md
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
- plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py
- plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_jobs.py
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/job-views.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/task-views.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/view-guide.json
- examples/Project-Ladder/blueprint/b12_theme_design/s12-design-job/s12-design-job.html
- examples/Project-Ladder/blueprint/b12_theme_design/s13-design-task/s13-design-task.html
---

# Design Jobs in the workbench

## Prompts

- **exact message time unavailable** 好，你继续做呀，现在已经做完了吗？能不能就是进行一个前面的更新。然后我最终想要看到就是说我打开你这个五个半之后呢，我可以看到你这些内容，明白我意思吗。
- **exact message time unavailable** 那你现在要不要试一下，去完成一下。那你去执行吧。

## Check

- Design server and shared Job suites: 95 passed, 298 subtests passed. After final method/route guards, focused Design Jobs, context and use-case suites: 19 passed.
- Fresh-context skill review repeated after corrections: no remaining contradictions in the approved scope.
- Chrome on Tools host 5623: execution Main hides the Task row; selecting Designs shows t01 and Draft/Verify/Revise/State with original Runs; returning to Main restores its folds.
- Chrome: method Book Jobs Main shows Method, Steps, Versions and Used by; the signed version expands. Studio s12 Page loads actual Main, and s13 Design loads the selected t01 Task.
- Chrome: Files → Trace displays this trace and both exact user prompts and highlights its planned files. Earlier conversation excerpts remain in 1719_design_job_alignment.md; this is not an automatic full-chat archive.
- Read-only rendering tests preserve example content hashes and existing approval controls. No approval or release was submitted. Only the existing Tools host on port 5623 was restarted with its existing settings.
- All twelve changed paths match the approved plan; scoped git diff --check passed and each file stays below 700 lines.

## Summary

Implemented Design Main and role-specific Task content in the shared Job navigation, with live Studio Page examples and aligned contracts/skill guidance. Method Main is reached through its Book Jobs view or the Studio Method preview; the older standalone method Job route retains its generic view. Topics T03 and T05 are fixed with regression guards; the broader T01 session-view topic remains open. Existing unrelated work was preserved.

## Approval

The user approved the twelve-file list before this trace and implementation were written. The filename preserves the 17:41 planning anchor; exact message timestamps are unavailable. Only this confirmed scope is changed.
