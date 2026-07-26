# Renderer families and utilities
state: 🟡 PARTIAL
owner: JL
method: classify by artifact semantics first and implementation engine second

## Question
Which Display skills should be user-facing renderers, composers, or internal engines?

The current folder mixes paper unit renderers, whole-deck composers, and vendored HTML engines under one flat `skills/` directory. A clear taxonomy makes triggering predictable and prevents a low-level converter from owning high-level content decisions.

## Boundary
- ✅ Covered here
  The public renderer set, composer set, naming, and the place of utility engines.
- ↪ Covered elsewhere
  The ownership boundary is `QI1`; renderer inputs and outputs are `QI2`.

## Content
### Unit renderers
```
haipipe-display-table          structured table
haipipe-display-plot           data plot, currently named figure
haipipe-display-diagram        deterministic editable vector diagram
haipipe-display-illustration   generative conceptual image
```

### Composers
```
haipipe-display-slides
haipipe-display-poster
```

### Internal engines
`html-ppt`, `html-to-svg`, FigureSpec SVG code, Draw.io, Excalidraw, and image-generation bridges are engines or utilities.
They may be called by a renderer or composer without becoming the semantic owner of the result.

### Router
A thin `haipipe-display` router may choose among the public skills from the requested artifact kind.
It should not contain the rendering manuals itself.

## Items to Finish
- [x] 🧭 Separate renderers, composers, and engines
      The three groups have different contracts and trigger surfaces.
- [ ] 🏷 Rule `figure` versus `plot`
      In papers, figure can mean any visual Display, while this renderer handles only data plots.
- [ ] 📦 Correct plugin packaging
      The current `display/.claude-plugin/plugin.json` identifies the plugin as `html-ppt`, not the Display family.
- [ ] ✂️ Compact oversized skills
      Poster exceeds the preferred skill size and live folders contain history and feedback material.

## Where we are
The public skills already exist.
Their taxonomy, plugin identity, and runtime compactness are not yet coherent.

## Files
- `display/.claude-plugin/plugin.json`
  Current plugin identity.
- `display/skills/`
  Renderers, composers, and vendored engines mixed together.
