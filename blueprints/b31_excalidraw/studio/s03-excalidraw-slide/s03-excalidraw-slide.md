s03 · excalidraw-slide: a deck proposed before it is built
==========================================================

**Stage:** agreed

**Topic:** what the skill `excalidraw-slide` makes and how, told on one real slide job: j51, a five-minute
demo of looped experimental learning (DrFirst-SPACE, paper Paper-TestToLearn-MS2026). Its ask came from a
meeting on 2026-10-05 (j51 s01 what they want); its layout was marked and agreed on one canvas (j51 s61 demo
layout); one `slides.py` fed the drawing and the deck; the 14-slide deck was shown on 2026-10-08. This topic
draws that job, the deck it made, its two drawings, and what the skill should take from it. A slide draft keeps
its own colours by design; this topic's own drawing follows excalidraw-studio's principles.

**Feeds:** none yet


Files
-----

```text
s03-excalidraw-slide/
├── s03-excalidraw-slide.md              this face; the drawing's words are its yaml blocks
├── build_s03_excalidraw_slide.py        the builder; reads this face and j51's own files
├── s03-excalidraw-slide.excalidraw      four frames in two acts
├── s03-excalidraw-slide.png             its preview
├── examples/j51/                        j51's 14 slides, its two previews and facts.json, refreshed on each build
└── history/                             the first drawing (p01, the skill and the b11, b12 drafts)
```


What the drawing holds
----------------------

Four frames in two acts, a row each, named at the left; every frame has a badge and one key point. Words
written `<<name>>` are facts the builder reads from j51's files (its `slides.py`, its two builders, its faces,
its `delivery/`). When j51 is not beside Tools-SPACE, the builder reads the snapshot in `examples/j51/`.

```yaml
example:
  job: j51_insight_design_demo
  path: ../DrFirst-SPACE/examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026/j51_insight_design_demo
  snapshot: examples/j51
```

```yaml
acts:
- name: "Act 1 · The example: j51, a five-minute demo"
  frames: [①, ②]
  arrow: made
- name: "Act 2 · What excalidraw-slide takes from it"
  frames: [③, ④]
  arrow: teaches
between: {from: ①, to: ③, label: drawn first as}
```

```yaml
job_map:
  title: "🔁 j51: from a meeting to a deck in <<days>> days"
  sub: "A five-minute demo for <<audience>>, read from j51's own files: the ask from a meeting, one slides.py, a layout a person marks until it is agreed, then the deck."
  steps:
  - title: "🗣️ The meeting"
    lines:
    - "<<meeting>>, <<minutes>> minutes, a transcript"
    - "the ask in their words, each with its timestamp"
    - "people named by role only"
  - title: "🎯 s01 · What they want"
    lines:
    - "for <<audience>>"
    - "<<length>>"
    - "<<n_time>> dates: what is due when"
    - "<<n_pains>> pains, each answered by a slide"
  - title: "📄 slides.py, the one source"
    key: true
    lines:
    - "<<n_slides>> slides in <<n_groups>> groups"
    - "each: title, headline, ONE visual, caption, next, notes"
    - "slide_kit.py check: <<check>>"
  - title: "🧭 s61 · The layout"
    lines:
    - "build_s61_demo_layout.py draws it from slides.py"
    - "1 logic flow · 2 the slides at half size · 3 on disk"
    - "<<n_screens>> screens and <<n_figures>> figures inside"
  - title: "👤 A person marks it"
    lines:
    - "red for an open question, green for a change"
    - "<<n_changes>> change notes, <<change_dates>>"
    - "<<n_open>> questions still open"
  labels: [the ask, written into, drawn as, read by]
  back: "a change goes into slides.py; the layout is drawn again"
  agreed: agreed
  deck:
  - title: "📦 build_deck.py"
    lines:
    - "reads the same slides.py"
    - "python-pptx: native boxes and arrows, a picture where a screen is"
    - "the PDF exported by PowerPoint"
  - title: "📑 delivery/"
    lines:
    - "<<delivery>>"
    - "<<pages>> slides, speaker notes on each"
    - "generated, never edited"
  - title: "📽️ Shown <<shown>>"
    lines:
    - "to <<audience>>"
    - "<<length>>"
  deck_labels: [writes, shown]
  pains_title: "🎯 What hurts, and the slide that answers it (s01, from the meeting)"
  pains_arrow: "each pain answered by a slide"
```

```yaml
deck_grid:
  title: "🎞️ The deck it made: <<n_slides>> slides in <<n_groups>> acts"
  sub: "Rendered from j51's <<pdf>>; each row is one group of slides.py, named at the left with what the room should leave with."
  key: "<<group_names>>: <<group_counts>> slides; every slide is one skeleton: a title, a one-sentence headline, ONE visual, a caption"
```

```yaml
drawings:
  title: "🧭 Two drawings before any deck: the ask and the layout"
  sub: "j51's two Studio topics, as their previews are on disk. s01 holds what they want, from the meeting; s61 holds every slide, drawn from slides.py, with a person's red and green marks under each."
  key: "The deck is agreed on these two canvases first; build_deck.py runs only after"
  left: "j51 s01 · What they want"
  middle: "j51 s61 · Demo layout"
  tree: "📁 s61-demo-layout/ on disk"
```

