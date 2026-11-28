---
title: report word menu
date: 2026-11-25 15:30
aim: The section word beside a page's title (Report) opens the sections menu (Studio, Interactions, Decisions, Things to Know, Checklist, Timeline, Skills); the 📁 ball opens Files only.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1530_report_word_menu.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_shell.py
    what: the h1 section word is a button with ▾ that opens #side-menu
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
    what: the menu opens under the word; the ball toggles the Files pane straight away
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
    what: the word looks pickable (▾, hover); the menu under it
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/CONSTITUTION.md
    what: A05 the section word is the sections menu, the ball is Files
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1530_report_word_menu.md
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_shell.py
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_faces.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_status_map.py
  - plugins/haipipe-toolkit/servers/workbench-labeling/tests/test_decision_view.py
  - plugins/haipipe-toolkit/servers/workbench-labeling/tests/test_labeling_focus.py
  - plugins/haipipe-toolkit/skills/1_base/project/hai-block/CONSTITUTION.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-block/constitution/A05-section-word-menu.md
---

# report word menu

## Prompts

- **15:30** how could we make this work, that when I click this [Report], I can choose different things, like Studio, things to know, etc. How do you think? I will keep [the 📁 ball] maybe to be just the file it self.
- **16:05** how do you think we can remove this? [the ▾ caret beside Report]
- **16:06** or a better elelemtn, like the dot? what is your htoughts?
- **16:20** I might want a dot in the left of the Report, can you give me the review? a point, that is what I mean.

## Check

- 5623 b17: Report ▾ opens the menu under the word (Studio ... Skills, no Files); Studio opens in the pane.
- The 📁 ball switched the pane to Files with no menu; a second press closed it.
- workbench 230, labeling 85, paper 112, design 58 pass.
- 16:06: no caret; Report carries a dotted underline (accent on hover), seen on 5623 b17; workbench 230, labeling 85.
- 16:20: the dotted underline gave way to a grey dot left of Report (`.h1-pick::before`); on hover it turns accent and grows; seen on 5623 b17.

## Summary

The section word beside the title is the sections menu (hai-block A05); the ball is Files alone. Tests that
pinned the old `<span class="h1-section">` now pin the button. The ▾ (later an SVG chevron) was removed for a
dotted underline, then (16:20) for a small dot left of the word, which also separates the title from the section word.
