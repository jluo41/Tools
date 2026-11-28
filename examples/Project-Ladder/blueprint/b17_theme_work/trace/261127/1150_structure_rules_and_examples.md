---
title: Structure rules and examples
date: 2026-11-27 11:50
topic: s01-work-structure
aim: Distinguish fixed names, variable naming slots and real examples; make this work visible in Trace.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1150_structure_rules_and_examples.md
  what: Register this follow-up retrospectively; previous record was not discovered
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: Separate rules from concrete examples
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: Separate rules from concrete examples
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
  what: Separate rules from concrete examples
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
  what: Separate rules from concrete examples
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
  what: Separate rules from concrete examples
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
  what: Separate rules from concrete examples
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
  what: Route Structure and Examples separately
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/studio-views.json
  what: Route Structure and Examples separately
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/studio-views.json
  what: Route Structure and Examples separately
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/studio-views.json
  what: Route Structure and Examples separately
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: Record the naming rule and guard
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1048_organization_by_block_type.md
  what: Retain history and link the registered trace
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1150_structure_rules_and_examples.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/studio-views.json
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1048_organization_by_block_type.md
---

# Structure rules and examples

## Prompts

- **11:50** 为什么我发现你的这个 Trace 没有更新啊？
- Earlier in this chat: 我们怎么列这个呢？它这个是说每一个work block都要follow这种 style吗？还是这只是个 example啊？
- Earlier in this chat: 那你想想怎么就是把这个东西表达得更清楚一些。 就是说要么就是说你有两个，一个是指example，另外一个version，就是有的时候我们这个block就是说它的job name就是说是 至于当下的具体的任务 的，有的时候它的job name或job group name它是固定的。我想说你怎么就是区分它们？
- Earlier in this chat: 要不然你再重新再更新一下。

## Check

- check_organization.py passed for four models: rule/example routes, naming boundaries, real links and preserved Folder hashes.
- node --check passed for all four generated HTML scripts; scoped git diff --check passed.
- Actual Tailscale Work page: Structure shows naming slots; Examples shows real folders and First command line source links. Files Trace title and current request are visible and openable.

## Summary

Structure and Draw now show naming rules, with literal fixed names and angle-bracket names chosen for the work; Examples retains the real content and Block link. CoWork keeps its fixed people Job and no Task rule; the legacy sample mismatch remains documented. Registered this work with the required numeric trace filename and complete metadata, preserved the old history, and verified it appears in Files. The trace was registered retrospectively, as explicitly recorded.

## Registration repair

This Trace was registered after the page edits, not before. The original request times are unavailable; 11:50 is registration time. The earlier record trace/261127/1048_organization_by_block_type.md is retained. Its filename lacked the numeric prefix required by trace_view.traces(), and its metadata lacked aim/do/changed fields. Appending prose there could not make it appear in Trace. No shared server code was changed. Future work must use trace.py before implementation.

## Contract decisions

Structure uses fixed literal names and 〈names chosen for this work〉. Groups are optional authored organization, distinct from execution types. CoWork j00_people is fixed by its skill; other Job names vary, and its rule has no Task level. Discovery Jobs are themselves inquiry groups. Blueprint Block Structure/Block UI Studio types follow the user decision. Examples retain actual source folders and links, including the separately documented CoWork contract/example mismatch.
