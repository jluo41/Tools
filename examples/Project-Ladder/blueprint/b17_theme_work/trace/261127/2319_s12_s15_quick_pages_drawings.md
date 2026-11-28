---
title: s12 to s15 quick pages and drawings
date: 2026-11-27 23:19
work: [s12, s13, s14, s15]
aim: "The six parts s12 to s15 still showed as the type's requirement become real: a quick page each (s12, s13, s14, s15) and a drawing each for s12 and s15, so every instance of Studio Type: Block Job UI Preview has every view."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2319_s12_s15_quick_pages_drawings.md
    what: this trace's own record, written first
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s12-blueprint-job-preview/delivery/ui/job-row-builds.html
    what: "quick page: a blueprint Job row says what it builds and where its code lives"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview/delivery/ui/job-row-next-move.html
    what: "quick page: cowork Jobs under who has the next move"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/delivery/ui/inquiry-to-papers.html
    what: "quick page: an inquiry Job leads to its papers"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s15-knowledge-job-preview/delivery/ui/goal-to-topics.html
    what: "quick page: the learning goal leads to its topics and the practice Job"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s12, s13, s14, s15: the topic's .html)
    what: one button per quick page
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s12-blueprint-job-preview/ (build_s12_blueprint_job_preview.py, .excalidraw, .png)
    what: "its drawing: Block, Job, Task, folds, read from disk"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s15-knowledge-job-preview/ (build_s15_knowledge_job_preview.py, .excalidraw, .png)
    what: "its drawing: Block, Job, Task, folds, read from disk"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s12, s15 faces)
    what: Files and Open name the new parts
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s12 to s15: studio-views.json, delivery/check.html, Checklist), s72 delivery
    what: rebuilt by s72's build_type_pages.py
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2319_s12_s15_quick_pages_drawings.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s12-blueprint-job-preview/ (delivery/ui/job-row-builds.html, its .html, its face, build_s12_blueprint_job_preview.py, .excalidraw, .png)
  - examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview/ (delivery/ui/job-row-next-move.html, its .html)
  - examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/ (delivery/ui/inquiry-to-papers.html, its .html)
  - examples/Project-Ladder/blueprint/b17_theme_work/s15-knowledge-job-preview/ (delivery/ui/goal-to-topics.html, its .html, its face, build_s15_knowledge_job_preview.py, .excalidraw, .png)
  - examples/Project-Ladder/blueprint/b17_theme_work/ (s12 to s15: studio-views.json, delivery/check.html, Checklist; rebuilt)
---

# s12 to s15 quick pages and drawings

## Prompts

- **23:19** pleaase go ahead to add them .

## Check

- build_type_pages.py --check: PASS, no part lacking; QuickHtml and Draw read ✅ in the Checklist of s12 to s15.
- hai-studio/scripts/checks/run.py --target b17: every line for s11 to s15 and s72 is PASS; placeholder_check.py: 0 bare slot names.
- The four quick pages answer 200 on 5623; each instance's QuickHtml and Draw item is its own file, not the type's requirement page.
- The two drawings were looked at as their .png (built with uv and pillow; the host python has no Pillow).
- A quick page's rows are read from the example Jobs' faces (goal, waiting-on, next, since, ticket; discovery.yaml's Runs); s12's rows carry the band's mark, since its Jobs' faces state no state.
- No server code changed.

## Summary

Every instance of the type now has a quick page and a drawing of its own.
