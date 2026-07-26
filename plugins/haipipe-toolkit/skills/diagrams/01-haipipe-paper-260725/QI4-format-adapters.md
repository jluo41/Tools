# Display adapters for every output
state: 🟡 PARTIAL
owner: JL
method: keep rendering reusable and let each consumer embed the result natively

## Question
Who turns a rendered Display into LaTeX, Word, HTML, slides, or a poster?

A renderer should not bake paper-specific captions, labels, and float placement into a supposedly generic asset. The consuming delivery layer knows whether the result must become a LaTeX float, a native Word table, an HTML figure, or a slide object.

## Boundary
- ✅ Covered here
  Consumer-side embedding and the special case of editable tables.
- ↪ Covered elsewhere
  Whole-document projections are `QC3`; the generic render bundle is `QI2`; semantic Display identity is `QBa4`.

## Content
### Adapter ownership
```
paper LaTeX adapter   float.tex, caption, label, width, placement
paper Word adapter    native paragraph, caption, cross-reference, editable table
Board HTML adapter    preview, semantic link, hover card
slides/poster         copy or place the accepted asset into the composition
```

### Portable visuals
Plots and diagrams can usually travel as SVG, PDF, or PNG plus a rebuild spec.
The consumer chooses the representation appropriate for its target.

### Tables are different
A LaTeX `tabular` is not an editable Word table.
The reusable table output therefore needs semantic data and a table spec from which LaTeX, Word, and HTML representations can be generated.

## Items to Finish
- [x] 🔌 Put embedding on the consumer side
      Generic renderers return assets and sources rather than manuscript placement.
- [ ] 📐 Define the semantic table spec
      Rows, columns, labels, notes, emphasis, precision, and provenance must survive target conversion.
- [ ] 🧱 Define adapter interfaces
      Each adapter must preserve stable Display identity and format-specific cross-references.
- [ ] 🧪 Render one table into all three document formats
      Values, notes, emphasis, caption, and provenance must agree.

## Where we are
The adapter boundary is selected.
Current table rendering is LaTeX-first and current unit renderers still write paper-specific `float.tex`.

## Files
- `display/skills/haipipe-display-table/SKILL.md`
  Current LaTeX-only table renderer.
- `paper/3-deliver/`
  Likely home of paper target adapters.
