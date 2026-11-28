---
title: fold rows not text
date: 2026-11-25 21:36
topic: s11-work-job-preview
aim: An opened Task fold in the Topic rows preview repeats nothing from its bar and holds no sentences; its rounds are rows (mark, round title, pass and date small on the right, the summary in the row's hover); the bar shows the Task's name and its mark only; a Task view's band holds its Run as one fold with the same rows.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2136_fold_rows_not_text.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: round rows instead of sentences; no repeated word on the bar; a Task view's Run fold
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2136_fold_rows_not_text.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
---

# fold rows not text

## Prompts

- **21:36** [Image] please open Chrome and test it yourself.
- **21:38** [Image] please focus here.

## Check

- 5623 Studio, s11 › Topic rows, zoomed: t01's bar reads "t01 · Block index page ✅" and nothing more; opened, two rows "✅ live restarts p02 · 11-25" and "✅ first check round p01 · 11-25", the summary in each row's hover; no fold inside a fold
- seen but left (JL 21:38 "focuing yourself here"): an opened Trace fold still repeats its time and ✓

## Summary

An opened Task fold holds round rows (mark, title, pass and date), not sentences, and its bar no longer repeats the newest round's title. Work stopped here on JL's word to focus on the Task folds.
