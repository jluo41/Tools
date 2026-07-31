# Page Files: the contextual action map
state: 🔴 OPEN
owner: JL
method: group the few files needed to continue under headings named for this page's real work

## Question
How should `## Files` use optional subsections without forcing every Page into the same source/output/implementation taxonomy?

Files is an action map, not an exhaustive change list.
Subsections help when a Page touches several coherent parts of the work, but their names must come from that Page's context.
Names such as Sources, Outputs, Implementation, and Generated views are examples, not reserved headings.

## Boundary
- ✅ Covered here
  The purpose of Files, when subsections are useful, contextual subsection names, generated-file warnings, and heading-level Copy and Chat paths.
- ↪ Covered elsewhere
  The fixed Page order is `QAa0`; the general subsection renderer and paragraph grammar are `QAa3`; generated heading paths and Chat focus are `QAb3`.

## Diagram

```
example for QA2b, the Board-Webpage design page

📎 Files
├── Board source
│   └── board.md                  the accepted Index structure
├── Index renderer
│   ├── src/page_board.py         builds the top view
│   └── assets/board.css          shared visual language
└── Generated view
    └── board.html                generated · never hand-edit

QA2b / Files / Index renderer                 [⧉ Copy] [🤖 Chat]
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAa7

## Content
### 1 · Files is the continuation map
List only the source, output, implementation, evidence, or generated files another person needs to continue this Page.
Every row names the path and explains its role in one sentence.
Mark generated artifacts explicitly so nobody edits the wrong layer.

### 2 · Context names the subsections
Use no subsection when the list is short and coherent.
When grouping helps, use `###` headings that identify the real parts of this Page's work, such as `Board source`, `Index renderer`, and `Generated view`.
Generic labels such as Sources, Outputs, and Implementation are useful examples during design, but they are not a required vocabulary.
Omit empty subsections.

### 3 · The source form
Each optional `###` heading groups the following file rows until the next heading.
The heading receives a generated breadcrumb with Copy and Chat actions.
The Page-level Files heading remains in the fixed frame even when its internal organization varies.

## Items to Finish
- [ ] 🏷 Settle the contextual naming test
      A Files subsection must identify one coherent continuation surface on this Page and distinguish it from sibling groups.
- [ ] 📐 Settle the row grammar
      Keep paths, roles, and generated-file warnings readable without forcing a table onto small Pages.
- [ ] 🧭 Give each subsection a copyable Chat path
      Reuse `QAb3` so the focus packet includes Page, Files, contextual subsection, source path, and visible rows.
- [ ] 🧠 JL confirms Files has its own QAa face

## Where we are
Opened 260730 after JL extended optional Page subsections to Files and clarified that subsection names must follow context.
No Files-subsection renderer or source grammar is implemented yet.

## Files
- `../../board/haipipe-board/ref/q-template.md`
  The shared Page source template that must eventually teach optional Files subsections.
- `../../board/haipipe-board/ref/board-form.md`
  The Page grammar where the settled Files form belongs.
- `../../board/haipipe-board/src/page_question.py`
  The renderer that will turn contextual `###` groups into visible subsections.
- `../../board/haipipe-board/assets/board.css`
  The shared visual treatment for subsection headings and paths.

## Log
260730 · Opened from JL's decision that Files may have optional subsections whose names come from each Page's context
