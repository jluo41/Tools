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
  version: "0.1.0"
  last_updated: "2026-10-16"
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
The door (the folder, the face, `page.py` build and serve) stays `../haipipe-draft/SKILL.md`; the Run list is
`../haipipe-draft-workflow/SKILL.md`.

## Pages

- `ref/context.md`: PREPARE, `Page.context`. Collect, resolve and freeze what the plan must satisfy into `draft/records/<stem>-context.md`.
- `ref/context-record.md`: the shape of that generated record (the generator is `../haipipe-draft/cli/context-record.py`).
- `ref/structure.md`: SHAPE and SURVEY, `run-structure-<slug>`. The versioned plan, the Evidence Items, the Local Input.
- `ref/scratch.md`: Save and Finish, `run-scratch-<target>`. A person's rough notes for one Section or paragraph group.
- `ref/history/haipipe-draft-{context,structure,scratch}-CHANGELOG.md`: the histories of the three pages.
- `CHANGELOG.md`: this skill's history.
