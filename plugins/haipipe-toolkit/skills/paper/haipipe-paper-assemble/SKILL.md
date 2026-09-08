---
name: haipipe-paper-assemble
description: >-
  The paper-level assembly contract: deterministically build the manuscript
  deliverables from the Section Pages' own LaTeX deliverables and accepted Page
  bindings, regenerating the paper's delivery/ folder whole.
  It separates the reusable document engine from paper configuration and venue
  profiles, produces DOCX/PDF/supplement artifacts and source manifests, and
  never uses a generated Word file as an input. Use for assemble, build Word,
  export the complete paper, regenerate submission files, or audit whether a
  document is stale.
metadata:
  version: "0.7.2"
  last_updated: "2026-09-08"
  summary: "Paper-level source-driven document assembly; page-level Word export remains a separate plugin."
---

# /haipipe-paper-assemble · build the paper from source

This is the paper-level document contract. It is different from
`haipipe-plugin-delivery/ref/word.md`, which exports one Board Page for a coauthor. Assembly
combines the Story's Section Narrative rows and the Section Pages into the complete deliverable
for one desk.

The public Paper door routes `assemble` here. The implementation is expected to
be a reusable engine plus a small paper configuration; a paper must not copy a
large venue-specific builder and edit it by hand for every new manuscript.

## 🧭 Authority and source of record

The layers have different jobs:

```text
Paper-<Slug>/                          the board at the paper root
  ├── A1-Story/Story<Letter>-<desk>-<idea-slug>/         boundary, claims, evidence, acceptance
  │       §8 Section Narrative + haipipe:compile-order block = reading order
  └── Ba-<desk>-Main/<page>/           each Section Page owns its words:
        └── delivery/latex/            <page>.tex (body fragment, what the paper
                                       \inputs) · <page>-complete.tex/.pdf (the
                                       page's own standalone deliverable)
              ↓
delivery/paper-build.toml              paper configuration
              ↓
delivery/latex/                        GENERATED whole from the pages
  ├── master.tex                       one \input per page, Story compile order
  ├── sections/ · appendices/          copies of the pages' <page>.tex fragments
  ├── displays/                        copies of accepted display floats + assets
  └── reference.bib                    merged from outline/evidence/bibex/<page>.bib
              ↓
shared assembly engine + venue profile
              ↓
DOCX / PDF / supplement / snapshots / build manifest
```

The Board and Page files decide what the paper is allowed to claim and whether
the relevant Section is CHECK-closed. Each Section Page owns its wording and
projects it into `delivery/latex/<page>.tex`, the body fragment used by the
paper builder. `<page>-complete.tex` is only the standalone Page wrapper;
it is not a manuscript input. The selected Story C8 compile-order block owns
the order. The paper's `delivery/latex/` is regenerated from the body fragments
and is never edited by hand (JL 260907; this replaces the 260824
desk-room law, under which `<N>-<desk><year>/sections/*.tex` was the source of
record). A builder may refuse or watermark a build when a page's deliverable is
not bound to its current accepted version, but it must not silently replace
the source with prose mined from Word.

## 🏁 The milestone that admits a page

A Section Page enters the build when three things exist on it: an approved
outline table (`outline/<page>-outline-v*.md` with its tick), a preview PDF for
every display unit the page CITES and that is LIVE
(`outline/evidence/display/<unit>/preview.pdf`), and its own compiled page PDF
(`delivery/latex/<page>.pdf` or `<page>-complete.pdf`). A page missing any of
the three is listed in the build manifest as not ready and the build is
`DRAFT`; the builder never substitutes an older desk-room copy for it.

**A display unit gates only when cited and live (0.6.2, JL 260908).** Cited
means the page's fragment or `.md` names the unit, or the fragment `\ref`s one
of the unit's `float.tex` labels. Live means the unit's own records do not say
`state: 🟣` (folded into another unit) or, under `## Placement`, retired / folded
into / no standalone display. An uncited folder or a folded unit is dead
weight, not a gate: it is reported under the page's `warnings` in the manifest
and never blocks. Before this rule a folded, uncited `S-Display-3a-funnel`
blocked a fully written §4 on a missing preview.

