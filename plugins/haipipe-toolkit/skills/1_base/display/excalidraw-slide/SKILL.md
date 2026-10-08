---
name: excalidraw-slide
description: >-
  Draw a slide draft: a deck proposed on one Excalidraw canvas before it is built, as a studio topic
  s61-s69. One `slides.py` is the ONE source that the drawing and the deck both read (AUDIENCE · LENGTH
  · SHOWN · GROUPS · SLIDES · OPEN; each slide n · slug · group · title · headline · ONE visual · caption ·
  source · next · notes, an optional ask in red). The canvas reads left to right: 1 logic flow (one box per slide, why the next
  follows) · 2 the slides at half size in one skeleton · 3 on disk and the open questions. Black around
  the slides; inside a slide one accent marks its key thing. The deck is generated into the topic's own
  delivery/. Use to propose, draw, check or revise a deck before building it. Trigger: slide draft,
  propose a deck, slides.py, deck outline, logic flow of a talk, s61, presentation draft,
  /excalidraw-slide.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.1.3"
  last_updated: "2026-10-08"
  # version history: ./CHANGELOG.md
---

# /excalidraw-slide · a deck on one canvas, before it is built

A slide draft lets the person read the whole argument and every slide at once, mark it, and agree it
before a deck is written (JL 261007: "one type is about propose the slide draft"). It is a studio topic
numbered s61-s69; its folder, face and sessions are `haipipe-studio`'s, and how it is drawn is this
skill's.

```text
slides.py ─▶ build_s6N_<deck>.py ─▶ s6N-<deck>.excalidraw ─▶ the person marks it ─▶ build_deck.py ─▶ delivery/
(one source)   (the drawing)          1 logic · 2 slides · 3 open    (agreed)               (.pptx · .pdf)
```

Read `ref/slide-draft.md` before drawing one: the folder, the frames, the slide skeleton, the colour
exception, the fields of `slides.py`, and the deck writer.


Make one
--------

```bash
python Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/new_topic.py \
  topic <level> --slug <deck> --title '<title>' --band slides          # studio/s6N-<deck>/
# write slides.py (ref/slide-draft.md § slides.py), then its builder, then:
python Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-slide/scripts/slide_kit.py check <topic>/slides.py
```

1. **One source**: the drawing and the deck read `slides.py`; never type a slide into either.
2. **Left to right**: logic flow · the slides · on disk and open, side by side.
3. **One skeleton**: every slide at half size: title and rule, headline, ONE visual, caption, number.
4. **Colour inside a slide only**: `ACCENT` marks the key thing, `MUTED` the caption; around them black,
   red for an open question, green for a change.
5. **Notes in place**: a change note sits under the slide it changed (`CHANGES` as `(where, date, what)`;
   `where` = a slide's n · "disk" · "all"), not in a list under the title.
6. **Deck with its draft**: `build_deck.py` writes the topic's own `delivery/`; the level points to it.


The kit
-------

`scripts/slide_kit.py`: `ACCENT · ACCENT_FILL · MUTED`, `off_palette(els)` (black · red · green and the
slide accent), `load(path)` and `check(path)` for a `slides.py`. haipipe-studio's `canvas` keeps the
same three colours for builders that read them there, and leaves a slide draft's colours as drawn.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-studio` | the topic folder s61-s69, its face, its sessions, the studio writer and its palette |
| `excalidraw-slide` | how a slide draft is drawn: `slides.py`'s fields, the frames, the skeleton, the accent, the deck writer's contract |
| `excalidraw-report` | a report's drawing; a scratch |
| `html-ppt` | a standalone HTML deck, when one is asked for |


Files
-----

```text
excalidraw-slide/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/slide-draft.md      the folder, frames, skeleton, colours, slides.py, the deck writer
├── scripts/slide_kit.py    colours, off_palette, load, check
└── tests/test_slide_kit.py
```
