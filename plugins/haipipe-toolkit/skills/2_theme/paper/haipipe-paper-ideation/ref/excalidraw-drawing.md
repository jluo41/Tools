How the s01-ideation topic is drawn by excalidraw-ideation and what each part of the drawing reads from the face; moved from SKILL.md.

## 🖼️ The drawing: excalidraw-ideation, when installed (JL 261014)

`s01-ideation/` is drawn by `excalidraw-ideation` whenever that skill is installed (JL 261014:
"haipipe-paper-ideation will call it to draw when it is available"). After every change to the ideas (a sync, a
test, a pilot, the G0 choice), refresh the drawing's words and redraw:

```bash
I=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-ideation/scripts/ideation_drawing.py
python $I make s01-ideation       # once: the forwarding builder and s01-ideation-drawing.yaml
python s01-ideation/build_s01_ideation.py
```

The words in `s01-ideation-drawing.yaml` are a projection of this face, never a second record:

| drawing | from this face |
|---|---|
| ① the question and every idea as steps | Direction; Ideas (ranked) in order; Eliminated / Merged / Deferred as the last group |
| ② the setting, in numbers on disk | Direction and Discovery Landscape: the data the ideas stand on |
| one card per lead idea | its Idea division: Why it matters (Origin / Opportunity), Closest and New (Core Claims / Novelty Check), If we find → it would mean (Expected Outcomes), Now (Pilot Result); the state line from Ideas (ranked) |
| from here to G0 | Next Evidence Queue and Suggested Execution Order and G0 Readiness |
| how it scores, where it goes (⑧) | the lead Idea's test receipts (novelty, pressure, journal fit, the Nature lens) and Journal / Venue Fit; each venue's rules only from a verified `haipipe-paper-venue` contract, else red |

A novelty check (`novelty-check`, `haipipe-ideation test`) lands in the face first: the Idea's Core Claims / Novelty
Check (each claim, its closest work, what stays new, the verdict) and Reviewer's Likely Objection (each reviewer
comment and what was done about it); the drawing then carries its two lines. Each claim's closest work is read from the Board's related-work map,
`s10-related-work-map/`, and its s11-s19 types (haipipe-paper-related) when the Board has them. The lead group is the person's or the machine's recommended attention order, not a selection: the drawing makes no
choice the face does not hold. When `excalidraw-ideation` is not installed, the face stands alone and nothing else
changes.
