---
mindmap: 1
title: s33 · One page shape: Block, Job, Task · structured
built: from-topic .
written: 261027, from the topic's face
---

# s33 · One page shape: Block, Job, Task <!-- root #2a6a42 -->

One page shape at every level: the answer first, then rows, then everything else as sections of one scrolling page.

- [problem] Today the content hides behind tabs <!-- n01 -->
  → What should one page show instead?
  - [found] On b19, Report and Work show the same page <!-- n02 -->
    Both come from one loop over `MODES` in `work_progress.spaces()`; Description repeats `goal_cards()` too.
  - [found] The first real number is four clicks deep <!-- n03 -->
    "95.8% same as Swift" sits in t12's Run table: Block › Report › j05 › t12.
  - [found] Runs are drawn in six places <!-- n04 -->
    Description, Report, Work, the Runs tab, Studio › Runs and the side rail each read them their own way.
- [shape] One page: answer, rows, next, sections <!-- n05 -->
  → How does a reader move around it?
  - [answer] The answer line comes first, in real numbers <!-- n06 -->
  - [rows] Rows are the children: Jobs, Tasks or Runs <!-- n07 -->
  - [sections] Studio, Related, Delivery, Timeline, Folder follow below <!-- n08 -->
- [layout] Top, left and right each do one job <!-- n09 -->
  → What rules keep it clean?
  - [top] The top says where we are, in folder names <!-- n10 -->
  - [left] The left lists the siblings at the same layer <!-- n11 -->
  - [right] The right is a line minimap of this page's sections <!-- n12 -->
    From JL's picture: one dark line for the section in view, grey lines for the rest, names on hover.
- [decided] Three decisions so far <!-- n13 -->
  → What is built next?
  - [D01] Names are the folder names only <!-- n14 -->
  - [D02] Layout A is accepted <!-- n15 -->
    B (a tree on the left) repeats the rows; C (menus in the breadcrumb) hides the siblings until hover.
  - [D03] HTML is rendered from Markdown, never saved <!-- n16 -->
- [next] One reader, then b19's live page <!-- n17 -->
  - [step] A shared reader returns data, never HTML <!-- n18 -->
  - [step] b19's page is drawn live behind a new button <!-- n19 -->
  - [check] Four counts: clicks, menu rows, duplicates, Runs shown <!-- n20 -->
- Files <!-- @files #6ce6c5 -->
  - [md] [s33-one-page-shape.md](s33-one-page-shape.md) <!-- @files/0 #17b7c6 -->
  - [html] [mock/one-page.html](mock/one-page.html) <!-- @files/1 -->
