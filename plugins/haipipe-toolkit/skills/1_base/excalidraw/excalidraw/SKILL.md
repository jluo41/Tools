---
name: excalidraw
description: "The one door for Excalidraw drawing: pick the kind, then read that kind's SKILL.md by path and follow it. Kinds: studio (how every Studio topic's drawing looks, draw.py, check.py; read first), job, task, story, ideation, workflow, slide, draft, report (or a scratch), read (a paper's PDF onto a canvas). Trigger: excalidraw, draw, drawing, redraw a topic, studio drawing, draw the job, draw the task, story drawing, slide draft, read a paper onto a canvas, /excalidraw."
argument-hint: "[kind] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /excalidraw · one door, ten drawing kinds

The ten `excalidraw-<kind>` skills beside this folder are hidden from the skill listing
(`disable-model-invocation: true`, JL 261026: "一个入口，其余隐藏，不搬家"). They stay where they are,
so every builder that imports `excalidraw-studio/scripts/draw.py` or `check.py` keeps working, and a
person can still type `/excalidraw-<kind>`. Claude reaches them through this door: pick the kind,
read `../excalidraw-<kind>/SKILL.md`, and follow it with the remaining args.

```text
the ask                                           kind        read
────────────────────────────────────────────────────────────────────────────────────────
how any Studio topic's drawing looks; draw.py     studio      ../excalidraw-studio/SKILL.md
a Job as a staircase of Tasks and Runs            job         ../excalidraw-job/SKILL.md
a Task as a staircase of its Runs                 task        ../excalidraw-task/SKILL.md
a paper's story: its research questions           story       ../excalidraw-story/SKILL.md
an ideation: every idea under the question        ideation    ../excalidraw-ideation/SKILL.md
a study's workflow as a building map              workflow    ../excalidraw-workflow/SKILL.md
a slide deck proposed on one canvas (s61-s69)     slide       ../excalidraw-slide/SKILL.md
a draft: a paper's Sections or one Section        draft       ../excalidraw-draft/SKILL.md
a report's drawing, or a scratch whiteboard       report      ../excalidraw-report/SKILL.md
one paper's PDF read onto a canvas                read        ../excalidraw-read/SKILL.md
```

1. **Studio first.** Before drawing or redrawing any Studio topic, read
   `../excalidraw-studio/SKILL.md` (its nine principles, `scripts/draw.py`, `scripts/check.py`),
   then the kind's own SKILL.md. `read` and a scratch `report` do not need it.
2. **Kind unclear**: name the two likeliest kinds from the table and ask which.
3. **Paths stay**: scripts are run and imported from their own folders,
   `../excalidraw-<kind>/scripts/`; never copy them here.

The topic folder, face, numbering and sessions stay `haipipe-studio`'s; this door only picks the
drawing kind.