**A stale fragment is a warning, never silent.** The body fragment is DERIVED
from the page `.md` by the LaTeX lane; when the `.md` is newer than
`delivery/latex/<page>.tex` the build would print yesterday's words. The engine
reports `fragment may be stale` under `warnings` (a warning, not a blocker,
because mtimes lie after a clone or a bulk rename sweep); rerun the lane.

Read the current outline's explicit `approved:` record, not merely its filename
or an older approved outline. When an `outline-version:` is declared, it must
match the file being admitted. An unsigned newer revision blocks admission;
a filename, successful test, or complete set of render files grants no approval.
The shared Page outline policy keeps `v0.x` unapproved; an inspection never
promotes it. Honor explicit `supersedes:` lineage before choosing a current
outline by numeric version, so a structural restart cannot revive an older
approval. Ambiguous lineage requires repair, not a guessed current plan.
Record the inspected outline path, version, approval, and content hash in the
manifest. These mechanical milestones do not establish G4: missing checks for
current Page CHECK closure, accepted evidence, or human submission approval
must remain explicit blockers, and the build stays `DRAFT`.

Generated complete-paper DOCX/PDF and `draft-sections/*.docx` are never wording
sources for the next build. Section-owned body fragments and accepted display
assets are intentional input projections; Page preview PDFs and receipts are
read for the checks they actually support, not as new evidence or prose.
A prior manifest may be inspected during an audit, but stale fields from a
failed build must not be presented as freshly verified results.

## 🔀 Two Word lanes; do not merge them

| Lane | Input | Output | Purpose |
|---|---|---|---|
| Page-level Delivery `ref/word.md` | one Page's Markdown and Page-local evidence | `<page>/delivery/word/` | coauthor review of one Section/Page |
| Paper-level `haipipe-paper-assemble` | every Section Page's `delivery/latex/<page>.tex` fragment, accepted display floats, merged `outline/evidence/bibex/` bibliography | `delivery/latex/` then `delivery/word/` | complete manuscript and supplement |

Page-level Word snapshots are not the assembly input. Paper-level assembly
does not concatenate those snapshots. Both lanes are projections of their
respective source, and a rebuild overwrites the projection.

## 🧩 Reusable engine, profile, and paper config

The implementation has four separable parts:

1. **Source adapter** — reads the declared source format. The adapter is a
   self-contained LaTeX room: recursively expand `\\input`, resolve
   labels/references/citations, read room-local displays and bibliography, and
   preserve section order from the master. The current assembly source is
   generated `delivery/latex/`, populated from the declared Section Pages.
2. **Document model** — turns source into typed title, abstract, prose,
   heading, list, table, figure, caption, reference, and appendix events.
3. **Venue profile** — supplies output rules such as font, spacing, title-page
   fields, main-text word-count basis, table/figure placement, supplement
   packaging, and required checks. A venue profile never creates evidence or
   rewrites claims.
4. **Renderer and validators** — emit DOCX/PDF and review snapshots, calculate
   the source manifest, and run structural plus rendered visual checks.

The shared engine lives under this skill: `scripts/build_delivery.py` is the
CANONICAL delivery engine (regenerates `delivery/latex/`, compiles, converts
Word, writes the display register and the manifest) and
`scripts/latex_room_to_docx.py` is the latex-room → DOCX adapter it calls. A
paper supplies configuration only: its `delivery/build.py` is the thin wrapper
at `ref/build.py.wrapper`, copied unchanged, which sets
`HAIPIPE_PAPER_BUILD_CONFIG` to the `paper-build.toml` beside it and execs the
engine inside its own module. A fix in the engine reaches every paper on the
next build; a paper-local `build.py` with logic of its own is the defect this
rule exists to prevent (260908: three real fixes were found in one paper's copy
while a sibling paper kept printing every display twice). `SKILL.md` is the
contract and routing layer; it is not a 1000-line copied renderer. The engine
requires Python 3.11+ for `tomllib`; run it with the workspace venv.

## 🔢 Three behaviors every build must have (260908)

Found paper-locally by Paper-MISQ-Board, now in the engine with a tooth each in
`tests/test_build_delivery.py`:

