---
name: haipipe-draft-logic
description: >-
  The plan of a Page: deciding what to say before it is written. Gather what the
  plan must satisfy (context, PREPARE); shape the Draft's `## 1 · Structure` and
  survey each Bullet's evidence needs (SHAPE, SURVEY, the Structure Run
  `run-structure-<slug>`); and keep a person's rough thinking (`## 2 · Scratch`,
  `run-scratch-<target>`). It writes no prose (that is haipipe-draft-writing) and
  judges nothing (that is haipipe-draft-review). Trigger: plan, logic, the logic
  of a Section, page outline, structure Run, shape the plan, SHAPE, SURVEY, survey
  the evidence items, outline pass, page context, PREPARE, context Run, scratch,
  scratch note, rough thinking, /haipipe-draft-logic, /haipipe-draft-structure,
  /haipipe-draft-context, /haipipe-draft-scratch.
metadata:
  version: "0.2.0"
  last_updated: "2026-10-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-draft-logic · the plan of a Page

The three middle skills of the draft line up with the sections of the Draft Markdown:

```text
haipipe-draft-logic     ## 1 · Structure   ## 2 · Scratch    what to say
haipipe-draft-writing   ## 3 · Draft                         how to say it
haipipe-draft-review    (reads all three)                     is it good
```

Run names did not change: `Page.context`, `run-structure-<slug>`, `run-scratch-<target>`.

## 🙋 Propose first: versions to compare, then the person picks (JL 261022)

Before writing or reshaping a Structure, propose two to four versions side by side and let the person choose; never
pick one for them and build on it (JL 261022: "你一会儿再给我 propose 几个版本吧，我可以比较一下，然后我们再决定 ...
永远把 propose 这个方法放到首位 ... 一定要 propose 几个 option，然后我可以选"). The order is the person's: the idea first,
then how the target venue's own papers write it, then the versions, then the pick (JL 261022: "我们第一步先脑子里有
idea，然后看看别人怎么写的；基于这个 context，我们把我们的 structure 定一下").

1. **Examples first, from the target venue only**: read how three to six papers of the journal we send to open the
   same Section (excalidraw-read, a Studio topic `sNN-<task>-<venue>-examples`); never mix in other venues (JL 261022:
   "我们尽量只用 NMI 的文章 ... 不要被其他地方给 confused"; "MUST NMI"). Each paper is named by its title first.
2. **Two to four versions**: each names the venue papers it follows, its paragraphs and words, where the research
   questions show and where the tasks show; one table and a sketch of each version's paragraph flow.
3. **Same claims, different shapes**: the versions share the evidence and claims; they differ in order and emphasis.
4. **A lean is allowed, a pick is not**: say which version you lean to and why, in one line; the person decides.
5. **Then write**: the picked version goes into `## 1 · Structure` as `[Role]` Points (ref/structure.md); only then
   one sentence per Point.

Where the versions live: the Section's Studio topic (its canvas face), under "Structure versions to compare", so the
Studio tab shows them beside the examples. First used: Paper-ScalingGlucose-NatSeries2026 s22 and s23.
The door (the folder, the face, `page.py` build and serve) stays `../haipipe-draft/SKILL.md`; the Run list is
`../haipipe-draft-workflow/SKILL.md`.

## Pages

- `ref/context.md`: PREPARE, `Page.context`. Collect, resolve and freeze what the plan must satisfy into `draft/records/<stem>-context.md`.
- `ref/context-record.md`: the shape of that generated record (the generator is `../haipipe-draft/cli/context-record.py`).
- `ref/structure.md`: SHAPE and SURVEY, `run-structure-<slug>`. The versioned plan, the Evidence Items, the Local Input.
- `ref/scratch.md`: Save and Finish, `run-scratch-<target>`. A person's rough notes for one Section or paragraph group.
- `ref/history/haipipe-draft-{context,structure,scratch}-CHANGELOG.md`: the histories of the three pages.
- `CHANGELOG.md`: this skill's history.
