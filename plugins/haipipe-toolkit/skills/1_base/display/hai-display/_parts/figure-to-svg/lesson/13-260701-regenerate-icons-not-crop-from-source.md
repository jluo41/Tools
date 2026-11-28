# Lesson 13: Regenerate icons from a reference — don't crop them from the source

## The Problem
On a dense multi-icon figure, cropping each icon out of the source (hand-read bboxes,
`crop_qc`, even SAM) produced mis-located, contaminated crops — a "hospital" crop that was
actually the title text, panel crops that were just text fragments.

## The Symptom
User: *"the performance is very bad, I delete them."* Repeated frustration; crop contact
sheets full of clipped text and neighbour bleed.

## The Solution
Don't localize-and-cut. **Regenerate.** Feed the section image to an image model (Codex native
image-gen via the `codex-image2` bridge) as a *reference* and ask it to redraw ALL the section's
icons as ONE regular grid; then slice the grid by equal division. The grid is regular *by
construction*, so slicing needs no detection.

## Why It Works
LLMs and vision models are poor at absolute pixel coordinates — **localization is the weak
link**. A generated regular grid removes localization entirely: cut positions are `image_size / N`.
The model is strong at redrawing a clean icon from a reference, weak at telling you exactly where
it sits in a busy source.

## When to Apply
Multi-icon infographics/figures where icons sit among text, on coloured panels, or touch
neighbours — especially when clean, editable, recolourable icons are the goal.

## Caveats
Regenerated icons are look-alikes, not pixel copies. Preserve any baked reading (e.g. "72",
"5.8", "!") with an explicit prompt instruction. If the figure is already discrete vectors
(a source PPT/SVG exists), reuse that instead — don't regenerate. Not for exact-fidelity
reproduction requirements.
