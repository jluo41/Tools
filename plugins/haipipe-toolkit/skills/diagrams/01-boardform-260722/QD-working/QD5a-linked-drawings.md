# Linked drawings: one source per Page, one composition per Group

state: ✅ SETTLED · linked Group/Page editing is live, owner-routed, and conflict-safe
owner: CC
method: keep one ordinary Excalidraw source per owner, then compose imports at runtime from an explicit Group manifest

## Opening
How can one Group drawing show every Page drawing without turning five editable pictures into five copies?
A Page drawing is the source for one question, while the Group drawing adds relationships and layout around several such sources.
The hard part is letting a person edit from either view without saving the same Page into two files that can disagree.
This page rules one source per owner, explicit edit modes, and recomposition after every source change.

**Where this page sits**: `QD5` owns the three-pane workspace in which a drawing will open, and `QB7` owns how one Page attaches a drawing to its Diagram section.

**Why it matters**: A Group must stay current when any child Page changes, while the Page must remain independently editable and recoverable.

**Current boundary**: The split, additive Page sync, namespaced runtime composition, Group layer editor, Arrange mode, Page-source entry, owner-scoped assets, revision conflicts, and Chat owner address are built.

## Diagram

**The ownership path**: Page sources flow into one Group view, while each save returns to exactly one owner.

```text
  📄 QD1.excalidraw ─┐
  📄 QD2.excalidraw ─┼──▶ 🧩 compose ──▶ 🗺 QD Group view
  📄 QD3.excalidraw ─┘                       │
                                             ├─ Arrange Instance ─▶ group.excalidraw
                                             └─ Edit Page Source ─▶ QD<n>.excalidraw

  🔁 Page save ──▶ revision changes ──▶ every importing Group recomposes
```

## Content

### 1 · One source for each owner

**The source boundary**: the files a person may edit and what each one owns.

```text
📁 Group folder   draw/
🗺 Group source   group.excalidraw · relations + instance placement
📄 Page source    QD<n>.excalidraw · Page-owned elements
🖼 Assets         assets/<owner>/ · external image bytes
```

Each Page drawing is an ordinary Excalidraw scene and remains useful when opened by itself.
The Group scene carries only Group-owned elements and an import manifest naming each Page source and its placement.
An empty Page still gets a source file, and an empty Group still gets a Group source, so existence never depends on whether someone has drawn the first shape.
The folder is named `draw/` in lowercase, as JL ruled on 260807.

### 2 · Composition is a view, not another source

**The composition boundary**: what is stored and what is derived.

```text
💾 stored       Group own layer · Page sources · import placements
⚙️ derived      one composed scene for reading or editing
🔒 identity     owner prefix on ids, bindings, containers, and groups
🚫 never stored a copied Page slice as a second editable truth
```

Opening a Group loads `group.excalidraw`, resolves every import, namespaces its element references by Page id, and applies the placement transform.
The resulting scene can show every Page drawing at once without merging their source files.
A Page save changes its revision and invalidates every composed Group that imports it.
The next Group load or live refresh recomposes from sources, so there is no manual intake step.

### 3 · Two edit modes in the Group view

**The save target**: one visible mode decides which file receives a gesture.

```text
🧭 Arrange Instance   position · scale · hide ─────▶ group.excalidraw
✏️ Edit Page Source  shape · text · binding       ──▶ QD<n>.excalidraw
👁 Read only          pan · zoom · inspect         ──▶ no write
```

`Arrange Instance` treats an imported Page as one portal and never changes the Page source.
`Edit Page Source` enters the selected Page's local source coordinates and saves only that Page scene.
The editor must show the active owner before the first editable gesture and again while saving.
Cross-owner selection is read-only until the person chooses which owner to enter.

### 4 · Revisions, conflicts, and Chat

**The safe save**: the values checked before a write is accepted.

```text
📥 opened revision   Page or Group hash at load time
📤 save request      owner · base revision · changed elements
✅ accepted          base still current
⚠️ conflict          source moved · reload, compare, or fork
```

