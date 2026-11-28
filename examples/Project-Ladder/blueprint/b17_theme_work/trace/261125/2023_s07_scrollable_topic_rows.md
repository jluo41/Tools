---
title: s11 scrollable topic rows
date: 2026-11-25 20:23
topic: s11-work-job-preview
aim: Bring the reviewed Job and Task navigation into Studio’s Topic rows preview for the Many and Few examples.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2023_s07_scrollable_topic_rows.md
    what: Record the confirmed plan, prompts, checks, and result.
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: Give Job and Task topics matching full-name tabs, hide the Task row in Main, and allow each row to scroll horizontally.
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2023_s07_scrollable_topic_rows.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
---

# s11 scrollable topic rows

## Prompts

- “How do you think you can make job topic with the full name, and for the task topics, they should have the same layout. How do you think? What is your design”
- “那像这个，当我这个，比如说照布或者踏斯黑多的时候，它就变成了多行。那有没有什么办法把它变成一行呢？比如说我可以变成一个一行的bar，我可以就是从左到右地去拽它。这样你可以做到吗？”
- “当我们选择比如说 main 的时候，那下面东西能不能 hide 掉啊，对吧？因为我们看 main 的时候就想看它这个长什么样子，对吧？所以我的思考就是说没必要把，没有必要把就是说那个 task 给选中了。就是说这 task 不选的话，我们就可以把它 hide 起来，明白我意思吗？就是省 space 嘛。”
- “I think it is much better. How do you wnat to update this ifrst.” The screenshot showed Studio → s07 → Page → Topic rows.
- “the Main here is not updated. and task tags here are not scrollable from left to right?”
- “what it take such a long time, please continue”

## Check

- Opened the live Studio iframe in desktop Chromium. Both Many and Few open on Main with three rows. Build and Check show one Task row, retain full labels, and restore the previously viewed Task per topic. Mouse drag moved the Task row in both directions without changing selection or moving the Job row.
- Opened the same served preview at a 390 px touch viewport. A native swipe moved the Check Task row. Main then hid the row and restored the Job overview.

## Summary

The Topic rows preview now uses matching full-name topic tabs and single-line horizontal rows. Main opens the Job overview with three rows. A Task topic opens the fourth row and restores the last Task viewed in that topic.
