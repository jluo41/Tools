---
title: Implement interactive Job Overview
date: 2026-11-27 09:12
work: [s11]
aim: Implement the reviewed interactive Overview on the real Work Job Main inside its owning Block, using disk-backed records and preserving the existing Block route.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/0912_overview_live.md
    what: Record this approved plan, prompts, changes and checks before implementation.
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
    what: Delegate Work Job Overview to its own renderer while preserving authored overrides and other levels.
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/job_overview.py
    what: Render Goal, Requirements and MindMap from real records, scoped controls, Task inspection and expanded reading within the Block.
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_overview.py
    what: Check grouping, record content, isolation, empty records and Block navigation boundaries.
  - do: edit
    path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/SKILL.md
    what: Document the live Overview contract and its verification.
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/job-elements.md
    what: Align the Work Job Overview elements with the live component inside its Block.
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: Fade the matching Effect once its implementation is verified in Page.
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: Record the live implementation and preserved comparison preview.
changed:
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/job_overview.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_overview.py
  - plugins/haipipe-toolkit/skills/2_work/work/workbench-work/SKILL.md
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/job-elements.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/0912_overview_live.md
---

# Implement interactive Job Overview

## Prompts

> 要不然现在你就直接 implement 一下吧，把它给弄到这个 page 里面去，我看看什么效果。

The assistant presented the eight-file plan above through the confirmation question. The user answered:

> 确认，按这份清单实现

## Decisions

- Continue the approved Effect from `0850_overview_effect.md` as a real Work Job Overview. Read the selected Job and its Tasks rather than copying the example's placeholder content.
- Keep the owning Block title and route. Task inspection is local to the embedded Overview, in accordance with PRINCIPLE.md and hai-ui A10.
- Preserve existing authored Overview sections, other levels and other themes. Retain the one Brief fold and shared left-tab/right-content control; apply the proposed visual treatment and diagram inside it.
- Existing unrelated working-tree changes remain intact.

## Check

- Passed 11 targeted unittest cases (four existing Job Main checks and seven new Overview cases): real record content, Task bands, Task ownership, local detail targets, cross-Block scope isolation, missing content and authored Overview precedence.
- Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=plugins/haipipe-toolkit/servers/_host uv run --offline --python 3.13 --with pyyaml python -m unittest discover -s plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests -p 'test_job_*.py'`.
- Extracted component JavaScript passed `node --check`.
- Restarted the existing workbench with its unchanged root, bind host, port and launch arguments; the live Block route returned HTTP 200 with the new renderer.
- Browser-verified Goal, Requirements, MindMap / Topics and Work Structure against b01's j11 records. Task t01 inspection showed its own goal, close condition and path; Escape restored focus to its originating control.
- Browser-verified expanded Overview, a nested t02 detail dialog, Close, and restoration of the selected MindMap / Work Structure content. The Block title and path stayed unchanged.
- Switched to j12: it showed its own Goal. Returning to j11 retained its MindMap / Work Structure selection. Final screenshot showed the actual two Task groups and their six Tasks in Topics.
- `ui_preview_check.py` passed for s11: one topic, zero problems. Scoped `git diff --check` passed.
- Fresh-context skill review by `validate_live_overview_skill` passed after correcting the old example reference and documenting the embedded Jobs route. The reviewer also confirmed the implemented Effect is marked `old`.
- Desktop side-list hiding is covered by the scoped implementation; this narrow browser viewport shows the shared responsive tabs instead. No claim of browser verification of that desktop-only dot.

The existing Pages rail still contains legacy child links; this change does not certify those unrelated links against A10.

## Summary

Implemented the accepted interactive Overview in the real Work Job Main, including Blueprint work. It reads Job and Task records and retains authored Overview overrides. Page › job-overview now renders it; Effect › Overview · interactive remains as a faded comparison. The skill and element definition describe the live behavior. No work records are changed by inspecting or expanding this UI.

Live entry (origin-relative): `/_board/workbench?path=examples%2FProject-Ladder%2Fwork%2Fb01_example_work&layout=focus&section=jobs&group=j11&mark=view=overview`.

This trace keeps the request, approved plan and implementation evidence; the preceding Effect discussion is recorded in `0850_overview_effect.md`.
