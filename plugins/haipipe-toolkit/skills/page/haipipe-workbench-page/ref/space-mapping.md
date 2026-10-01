# Page workbench Spaces · UI ↔ Page Folder ↔ Run Workflow mapping

This is the small implementation contract for the three Spaces (Draft,
Evidence, Delivery), the Runs panel beside each, and the All-runs view.
It answers one question: when a person clicks a Space, which renderer reads
which Markdown or Result files, and which component is allowed to write them?

## 1. The naming boundary

The interface uses plain names:

```text
Draft Space       Evidence Space       Delivery Space       (each with its Runs panel)
All-runs view     no button; opened by a ?run=<id> link
```

The implementation keeps stable internal names for compatibility:

```text
data-space=bullet  · lens=div       · servers/workbench-page/outline.py
data-space=evidence· lens=evidence  · servers/workbench-page/space_views.py (Card view: evidence.py)
data-space=delivery· lens=delivery  · servers/workbench-page/space_views.py
lens=run (no button)                · servers/workbench-page/runs.py
Runs panel (each Space)             · servers/workbench-page/runs_panel.py
```

`Bullet`, `div`, and `/_board/evidence` or `/_board/runs` are implementation
identifiers. They are not required to appear in the reader-facing UI. The old
`lens=workspace&seg=...` URLs remain aliases during migration.
## Workflow versus Space

A Space is a read-only UI projection; a workflow is the lifecycle that
changes the Page records behind it. They are related, but they are not
additional folders:

| Compatibility dispatch → owning work | Primary Space | Authoritative files |
|---|---|---|
| SHAPE + SURVEY → Structure RP | Draft Space | `draft/*-draft-v*.md`, `*-evidence-items.md` |
| LAND → typed RE and Supporting Runs | Runs panel + Evidence Space | `runs/re-*.md`, `results/re-*/result.yaml`, supporting references |
| EMBED → evidence interpretation within the owning Run | Draft Space + Evidence Space | current Outline candidate plus selected Result label bindings |
| CHECK → independent controller judgment | Draft + Evidence + Run + Delivery Spaces | exact candidate, plan, selected Results, acceptance records, receipts, and artifact versions |

The workbench documents define the protocol. Each Page stores only its current
plan, process records, Run tickets, Results, and receipts. The browser never
writes a second Space-specific copy.

## Workflow × Space Specification

The umbrella word for an explanatory “说明书” is **documentation**. For this
artifact, the precise reader-facing name is **Workflow × Space Specification**:
it is a
normative reference that says where each Run Spec appears and which file or
folder is authoritative. A lighter, non-normative version may be called a
**Workflow × Space Guide**. Internally, the normalized schema may still use
`workspace_id`; in the workbench vocabulary, `Workspace` and `Space` mean the
same member surface. The table below is the canonical specification;
the All-runs view's `Workflow map` is its read-only UI projection.

Rows are planned Run Specs. Columns are Spaces, not physical directories.
Every cell is intentionally compact: `mode · schema · path`. A `—` cell means
that the Space does not own or project that Run Spec. The path is a
parameterized Page-relative path, with `<stem>` equal to the current Page
Markdown stem.

| Run Spec | Draft | Evidence | Run (`runtime`) | Delivery |
|---|---|---|---|---|
| `structure` | `action · OutlinePlan · draft/<stem>-draft-v*.md` | `review · EvidenceItemPlan · draft/<stem>-evidence-items.md` | `run · StructureRun · runs/rp-struct-* + results/rp-struct-*/` | `—` |
| `scratch` | `input · ScratchNote · draft/<stem>-draft-v*.md#2-Scratch` | `—` | `run · ScratchResult · runs/rp-scratch-* + results/rp-scratch-*/` | `—` |
| `section-writing` | `review · WritingResult · draft/<stem>-draft-v*.md` | `review · EvidenceBinding · results/re-*/result.yaml` | `run · SectionWritingRun · runs/rp-sec-* + results/rp-sec-*/` | `read · PageDraft · <stem>.md` |
| `paragraph-writing` | `review · WritingResult · draft/<stem>-draft-v*.md` | `review · EvidenceBinding · results/re-*/result.yaml` | `run · ParagraphWritingRun · runs/rp-para-* + results/rp-para-*/` | `read · PageDraft · <stem>.md` |
| `evidence-item` | `review · EvidenceBinding · draft/<stem>-evidence-items.md` | `action · EvidenceResult · results/re-{value,display,cite}-*/result.yaml` | `run · EvidenceRun · runs/re-* + results/re-*/` | `review · ArtifactDependency · delivery/<lane>/ built files` |
| `delivery` | `read · PageSource · <stem>.md` | `read · EvidenceResult · results/re-*/result.yaml` | `run · DeliveryRun · runs/rd*.md + results/rd*/` | `write · DeliveryArtifact · delivery/{web,latex,word,render}/` |