```text
A  print a display ONCE          md2tex already embeds a cited display as a real float inside the
                                 fragment; the master never re-\inputs the unit's float.tex after it.
                                 Without this every figure and table printed twice (Figure 1 = Figure 2).
                                 switch: DEDUPE_EMBEDDED_FLOATS
B  a not-ready page keeps        its H1 declares number and title ("# S-<desk>-Main-X · §4 Title"):
   its number                    the master emits a real numbered \section{Title} plus one italic
                                 "[This section is not yet compiled into this build.]" line; the
                                 REASONS live in build-manifest.json and the register, never in the
                                 reader's PDF/DOCX (JL: "the delivered pdf or word must be clean").
                                 An unnumbered
                                 "[NOT READY]" heading slid every later section down one number.
                                 parser: page_heading()
C  the display register          delivery/display-register.md counts what the MASTER prints, walking
                                 master.tex in \input order, and compares with the number each unit's
                                 README `## Placement` declares. Four teeth: declared ≠ printed · printed
                                 with no declared number · one label printed twice · one number claimed
                                 by 2+ units, scanned over ALL units on disk so a collision on a
                                 not-ready page is visible before that page compiles.
                                 also in build-manifest.json under "displays"
```

## 🧪 The expect-fail procedure (the Gate-1 lesson)

A check that measures what a page CONTAINS is blind to what the document
PRINTS: the first register counted fragments and reported the same findings on
the broken build as on the good one. Every tooth in this skill is therefore
proven by making it fail first: `test_behavior_A_expect_fail_register_catches_the_double_print`
switches `DEDUPE_EMBEDDED_FLOATS` off and asserts the register reports the
double print; only then does the positive test count. When you add a behavior,
add the tooth that fails without it, and record both runs. Run the suite with
`bash Tools/plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/tests/run.sh`
(it runs from the tests directory on purpose: the repository's `code/` package
shadows the stdlib `code` module and breaks pytest startup from the repo root).

Since 0.7.0 the engine also guarantees: a display prints once in the whole
DOCUMENT, so a page that `\ref`s a float another page embeds never re-inputs it,
whichever page comes first; a bib key that two pages define differently is a
document warning (first page's entry kept); a missing `latexmk` or Word engine is
reported as `rc 127` in the manifest, never a traceback; the master carries the
status word only, never counts or build times.

## 📊 Tables must arrive in Word (0.7.1)

The Word engine parses each `table` float into rows itself. Its column-spec
reader is brace-aware (`p{3cm}`, `@{}`, `>{\raggedright\arraybackslash}`,
`*{6}{X}`, `tabularx` width argument, `tabular*`, `longtable`); rows split on
`\\` only at brace depth 0 so `\shortstack{a\\b}` stays one cell; a
`\multicolumn{n}` cell pads `n-1` empties. Supplement displays are numbered
(`Table S1.`, `Figure S1.`; profile keys `supplement_table_prefix`,
`supplement_figure_prefix`). After both `.docx` files are written the engine
counts their real `<w:tbl>` elements against the table displays it meant to
emit and against the master's table floats, records
`build.checks.tables_rendered` in the manifest, and exits non-zero on any
mismatch: a table that reaches the PDF and not the Word file is a loud failure,
never a caption with nothing under it (found by Paper-MISQ-Board, 260908: 3 of 4
main tables and 7 of 12 appendix tables were lost). `tests/test_latex_room_to_docx.py`
drives the real engine over a room with those exact column specs.

## 🎭 Venue profiles

A profile is presentation, never claims: `profiles/<name>.toml`, selected by
`[paper] venue_profile` in `paper-build.toml`; `[profile]` there may override
single keys. Flat keys drive the Word engine (`layout`, `font`, `line_numbers`,
`venue_label`, `draft_label`, `abstract_heading`, `references_heading`, …); the
`[latex]` table drives `write_master()`:

```text
[latex] key          values                    what it does in the generated master
spacing              single · onehalf · double  \setspace command
bibstyle             a .bst name (apalike)      \bibliographystyle
displays             inline · end               end = endfloat: every float on its own page after the text
appendix_newpage     true · false               \clearpage before each lettered appendix
title_page           inline · separate          separate = blind title page alone, then \clearpage
abstract_page        true · false               abstract (+ keywords) alone on its page
running_head         true · false               false = only the DRAFT word while drafting, nothing once clean
```

Shipped: `jama-internal-medicine` (Word-side layout, eTable/eFigure supplement)
and `misq` (double-spaced, blind title page, abstract page, lettered appendices
on new pages, `displays` switchable inline/end; `apalike` stands in for MISQ's
author-date style because the desk's own `.bst` is not shipped). A paper with no
profile builds as before 0.7.0.

## ⚙️ Canonical configuration

The paper keeps one `delivery/paper-build.toml`. Paths are resolved relative
to that config file. The following is the minimum contract; fields may be
omitted only when the selected profile supplies a declared default:

```toml
[paper]
id = "Paper-AgreeablePrescription"
desk = "misq2026"
source_format = "latex-room"
venue_profile = "misq"

