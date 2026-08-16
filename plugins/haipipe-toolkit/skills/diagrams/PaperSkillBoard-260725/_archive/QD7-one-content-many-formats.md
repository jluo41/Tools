# One Content, several projections
state: 🟡 PARTIAL
owner: JL
method: author once in the S page, then render through target-specific adapters

## Question
How can the same section become LaTeX, Word, and HTML without creating three writable manuscripts? Formats are delivery, not authorship. The real questions are what an adapter may do, and what happens when somebody edits the output instead of the source.

The paper needs several delivery formats, but format conversion becomes unsafe when each output is edited as a separate source. The system needs one authored Content model and explicit one-way projections whose style rules belong to the target format.


The approach is one authored Content with format adapters hanging off it, never three parallel manuscripts. What we want is to be able to hand someone a Word file without creating a second source of truth that will quietly diverge from the one the board reviews.
## Boundary
- ✅ Covered here
  The source-to-output direction and the ownership of LaTeX, Word, and HTML adapters.
- ↪ Covered elsewhere
  What the canonical stage artifact is comes from `QB2d`; sentence attachments are `QC1` to `QC4`, one page per type; Display embedding is `QD4`.

## Diagram
```
 ONE AUTHORED CONTENT, THREE PROJECTIONS, ZERO ROUND TRIPS

                    S page  ## Content
                    the one authored semantic structure
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   LaTeX adapter       Word adapter        HTML adapter
   section .tex        native DOCX ¶       board / web view
   bib style           citation fields     hover apparatus
   float refs          tables              sentence lanes

 WHAT BELONGS TO THE ADAPTER, NOT TO THE SENTENCE
   AMA numbering · author-year · \citep vs (Author, Year) · Word fields
   these are OUTPUT decisions. A sentence that carries three competing
   syntaxes is three manuscripts wearing one file's name.

 THE UNRESOLVED EDGE: a coauthor edits the Word file
   ┌───────────────────────────────────────────────────┐
   │ safe   while conversion stays ONE-WAY             │
   │ ⚠️     the moment someone edits the output        │
   └───────────────────────────────────────────────────┘
   two answers, and the ruling has to pick one:
     A  backport the change into the S page
     B  declare the manuscript has CROSSED into a new authoritative
        mode, and the S page is no longer the paper
   silence is the one option that is certainly wrong.
```

## Content
### Proposed direction
```
S page ## Content
        │
        ├── LaTeX adapter ──→ section .tex + bibliography style + float references
        ├── Word adapter  ──→ native DOCX paragraphs + citations + tables
        └── HTML adapter  ──→ Board or web reading view + hover apparatus
```

### Projection, not independent export
Each adapter reads the same semantic structure and applies its own venue or format style.
AMA numbering, author-year citations, Word fields, and LaTeX commands are output decisions.
They do not belong in the authored sentence as competing syntaxes.

### One review order in HTML
The Board HTML projection uses a fixed reader order for a paper Display: Current Float, live artifact, Display Versions, real folder, then explanation.
Display Versions is an inventory projection, not a version chooser: `float.tex` alone marks the current artifact; saved versions, candidates, and other assets remain visibly non-current unless an explicit stage record says otherwise.
It is a review view of the same unit bundle, not a second asset store or a place to choose a winner.

### The unresolved round-trip
Generated outputs are safe while conversion is one-way.
If a coauthor edits Word or TeX directly, the change must either be backported into the S page or explicitly declare that the manuscript has crossed into a new authoritative mode.

## Items to Finish
- [~] ↪ MOVED to `QC6` · rule external edits
      Open on this page since it was written and closable here never, because the edit is not abstract: it is what happens when you hand somebody a `.docx`. `QC6` makes that file, so `QC6` rules it.
- [~] ↪ SPLIT into `QC5` and `QC6` · render one real section three ways
      The LaTeX round-trip is a diff and lives on `QC5`; the Word export's acceptance test is a human reading it and lives on `QC6`. This page keeps the model: one authored Content, one-way projections, no round trips.
- [x] 🧭 Choose one authored Content source
      LaTeX, Word, and HTML are projections of the same S-page Content.
- [ ] 📐 Define one intermediate content contract
      Headings, paragraphs, sentences, citations, values, and Displays need a shared semantic representation.
- [x] 🔁 Rule external edits
      Ruled 260727 on `QC6`, which is where the Word file is actually made, and this face should stop restating it. BACKPORT: a change that comes back in an output is carried into the S page, and the output never becomes authoritative. What made it takeable was a mechanism rather than an argument: every Word comment carries `w:author`, so the export writes `haipipe` and a coauthor writes their own, and the backport partitions on that field instead of guessing which comments are ours. This item had been open on both this face and `QB2d` and was closable on neither, because the edit is not hypothetical in the abstract: it is what happens when you hand someone a Word file.
- [ ] 🧪 Render one real section three ways
      Compare prose, citations, values, Display placement, and section structure across all outputs.

## Where we are
The one-source direction is selected.
The adapter contract and external-edit policy are still open.

## Files
- `stages/5-section-edit/`
  The authored section structure.
- `3-deliver/`
  The likely owner of target-format adapters.
- `haipipe-board/`
  The existing HTML reading projection.

## Log
- 260726 · JL raised opening `QC5`/`QC6` for converting a stage page's Content into the sections, appendices, displays and a `paper-xxx.docx`. Routed here instead of opened: this face already owns the direction and the missing generator, `QD7` owns the several projections, `QD4` owns the adapters, and `QA6` ⑦ owns where the generated files land on disk. Splitting the same open items across a third group would have made four faces answer one question. Nothing about the question is new; what is missing is that this face's items are still open.