Context collection, Content adoption, and whole-Page Check are controller
operations outside this Run Spec table. Their records remain inspectable:

| Controller operation | Records and coverage |
|---|---|
| Context | `draft/records/<stem>-context.md` and the selected Folder identity/owner contract |
| Adoption | Accepted Writing Results → `<stem>.md`, plus release provenance |
| Check | Selected Draft/version, bound Evidence Results, Run acceptance and Step integrity, and Delivery build/source agreement; owner ruling when required |

A separately commissioned operation may become a Run only under a complete
explicit Run Spec; its compatibility label alone never creates a row.

This table does not allocate Runs and does not move ownership. The Run Spec
still owns target, actor, Gates, Routes, Result/receipt, and cardinality; the
cell only binds that contract to a Space projection. Concrete Run
instances show in each Space's Runs panel and in the All-runs view.

## 2. The Page Folder is the backend

The current lightweight Page is file-backed. There is no separate database
model for these Spaces.

```text
<page-folder>/
├── <page>.md                         Page product: Opening · Content
├── page.toml                          optional source/title manifest
├── draft/                             (a legacy Page: outline/)
│   ├── <stem>-draft-v*.md             three-section Draft Markdown / Shape authority
│   ├── <stem>-evidence-items.md       authored Item contracts: ## Citations · ## Displays · ## Values
│   ├── records/<stem>-context.md, ... durable process records; off-stage
│   └── previous/                      superseded plan versions
├── runs/
│   ├── `run-structure-<MMDD>-<slug>`.md, `run-scratch-<MMDD>-<slug>`, `run-section-<MMDD>-<slug>`.md,
│   │   `run-paragraph-<MMDD>-<slug>`          Run P Markdown tickets
│   ├── `run-value-<MMDD>-<slug>`,
│   │   `run-display-<MMDD>-<slug>`,
│   │   `run-citation-<MMDD>-<slug>`              RE Evidence Run tickets
│   └── run-delivery-<lane>.sh  the fixed Delivery Runs; written by page.py export
├── results/
│   ├── rp-*/                            Run P history / working drafts
│   ├── re-*/                            RE result.yaml + payloads
│   (a Delivery Run keeps no results/ folder: delivery/<lane>/ is its result)
├── workflow/                           Runtime/compatibility receipts; off-stage
├── scripts/                            execution support; off-stage
├── _archive/legacy-outline-evidence/   old Evidence material; migration only
└── delivery/                           built outputs; not Space authority
```

The tree is a projection of ownership, not duplicated Space folders. The three
core Spaces are projections of one Page Run Workflow Runtime: Draft reads the
current Outline and writing Result, Evidence reads typed Result/Card bindings,
and Run reads Run Instances plus recorded Gate/Route state. In
particular, there is no separate `evidence/` or `run-space/` directory.
Any old generated `outline/*-evidence.md` file or `outline/evidence/` tree must
be moved to `_archive/legacy-outline-evidence/` before the Page is considered
v4-ready. The authored `draft/*-evidence-items.md` contract remains active;
the runtime never reads the retired archive.

## 3. Space mapping

| UI Space | Visible projection | Backend read set | Write authority |
|---|---|---|---|
| Draft Space | Structure card + Table / Reading / Scratch / Revise views | selected `draft/*-draft-v*.md` (its three sections), and Results metadata | Table/Reading: none; Scratch: `action: scratch` writes the selected Outline registry plus its paired Run receipt; Revise: `action: revise` writes changed Draft fields plus the paragraph's Revise Run ledger; Structure: `action: structure` rewrites C/P headings |
| Evidence Space | Citations · Displays · Values · Supporting Runs tabs; views All items (table), Card (Result-first page in a frame), Source (Evidence Markdown) | `results/**/result.yaml` and payload metadata | Evidence/Run workflow or producer writes Results; Space is read-only |
| Runs panel · All-runs view | RP, RE, RD, Supporting Runs | `runs/`, paired `results/`, `delivery/<lane>/` file times, external Run registry and `supporting_results` references | owning workflow/CLI writes tickets and Results; Space is read-only |
| Delivery Space | source-to-delivery consistency receipt by lane | current Page source, `delivery/web/`, built lane files and their mtimes | none in the Space; delivery builders write artifacts and manifests |

