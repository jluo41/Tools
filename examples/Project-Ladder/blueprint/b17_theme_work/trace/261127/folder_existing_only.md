---
title: Folder shows existing directories only
date: 2026-11-27
work: [s01, s02, s03, s04]
closed: true
plan:
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
    what: Correct folder depiction without changing work directories.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
    what: Correct folder depiction without changing work directories.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
    what: Correct folder depiction without changing work directories.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
    what: Correct folder depiction without changing work directories.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
    what: Correct folder depiction without changing work directories.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
    what: Correct folder depiction without changing work directories.
  - path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
    what: Correct folder depiction without changing work directories.
  - path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/folder_existing_only.md
    what: Correct folder depiction without changing work directories.
---

## Request

> No!!!! The folder will still be what we have now. No topic folder

## Decision

Folder reads the existing example Block directory tree rather than inventing a template. Job topic and Task topic are organization labels only. Existing sNN directories stay exactly as they are. No directory migration, rename or scaffold. Preserve Organization and Draw controls; Folder Draw uses the same observed directory tree.

## Check

- Guard passed: every Folder node resolves to an existing file or directory under its source Block, preserving parentage; no generated topic directories.
- Browser reload shows b01_example_work/, j11_core_checks/ and s01-what-it-checks/ with actual names; the schematic sNN-topic/ is gone.
- Scoped diff check passed. Source work directories were only read, never changed.
- The Folder content is a build-time inventory; rebuilding refreshes it from disk. Organization remains conceptual and separate.

