One Studio, every Theme
-----------------------

The Studio is the same in every Theme (JL 261030: "how could the haipipe-studio skill will be adopted to different
theme?"): an sNN beside the Jobs or Tasks it serves, its face (`**For:**`, Covers, Excluded), its drawing in five
parts, its `delivery/`, and a render out. A Theme plugs in by three things only: the kinds of delivery its sNN make,
where the render writes, and which skill renders. The Theme's own skill renders; haipipe-studio never builds a paper,
a label set or a release itself.

```text
Theme      an sNN delivers (Block · Job · Task)                      render writes into               rendered by
work       skill design · table contract · display, a figure         a skill, the workbench, a store render_delivery.py, a Task
paper      story · paper version · section                           the Section page, manuscript    haipipe-paper-assemble
display    a figure or table, its slide rules                        the page's displays             haipipe-display
labeling   label contract · items, ground truth, building, scanning,  the labeling Job                haipipe-labeling
           score
design     design goals · design Job · reason ideas, one design,      designs.json, the release       haipipe-design-delivery
           review whole
insight    question map · analysis plan, a release on a freeze ·      the Design handoff              haipipe-insight
           Data, Information, Knowledge, Wisdom
discovery  a question's evidence · a paper's card                     the evidence Bib                haipipe-discovery
cowork     ask, a letter or meeting note                             sent to a person                a person, haipipe-cowork
```

In `delivery/render.yaml` a piece is one of three: a text piece (`from:`, `to:`, `block:`), written between render
markers by `render_delivery.py`; a code piece (`code:`, `by:` a Task); or a Theme piece (`from:`, `rendered_by:` the
Theme's skill), which `render_delivery.py` only reports, since the Theme's skill builds it (the paper's manuscript, a
designs.json release).