### Draft Space

Draft is the planning, reading, and human rehearsal view. The Markdown plan
supplies the paragraph groups, the candidate wording, and the Structure text
at the top: its `## C<n>` and `### C<n>.P<m>` headings, one line each, editable
in place through `action: structure`. Table and Reading are read-only for the
plan in the browser; Revise edits a paragraph's Draft through `action: revise`;
the Draft endpoint rejects the legacy Bullet edit actions. Generated HTML is never the edit target. Draft shows no
evidence chips (JL 260927); the full Evidence item remains in Evidence Space.
Clicking a paragraph selects it and narrows the Runs panel.

Scratch is explicit and quiet: in Scratch view, clicking a Section or paragraph
heading opens its note form. The current Outline grammar has no
separate subsection node, so it avoids a duplicate Subsection plus; explicit
subsection-scope records remain accepted for future Page schemas. B/symbol rows
have no Scratch control. The form captures rough notes
without changing the Draft. `Save` creates or updates
`run-scratch-<MMDD>-<slug>` and its `## Scratch` registry record; the person
manually clicks `Finish Scratch` to ask the AI for a concise Summary from the
notes and close the Run. There is no `💬 Notes` thread,
old feedback badge, or `action: feedback` composer in Draft Space. In Scratch
Mode, saved raw Scratch is displayed by default even when the body is hidden;
the `+` reopens the editor.

### Evidence Space

Evidence is Result-first and typed. Tabs: `Citations` (`CITE`), `Displays`
(`DISPLAY`, including legacy `TABLE`), `Values` (`VALUE`) and Supporting Runs.
All items is a table, one row per item; selecting a row selects that item for
the Runs panel. Card shows the Result-first cards of the current tab only, each
collapsed to type, label, title, address and status; opening one selects its
item too, and reveals the contract-level detail:
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
Result paths show in the Runs panel's Results, not on the cards.

### Runs panel and All-runs view

Each Space's Runs panel lists its view's run types (`../SKILL.md` § Runs panel).
The All-runs view (`lens=run`) is the fuller readback, separated by ownership:

```text
RP                human ↔ Page interaction and Page writing
RE                one Page Evidence Item's execution lineage
RD                one fixed Delivery Run per lane (run-delivery-<lane>)
Supporting Runs   external/upstream Runs that remain inspectable in place
```

RP reads `rp*.md` tickets and their `results/rp*/` journals, including the
human-first `run-scratch-<MMDD>-<slug>` records. RE reads
Page-owned evidence tickets and their paired Result manifests. RD reads the
delivery lane's built files and their times. Supporting Runs are
assembled from references in an RE Result and the owner-native registry;
the Page shows the identity and available Result pointer, but does not copy or
symlink the external ticket, Result, or protected payload.

## 4. Frontend ↔ backend request flow

```text
Browser
  │ click Draft / Evidence / Delivery Space
  ▼
Page outer page: servers/workbench-page/outline.py
  │ Draft, Evidence, Delivery: render in place (space_views.py), each with runs_panel.py
  │ Evidence Card view: lazy iframe → /_board/evidence
  │ Delivery previews: lazy iframes of the built files
  │ lens=run:  lazy iframe → /_board/runs
  ▼
Page server adapter: servers/haipipe-page/standalone_server.py
  │ resolves the Page source and dispatches the route
  ▼
Space renderer
  ├── servers/workbench-page/outline.py  → plan / logic / preview Markdown
  ├── servers/workbench-page/evidence.py → Result manifests + payload metadata
    ├── servers/workbench-page/runs.py     → tickets, Results, registry references
    └── servers/workbench-page/delivery.py → source/artifact consistency receipt
  ▼
HTML projection returned to the browser
```

The Board uses the same Page renderer. `assets/js/07-workbench-outline.js` handles
Board navigation and deep links; it does not own a second data model. The
standalone `src/page_workspace.py` exposes the 📃 Page workbench, 📤 Delivery and
📂 Folder tabs. The three Spaces and the Runs panels live inside 📃 Page.

## 5. Read/write contract

```text
Draft Space      GET, plus bounded POSTs
                                      ← Table/Reading remain GET-only; Scratch,
                                        Revise and the Structure card write only
                                        their sections and paired Run records
Evidence Space   GET only            ← Run/Result producers
Runs panel       GET only            ← Page workflow, Task workflow, registry
                                        (copies prompts; starts nothing)
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
