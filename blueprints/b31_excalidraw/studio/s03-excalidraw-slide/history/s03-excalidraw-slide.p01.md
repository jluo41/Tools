s03 · excalidraw-slide: a deck proposed before it is built
==========================================================

**Stage:** explore

**Topic:** what the skill `excalidraw-slide` makes and how. A slide draft puts a whole talk on one canvas
before any deck exists: one source, `slides.py`, feeds both the drawing and the deck, so the argument and every
slide can be read, marked and agreed first. This topic reads the skill's own files (SKILL.md, CHANGELOG.md,
`ref/slide-draft.md`, `scripts/slide_kit.py`) and the two slide drafts made with it so far, and draws what it
makes, how it flows, where it lives and what it has made. It sits beside s01 (the principles) and the topics
for the other excalidraw skills. A slide draft keeps its own colours by design (one accent inside a slide);
this topic's own drawing follows excalidraw-studio's principles.

**Feeds:** none yet


Files
-----

```text
s03-excalidraw-slide/
├── s03-excalidraw-slide.md              this face; the drawing's words are its yaml blocks
├── build_s03_excalidraw_slide.py        the builder; reads this face, the skill and the drafts from disk
├── s03-excalidraw-slide.excalidraw      four frames in two acts
└── s03-excalidraw-slide.png             its preview
```


What the drawing holds
----------------------

Four frames in two acts, a row each, named at the left; every frame has a badge and one key point. Words
written `<<name>>` are facts the builder reads from disk (the skill's version, its functions, the drafts).

```yaml
acts:
- name: Act 1 · What it draws
  frames: [①, ②]
  arrow: its flow
- name: Act 2 · Where it lives and what it made
  frames: [③, ④]
  arrow: made with it
between: {from: ①, to: ③, label: where it lives}
```

```yaml
mindmap:
  centre: a talk drawn on one canvas, before the deck is built
  branches:
  - title: 📄 slides.py, the one source
    by: standing
    summary: "data only: the drawing and the deck both read it"
    leaves:
    - "module fields: AUDIENCE, LENGTH, SHOWN, GROUPS, SLIDES, OPEN"
    - "a slide: n, slug, group, title, headline, ONE visual, caption, source, next, notes, ask"
    - "checked by slide_kit.py check (errors and warnings)"
  - title: 🖼️ the frames
    by: standing
    summary: "three frames read left to right"
    leaves:
    - "1 logic flow: one box per slide, the arrow words say why the next follows"
    - "2 the slides at half size, in one skeleton"
    - "3 on disk, and the open questions under it"
  - title: 🔲 the slide skeleton
    by: standing
    summary: "same shape every slide: title, headline, one visual"
    leaves:
    - "half size, 800 x 450 of 1600 x 900"
    - "title and rule, headline, ONE visual, caption, number"
    - "a visual kind (cover, timeline, cycle, flow, table, tree, screen, converge) has a renderer in both builders"
  - title: 📦 the deck
    by: standing
    summary: "made after the draft is agreed, kept beside it"
    leaves:
    - "build_deck.py reads the same slides.py"
    - "writes the topic's own delivery/ (.pptx and .pdf)"
    - "the PDF comes from a temporary copy of the .pptx, never the person's open file"
  - title: 🎨 its colours
    by: standing
    summary: "colour only inside a slide"
    leaves:
    - "ACCENT marks the key thing and the title rule, MUTED the caption"
    - "around the slides: black; red an open question; green a change"
    - "off_palette(els) lists any colour outside these"
  - title: 🧰 the kit and the notes
    by: standing
    summary: "<<n_funcs>> functions in slide_kit.py, notes in place"
    leaves:
    - "<<funcs>>"
    - "a change note sits under the slide it changed (CHANGES: where, date, what)"
    - "❓ the draft's colours: is_slide_draft in canvas.py keeps them (Open 2)"
```

```yaml
flow:
  steps:
  - title: 📄 slides.py
    lines:
    - "the one source, data only"
    - "slide_kit.py check reads it"
    - "one file per draft"
  - title: ⚙️ build_s6N_<deck>.py
    lines:
    - "draws the topic's canvas from slides.py"
    - "keeps a person's marks (canvas.write)"
  - title: 🖼️ s6N-<deck>.excalidraw
    key: true
    lines:
    - "1 logic flow"
    - "2 the slides at half size"
    - "3 on disk and open"
  - title: 👤 the person marks it
    lines:
    - "red marks, comments, a slide's ask"
    - "the draft is changed and rebuilt until agreed"
  - title: 📦 build_deck.py
    lines:
    - "reads the same slides.py"
    - "lives in each topic, not in the skill (Open 1)"
  - title: 📑 delivery/
    lines:
    - "<deck>.pptx and <deck>.pdf"
    - "generated, never edited"
  labels: [build, open it, agree, write, generate]
loop: "a change goes into slides.py, then the builder is run again; neither the drawing nor the deck is edited by hand"
```

```yaml
checks:
- "1 one screen: a draft's frames are far past 2800 x 1600; the skill keeps them (slides are the exception, Open 2)"
- "2 a map inside: the logic flow is a map of boxes and arrows; the slides are a grid of the same skeleton"
- "3 acts and named arrows: three frames left to right, no acts; each logic arrow carries its words"
- "4 folder tree only for folders: frame 3 draws a real folder, so it fits"
- "5 big words, one colour: slide text is small by design (a half-size slide); the accent is its one colour"
- "6 density: shown in each frame's badge, measured from the drawing's own file"
```


Decided
-------

- s03-D01 · Created (asked 261012: "for the excalidraw report, slide, read, and section, we should have the
  s02, 03, 04, 05 for them as well. Please go ahead and do it."): the topic on excalidraw-slide, beside b31 s01
  (excalidraw-studio)


Open
----

1. ❓ the skill's contract and the two real drafts differ: the drafts' slides.py use bullets, lead, picture, src
   (no headline, visual, caption, next, OPEN) and `slide_kit.py check` errors on both; which is right?
2. ❓ the drafts' frames pass 2800 x 1600 and use 9 px words; canvas.py's is_slide_draft skips those checks,
   but the skill never says so; write it in SKILL.md?
3. ❓ `build_deck.py` is copied into every topic (the skill has no deck writer yet); when does it move into the skill?
4. ❓ each draft keeps its own copy of `slide_kit.py` (b12) or loads another's (b11); one copy in the skill?

(write here, or mark the drawing in red)
