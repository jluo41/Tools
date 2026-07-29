# Renderer families and utilities
state: 🟡 PARTIAL
owner: JL
method: classify by artifact semantics first and implementation engine second

## Question
Which Display skills should be user-facing renderers, composers, or internal engines? The folder currently mixes all three, so a reader cannot tell from a name what is safe to call, and discovers by reading it that a public skill is really an internal one.

The current folder mixes paper unit renderers, whole-deck composers, and vendored HTML engines under one flat `skills/` directory. A clear taxonomy makes triggering predictable and prevents a low-level converter from owning high-level content decisions.


The approach is to classify each skill by its role, unit renderer, composer, or internal engine, and let that decide whether it is public. What we want is for a reader to know from the name what a skill is for, instead of discovering by reading it that a public skill is really an internal one.
## Boundary
- ✅ Covered here
  The public renderer set, composer set, naming, and the place of utility engines.
- ↪ Covered elsewhere
  The ownership boundary is `QD1`; renderer inputs and outputs are `QD2`.

## Diagram
```
 THREE TIERS, AND THE MIDDLE ONE IS WHERE MEANING LIVES

 ┌ UNIT RENDERERS ── public, one artifact each ────────────────┐
 │ haipipe-display-table          a structured table           │
 │ haipipe-display-plot           a data plot   (today: -figure)│
 │ haipipe-display-diagram        deterministic editable vector │
 │ haipipe-display-illustration   generative conceptual image   │
 └─────────────────────────────────────────────────────────────┘
 ┌ COMPOSERS ── public, whole artifacts ───────────────────────┐
 │ haipipe-display-slides · haipipe-display-poster             │
 └─────────────────────────────────────────────────────────────┘
 ┌ INTERNAL ENGINES ── callable, never semantic owners ────────┐
 │ html-ppt · html-to-svg · FigureSpec SVG · Draw.io ·         │
 │ Excalidraw · image-generation bridges                       │
 └─────────────────────────────────────────────────────────────┘

 THE FLAT FOLDER IS THE PROBLEM
   today skills/ mixes all three. A user cannot predict what
   triggers, and a low-level CONVERTER can end up owning a
   high-level CONTENT decision, which is the QD1 failure exactly.

 THE ROUTER, AND ITS ONE CONSTRAINT
   a thin haipipe-display picks among the PUBLIC skills from the
   requested artifact kind.
   ⛔ it must not contain the rendering manuals itself, or it
      becomes a fifth renderer wearing a router's name.

 ONE RENAME IS OWED
   -figure renders PLOTS. A diagram and an illustration are also
   figures, so the name claims the whole category and delivers
   one member of it.
```

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

### One unit shape, several renderers
The renderer kind selects the recipe and output representation, not a different unit anatomy.
Every paper-facing result returns through the same `intake/ → recipe/ → candidates/ or assets/ → float.tex → preview.pdf` route, with legacy `source/` units explicitly marked until migrated.

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
