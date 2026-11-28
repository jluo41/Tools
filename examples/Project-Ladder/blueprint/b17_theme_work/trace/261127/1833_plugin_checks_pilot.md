---
title: 'Plugin checks: scoped Studio validation'
date: 2026-11-27 18:33
topic: s60-skill-studio
aim: Add modular read-only checks for Studio bindings, generated freshness and type placeholders; validate Skills-view writes without a background sweep.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1833_plugin_checks_pilot.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/checks/README.md
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/run.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/common/results.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/common/paths.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/skills/studio/scope.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/skills/studio/manifest.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/skills/studio/freshness.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/skills/studio/placeholders.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/tests/test_studio_checks.py
  what: Lightweight scoped checks, separated by responsibility.
- do: add
  path: plugins/haipipe-toolkit/checks/tests/test_runner.py
  what: Lightweight scoped checks, separated by responsibility.
- do: edit
  path: PRINCIPLE.md
  what: Describe checks as Define-side validation.
- do: edit
  path: AGENTS.md
  what: Add one scoped validation command for Studio changes.
- do: edit
  path: plugins/haipipe-toolkit/README.md
  what: Document checks beside skills and servers.
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: Link Check view contract and lightweight validation entry.
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: Bind existing Skills rule to executable acceptance.
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_views.py
  what: Validate generated outputs before reporting success; preserve check_type.
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: Record this topic, explicit coverage and its guard.
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1833_plugin_checks_pilot.md
- plugins/haipipe-toolkit/checks/README.md
- plugins/haipipe-toolkit/checks/run.py
- plugins/haipipe-toolkit/checks/common/results.py
- plugins/haipipe-toolkit/checks/common/paths.py
- plugins/haipipe-toolkit/checks/skills/studio/scope.py
- plugins/haipipe-toolkit/checks/skills/studio/manifest.py
- plugins/haipipe-toolkit/checks/skills/studio/freshness.py
- plugins/haipipe-toolkit/checks/skills/studio/placeholders.py
- plugins/haipipe-toolkit/checks/tests/test_studio_checks.py
- plugins/haipipe-toolkit/checks/tests/test_runner.py
- PRINCIPLE.md
- AGENTS.md
- plugins/haipipe-toolkit/README.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
---

# Plugin checks: scoped Studio validation

## Prompts

- **Earlier in this chat; exact message time unavailable** 我觉得不仅仅是增加一个 Check PY，而是加一个 Check Folder。我们现在不是有 Skills、Service，还有这个这两个大类吗？那所以要不要再加一个 Checks 呢？你明白我的意思吗？
- **Earlier in this chat; exact message time unavailable** 这个 Tracks 的 folder，我们要不要跟我们的，就是说 source 里面内容或者 SQL 里面内容对应起来啊？我不想让它就是一整个变成一个非常长的这个，非常长的这个 Python files，可以加一些 submodule 吗？
- **Earlier in this chat; exact message time unavailable** OK，行，呃，我们尽量比较晚但不要搞得太复杂。而且跑的时候应该也不会很 heavy吧。也不是说每次都要跑。你看看就是说怎么就是让它更……就有一些比较重要的一些路啊，就是我反复强调一直犯错那些路，你可以加一加。
- **Earlier in this chat; exact message time unavailable** 他妈一直设计设计，赶紧赶紧干啊，你这干嘛呀我操。

## Check

- New tests: 29 passed. Existing skills_views tests: 4 passed. Existing Check view tests: 8 passed (current concurrent suite). Total: 41.
- Nine named real targets (eight Skills topics plus S76) passed in 0.148 seconds. Single s62 target passed in 0.046 seconds. Timings are local measurements, not latency guarantees.
- Broader registered Block scope returns exit 1 for stale S01/S72 generation; see Remaining artifact findings. This result is preserved, not described as all-pass. No output files belonging to those topics were regenerated.
- Bad fixtures cover missing files, malformed manifests, duplicate or wrong names, added skill files, stale Check sources, missing types, bare placeholders, path escapes, external topic/manifest/face/type-source symlinks, empty scopes, unsupported targets and missing dependencies. Correct fixtures pass and the check leaves record bytes and mtimes unchanged.
- Standalone Skills writer ran successfully in a temporary SPACE without PYTHONPATH. It checks completed writes and preserves check_type; invalid duplicate skill output returns failure. No production topic was rewritten for this test.
- Fresh-context read-only reviewer invoked the documented CLI on real S51 and temporary broken/stale records. Reviewer found external manifest-symlink acceptance; fixed and independently rechecked: both topic and Block targets now error before reading outside sources.
- All 18 planned files exist and are below 700 lines; new Python modules parse. Runtime source files are 14-79 lines. Snapshot review preserved concurrent additions to Studio SKILL.md/CONSTITUTION.md. No service, CI, background watcher, global Trace writer or installed skill link changed.

## Summary

Added a small plugin-level checks package, split into common helpers and Studio scope, binding, generation and placeholder modules. Explicit targets keep checks bounded; errors and uncovered targets cannot pass. Skills-view writes run validation automatically through the existing owners. Documentation links the entry and explains its limited coverage. The pilot is complete; broader S01/S72 generation mismatches remain reported, and Check-view semantic criteria remain Not verified.

## Scope

The user instructed implementation after the scoped, modular proposal. This pilot invokes current owners instead of duplicating their rules. No CI, watcher, service restart, runtime UI change or blanket skill rewrite. Check-view freshness is distinct from executing the prose criteria in elements.md; the Not verified marks remain unchanged. Explicit unsupported targets fail as uncovered. The existing global Folder hash issue is outside this pilot.

## Remaining artifact findings

The broader registered Block scope returned exit 1 in 0.156 seconds. These current source/output mismatches are not fixed by this pilot; other sessions own those artifacts:

- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/delivery/check.html: out of date; regenerate this topic with check_views.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-job--job-rows.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-job--job-overview.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-job--job-tasks.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-job--job-findings.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-task--task-rows.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-task--task-overview.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-task--task-runs.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/page-task--task-findings.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/job-types--job-group-type.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/job-types--job-type.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/task-types--task-group-type.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/task-types--task-type.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/quickhtml.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/draw.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/requirements/delivery.html: out of date; regenerate this topic with type_requirements.py
- FAIL [generated] examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/studio-views.json: out of date; regenerate this topic with type_requirements.py
