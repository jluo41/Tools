---
title: topic contract split
date: 2026-11-26 10:04
work: [s11]
aim: "haipipe-studio's ref/topic-contract.md becomes one file per topic, as ui-preview-topic.md already is; topic-contract.md keeps what a topic is, its count and ownership, and the list of these files."
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1004_topic_contract_split.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-contract.md
    what: the index, what a topic is, its count and ownership, and one line per file below
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-folder.md
    what: from topic-contract.md § The folder
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-transcripts.md
    what: from topic-contract.md § Transcript originals inside a Task Studio
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-numbering.md
    what: from topic-contract.md § Numbering, with the s99 row
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-face.md
    what: from topic-contract.md § The face
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-look.md
    what: from topic-contract.md § The look
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/proposal-topic.md
    what: from topic-contract.md § A proposal topic
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/slide-draft-topic.md
    what: from topic-contract.md § A slide draft (a pointer to excalidraw-slide)
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-builder.md
    what: from topic-contract.md § Drawing with a builder
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-rounds.md
    what: from topic-contract.md § Rounds
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-buttons.md
    what: from topic-contract.md § The buttons
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-scripts.md
    what: from topic-contract.md § The scripts
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/SKILL.md
    what: its file tree lists the new files; § The face and § A proposal topic links point at their files
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/CHANGELOG.md
    what: one entry for the split
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s01-work-ladder/result/theme-alignment-proposal.md
    what: its link to § Numbering points at ref/topic-numbering.md
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1004_topic_contract_split.md
  - plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/topic-contract.md (the index)
  - plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/ (11 new files, topic-folder, topic-transcripts, topic-numbering, topic-face, topic-look, proposal-topic, slide-draft-topic, topic-builder, topic-rounds, topic-buttons, topic-scripts)
  - plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/SKILL.md
  - plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/CHANGELOG.md
  - blueprints/Project-Ladder/work/b17_theme_work/s01-work-ladder/result/theme-alignment-proposal.md
---

# topic contract split

## Prompts

- **10:02** topic-contract.md <--- I think for each of them, we should have one topic one file.

## Check

- Each section moved as it was, under its own title; one "(below)" in topic-look.md now names ref/slide-draft-topic.md.
- No link to a moved section is left (grep for "topic-contract.md § " outside CHANGELOG and traces); SKILL.md's two section links and its file tree point at the new files.
- haipipe-studio tests: 41 passed (with Pillow, which its drawing tests need).
- Largest new file topic-face.md, 78 lines; the index 35.

## Summary

haipipe-studio's topic contract is one file per topic: topic-contract.md lists them, each part (folder, face, numbering, look, builder, transcripts, rounds, buttons, scripts) and each kind of topic (proposal, slide draft, UI preview) has its own ref file.
