---
title: Studio Check pilot
date: 2026-11-27 18:14
topic: s71-studio-type-block-structure
aim: S71/S01 and S76/S51 show type-owned checks without claiming unperformed verification.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1814_studio_check_pilot.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/check_views.py
  what: Generate Check from its owning type requirements
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
  what: Preserve and generate the managed Check view
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_views.py
  what: Keep Check separate from skills during generation
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_check_views.py
  what: Test inheritance, regeneration and invalid bindings
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/check-view.md
  what: Define Check source and verification boundary
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
  what: Bind owning type and append Check
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/check.html
  what: Generated criteria and verification methods
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
  what: Bind owning type and append Check
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/delivery/check.html
  what: Generated criteria and verification methods
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/studio-views.json
  what: Bind owning type and append Check
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/delivery/check.html
  what: Generated criteria and verification methods
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work/studio-views.json
  what: Bind owning type and append Check
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work/delivery/check.html
  what: Generated criteria and verification methods
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: Accept a validated managed Check view
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: Record pilot and acceptance
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1814_studio_check_pilot.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/check_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_check_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/check-view.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/check.html
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/delivery/check.html
- examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/delivery/check.html
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work/delivery/check.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
---

# Studio Check pilot

## Prompts

- **18:14** Work Skills Studio 你读一读这个吧，你读一读这个。然后我觉得，无论是S，无论是就是说S7，还是说是S，还是比如Skill Type，我们都先再加一个Top View，Bottom，再加一个新东西叫做Check。就是说在这里我们需要Check什么啊。
- Direction approved: “OK，行，你你先试试吧啊。”
- Exact 16-file list approved: “好，我确认了，你继续整吧。”

## Check

- Ten unit tests pass: six Check-specific tests and four existing Skills-view tests.
- check_views.py --check passes on S71/S01/S76/S51. Type generators pass --check for both S71 and S76; Skills generator passes --check for S51.
- Fresh-context subagent invoked hai-studio/ref/check-view.md with independent temporary types and two actual skill folders: source inheritance, invalid/missing/empty type rejection, fingerprint changes, regeneration and unverified marks all passed. It identified an unaddressed discoverability gap: SKILL.md does not yet link the new reference; that file was outside this approved pilot.
- Actual Tailscale Block page: all four Check tabs opened. S01 shows S71 requirements, Verify expands the check method and source; S51 left items are its five skills and switching to hai-job changes its selected content. S71/S76 use definition marks, S01/S51 unverified marks.
- Opened the actual S71 elements.md source URL successfully. At 390 × 844, S76 Check criteria wrap readably without horizontal clipping; viewport restored.
- Baseline comparison confirms all four pre-existing view lists are unchanged. All 16 approved paths exist, remain under 700 lines, and scoped whitespace checks pass.
- Full check_organization.py remains failing on its historical work Folder hash. It reaches that check after validating the managed Check view. This failure predates this pilot; no Folder HTML is changed by this batch and no hash assertion was removed. It is not reported as a pass.

## Summary

Implemented the four-page Check presentation pilot. Types own the criteria; instances inherit them, and both generators preserve Check. The UI exposes requirements, verification methods and source links, without shell execution or fabricated result receipts. Shared server code was not changed and the service was not restarted. Automated result integration, the main skill reference link and full S71 product compliance remain separate work.