Every source save carries the revision that was opened.
The server accepts the write only when that revision is still current, which prevents a Group editor and a Page editor from silently replacing each other.
Chat receives the same owner address as the canvas, so a request such as edit `QD1` from the Group view is routed to `QD1.excalidraw`, not to the composed result.
The page status strip and Chat context can therefore name the Board, Group, Page, and drawing owner in one address.

### 5 · Migration and staged delivery

**The first migration**: what this round writes and what it deliberately leaves alone.

```text
① split dry run    inspect frames, aliases, titles, and target paths
② split --apply    create only new draw/ sources
③ sync             add Pages declared after the first split
④ verify           rebuild 175 legacy elements exactly
⑤ compose          derive a namespaced Group scene on every open
⑥ live             connect Work pane, owner modes, assets, and revisions
```

The migration reads the current `board.excalidraw` and never edits it.
It refuses before writing anything if one target source already exists.
Every new file is created exclusively, and a failed run removes the files it created before reporting the failure.
An existing unframed relation enters a Group source when its explicit owner or its bound endpoints name one Group; an ownerless or cross-Group element stops the migration for a human ruling.
For this Board it created nine Group folders and sixty-six initial Page sources, then `sync` additively created `QBt11` and `QC5` when the Board reached sixty-eight Pages.
The current sources still restore all 175 legacy elements and zero embedded files exactly.
The old scene remains the rollback path while the linked runtime is adopted.

## Aims

### A1 · One source for each owner
- A1.1 · Every Page group has one lowercase `draw/` directory with a Group source and one source per Page.
  **Done when:** The inventory from `board.md` and the linked source inventory match exactly.
- A1.2 · A Page source can be opened and edited without loading its Group.
  **Done when:** It is an ordinary Excalidraw scene whose coordinates are local to that Page.

### A2 · Composition is a view, not another source
- A2.1 · A Group source imports every Page source without copying Page content into its own source layer.
  **Done when:** The Group manifest names every Page once and composition resolves the list.
- A2.2 · Independent element ids and bindings remain valid after composition.
  **Done when:** Runtime namespacing rewrites ids and all reference-bearing fields together.

### A3 · Two edit modes in the Group view
- A3.1 · Arrange Instance changes only Group placement data.
  **Done when:** Moving an import leaves the Page source byte-for-byte unchanged.
- A3.2 · Edit Page Source writes through from the Group view to the selected Page source.
  **Done when:** A Group-view text edit appears when that Page source is opened alone.

### A4 · Revisions, conflicts, and Chat
- A4.1 · A stale editor cannot overwrite a newer Group or Page source without a visible conflict.
  **Done when:** Saves compare the opened revision and reject a stale base.
- A4.2 · Chat and canvas gestures resolve the same drawing-owner address.
  **Done when:** A Page-targeted change from Group view updates that Page source and refreshes every importing Group.

### P · Page-level
- P1 · The legacy Board scene remains a complete rollback path through the migration.
  **Done when:** Its hash is unchanged and exact recomposition matches every element and file.

## States

### A1 · One source for each owner
- ✅ A1.1 · Met; nine lowercase `draw/` directories contain nine Group sources and sixty-eight Page sources from the current Board inventory.
- ✅ A1.2 · Met; each Page scene is standalone and its migrated elements use Page-local coordinates.

### A2 · Composition is a view, not another source
- ✅ A2.1 · Met live; every Group manifest imports its Board-ordered Page list and each Group open resolves the current sources.
- ✅ A2.2 · Met live; runtime composition namespaces ids and rewrites binding references with their owners.

### A3 · Two edit modes in the Group view
- ✅ A3.1 · Met; Arrange writes one import placement in `group.excalidraw`, and regression tests prove the Page source remains byte-for-byte unchanged.
- ✅ A3.2 · Met; Edit Page Source enters the selected ordinary Page scene, saves only it, and returns to the recomposed Group.

### A4 · Revisions, conflicts, and Chat
- ✅ A4.1 · Met; Page and composed-Group revisions are checked inside per-source save locks, and stale writers receive HTTP 409 with a visible reload conflict.
- ✅ A4.2 · Met; Group and Page Chat prompts receive the same `draw/group.excalidraw` or `draw/<Page>.excalidraw` owner path used by the canvas and forbid editing the derived composition.

