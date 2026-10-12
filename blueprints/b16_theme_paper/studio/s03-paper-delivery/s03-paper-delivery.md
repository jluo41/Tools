s03 · Paper Delivery: the built paper, per version
==================================================

**Tags:** `Structure`

**Stage:** explore

**Topic:** the paper Board's one `delivery/` (b10 s09-D05, s01-D32): each version's built paper sits under
`delivery/jNN_<version>/` (LaTeX, Word, cover letter), and each Section's own output under
`delivery/jNN_<version>/tNN_<section>/`. haipipe-paper-assemble builds the paper from the Sections'
outputs; haipipe-delivery owns the folder and the rule that only a person marks a send done. This topic
settles what paper adds: the lanes a paper needs, how versions sit side by side, and what a send freezes.

**Feeds:** `reports/` q02_venues_related_built


Files
-----

```text
s03-paper-delivery/
├── s03-paper-delivery.md          this face
├── s03-paper-delivery.excalidraw  one frame: where it sits, what b10 gives, what is open
├── s03-paper-delivery.png         its preview
└── build_s03_paper_delivery.py    the builder (the person's marks are kept)
```


Decided
-------

(none yet: a decision is one line, s03-DNN · <what was decided> (<who> <date>))


Open
----

1. The Board's Delivery: each version side by side, or the newest first? (was s33 open 1)
2. The cover letter and a rebuttal letter: a Section Task's output, or the version's own?
3. A sent version: which files freeze, and where does the send's decision live? (was s33 open 3)
4. The supplement: its own lane, or inside latex/?

(write here, or mark the drawing in red)
