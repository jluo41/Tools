---
title: job preview band
date: 2026-11-26 10:26
work: [s11, s12, s13]
aim: "The s1N band is the Job UI Previews, one per theme: s11 work (was s11-work-job-preview), s12 cowork (was s13-cowork-job-preview), s13 discovery (was s14-discovery-job-preview); every reference follows, b17's face records the renumbering."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1026_job_preview_band.md
    what: this trace's own record, written first
  - do: move
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/
    what: from s11-work-job-preview/ (its face, page, drawing, builder and delivery/ui renamed with it)
  - do: move
    path: examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview/
    what: from s13-cowork-job-preview/, its Page leads with the cowork example's Job
  - do: move
    path: examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/
    what: from s14-discovery-job-preview/, its Page leads with the discovery example's Job
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
    what: a Renumbered note (s07 to s11, s08 to s12, s09 to s13)
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
    what: s11-s19 are Job UI Previews, one per theme (work, cowork, discovery)
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
    what: the Kinds table names s11, s12, s13 as the work, cowork and discovery Job UI Previews
  - do: edit
    path: examples/
    what: every other reference to the old names (faces, traces' work lists, skills and docs) rewritten to the new ones; a quoted prompt keeps its words
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1026_job_preview_band.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/ (from s07-job-page-view/, its files renamed)
  - examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview/ (from s08-cowork-block-view/, Job view first)
  - examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/ (from s09-discovery-block-view/, Job view first)
  - examples/Project-Ladder/blueprint/b17_theme_work/board.md (## Renumbered)
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md (Kinds, the s1N Job UI Previews)
  - 58 files with the full old names, 64 in b17 with a bare s07 (traces' work lists and words); trace file names kept
---

# job preview band

## Prompts

- **10:20** for the job UI preview, could we index them from j1N? like j11, j 12, etc.
- **10:22** No, I mean s11, s12, the s1N series will be the Job Preivew xxx
- **10:25** No, each s1N will be a job level. It can be work job UI preview, and can be coworkd job UI preview and discovery job UI preview, do you get it now?

## Check

- No file outside references/ still names s07-job-page-view, s08-cowork-block-view or s09-discovery-block-view.
- A bare s07 in b17 meant this topic except where it named b03's s07 (q01_work_ladder.md, build_s01_work_ladder.py, two option pages and a mock): those five were put back, the tracked ones only where my replacement was their only change.
- 5623 restarted: b17's Studio lists s11-work-job-preview (Page, Effect, Draw, Delivery), s13-cowork-job-preview (Page with the Job first), s14-discovery-job-preview (Page with the Job first), no traceback.
- ui_preview_check.py: s11, s12, s13 pass. folder_icons_check.py: the 3 problems left are the b10 merge traces of another session.

## Summary

The s1N band holds the Job UI Previews, one per theme: s11 work, s12 cowork, s13 discovery; the topics moved, every reference follows, and b17's face records the renumbering.