### P · Page-level
- ✅ P1 · Met; `verify` restored all 175 elements and zero files exactly, and the legacy scene hash remained `c23889f3021914483dc4af6652efb595ad342bc86a542f78308051227ad5f21a`.

## Files

### ⚙️ Engines · what RUNS THE LINKED DRAWING
- `../../board/haipipe-board/cli/draw.py`
  Plans and creates the non-destructive split, composes namespaced sources, and verifies the exact migration round trip.
- `../../board/haipipe-board/live/xcal.py`
  Composes linked Groups, serves Page sources, externalizes assets by owner, and performs compare-and-save writes while retaining the legacy route.
- `../../board/haipipe-board/assets/xcal-boot.js`
  Shows the save owner, locks imported Page elements, switches Group/Arrange/Page modes, and carries revisions on each save.

### 🧪 Checks · what CATCHES A BROKEN OWNERSHIP RULE
- `../../board/haipipe-board/tests/test_linked_drawings.py`
  Checks migration safety, additive Page sync, transforms, ownership, exact reconstruction, empty sources, and namespaced references.
- `../../board/haipipe-board/tests/test_linked_live.py`
  Proves owner-routed Page saves, Group-only layout saves, imported-element isolation, runtime composition, and stale-revision conflicts.
- `../../board/haipipe-board/checks/linked_drawings_browser.py`
  Drives Group layer, Arrange, Edit Page Source, and Back to Group through the real proxied Excalidraw UI.

### 📥 Input files · what THE MIGRATION READS
- `board.excalidraw`
  The untouched legacy scene and rollback source for the first migration.
- `board.md`
  The authoritative Group and Page inventory and order.

### 📤 Output files · what THE SPLIT WRITES
- `QD-working/draw/group.excalidraw`
  The pattern repeated under each Group folder for Group-owned elements and Page imports.
- `QD-working/draw/QD5a.excalidraw`
  This Page's independently editable source, empty until its first drawing is made.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QD5 page](QD-working/QD5-split-workspace.md)
  The linked editor must live inside the split workspace without coupling Page refresh to Chat refresh.
- `continues · ALL` · [QB7 page](QB-delivery/QB7-diagramattach.md)
  This Page replaces the source architecture beneath the Page-level drawing attachment.

## Law
- 260807 JL · 📁 The drawing folder is named `draw/` in lowercase
  Each Page group keeps its drawing sources together without adding drawing files beside every Markdown page.
- 260807 JL · 🔗 A Group view may edit Group-owned layout or enter one Page source, but it never becomes a second Page source
  Page changes flow outward by recomposition, and Group placement changes stay in the Group manifest.

## Log
260807 · Fresh-context validation caught Excalidraw load normalization issuing no-op saves during toolbar navigation; linked editors now arm only from a non-toolbar human gesture, and the browser check fails on any navigation POST.
260807 · Added the drawing-owner address to Group and Page Chat context so canvas and discussion route edits to the same source file.
260807 · Connected every generated Group Work pane to its live composed canvas and passed the headless Group → Page → Group browser route.
260807 · Added owner-routed Group/Page saves, locked imports, Arrange controls, owner-scoped assets, and stale-revision HTTP 409 conflicts.
260807 · Added additive `draw.py sync` and brought the new QBt11 and QC5 Pages into the linked inventory without touching the legacy scene.
260807 · Added the Page-to-Page binding rejection regression that the fourth completed fresh review found missing.
260807 · Validated every scene reference before owner inference and rejected explicit cross-Group relations and unresolved Page bindings after the third fresh review.
260807 · Rejected every unresolved relation binding before Group ownership inference and added dangling, ownerless, and cross-Group negative tests after the second fresh review.
260807 · Added exclusive atomic creates, rollback after a partial write, Group relation ownership from explicit tags or bound endpoints, and Page-owner binding namespaces after the fresh review.
260807 · Created the QD5a DRAFT, the linked-source splitter and compositor, nine Group `draw/` folders, sixty-six Page sources, and an exact 175-element migration proof.
