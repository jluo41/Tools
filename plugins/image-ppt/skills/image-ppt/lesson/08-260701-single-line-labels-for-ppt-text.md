# Lesson 08: Keep text editable through a naïve SVG→PowerPoint import — make labels single-line

## The Problem
The user's delivery path was "convert the master SVG to PowerPoint myself." PowerPoint's built-in
SVG importer (Insert → Picture → SVG, then Convert to Shape) splits a single multi-line `<text>`
element (one `<text>` with several `<tspan>` lines) into **one text box per line** — so a two-line
label like "Voice &" / "Robots" arrived in the deck as two detached boxes, and some shapes came in
slightly skewed.

## The Symptom
After the user imports the SVG, every wrapped label is broken into separate, individually-draggable
text boxes; retyping a label means editing two or three fragments.

## The Solution
When the deliverable will be imported into PowerPoint as *editable text* (not the svgBlip route —
see Lesson 05), author each label as a **single-line `<text>`** so it imports as one box:
- Collapse wrapped labels to one line (`lines:[...]` → `content:"..."` in items.json).
- **Overflow is acceptable** — a single-line label that runs past its card, or two long labels that
  meet in the middle, is fine because the user repositions boxes in PowerPoint anyway.
- Where single-line genuinely can't fit (runs off-slide, or protrudes from a narrow card so badly
  it's unreadable in the SVG itself), keep those few wrapped and say which — you can't have it both
  ways for those.
- Multi-part titles that stack (a hero title like "AI Care / Transformation / Platform") are best as
  **separate single-line `<text>` items**, one per line — each is then its own clean box.

## Why It Works
The importer keys off `<text>` element boundaries, not visual lines. One `<text>` per label ⇒ one
box; multiple `<tspan>` lines inside a `<text>` ⇒ multiple boxes. Collapsing to a single physical
line removes the tspans, so there's nothing for the importer to fragment.

## When to Apply
Any time the user will round-trip the SVG through PowerPoint's SVG import (or a similar converter)
and wants editable native text boxes — and is willing to trade the tidy two-line wrapping for
one-box-per-label integrity.

## Caveats
This is the opposite trade from Lesson 05 (embed as svgBlip → Convert to Shape keeps wrapping but
requires that workflow). Pick per delivery: **svgBlip** when you control the export and want layout
fidelity; **single-line labels** when the user imports the raw SVG and wants clean editable boxes.
A native-textbox PPTX exporter (background image + one text box per label) sidesteps both — see the
compose/export feedback.
