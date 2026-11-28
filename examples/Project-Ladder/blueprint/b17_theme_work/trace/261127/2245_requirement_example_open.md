---
title: Requirement pages show their Example open
date: 2026-11-27 22:45
topic: s71-studio-type-block-structure
aim: The Example of a requirement page is open when the page loads, so the Pattern and the real example are seen together.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2245_requirement_example_open.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/requirement_examples.py
  what: the Example fold starts open
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements
  what: pages rebuilt
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2245_requirement_example_open.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/requirement_examples.py
---

# Requirement pages show their Example open

## Prompts

- **22:45** go ahead and let me check s71

## Check

- checks/run.py --target s71 passes; test_requirement_examples.py passes; pages rendered from the server in headless Chrome

## Summary

The Example fold of a requirement page starts open; s71 rebuilt.

