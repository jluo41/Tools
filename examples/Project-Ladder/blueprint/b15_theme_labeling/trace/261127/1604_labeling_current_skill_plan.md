---
title: Labeling current skill contracts — file review
date: 2026-11-27 16:04
topic: s01-labeling-ladder
aim: Align the owning Labeling skills with approved Block boundaries and shared Studio rules, after file-level confirmation.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1604_labeling_current_skill_plan.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
  what: State three Block boundaries, typed routing and Block-only entry; remove historical narrative
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/1_data/hai-labeling-preparation/SKILL.md
  what: Keep Items operations inside one Task and open its owning Block
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-interaction/SKILL.md
  what: Keep Meaning interaction and signatures in its Block; preserve engine identifiers
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-expression/SKILL.md
  what: Describe Expression as a Task within Guideline Generation with Block-only navigation
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling-scanning/SKILL.md
  what: Bind Scale to one Scanning Task and frozen inputs; retain its operation laws
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling-workflow/SKILL.md
  what: Separate Run dependencies from Block Job and Task taxonomy
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/SKILL.md
  what: Use shared Block entry and Bands; document actual content owners and implementation gaps
- do: add
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/CONSTITUTION.md
  what: Codify Block-only UI, shared Bands, embedded examples and current-only skill writing
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1604_labeling_current_skill_plan.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/1_data/hai-labeling-preparation/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-interaction/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-expression/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling-scanning/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling-workflow/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/CONSTITUTION.md
---

# Labeling current skill contracts — file review

## Prompts

- **16:04** Current coordination request: 同步 owning skills/constitutions/refs：用户绝对禁止 skill 内 legacy、旧版比较、“之前如何”的叙述；只写当前规则。历史保留在技能外 Trace/Git，不在skill里新建legacy归档。重写有依赖的生成源，不能只改生成HTML。不得直接删除仍有有效职责或调用的技能。
- **17:27** 好，现在我确认了，然后你就是进行这个更改吧，好吗。

## Check

- Applied 25 confirmed targets across the two plans; all pre-apply hashes matched; only the planned source/content files and their Trace records were written.
- Presentation builder --check passed; generated type-page checks passed for all three Studios (1 / 2 / 2 pages).
- 12 shared Structure-view tests and 33 shared mindmap tests passed. Topic-title check passed for b15.
- Applied source in isolated fixtures rejected six negative cases: missing catalog, empty Task inventory, wrong owner, wrong source, missing evidence, and a generated child-page member link.
- All authored changed files are under 700 lines; changed Python/JSON parses; no trailing whitespace. Skill metadata reflects 2026-11-27.
- Chrome acceptance from the Tailscale b15 Block: all three Studio folds show Structure / Task types / Draw / Skills. Items has one full-width type page; Meaning/Expression and Scanning/eval use shared left tabs. All five type pages show their real for/holds text. Guideline Job Type → Job Name → both Task Types → Task Names expanded correctly; Structure and Draw use the same source. Sources includes the type catalog. The actual b02 Block loads embedded and the top-level b15 Block title/route stays. Actual owning skills load; eval’s ModelInstance contract is visible. The three shared Block Structure folds and preserved Task Procedure folds remain. No shared service restart.
- Fresh-context agent invoked the applied workbench-labeling skill, read its Constitution and all three catalogs, followed Block-only entry and correctly distinguished preview-only designs from actual b02 records. It confirmed no invented Job/group types and exposed the documented dependency/adapter gaps. No repository writes or browser actions by the agent.
- Shared contract check is NOT passing: 3 catalogs, 9 empty-level failures (Job group, Job type, Task group for each design). No types were invented to suppress those failures. Shared helper child routes, missing-field coverage, dependent Task-page navigation, the b04 preview’s operation-as-Task layout and actual Block Jobs selectors remain implementation gaps.

## Summary

Applied the eight confirmed owning-skill changes: three Block boundaries, Block-only entry, Task/operation ownership, shared Studio rules and current-only instructions. Fresh-context invocation and real source previews were verified. Runtime writers and dependency navigation are not claimed complete.