```yaml
mindmap:
  title: "🧠 excalidraw-slide, as j51 teaches it"
  sub: "What a slide job needs, each branch read from what j51 did; ⏳ is what the skill (v<<version>>) leaves for later."
  centre: "A slide job: the ask, then one slides.py, a layout agreed on a canvas, then the deck"
  branches:
  - title: "🎯 The ask comes first"
    summary: "a topic before the draft says what they want"
    leaves:
    - "j51 s01: who, how long, what is due when, from the meeting"
    - "each pain names the slide that answers it"
    - "<<gap_ask>>"
  - title: "🧭 Groups tell the story"
    summary: "slides in acts, each with what the room should leave with"
    leaves:
    - "<<groups>>"
    - "each slide's next says why the next one follows"
  - title: "📄 One slides.py"
    summary: "the drawing and the deck read the same file"
    leaves:
    - "j51: <<check>>"
    - "<<drafts>>"
  - title: "🔲 One skeleton"
    summary: "title, headline, ONE visual, caption, notes"
    leaves:
    - "visual kinds in j51: <<kinds>>"
    - "hl: the one accent on each slide"
  - title: "🖼️ Real screens, never pasted"
    summary: "a script retakes them from a running host"
    leaves:
    - "capture_screens.py → screens/: <<screens>>"
    - "figures/: <<figures>>"
    - "<<gap_pics>>"
  - title: "📦 The deck beside its draft"
    summary: "generated into the topic's own delivery/"
    leaves:
    - "build_deck.py: python-pptx, the PDF by PowerPoint"
    - "the Job's delivery/ points to it"
    - "⏳ later: build_deck.py is copied into each topic"
  - title: "✍️ Marks in place"
    summary: "a change note under the slide it changed"
    leaves:
    - "<<n_changes>> notes in j51 s61: <<per_slide>>"
    - "a slide's ask: red in the draft; j51 also shows it in its deck, its own choice"
  - title: "🔧 What the skill took from j51"
    summary: "<<closed>> of <<gaps>> gaps closed in v<<version>>"
    leaves:
    - "<<gap_ask>>"
    - "<<gap_j51>>"
    - "<<gap_sizes>>"
    - "<<gap_deck>>"
```


Decided
-------

- s03-D01 · Created (asked 261012: "for the excalidraw report, slide, read, and section, we should have the
  s02, 03, 04, 05 for them as well. Please go ahead and do it."): the topic on excalidraw-slide, beside b31 s01
  (excalidraw-studio)
- s03-D02 · Redrawn around j51 (asked 261012: "for the s03, it is very bad, I think you should use the examples
  from .../Paper-TestToLearn-MS2026, there is a slide job, and I think you can make it."): Act 1 is j51's job as a
  map and the 14-slide deck it made; Act 2 is its two drawings and what the skill takes from it. The first
  drawing (the skill's own files and the b11, b12 drafts) is in `history/`.
- s03-D03 · The first Open 1 has narrowed, read live 261012: the b11 and b12 drafts now carry every slide field,
  but each still fails on one error (no OPEN) with three warnings (no AUDIENCE, LENGTH, SHOWN); j51's slides.py
  passes clean. What is left is Open 7.
- s03-D04 · The skill updated from j51 (asked 261012: "could you update the skills of the excalidraw-slide?"):
  excalidraw-slide 0.2.0 has the ask as step 0 (ref § The ask, before the draft), j51 as the slide job to
  copy, screens and figures named by `file` and checked on disk, and a slide draft's own sizes written down
  (excalidraw-studio 0.2.3's check.py names a slide draft and does not judge them). Opens 1, 2 and 5 settled;
  the mind map's last branch reads each gap from the skill's files.
- s03-D05 · Stage → agreed (JL 261012: "I think for others sNN, we can give them to level 3 as well"): the topic
  tells excalidraw-slide on j51; its four open points (a deck writer, one drawing kit, j51's slides in Tools, b11 and
  b12's OPEN) moved to Later


Open
----

1. Settled 261012 (s03-D04): the ask is the skill's step 0.
2. Settled 261012 (s03-D04): j51 is named in SKILL.md as the slide job to copy.
5. Settled 261012 (s03-D04): a slide draft's own sizes are written in SKILL.md, and check.py names it.

(none open: agreed 261012, s03-D05; 4 points moved to Later)


Later
-----

Not needed now; each comes back as a new point if it is wanted.

1. `build_deck.py` is copied into every topic (the skill has no deck writer yet); when does it move into the skill?
2. each draft keeps its own drawing kit (j51 `_build/sketch.py`, b12 `slide_kit.py`); one in the skill?
3. `examples/j51/` copies DrFirst slides into Tools-SPACE: keep it out of anything shared beyond the team?
4. b11 and b12 still fail the field check on one error each (no OPEN): give them OPEN, AUDIENCE, LENGTH and
   SHOWN, as j51 has?