[pages]
# where the words come from: the Section Page groups, and the Story page whose
# `haipipe:compile-order` block fixes the reading order. Each page contributes its body fragment
# <page>/delivery/latex/<page>.tex, its outline/evidence/bibex/<page>.bib, and the float.tex +
# asset of every display unit its fragment \ref's.
main = "../Ba-MISQ-Main"
appendix = "../Bb-MISQ-Appendix"
order = "../A1-Story/StoryA-misq-phytrait-discretion/StoryA-misq-phytrait-discretion.md"   # selected C8 compile-order block

[source]
# the GENERATED room; the builder writes it, nobody edits it
room = "latex"
master = "master.tex"
sections = "sections"
appendices = "appendices"
displays = "displays"
bibliography = "reference.bib"

[evidence]
# A Page-generated receipt: provenance/state only, never manuscript prose.
lock = "latex/evidence-lock.json"
# "draft" permits visible [E## pending] markers; "final" rejects them.
mode = "draft"

[outputs]
main_docx = "word/Paper-AgreeablePrescription-draft.docx"
supplement_docx = "word/Paper-AgreeablePrescription-supplement-draft.docx"
main_pdf = "latex/Paper-AgreeablePrescription-draft.pdf"
supplement_pdf = "latex/Paper-AgreeablePrescription-supplement-draft.pdf"
section_snapshots = "word/draft-sections"
assets = "latex/submission-assets"
manifest = "build-manifest.json"
```

The selected C8 compile-order block and declared Section groups determine the
current build inputs. A missing or ambiguous order is a repair requirement,
not permission to read a retired planning Page or silently choose another
desk room. Inspect older adapters before use and report unsupported checks;
this contract does not claim that all historical parser paths were removed.
For the single-target interface, require exactly one complete marker block.
Reject duplicate or malformed Section entries instead of silently omitting
them; candidate tellings are narrative plans, not additional active blocks.

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
- a display is declared in the source and resolved from `delivery/latex/displays/`,
  a copy of the owning page's accepted asset;
- the engine never copies prose, values, citation text, or display contents
  out of the receipt.

`mode = "draft"` keeps unresolved `[E## pending]` markers explicit in the
candidate. `mode = "final"`/`"submission"` rejects both pending markers and
any non-accepted receipt item. This is a preflight, not a claim-making step.

## ▶️ Build protocol

The public operation is `assemble`:

```text
resolve Paper and its delivery/
  → load delivery/paper-build.toml
  → read the [pages] groups · check each page's milestone (outline tick,
    display PDFs, page PDF) · read the Story's compile-order block for order
  → regenerate delivery/latex/ whole: master.tex · sections/ · appendices/ ·
    displays/ · reference.bib, all copied from the pages
  → verify source files and accepted bindings
  → parse source with the selected adapter
  → render main manuscript and online supplement
  → render optional section snapshots
  → write assets and the build manifest
  → render DOCX/PDF previews and inspect layout when requested
  → ON SEND (a person's act): mint or name the Round, copy every declared
    output (main/supplement PDF + DOCX when present) plus the manifest and
    display register into
    B<x>-<desk>-Round/RD<NN>-<desk>-<event>-<YYYYMMDD>/sent/
  → ON ROUND CLOSE: rebuild, then copy into that Round's released/
```

`sent/` and `released/` are frozen copies and never rebuilt in place; the
Round's close receipt under `outline/` carries their manifest hashes.
`haipipe-paper-round` owns the folder shape. A freeze fails if any declared
output is missing or if the destination already contains a prior snapshot;
this prevents a partial send from masquerading as a complete Round.

The paper-specific command is the thin wrapper `ref/build.py.wrapper`,
installed as `delivery/build.py`:

```bash
.venv/bin/python delivery/build.py            # build · DRAFT unless every page is ready
.venv/bin/python delivery/build.py send RD02  # freeze the current build into that Round's sent/
.venv/bin/python delivery/build.py release RD02  # after G5 approval, freeze the answering build
```

The wrapper contains no logic of its own; it delegates to
`scripts/build_delivery.py` and the paper's `paper-build.toml`. It must not
contain a second source model or read a prior `.docx`. An installation that packages
the engine may additionally expose a module command:

```bash
python3 -m haipipe_paper_assemble build --config delivery/paper-build.toml
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
3. inspect the readiness, evidence, unresolved-reference, and renderer fields
   in `build-manifest.json`;
4. if appropriate, invoke only the wrapper's early environment preflight;
   never invoke the renderer merely to answer an audit question;
5. report stale/missing/mismatched outputs explicitly and name the source file
   that must change before a rebuild.

If sources or receipts change during the audit, report the exact snapshot and
its limits or repeat the comparison on a stable copy. Do not merge observations
from different builds into a single currentness claim. A wrapper without an
explicit read-only preflight must be inspected rather than invoked with its
default build command.

Run an actual build only when the user asks to assemble, regenerate, or update
the delivery artifacts. A read-only audit may not alter `delivery/`, its
   manifests, or other generated receipts.

## 📦 Required outputs

At minimum, a complete manuscript build records:

- main manuscript DOCX, and PDF twin when the environment supports rendering;
- online supplement DOCX/PDF when the paper declares one;
- optional `draft-sections/*.docx` snapshots generated from the active source;
- copied or normalized submission assets;
- `build-manifest.json` or equivalent containing engine/profile versions,
  config hash, source paths and source hashes, and output paths;
- a machine-readable `build-manifest.json` containing page readiness, counts,
  unresolved references, missing assets, word-count results, renderer outcomes,
  and build status.

The manifest is the sole delivery receipt; Page-level acceptance remains the
`CHECK` phase. The display register is a derived reader index whose findings
are also recorded in the manifest, not an independent acceptance or readiness
receipt. Do not create a competing delivery-status authority.

The manifest is provenance, not a second content store. A generated snapshot
may be opened and marked up by a coauthor, but its corrections must be routed
back to the source Section or config before the next build.

## 🚦 DRAFT versus SUBMISSION-READY

Assembly can run at any time. It does not itself pass G4. The output status is
derived from the declared checks:

```text
Section Pages CHECK-closed + source bindings current + build manifest has no blockers
    → SUBMISSION-READY candidate
otherwise
    → DRAFT, with the blockers visible in the build manifest
```

Only a person declares the manuscript ready for upload. A successful Python
run, a clean DOCX, or an attractive rendered page is not a human submission
decision.

The current `build_delivery.py` implements order, outline-admission and render
checks but does not ingest current Page CHECK, accepted-evidence, or exact-build
human submission receipts. Its `build_readiness()` therefore keeps `DRAFT` and
names the missing validation. The DOCX adapter's lexical pending/citation flags
are not substitutes for those semantic bindings; a `final` mode flag alone
cannot close G4. Report missing validator coverage rather than treating a green
syntax flag as complete evidence, venue, output, or provenance verification.

## ✅ Build checks

The assembly engine must check, or explicitly report that a check is not
available:

- every declared source file exists and is inside generated `delivery/latex/`;
  the selected C8 order agrees with `[pages]`, and every listed Section meets
  the milestone or is reported as not ready;
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
- if the build is run before G4, the result is visibly marked `DRAFT`.

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
- structural and visual check result;
- unresolved author actions and whether G4 is still open;
- the build's warnings (stale fragments, non-gating display units, bib key
  collisions) and the display register's findings, or "none".
