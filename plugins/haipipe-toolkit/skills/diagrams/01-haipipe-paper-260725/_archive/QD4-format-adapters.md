# Display adapters for every output
state: ✅ SETTLED
owner: JL
method: keep rendering reusable and let each consumer embed the result natively

## Question
Who turns a rendered Display into LaTeX, Word, HTML, slides, or a poster? Renderers own the visual and adapters own the format, so one render can feed every destination instead of one render being needed per destination.

A renderer should not bake paper-specific captions, labels, and float placement into a supposedly generic asset. The consuming delivery layer knows whether the result must become a LaTeX float, a native Word table, an HTML figure, or a slide object.


The approach is that renderers own the visual and adapters own the format, so captions, labels and float placement are never baked into the picture. What we want is one render feeding LaTeX, Word, HTML, slides and a poster, rather than a separate render per destination.
## Boundary
- ✅ Covered here
  Consumer-side embedding and the special case of editable tables.
- ↪ Covered elsewhere
  Whole-document projections are `QD7`; the generic render bundle is `QD2`; semantic Display identity is `QC3` for a table and `QC4` for a figure.

## Diagram
```
 THE RENDERER MAKES THE ASSET. THE CONSUMER DECIDES WHAT IT BECOMES.

              a rendered display  (QD2's bundle)
                        │
     ┌──────────┬───────┴───────┬──────────────┐
     ▼          ▼               ▼              ▼
 paper LaTeX  paper Word    Board HTML    slides / poster
 float.tex    native ¶      preview       copy or place the
 caption      caption       semantic link accepted asset into
 label        cross-ref     hover card    the composition
 width        EDITABLE
 placement    table

 PORTABLE, and mostly fine
   plots and diagrams travel as SVG · PDF · PNG + a rebuild spec.
   the consumer picks the representation its target wants.

 TABLES ARE DIFFERENT, and this is the whole page  ⚠️
   ┌───────────────────────────────────────────────────────┐
   │ a LaTeX \tabular is NOT an editable Word table.       │
   │ converting one into the other loses the thing a       │
   │ coauthor needs: the ability to edit a cell.           │
   └───────────────────────────────────────────────────────┘
   so a reusable table output cannot be a rendered artifact.
   it has to be   SEMANTIC DATA + A TABLE SPEC,
   from which LaTeX, Word and HTML are each GENERATED.

 THE RULE UNDERNEATH
   a renderer that bakes captions, labels and float placement into
   a "generic" asset has made a paper-specific thing and called it
   reusable.  Same failure as QD2, one layer later.
```

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

### The Board's inspection projection
The Board does not replace the manuscript float with a thumbnail.
For every allocated unit it shows the Current Float first, then the artifact currently referenced by `float.tex`, then Display Versions, the actual unit folder, and finally the authored explanation.
Display Versions lists saved files in `versions/`, unpromoted files in `candidates/`, and non-current files in `assets/`. It marks only the `float.tex` target as current, so a reviewer can inspect alternatives without mistaking a directory listing for approval or chronology.
This lets a reviewer distinguish a caption-and-placement problem, a live-asset problem, an alternative-version question, and a provenance or migration problem without opening the file system separately.

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
