---
name: slide
part-of: haipipe-display
description: "Slide-picture renderer of the display family: each slide is one finished picture made by image generation, in one named style chosen per deck (19 styles: sketch-notes, intuition-machine, ian-handdrawn, glossy-cartoon, blueprint …). Use for idea slides in a Studio topic, a Report deck, or any deck read as pictures. Trigger: slide style, idea slides, sketch-notes, make slides as pictures."
metadata:
  version: "0.1.0"
  last_updated: "2026-10-29"
---

# 🖼 slide · one picture per slide, one style per deck

A slide here is a finished picture, not an editable text box: the image model draws the whole page, words included.
The deck names its look once, as a parameter; every slide in it is drawn in that look.

```text
<name>.slides.json   {"style": "sketch-notes", "slides": [{"id", "idea", "content", "image", "notes"}]}
        │
slide_prompt.py      base-prompt.md + styles/<style>.md + the slide's content
        │
codex-image2         one picture per slide ─▶ the caller gathers them (Studio: topic_slides.py ─▶ .html + .pptx)
```

## Scratch first, pictures when asked

1. **A scratch first**: a new slide is its `content` block in `.slides.json` and its leaf's drawing; no image call.
2. **Pictures when asked**: draw a slide's picture only when the person asks for it; each one costs an image call
   (JL 261029: "could you first try to make the quick scratch, and later we can draw the images? the images are
   expensive").

## The style is a parameter

1. **One per deck**: `"style"` at the top of `.slides.json`; never mixed inside a deck.
2. **Any file in `styles/`**: `python scripts/slide_prompt.py --styles` lists them with their look.
3. **Defaults by caller**: a Studio deck `sketch-notes` (JL 261029: "sketch note looks great"); a Report deck
   `intuition-machine` (not yet tried).
4. **Changing it**: change the word, then redraw every slide (one image call each, about 50 seconds).
5. **A new look**: add `styles/<name>.md` in the same shape (look line, background, type, palette, elements,
   density, do and don't, best for).

| Style | Where it came from | Use |
|---|---|---|
| `sketch-notes` | baoyu-skills | Studio: open ideas, hand-drawn, pulls you in |
| `intuition-machine`, `scientific`, `blueprint` | baoyu-skills | settled, technical explanations |
| 14 more baoyu looks | baoyu-skills | `--styles` lists them |
| `ian-handdrawn` | Ian Handdrawn PPT, by Ian | calm article figures; too quiet for a Studio |
| `glossy-cartoon` | b15 deck v12 | launch-style summaries; reads finished |

## Making one slide

1. Write the slide's `content` by `content-rules.md`: headline that says the point, text groups with what is
   drawn, layout, focal point; at most four text groups, short words.
2. `python scripts/slide_prompt.py --deck <folder> --slide NN` prints the full prompt.
3. Send it to `mcp__codex-image2__generate_start` (its `outputPath` must sit under the SPACE's
   `figures/ai_generated/`), poll `generate_status`, then copy the picture to the deck's `image` path.
4. **Look at it before keeping it**: every word spelled right, the focal point first, nothing crowded. A wrong word is
   a new prompt and a new picture, never a paint-over.

## Sources and credit

`styles/` holds 17 files copied unchanged from baoyu-skills (JimLiu, MIT) and two written here; each file's first line
names its source. `base-prompt.md` and `content-rules.md` are adapted from the same skill. `ian-handdrawn` is adapted
from Ian Handdrawn PPT by Ian (MIT; the author asks for credit). Both upstreams sit read-only in
`Tools/references/baoyu-skills` and `Tools/references/ian-handdrawn-ppt`; re-copy from there to update.
