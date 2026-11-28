---
title: Each Studio topic its own emoji
date: 2026-11-27 12:28
topic: s32-trace-section
aim: 'A Studio topic''s fold shows the emoji its face names on an emoji: line, 🎨 when none; each b17 topic names its own.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1228_topic_emojis.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: 'the fold''s emoji from the face''s emoji: line, else 🎨'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
  what: 'a topic''s emoji: line shows on its fold'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.md
  what: 'emoji: 🛠️ (and s02 📐, s03 🤝, s04 🔭, s11 🛠️, s12 🤝, s13 🔭, s14 📐, s31 🗂️, s32 🧵, s99 📖 in their faces)'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1228_topic_emojis.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.md
---

# Each Studio topic its own emoji

## Prompts

- **12:28** for the emojis for each studio, could they be different? did you update the trace now?

## Check

- studio and side_pane tests 55 pass (new: emoji line shows, else 🎨); served b17 Studio shows 🛠️ 📐 🤝 🔭 🛠️ 🤝 🔭 📐 🗂️ 🧵 📖

## Summary

A topic's face names its emoji on an emoji: line; each b17 topic has its own.

