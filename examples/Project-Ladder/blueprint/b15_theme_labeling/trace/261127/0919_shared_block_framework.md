---
title: One shared Block framework
date: 2026-11-27 09:19
aim: PRINCIPLE requires every theme and preview to reuse the shared Block framework; themes supply content only.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/0919_shared_block_framework.md
  what: this trace's own record, written first
- do: edit
  path: PRINCIPLE.md
  what: Require shared Block implementation across all themes and previews
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/0919_shared_block_framework.md
- PRINCIPLE.md
---

# One shared Block framework

## Prompts

- **09:19** 我觉得你是一个大体设计是一样的，但是你的 framework 为什么跟 Work Theme 的 framework 不一样呢？就是你这些东西应该是有那个。因为你看 blog 里面是有所谓的不同的 view 的，report 啊，studio 啊，和 jobs你再看看。
- **09:19** 这样不对 ， 要沿用一套框架 你放到 principle里

## Check

- Compared focus_shell.page_shell, focus_render.rail_sections/open_section and the Labeling preview bypass. The existing shared code owns Report, Studio and Jobs; the custom preview bypass is not compliant.
- PRINCIPLE shared-framework assertions passed; git diff --check passed; document remains under 700 lines.

## Summary

Added the user-requested rule to PRINCIPLE: all themes, examples and inline previews must reuse the same shared Block rendering and navigation implementation. Themes provide content, and Jobs and Tasks remain embedded in the Block. This trace closes the documentation request only; the current custom Labeling preview still requires migration to shared code and is not claimed fixed.

