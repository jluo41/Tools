# Outline Spaces · UI ↔ Page Folder ↔ Run Workflow mapping

This is the small implementation contract for the three core Spaces plus the
read-only Delivery Space.
It answers one question: when a person clicks a Space, which renderer reads
which Markdown or Result files, and which component is allowed to write them?

## 1. The naming boundary

The interface uses plain names:

```text
Draft Space       Evidence Space       Run Space       Delivery Space
```

The implementation keeps stable internal names for compatibility:

```text
data-space=bullet  · lens=div       · live/outline.py
data-space=evidence· lens=evidence  · live/evidence.py
data-space=run     · lens=run       · live/runs.py
data-space=delivery· lens=delivery · /_board/delivery?workspace=1
```

`Bullet`, `div`, and `/_board/evidence` or `/_board/runs` are implementation
identifiers. They are not required to appear in the reader-facing UI. The old
`lens=workspace&seg=...` URLs remain aliases during migration.

## 2. The Page Folder is the backend

The current lightweight Page is file-backed. There is no separate database
model for these Spaces.

```text
<page-folder>/
├── <page>.md                         Page product: Opening · Content · Aims
├── page.toml                          optional source/title manifest
├── outline/
│   ├── <stem>-outline-v*.md           Draft plan + candidate prose / Shape authority
│   ├── <stem>-logic.mmd               Draft Mermaid Structure
│   ├── <stem>-evidence-items.md       authored Item contracts for Outline/Evidence
│   └── <stem>-context.md, ...         durable process records; off-stage
├── runs/
│   ├── rp-struct-NN.md, rp-scratch-NN_<target>.md, rp-sec-NN.md,
│   │   rp-para-NN_Pxx[-Pyy].md          Run P Markdown tickets
│   ├── re-value-NN_<slug>.md,
│   │   re-display-NN_<slug>.md,
│   │   re-cite-NN_<slug>.md              RE Evidence Run tickets
│   └── rdNN_*.md                        RD Delivery Run tickets
├── results/
│   ├── rp-*/                            Run P history / working drafts
│   ├── re-*/                            RE result.yaml + payloads
│   └── rdNN_*/                         RD receipt/diagnostics when stored here
├── workflow/                           Runtime/compatibility receipts; off-stage
├── scripts/                            execution support; off-stage
├── _archive/legacy-outline-evidence/   old Evidence material; migration only
└── delivery/                           built outputs; not Space authority
```

The tree is a projection of ownership, not duplicated Space folders. The three
core Spaces are projections of one Page Run Workflow Runtime: Draft reads the
current Outline and writing Result, Evidence reads typed Result/Card bindings,
and Run reads Run Instances plus recorded Gate/Route state. In
particular, there is no new `draft/`, `evidence/`, or `run-space/` directory.
Any old generated `outline/*-evidence.md` file or `outline/evidence/` tree must
be moved to `_archive/legacy-outline-evidence/` before the Page is considered
v4-ready. The authored `outline/*-evidence-items.md` contract remains active;
the runtime never reads the retired archive.

## 3. Space mapping

| UI Space | Visible projection | Backend read set | Write authority |
|---|---|---|---|
| Draft Space | Mermaid + Table / Reading / Scratch views | selected `outline/*-outline-v*.md` (including embedded Draft fields and `## Scratch` registry), `outline/*-logic.mmd`, and Results metadata | Table/Reading: none; Scratch: only `action: scratch` writes the selected Outline registry plus its paired Run receipt |
| Evidence Space | typed `Displays`, `Citations`, and `Values` sections; each item is a collapsed Result-first card | `results/**/result.yaml` and payload metadata | Evidence/Run workflow or producer writes Results; Space is read-only |
| Run Space | RP, RE, RD, Supporting Runs | `runs/`, paired `results/`, delivery receipts, external Run registry and `supporting_results` references | owning workflow/CLI writes tickets and Results; Space is read-only |
| Delivery Space | source-to-delivery consistency receipt by lane | current Page source, `delivery/web/`, lane `build-manifest.json` files, artifact hashes and mtimes | none in the Space; delivery builders write artifacts and manifests |

### Draft Space

Draft is the planning, reading, and human rehearsal view. The Markdown plan
supplies the paragraph groups and candidate wording; `*-logic.mmd` supplies
the Mermaid map. Mermaid appears as a collapsed native disclosure:
opening it only reveals the rendered diagram and closing it removes that
visual weight again. Table and Reading are read-only for the plan in the
browser: the Outline endpoint registers the view but rejects legacy edit
actions. Generated HTML is never the edit target. Each Bullet keeps its visible
bracketed role label and, when evidence is bound, a compact read-only Evidence
route/card tag; the full Evidence item remains in Evidence Space.

