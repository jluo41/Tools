# Outline Spaces · UI ↔ Page Folder mapping

This is the small implementation contract for the three user-facing Spaces.
It answers one question: when a person clicks a Space, which renderer reads
which Markdown or Result files, and which component is allowed to write them?

## 1. The naming boundary

The interface uses plain names:

```text
Draft Space       Evidence Space       Run Space
```

The implementation keeps stable internal names for compatibility:

```text
data-space=bullet  · lens=div       · live/outline.py
data-space=evidence· lens=evidence  · live/evidence.py
data-space=run     · lens=run       · live/runs.py
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
│   ├── <stem>-outline-v*.md           Draft plan / Shape authority
│   ├── <stem>-logic.mmd               Draft Mermaid Structure
│   ├── <stem>-preview.md              Draft candidate prose
│   ├── <stem>-evidence-items.md       legacy Evidence compatibility index
│   ├── <stem>-evidence.md             legacy Evidence status fallback
│   └── <stem>-context.md, ...         durable process records; off-stage
├── runs/
│   ├── rp00_*.md, rpNN_*.md            Run P Markdown tickets
│   ├── reNN_*.md                        RE Evidence Run tickets
│   └── rdNN_*.md                        RD Delivery Run tickets
├── results/
│   ├── rpNN_*/                         Run P history / working drafts
│   ├── reNN_*/                         RE result.yaml + payloads
│   └── rdNN_*/                         RD receipt/diagnostics when stored here
├── workflow/                           phase receipts; off-stage
├── scripts/                            execution support; off-stage
└── delivery/                           built outputs; not Space authority
```

The tree is a projection of ownership, not three duplicated folders. In
particular, there is no new `draft/`, `evidence/`, or `run-space/` directory.
`outline/evidence/` is legacy compatibility material and is not a new-write
target.

## 3. Space mapping

| UI Space | Visible projection | Backend read set | Write authority |
|---|---|---|---|
| Draft Space | Mermaid + read-only paragraph/Bullet/Draft table + compact Evidence routes | `outline/*-outline-v*.md`, `outline/*-logic.mmd`, `outline/*-preview.md`, plus `<page>.md` for current product context | none in the Space; Page/Run workflow writes Markdown |
| Evidence Space | one `Evidence · Bullet · Result` table | `results/**/result.yaml` and payload metadata; legacy `outline/*-evidence*.md` only to fill compatibility labels/addresses | Evidence/Run workflow or producer writes Results; Space is read-only |
| Run Space | RP, RE, RD, Supporting Runs | `runs/`, paired `results/`, delivery receipts, external Run registry and `supporting_results` references | owning workflow/CLI writes tickets and Results; Space is read-only |

### Draft Space

Draft is the planning and rehearsal view. The Markdown plan supplies the
paragraph/Bullet rows; `*-logic.mmd` supplies the Mermaid map; `*-preview.md`
supplies candidate wording. Mermaid appears as a collapsed native disclosure:
opening it only reveals the rendered diagram and closing it removes that
visual weight again. Draft is read-only in the browser: the Outline endpoint
registers the view but rejects legacy edit actions. The owning Page/Run
workflow validates and updates the Markdown-backed source. Generated HTML is
never the edit target. Each Bullet keeps its visible bracketed role label and,
when evidence is bound, a compact read-only Evidence route/card tag; the full
Evidence item remains in Evidence Space.

### Evidence Space

Evidence is Result-first. A Result manifest identifies the Evidence item, its
type (`VALUE`, `DISPLAY`/legacy `TABLE`, or `CITE`), optional `bullet` address,
status, producing Run, and any Supporting Run references. The legacy Evidence
index may still supply the Bullet address or readable title while old Pages are
being migrated. When the Result carries `bullet` or `title`, those fields win;
Result status and path always win. The legacy file is not a new write
destination.

### Run Space

Run is the execution/readback view, separated by ownership:

```text
RP                human ↔ Page interaction and Page writing
RE                one Page Evidence Item's execution lineage
RD                one Page delivery target/version
Supporting Runs   external/upstream Runs that remain inspectable in place
```

RP reads `rp*.md` tickets and their `results/rp*/` journals. RE reads
Page-owned evidence tickets and their paired Result manifests. RD reads the
delivery lane's artifacts and `build-manifest.json`. Supporting Runs are
assembled from references in an RE Result and the owner-native registry;
the Page shows the identity and available Result pointer, but does not copy or
symlink the external ticket, Result, or protected payload.

## 4. Frontend ↔ backend request flow

```text
Browser
  │ click Draft / Evidence / Run
  ▼
Outline outer page: live/outline.py
  │ Draft: render in place
  │ Evidence: lazy iframe → /_board/evidence
  │ Run:      lazy iframe → /_board/runs
  ▼
Page server adapter: src/standalone_server.py
  │ resolves the Page source and dispatches the route
  ▼
Space renderer
  ├── live/outline.py  → plan / logic / preview Markdown
  ├── live/evidence.py → Result manifests + legacy compatibility index
  └── live/runs.py     → tickets, Results, registry references
  ▼
HTML projection returned to the browser
```

The Board uses the same Page renderer. `assets/js/07-plugin-outline.js` handles
Board navigation and deep links; it does not own a second data model. The
standalone `src/page_workspace.py` exposes only the top-level Outline plugin,
Delivery, and Folder. Evidence and Run are children of Outline.

## 5. Read/write contract

```text
Draft Space      GET only            ← Page/Run workflow writes Markdown
Evidence Space   GET only            ← Run/Result producers
Run Space        GET only            ← Page workflow, Task workflow, registry
```

This separation is intentional: the front end is a projection, while the
Markdown and Result files remain the backend authority. A future UI can replace
the server-rendered HTML, but it must preserve these paths, ownership rules,
and the no-copy rule for Supporting Runs.
