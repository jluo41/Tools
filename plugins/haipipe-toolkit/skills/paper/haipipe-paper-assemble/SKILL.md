---
name: haipipe-paper-assemble
description: >-
  The paper-level assembly contract: deterministically build the manuscript
  deliverables from the active desk-room source and accepted Page bindings.
  It separates the reusable document engine from paper configuration and venue
  profiles, produces DOCX/PDF/supplement artifacts and source manifests, and
  never uses a generated Word file as an input. Use for assemble, build Word,
  export the complete paper, regenerate submission files, or audit whether a
  document is stale.
metadata:
  version: "0.2.1"
  last_updated: "2026-09-04"
  summary: "Paper-level source-driven document assembly; page-level Word export remains a separate plugin."
---

# /haipipe-paper-assemble · build the paper from source

This is the paper-level document contract. It is different from
`haipipe-plugin-delivery/ref/word.md`, which exports one Board Page for a coauthor. Assembly
combines the accepted Narrative/Section graph into the complete deliverable
for one desk.

The public Paper door routes `assemble` here. The implementation is expected to
be a reusable engine plus a small paper configuration; a paper must not copy a
large venue-specific builder and edit it by hand for every new manuscript.

## 🧭 Authority and source of record

The layers have different jobs:

```text
0-paperboard/                         boundary, claims, evidence, acceptance
  └── Ba-<desk>-Main/S<D>...          Section Page tracking and CHECK state
              ↓
<N>-<desk><year>/                      self-contained desk room
  ├── master.tex                       composition and reader order
  ├── sections/*.tex                   manuscript wording: source of record
  ├── displays/                        room-local accepted display copies
  └── reference.bib                    room-local bibliography
              ↓
paper-build.toml                       paper configuration
              ↓
shared assembly engine + venue profile
              ↓
DOCX / PDF / supplement / snapshots / manifest / QA report
```

The Board and Page files decide what the paper is allowed to claim and whether
the relevant Section is CHECK-closed. The desk-room TeX owns the actual
reader-facing wording and order. A builder may refuse or watermark a build
when the room source is not bound to the current accepted Section versions,
but it must not silently replace the source with prose mined from Word.

Generated DOCX, PDF, `draft-sections/*.docx`, copied assets, previews, and
manifests are derived artifacts. They are never source of record and never
become inputs to the next build.

## 🔀 Two Word lanes; do not merge them

| Lane | Input | Output | Purpose |
|---|---|---|---|
| Page-level Delivery `ref/word.md` | one Page's Markdown and Page-local evidence | `<page>/delivery/word/` | coauthor review of one Section/Page |
| Paper-level `haipipe-paper-assemble` | desk-room master, sections, displays, bibliography | `<desk>-word/` or configured output room | complete manuscript and supplement |

Page-level Word snapshots are not the assembly input. Paper-level assembly
does not concatenate those snapshots. Both lanes are projections of their
respective source, and a rebuild overwrites the projection.

## 🧩 Reusable engine, profile, and paper config

The implementation has four separable parts:

1. **Source adapter** — reads the declared source format. The initial adapter
   is a self-contained LaTeX desk room: recursively expand `\\input`, resolve
   labels/references/citations, read room-local displays and bibliography, and
   preserve section order from the master.
2. **Document model** — turns source into typed title, abstract, prose,
   heading, list, table, figure, caption, reference, and appendix events.
3. **Venue profile** — supplies output rules such as font, spacing, title-page
   fields, main-text word-count basis, table/figure placement, supplement
   packaging, and required checks. A venue profile never creates evidence or
   rewrites claims.
4. **Renderer and validators** — emit DOCX/PDF and review snapshots, calculate
   the source manifest, and run structural plus rendered visual checks.

The shared engine belongs under the Paper assembly skill's implementation
(`scripts/` or its installed package). A paper room supplies configuration and,
only when necessary, a small adapter for genuinely unusual source constructs.
`SKILL.md` is the contract and routing layer; it is not a 1000-line copied
renderer. The reference `latex-room` implementation currently lives at
`scripts/latex_room_to_docx.py` and is invoked by a paper-room thin wrapper.
The reference TOML implementation requires Python 3.11+ (or an equivalent
TOML parser supplied by the installation).

## ⚙️ Canonical configuration

Each desk may keep one `paper-build.toml` beside its Word output room. Paths
are resolved relative to that config file. The following is the minimum
contract; fields may be omitted only when the selected profile supplies a
declared default:

```toml
[paper]
id = "Paper-CGMtoHbA1c"
desk = "dc2026"
source_format = "latex-room"
venue_profile = "diabetes-care"

[source]
room = "../1-dc2026"
master = "CGMtoHbA1c-DC2026.tex"
sections = "sections"
displays = "displays"
bibliography = "reference.bib"

[evidence]
# A Page-generated receipt: provenance/state only, never manuscript prose.
lock = "../1-dc2026/assembly/evidence-lock.json"
# "draft" permits visible [E## pending] markers; "final" rejects them.
mode = "draft"

[outputs]
main_docx = "CGMtoHbA1c-DC2026-submission-draft.docx"
supplement_docx = "CGMtoHbA1c-DC2026-online-supplement-draft.docx"
main_pdf = "CGMtoHbA1c-DC2026-submission-draft.pdf"
supplement_pdf = "CGMtoHbA1c-DC2026-online-supplement-draft.pdf"
section_snapshots = "draft-sections"
assets = "submission-assets"
manifest = "build-manifest.json"
qa_report = "build-qa.json"
```

