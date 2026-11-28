---
title: Renumber b16 Studio topics to the shared bands
date: 2026-11-27 13:25
topic: board
aim: b16's topics sit in the Studio Type bands (b17 s70-s79) with band-prefixed titles; title check 0 problems.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1325_renumber_bands.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b16_theme_paper/_archive/20261127/s11-paper-block/
  what: old per-level Block page design, retired
- do: move
  path: examples/Project-Ladder/blueprint/b16_theme_paper/_archive/20261127/s13-paper-task/
  what: old per-level Task page design, retired
- do: move
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s11-idea-job-preview/
  what: from s11-idea-job-preview, same second digit as s01 Idea
- do: move
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s13-paper-job-preview/
  what: from s13-paper-job-preview, same second digit as s03 Paper
- do: move
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s53-paper-skills/
  what: from s53-paper-skills, s5N Skills
- do: move
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s81-paper-guide/
  what: from s81-paper-guide, s8N Theme Guide
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/s02-grant-block-structure.md
  what: title Block Structure: Grant
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.md
  what: title Block Structure: Paper
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/board.md
  what: Renumbered note; topic links follow the moves
- do: delete
  path: examples/Project-Ladder/blueprint/b16_theme_paper/_studio_groups.txt
  what: bands come from the Studio Type topics now
- do: edit
  path: examples/ plugins/ (every text file naming the old topics)
  what: old topic names swept to the new ones
---

## Prompts

- "check its s01, update yours accofdingly. go" (after the renumber plan: s14→s11, s12→s13, s21→s5N, s31→s7N/s8N)
- (b17 relay) theme Guide band is s8N, so s31-paper-guide went to s81, not s71.

## Changed

- Topic folders moved and inner files renamed as planned; s31 went to s81.
- Text sweep: 60 files in examples/ and plugins/ (incl. workbench-paper guide.yaml and ref/topics.md, b12 archive cross-links, b17's generated blueprint-organization.html which b17's builder rewrites the same way).
- Titles band-prefixed on s01, s02, s03, s11, s13, s53, s81. board.md Renumbered (261127). _studio_groups.txt deleted. No bands: line needed: a blueprint Block reads its bands from b17's Studio Type topics.

## Check

- topic_titles_check.py b16: 0 problems.
- 5623 Studio page (200): bands 🧱 Block Structure, 👀 Block Job UI Preview, 🧰 Skills, 🗺️ Theme Guide; topics s01 s02 s03 s11 s13 s53 s81.

## Summary

b16's Studio now sits in the shared bands with band-named titles; the old per-level page topics are archived.
