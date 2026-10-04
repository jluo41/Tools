# Paper structure and delivery reference

Read this reference when creating, migrating, naming, or auditing a Paper
folder. `haipipe-paper` keeps only the routing consequence in its entrypoint;
the Page, Story, Venue and assembly owners remain authoritative for their own
records.

## Paper layout

```text
Paper-<Slug>/
├── board.md                         paper-root: .
├── board/                           generated HTML, never wording authority
├── A1-Story/
│   ├── Story00-ideation/            one idea portfolio
│   └── Story<Letter>-<desk>-<idea>/ one prospective paper Story
├── Ba-<desk>-Main/                  named Main Section Pages
├── Bb-<desk>-Appendix/              named Appendix Section Pages
├── Bc-<desk>-Round/                 RD<NN> feedback Round Pages
├── studio/                          drawings: make_<name>.py writes <name>.excalidraw
├── reports/                         one Report Page per Story question
│   └── qNN_<topic>/qNN_<topic>.md   answers: RQ<n> · answer-status: open | partial | answered
└── delivery/                        generated complete-paper projection
    ├── paper-build.toml             order, venue profile, output names
    ├── latex/                       master, fragments, displays, bib, PDF
    └── word/                        DOCX converted from the LaTeX room
```

`A1-Story/` contains the idea pool and one Story per surviving idea. Section
and Round groups sit at the paper root.

`reports/` and `studio/` are board-level folders, not Page groups: board.md lists
neither (JL 261003: "just like the studio and reports, like other board level
folder"). A Report answers one Story question from the closed Runs of its work, in
the shape `haipipe-question` gives every board's questions (`state:`, `answers: RQ<n>`, `answer-status:`,
an Opening whose first paragraph is the answer, then Answer · Evidence · Limits ·
Next under Content, and a `page.toml`). It is the G2 record: a hypothesis shows ✅
in the Paper Workbench only when its question's Report says `answered`; before
that it shows 📝 (stated, not yet shown). Sections cite the Report's finding
rather than re-arguing it. A second desk continues with the next
free group letter. There is no `0-paperboard/` wrapper in the current layout.

## Naming and routing invariants

- Group headings name their actual folder: `### Ba · Ba-ManSci-Main`, not a
  display title. The Paper Workbench binds the token after `·` to disk.
- Current Section IDs are semantic: `S-<desk>-Main-<N>-<Title>` or
  `S-<desk>-Appendix-<L>-<Title>`. Unnumbered Pages keep their title.
- A Story Section Narrative row (§8) is recognized only when the Section id is its first table cell.
- Compile order is read only from the Story's
  `<!-- haipipe:compile-order:start -->` / `end` markers with `- ` ids.
- Task Roadmap (§7) work lives in the Task layer's project folder. The Paper folder records
  the evidence need and consumes the accepted Result; it does not execute the
  Task.

## Source and delivery law

Section Pages own manuscript wording and Page-local Evidence Results. Each
Section's `delivery/latex/<page>.tex` body fragment is the Paper assembly input.
The assembler regenerates the Paper `delivery/` tree from those fragments, the
Story compile order, accepted display assets and the declared build config.
Generated Word/PDF files, Round snapshots and old desk-room copies are never
wording or evidence sources.

Assembly may run early, but its manifest remains `DRAFT` until the intended
Section set has current outlines, evidence, display previews, Page delivery and
Page CHECK closure. A send freezes the current build in the Round's `sent/`
folder; the answering build is frozen in `released/`.

## Migration boundary

The former S01–S10 runtime, old desk-room layouts, SD/SA/NA aliases and shadow
Page names are historical inputs. Migrate active Pages in place, preserve Story,
Section, claim, Evidence and Run identities, and do not edit frozen Round or
generated delivery material by hand.