Configuration selects and names inputs/outputs. It does not duplicate prose,
claims, values, citations, captions, or table cells. If a paper needs a
special section boundary or a nonstandard supplement, that behavior belongs in
the venue profile or an explicitly named adapter, not in a second hidden Word
source.

### Evidence receipt boundary

The optional `[evidence] lock` is a materialized receipt generated from the
Section Pages. It may identify the Section source, Page evidence item, type
(`VALUE`, `CITE`, or `DISPLAY`), state, and source hashes. The engine uses it
only to validate traceability and build status:

- the Section source owns the reader-facing claim and any accepted number;
- the citation is authored in that source and resolved against the declared
  bibliography;
- a display is declared in the source and resolved from the desk-room display
  directory;
- the engine never copies prose, values, citation text, or display contents
  out of the receipt.

`mode = "draft"` keeps unresolved `[E## pending]` markers explicit in the
candidate. `mode = "final"`/`"submission"` rejects both pending markers and
any non-accepted receipt item. This is a preflight, not a claim-making step.

## ▶️ Build protocol

The public operation is `assemble`:

```text
resolve Paper and desk room
  → load paper-build.toml
  → verify source files and accepted bindings
  → parse source with the selected adapter
  → render main manuscript and online supplement
  → render optional section snapshots
  → write assets, manifest, and QA report
  → render DOCX/PDF previews and inspect layout when requested
```

The paper-specific command may be a thin wrapper, for example:

```bash
python3 1-dc2026-word/build_word.py
```

That wrapper must delegate to the shared engine and config. It must not contain
a second source model or read a prior `.docx`. An installation that packages
the engine may additionally expose a module command:

```bash
python3 -m haipipe_paper_assemble build --config 1-dc2026-word/paper-build.toml
```

The module command is an installation interface; the paper-room wrapper is the
portable command for a checkout that has not installed the package.

The build is deterministic with respect to its declared source, config,
profile, engine version, and asset files. No LLM call is part of assembly. An
LLM may edit the source before the build, but it is not a synchronization
mechanism between Word and TeX.

### Read-only audit protocol

When the request is to inspect provenance, determine whether an assembled
document is stale, or verify a prior build, do **not** rebuild by default.
Instead:

1. read `paper-build.toml` and resolve the declared master, sections, displays,
   bibliography, profile, evidence lock, and output paths;
2. inspect `build-manifest.json` and compare its config/source/profile/output
   hashes against the declared files currently on disk;
3. inspect `build-qa.json` for evidence state, unresolved references, renderer
   availability, PDF outcome, and G6 status;
4. if appropriate, invoke only the wrapper's early environment preflight;
   never invoke the renderer merely to answer an audit question;
5. report stale/missing/mismatched outputs explicitly and name the source file
   that must change before a rebuild.

Run an actual build only when the user asks to assemble, regenerate, or update
the delivery artifacts. A read-only audit may not alter the desk-room,
deliverables, manifests, or QA receipts.

## 📦 Required outputs

At minimum, a complete manuscript build records:

- main manuscript DOCX, and PDF twin when the environment supports rendering;
- online supplement DOCX/PDF when the paper declares one;
- optional `draft-sections/*.docx` snapshots generated from the active source;
- copied or normalized submission assets;
- `build-manifest.json` or equivalent containing engine/profile versions,
  config hash, source paths and source hashes, and output paths;
- a machine-readable QA report containing counts, unresolved references,
  missing assets, word-count results, and build status.

The manifest is provenance, not a second content store. A generated snapshot
may be opened and marked up by a coauthor, but its corrections must be routed
back to the source Section or config before the next build.

## 🚦 DRAFT versus SUBMISSION-READY

Assembly can run at any time. It does not itself pass G6. The output status is
derived from the declared checks:

```text
Section Pages CHECK-closed + source bindings current + build QA passes
    → SUBMISSION-READY candidate
otherwise
    → DRAFT, with the failing checks visible in the receipt/QA report
```

Only a person declares the manuscript ready for upload. A successful Python
run, a clean DOCX, or an attractive rendered page is not a human submission
decision.

## ✅ Build checks

The assembly engine must check, or explicitly report that a check is not
available:

- every declared source file exists and is inside the desk-room boundary;
- no generated DOCX/PDF/snapshot is read as an input;
- every `\\input`, citation, label/reference, table asset, and figure asset
  resolves or is listed as a visible failure;
- when an evidence receipt is declared, its source bindings are recorded and
  final/submission modes reject pending or non-accepted evidence;
- no raw TeX commands or parser sentinels leak into emitted prose/cells;
- main-text word count uses the selected venue profile and states what it
  excludes;
- source, config, profile, engine version, and output hashes are recorded;
- DOCX structure has the expected tables, figures, headings, and sections;
- rendered pages are visually inspected when the output is being handed off;
- if the build is run before G6, the result is visibly marked `DRAFT`.

## ⛔ Prohibited shortcuts

- Do not open the previous assembled Word file and mutate paragraph/table
  indices to create the next candidate.
- Do not make `draft-sections/*.docx` or a coauthor's edited Word file a builder
  input.
- Do not let a venue profile silently change the paper's claims or evidence.
- Do not put per-paper prose into the shared engine or the Skill itself.
- Do not call a manually edited Word file “synchronized” unless its changes
  have been applied to the declared source and rebuilt.

## ✅ Completion receipt

Before reporting assembly complete, name:

- the source room, master, sections, displays, bibliography, and config;
- the engine and venue profile versions;
- the generated main/supplement outputs and manifest;
- word-count basis and result;
- structural and visual QA result;
- unresolved author actions and whether G6 is still open.
