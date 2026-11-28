---
title: trace name in bar
date: 2026-11-25 17:34
topic: s31-files-pane
aim: "The picked trace's name sits in the top row between the Trace icon and the metro icon; a click on it opens or closes its content; the card has no fold arrow, no colour bar and no Open link."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1734_trace_name_in_bar.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: the trace name in the top row between the two icons, a click opens or closes its content; no fold arrow, colour bar or Open link
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the name button in the top row
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
    what: the same in the Metro map preview
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1734_trace_name_in_bar.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
---

# trace name in bar

## Prompts

- **17:34** this is too long, I just want to put the name in between of the two icon, and I can click and show the content should just be okay
- **17:36** no, it should be in between [the two icons]; and no need to have [▸ and the colour bar] [Open ↗], save the words, be concise, let UI explain themself.
- **17:37** yes

## Check

- 5623 b17 Files: Trace on shows "trace name in bar" between the highlighter and the arrows; the content stays closed;
  a click on the name opens it (aim, prompts) with no fold arrow, colour bar or Open link. workbench tests: 239 passed.
- s31 Metro map preview: the same.

## Summary

The picked trace's name sits between the two icons; a click on it opens or closes its content, which carries no fold
arrow, colour bar or Open link.