## Review artifact

The exact patch is staged at /tmp/labeling-band-update/skills.patch. Full proposed files are under /tmp/labeling-band-update/proposed/, matching their repository paths. No listed target has been edited. Original hashes are in /tmp/labeling-band-update/skill-plan.json; recheck them before applying. The requested changes introduce no engine rename and remove no active skill. Current API identifiers such as label_audit.py legacy and legacy_votes remain literal code names, not historical narrative.

## Dependencies

The eight targets contain no generated render regions. The preserved s41/s42 delivery/render.yaml files have pieces: []; those procedure artifacts do not generate these targets. The Work-owned shared Band/type reader, s75/s77/s79 definition retirement, and Labeling production adapters remain separate pending work. workbench-task-labeling and start.py still need navigation alignment; this patch states the shared Block-only rule and records that gap without claiming those runtime files changed.

## Validation prepared

README fresh-context review invoked the staged workbench-labeling skill with actual b02/b03/b04/b05 records. It confirmed the three approved boundaries and unregistered independent Job types; its routing and interpreter findings were corrected in the draft. This does not replace an after-apply check. Parent browser acceptance of the applied Studio changes is in the separate 1549_labeling_shared_bands trace.

## Shared runtime receipt

Work confirmed its shared registry/type-definition changes and service reload accepted; the parent independently saw b15's two correct shared Bands after reload. No additional shared changes or unified simulated-example work are part of this plan. The common Block Structure view-requirement reconciliation and Labeling production adapters remain distinct open work.

## Authorization

User confirmed both displayed file plans at 2026-11-27 17:27 EST. All 25 target paths are authorized: the 17-file catalog/presentation plan and eight-file owning skill plan. Preserve all pre-existing changes and apply only the reviewed files. Shared servers, registries, other themes, example execution records and human canvases are outside this change.

## Application

Applied the confirmed review artifacts at 2026-11-27 17:27 EST. All pre-apply hashes matched; copies of touched originals are in /tmp/labeling-types-review/before-apply. Generated pages will be rebuilt from the confirmed sources before final checks. No shared service was restarted.

## Browser receipt

Chrome acceptance from the Tailscale b15 Block: all three Studio folds show Structure / Task types / Draw / Skills. Items has one full-width type page; Meaning/Expression and Scanning/eval use shared left tabs. All five type pages show their real for/holds text. Guideline Job Type → Job Name → both Task Types → Task Names expanded correctly; Structure and Draw use the same source. Sources includes the type catalog. The actual b02 Block loads embedded and the top-level b15 Block title/route stays. Actual owning skills load; eval’s ModelInstance contract is visible. The three shared Block Structure folds and preserved Task Procedure folds remain. No shared service restart.

## Fresh-context receipt

Fresh-context agent invoked the applied workbench-labeling skill, read its Constitution and all three catalogs, followed Block-only entry and correctly distinguished preview-only designs from actual b02 records. It confirmed no invented Job/group types and exposed the documented dependency/adapter gaps. No repository writes or browser actions by the agent.

## Remaining work

Shared contract check is NOT passing: 3 catalogs, 9 empty-level failures (Job group, Job type, Task group for each design). No types were invented to suppress those failures. Shared helper child routes, missing-field coverage, dependent Task-page navigation, the b04 preview’s operation-as-Task layout and actual Block Jobs selectors remain implementation gaps. Independent Job identifiers, actual Work Studio Band names/numbering and the eval input adapter remain explicit design gaps. Completion here covers the confirmed presentation and skill files, not the production labeling harness.

## Final artifact

The applied repository files are authoritative. The reviewed /tmp artifacts record the approved proposal; current metadata dates and the observed live-selector limitation were synchronized within the same confirmed paths. Existing file baselines matched before application; original touched files were preserved in /tmp/labeling-types-review/before-apply/. The shared generators rebuilt the derived HTML.
