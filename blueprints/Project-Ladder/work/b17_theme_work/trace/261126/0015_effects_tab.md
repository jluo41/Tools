---
title: effects tab
date: 2026-11-26
topic: s11-work-job-preview
aim: s11 gets an Effects tab after Job Main; the Topic rows page with one Task per state (done, running, waits for you, not yet, new Task, a done Task with a new Run, void), each opened, beside a legend as s06's files-trace-effects.html has; a new Task or Run is grey italic with a plus, fading.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0015_effects_tab.md
    what: this trace's own record, written first
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: ?demo=effects data, one Task per state; a new mark (🆕) and its effect; not yet no longer fades
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-effects.html
    what: the page with ?demo=effects in a frame, the legend beside it
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: an Effects tab after Job Main
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: the Effects preview in Files
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0015_effects_tab.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-effects.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# effects tab

## Prompts

- **00:26** [Image] can you show the effects first? I think for the new runs, and new task, you can show it as well. can you just create a new one to host it in, do you get what I mean?

## Check

- 5623, job-view-effects.html: t01 to t07 opened, each state's effect shows; + t05 New Task and + third round grey italic, fading; t06 keeps its done mark; t07 struck; the group bar's blue dot pings; the legend beside it

## Summary

s11 has an Effects tab: the Topic rows page with ?demo=effects, one Task per state opened, a legend beside it. A new Task or Run (🆕) is a plus, grey italic, fading; not yet is grey and still.
