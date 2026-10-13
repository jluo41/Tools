---
name: excalidraw-slide
description: >-
  Draw a slide draft: a deck proposed on one Excalidraw canvas before it is built, as a studio topic
  s61-s69. It starts from the ask: a topic before the draft (s01 what they want) holds who the deck is
  for, how long, when it is shown, and each pain with the slide that answers it. Then one `slides.py` is
  the ONE source that the drawing and the deck both read (AUDIENCE · LENGTH · SHOWN · GROUPS · SLIDES ·
  OPEN; each slide n · slug · group · title · headline · ONE visual · caption · source · next · notes, an
  optional ask in red). The canvas reads left to right: 1 logic flow (one box per slide, why the next
  follows) · 2 the slides at half size in one skeleton · 3 on disk and the open questions. Black around
  the slides; inside a slide one accent marks its key thing. A screen is retaken by a script, never
  pasted. The deck is generated into the topic's own delivery/. The slide job to copy is j51
  (DrFirst-SPACE: a meeting, the ask, 14 slides, a deck). Use to take the ask, propose, draw, check or
  revise a deck before building it. Trigger: slide draft, propose a deck, what they want, the ask,
  slides.py, deck outline, logic flow of a talk, s61, presentation draft, /excalidraw-slide.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.2.0"
  last_updated: "2026-10-12"
  # version history: ./CHANGELOG.md
---

# /excalidraw-slide · a deck on one canvas, before it is built

A slide draft lets the person read the whole argument and every slide at once, mark it, and agree it
before a deck is written (JL 261007: "one type is about propose the slide draft"). It is a studio topic
numbered s61-s69; its folder, face and sessions are `haipipe-studio`'s, and how it is drawn is this
skill's. It starts from the ask, written in a topic of its own before any slide (learned on j51, 261012).

```text
the ask ─▶ slides.py ─▶ build_s6N_<deck>.py ─▶ s6N-<deck>.excalidraw ─▶ a person marks it ─▶ build_deck.py ─▶ delivery/
(s01)      (one source)  (the drawing)          1 logic · 2 slides · 3 open  (until agreed)       (.pptx · .pdf)
```

Read `ref/slide-draft.md` before drawing one: the ask, the folder, the frames, the slide skeleton, the
colour exception, the fields of `slides.py`, screens and figures, and the deck writer.


The slide job to copy: j51
--------------------------

j51 (`j51_insight_design_demo`, DrFirst-SPACE, under
`examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026/`) is a five-minute demo of
looped experimental learning for leadership and product. It went from a 36-minute meeting on 2026-10-05
to a 14-slide deck shown on 2026-10-08, and its `slides.py` passes `slide_kit.py check` clean. b31
s03-excalidraw-slide (`Tools/blueprints/b31_excalidraw/studio/`) draws the whole job: its map, its deck,
its two drawings, and what this skill took from it.

```text
j51_insight_design_demo/
├── j51_insight_design_demo.md        the Job face: kind, audience, length, due, the narrative, delivery
└── studio/
    ├── s01-what-they-want/           the ask: who, how long, what is due when, each pain → its slide
    └── s61-demo-layout/              the slide draft
        ├── slides.py                 14 slides in 3 groups: Why · The loop · What it solves
        ├── build_s61_demo_layout.py  the drawing, a change note under the slide it changed
        ├── capture_screens.py        retakes screens/ from a running host
        ├── screens/ · figures/       2 workbench screens · the loop figure and 2 designs
        ├── build_deck.py             the deck writer: python-pptx, one renderer per visual kind
        └── delivery/                 insight-design-demo.pptx · .pdf, generated
```


Make one
--------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts
python $S/new_topic.py topic <job> --slug what-they-want --title 'What they want' --band concept   # the ask
python $S/new_topic.py topic <job> --slug <deck> --title '<title>' --band slides                  # s6N-<deck>/
# write slides.py (ref/slide-draft.md § slides.py), then its builder, then:
python Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-slide/scripts/slide_kit.py check <topic>/slides.py
```

0. **The ask first**: a topic before the draft says who the deck is for, how long, when it is shown, what
   is due when, and each pain with the slide that answers it, every line with where it was said (a
   meeting's timestamp); people by role only. Each slide's `source` names its line in the ask.
1. **One source**: the drawing and the deck read `slides.py`; never type a slide into either.
2. **Left to right**: logic flow · the slides · on disk and open, side by side.
3. **One skeleton**: every slide at half size: title and rule, headline, ONE visual, caption, number.
4. **Colour inside a slide only**: `ACCENT` marks the key thing, `MUTED` the caption; around them black,
   red for an open question, green for a change.
5. **Notes in place**: a change note sits under the slide it changed (`CHANGES` as `(where, date, what)`;
   `where` = a slide's n · "disk" · "all"), not in a list under the title.
6. **Deck with its draft**: `build_deck.py` writes the topic's own `delivery/`; the level points to it.
7. **Screens retaken, never pasted**: a `screen` visual's `file` comes from a script that takes it from a
   running host (j51's `capture_screens.py`); a `figure` keeps its own shape. `slide_kit.py check` fails a
   visual whose `file` is not on disk.


Sizes and words: a slide draft's own
------------------------------------

A slide draft is one of the shapes that keep their own rules (excalidraw-studio § Shapes): its slides
frame is far past one screen (2800 x 1600), and a half-size slide's words are small by design.
haipipe-studio's `canvas.is_slide_draft` (a drawing named s61-s69) keeps its colours and skips those
checks; excalidraw-studio's `check.py` names it a slide draft and does not judge its sizes or words. The
ask topic is an ordinary topic: excalidraw-studio's principles apply to it.


The kit
-------

`scripts/slide_kit.py`: `ACCENT · ACCENT_FILL · MUTED`, `off_palette(els)` (black · red · green and the
slide accent), `load(path)` and `check(path)` for a `slides.py` (its fields, and every screen or figure
`file` on disk). haipipe-studio's `canvas` keeps the same three colours for builders that read them there,
and leaves a slide draft's colours as drawn.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-studio` | the topic folders (the ask, s61-s69), their faces, sessions, the studio writer and its palette |
| `excalidraw-slide` | how a slide job goes: the ask before the draft, `slides.py`'s fields, the frames, the skeleton, the accent, screens and figures, the deck writer's contract |
| `excalidraw-studio` | how an ordinary topic reads, the ask topic among them; it leaves a slide draft's sizes to this skill |
| `excalidraw-report` | a report's drawing; a scratch |
| `html-ppt` | a standalone HTML deck, when one is asked for |


Files
-----

```text
excalidraw-slide/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/slide-draft.md      the ask, folder, frames, skeleton, colours, slides.py, screens, the deck writer
├── scripts/slide_kit.py    colours, off_palette, load, check
└── tests/test_slide_kit.py
```