Scratch is explicit and quiet: entering Scratch reveals a small `+` beside
each Section and whole paragraph group. The current Outline grammar has no
separate subsection node, so it avoids a duplicate Subsection plus; explicit
subsection-scope records remain accepted for future Page schemas. B/symbol rows
have no Scratch control. The form captures rough notes
without changing the `Draft:` field. `Save` creates or updates
`rp-scratch-NN_<target>` and its `## Scratch` registry record; the person
manually clicks `Finish Scratch` to ask the AI for a concise Summary from the
notes and close the Run. There is no `💬 Notes` thread,
old feedback badge, or `action: feedback` composer in Draft Space. In Scratch
Mode, saved raw Scratch is displayed by default even when the body is hidden;
the `+` reopens the editor.

### Evidence Space

Evidence is Result-first and typed. The surface has three sections —
`Displays` (`DISPLAY`, including legacy `TABLE`), `Citations` (`CITE`), and
`Values` (`VALUE`) — rather than one mixed table. Each section shows only a
high-level, collapsed card by default: type, readable label, short title,
Bullet address, and status. Opening a card reveals the contract-level detail:
Evidence Label, immutable Evidence Item id, Evidence Run, Supporting Runs,
Result, Expected, and Acceptance. This makes the distinction explicit:
the Item is the thing being claimed, the Evidence Run is the Page-owned
execution lineage that produces its Result, and Supporting Runs are external
or upstream references that remain inspectable in their owner space.

A Result manifest identifies the Evidence item, its type, optional `bullet`
 address, status, producing Run, and any Supporting Run references. Result
status, identity, and path are authoritative. Old generated Evidence snapshots
and the retired Evidence folder are not read by the new renderer; they must be
moved to `_archive/legacy-outline-evidence/` as a one-time migration step.
Result paths remain behind a small `Sources`
disclosure.

### Run Space

Run is the execution/readback view, separated by ownership:

```text
RP                human ↔ Page interaction and Page writing
RE                one Page Evidence Item's execution lineage
RD                one Page delivery target/version
Supporting Runs   external/upstream Runs that remain inspectable in place
```

RP reads `rp*.md` tickets and their `results/rp*/` journals, including the
human-first `rp-scratch-NN_<target>` records. RE reads
Page-owned evidence tickets and their paired Result manifests. RD reads the
delivery lane's artifacts and `build-manifest.json`. Supporting Runs are
assembled from references in an RE Result and the owner-native registry;
the Page shows the identity and available Result pointer, but does not copy or
symlink the external ticket, Result, or protected payload.

## 4. Frontend ↔ backend request flow

```text
Browser
  │ click Draft / Evidence / Run / Delivery Space
  ▼
Outline outer page: live/outline.py
  │ Draft: render in place
  │ Evidence: lazy iframe → /_board/evidence
  │ Run:      lazy iframe → /_board/runs
  │ Delivery Space: lazy iframe → /_board/delivery?workspace=1
  ▼
Page server adapter: src/standalone_server.py
  │ resolves the Page source and dispatches the route
  ▼
Space renderer
  ├── live/outline.py  → plan / logic / preview Markdown
  ├── live/evidence.py → Result manifests + payload metadata
    ├── live/runs.py     → tickets, Results, registry references
    └── live/delivery.py → source/artifact consistency receipt
  ▼
HTML projection returned to the browser
```

The Board uses the same Page renderer. `assets/js/07-plugin-outline.js` handles
Board navigation and deep links; it does not own a second data model. The
standalone `src/page_workspace.py` exposes only the top-level Outline plugin,
Delivery, and Folder. Evidence and Run are children of Outline.

## 5. Read/write contract

```text
Draft Space      GET, plus bounded Scratch POST
                                      ← Table/Reading remain GET-only; Scratch
                                        writes only `## Scratch` and its paired
                                        Run receipt
Evidence Space   GET only            ← Run/Result producers
Run Space        GET only            ← Page workflow, Task workflow, registry
Delivery Space GET only              ← delivery builders and manifest writers
```

This separation is intentional: the front end is a projection, while the
Markdown and Result files remain the backend authority. Table/Reading,
Evidence, Run, and Delivery remain read-only; Scratch is the one bounded human
capture exception. Feedback and prose acceptance enter through the owning Run
interaction and its recorded Steps/Versions, never through the retired browser
composer.
A future UI can replace
the server-rendered HTML, but it must preserve these paths, ownership rules,
and the no-copy rule for Supporting Runs.
