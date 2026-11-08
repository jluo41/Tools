s07 · The venue’s displays, as examples
=======================================

**Tags:** `Plan`

**Stage:** explore

**For:** the authors choosing each display's layout: the venue's published figures and tables on one canvas, beside ours

**Delivery type:** display

**Covers:** <which published papers of the venue>, their figures and tables as pictures, and which of our displays
each one is compared with

**Excluded:** the plan of our displays (`s06-paper-displays`); drawing them (the Runs of `j01_evidence_display`)

**Topic:** <the target venue's recent papers>: their figures and tables on one canvas, so each of our displays is
drawn the way the venue's readers already read them. Until the pictures are pasted in, a placeholder box stands where
each published display goes.

**Feeds:** `j01_evidence_display` (each display Task's layout) and `s06-paper-displays` (the plan's open choices)


### Examples

The builder reads this block on every build; a pasted picture of a published display goes on the canvas itself.

```yaml
key: "<what the venue’s displays share: one panel, few colours, each estimate with its interval>"
examples:
  - {name: "<paper A> · Figure 1", shows: "<bars by group>", sketch: bars, ours: "Display A"}
  - {name: "<paper B> · Figure 2", shows: "<a trend over time>", sketch: line, ours: "Display A"}
  - {name: "<paper C> · Figure 3", shows: "<estimates with intervals>", sketch: dots, ours: "Display C"}
  - {name: "<paper A> · Table 1", shows: "<the sample at baseline>", sketch: table, ours: "Display B"}
  - {name: "<paper D> · Table 2", shows: "<the main estimates>", sketch: table, ours: "Display B"}
ours:
  - {name: "Display A", kind: "<figure: outcome by group>"}
  - {name: "Display B", kind: "<table: sample at baseline>"}
  - {name: "Display C", kind: "<figure: placebo check>"}
open: "? <which example Display C should follow>"
```


Files
-----

```text
s07-paper-display-examples/
├── s07-paper-display-examples.md           this face
├── s07-paper-display-examples.excalidraw   the canvas (build_s07_paper_display_examples.py; marks kept)
├── s07-paper-display-examples.png          its preview, read by the Board's Displays › Examples
└── build_s07_paper_display_examples.py     the builder
```


Decided
-------

(none yet: a decision is one line, s07-D01 · <what was decided> (<who> <date>))


Open
----

1. <which published papers of the venue to take the examples from>
2. <which example Display C should follow>

(write here, or mark the drawing in red)
