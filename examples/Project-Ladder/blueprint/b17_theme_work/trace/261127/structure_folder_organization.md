---
title: Folder and organization in four structure Studios
date: 2026-11-27
work: [s01, s02, s03, s04]
closed: true
plan:
  - path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/structure_folder_organization.md
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/s01-work-ladder.md
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/result/structure-before-organization-261127.md
    what: Preserve the current face verbatim.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/s02-work-skills.md
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/studio-views.json
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/result/structure-before-organization-261127.md
    what: Preserve the current face verbatim.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/s03-q01-work-ladder.md
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/studio-views.json
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/result/structure-before-organization-261127.md
    what: Preserve the current face verbatim.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/studio-views.json
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/result/structure-before-organization-261127.md
    what: Preserve the current face verbatim.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
    what: Align the four structure topics with the approved content organization.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
    what: Align the four structure topics with the approved content organization.
  - path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
    what: Align the four structure topics with the approved content organization.
---

## Request

> 第一个内容是 folder，第二个内容是我们 job，task organization，再个就是我们的 studio organization。

> 你接下来就直接去执行吧,然后我到时候我就起来我看看那什么样子。

## Plan

Use s01 Work, s02 Blueprint, s03 CoWork, s04 Discovery. Structure has Folder, Job / Task Organization, Studio Organization. Draw covers the same three models. Examples and Skills remain in this Studio. Preserve previous faces and canvases; retain paths so existing references resolve. S11–S13 remain UI topics. The user authorized execution after the design plan; the concrete file list was displayed before edits. Reuse shared authored Studio views without modifying the shared server.

## Check

- `check_organization.py`: passed four models, three Structure and Draw items, local file and Block destinations, retained face hashes, output reproducibility, and theme-specific folder invariants.
- JavaScript extracted from generated content passed `node --check`.
- Scoped `git diff --check` passed. All edited source/documentation files remain under 700 lines.
- Actual workbench at the existing Tailscale origin: verified the four corrected topic titles, Work Folder / Job / Task Organization / Studio Organization switching, and Draw hiding explanations while retaining the same tree.
- Browser-verified CoWork's Job organization has no Task nodes. Fresh-context review found the missing people Job and Discovery files; both were added and now have guard assertions.
- Browser-verified Blueprint Studio Organization separates the Structure and UI responsibilities; its Example opened b16_theme_paper inside the shared workbench.
- Browser-verified Discovery Draw exposes discovery.yaml, draft/, the same-stem ticket and result card/Bib/facts/runtime/source-access files. Skills loads its real contract text.
- Fresh-context reviewer `review_structure_content` rechecked the corrections and reported no remaining material issue in this scope.
- Original faces are preserved byte-for-byte under the hashes below. Existing historical canvases and builders were not edited. No shared framework code or S11–S13 UI content was changed.

## Result

Structure now contains Folder, Job / Task Organization and Studio Organization for s01 Work, s02 Blueprint, s03 CoWork and s04 Discovery. Draw follows the same models; Examples and Skills retain their own views. The existing topic paths are preserved. Content updates appeared on the running server without a restart.

Entry: `/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb17_theme_work&layout=focus&section=studio&group=Structure#s01-work-ladder`.


## Preserved face hashes

```json
{
  "examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/result/structure-before-organization-261127.md": "02725b2ec3e5831a44f9900352261fb96d843a3046213efa2e2023f343d09c3b",
  "examples/Project-Ladder/blueprint/b17_theme_work/s02-work-skills/result/structure-before-organization-261127.md": "e13b53db07338c46c3cdbb04f68b7e26f5e1ded9dadd5b91dd0e94b29a581a58",
  "examples/Project-Ladder/blueprint/b17_theme_work/s03-q01-work-ladder/result/structure-before-organization-261127.md": "60919e5e9b72dc8e10d3d508c07c915278955a5e62ad40df65ea7d3b0147d586",
  "examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/result/structure-before-organization-261127.md": "ad41c0bf02c8bccf4e88707dfe78eb22ef757115f2d2f04a7ca5dcf3066981d5"
}
```
