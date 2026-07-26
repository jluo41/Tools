# One Content, several projections
state: 🟡 PARTIAL
owner: JL
method: author once in the S page, then render through target-specific adapters

## Question
How can the same section become LaTeX, Word, and HTML without creating three writable manuscripts?

The paper needs several delivery formats, but format conversion becomes unsafe when each output is edited as a separate source. The system needs one authored Content model and explicit one-way projections whose style rules belong to the target format.

## Boundary
- ✅ Covered here
  The source-to-output direction and the ownership of LaTeX, Word, and HTML adapters.
- ↪ Covered elsewhere
  What the canonical stage artifact is comes from `QC1`; sentence attachments are `QBa4`; Display embedding is `QI4`.

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

### The unresolved round-trip
Generated outputs are safe while conversion is one-way.
If a coauthor edits Word or TeX directly, the change must either be backported into the S page or explicitly declare that the manuscript has crossed into a new authoritative mode.

## Items to Finish
- [x] 🧭 Choose one authored Content source
      LaTeX, Word, and HTML are projections of the same S-page Content.
- [ ] 📐 Define one intermediate content contract
      Headings, paragraphs, sentences, citations, values, and Displays need a shared semantic representation.
- [ ] 🔁 Rule external edits
      Decide how a direct Word or TeX edit returns to the canonical Content without silent drift.
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
