---
name: haipipe-paper-assemble
description: "Builds the whole manuscript deterministically from the Sections' LaTeX and accepted bindings, regenerating delivery/ (DOCX, PDF, supplement). Use to assemble, export the paper or check whether a document is stale. Trigger: assemble, build Word, export the paper, /haipipe-paper-assemble."
metadata:
  version: "0.23.0"
  last_updated: "2026-11-13"
  summary: "Paper-level source-driven document assembly; page-level Word export remains a separate workbench."
---

# /haipipe-paper-assemble · build the paper from source

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; the SPACE's AGENTS.md § Working rules). Here that means the paper's `delivery/` (`master.tex`, `sections/`, `appendices/`, `displays/`, `reference.bib`, PDF, DOCX, build manifest): fix a Section Page or `scripts/build_delivery.py`, then rebuild.
>
> ⛔ **No sha256 or other content hashes** (hard rule, JL 260928; the SPACE's AGENTS.md § Working rules). Since 0.8.4 the engine writes none: `build-manifest.json` lists inputs by path, a version is its number and date, and a stale fragment is found by file time.

This is the paper-level document contract. It is different from
`workbench-task-draft/ref/delivery.md`, which exports one Board Page for a coauthor. Assembly
combines the version's `## Narrative` rows and the Section Pages into the complete deliverable
for one desk.

The public Paper door routes `assemble` here. The implementation is expected to
be a reusable engine plus a small paper configuration; a paper must not copy a
large venue-specific builder and edit it by hand for every new manuscript.


Delivery storage (JL 261010)
---------------------------

Only the Block owns a physical `delivery/` directory. Job, Task and Report
outputs retain their source identity under it: `delivery/jNN_<job>/`,
`delivery/jNN_<job>/tNN_<task>/<lane>/`, and
`delivery/reports/qNN_<report>/<lane>/`. The Block's own output uses
`delivery/<lane>/`. Job and Task Delivery views select their source subtree
and link to the whole Block Delivery; they never create local delivery folders.
Runs and Results remain with their source. Every writer and reader uses the
shared `haipipe-draft/src/common.py` Delivery helpers. Standalone Pages without
a Block keep their own output root; an orphan jNN/tNN must acquire a Block.

In this skill, a Page's or Job's `delivery/<lane>/` means its source subtree
inside Block Delivery. Old local lanes are read-only migration inputs. Rebuild
from source before removing generated output; preserve a hand-owned fragment
when the source cannot reproduce it. A storage migration grants no acceptance,
release, send or submission approval.


## 🧭 Authority and source of record

The layers have different jobs:

Layout: the ladder (the Story as `sNN-…` topics beside the Jobs and `reports/` Questions, `jNN_writing_v<MMDD>_<desk>/` per version) is current; the layout below is still read. Both are in `haipipe-paper/ref/paper-ladder.md`.

```text
Paper-<Slug>/
  j11_writing_v<MMDD>_<desk>/<version>.md   Narrative and compile order
  j11_writing_v<MMDD>_<desk>/t0N_<title>/   Page source, Draft, Runs, Results
  delivery/j11_writing_v<MMDD>_<desk>/
    paper-build.toml · build.py         maintained build inputs
    latex/ · word/                     generated complete manuscript
    t0N_<title>/latex/<page>.tex         generated Page body fragment
    t0N_<title>/latex/<page>.pdf         standalone Page preview
    t0N_<title>/latex/selected-bibliography/<page>.bib
    t0N_<title>/word/ · web/             generated Page snapshots
    build-manifest.json                build checks; never approval

```

The Board and Page files decide what the paper is allowed to claim and whether
the relevant Section is CHECK-closed. Each Section Page owns its wording and
projects it into `delivery/latex/<page>.tex`, the body fragment used by the
paper builder. `<page>-master.tex` is only the standalone Page wrapper;
it is not a manuscript input. The version face's compile-order block owns
the order (an older Board: the Story Section Narrative block). The paper's `delivery/latex/` is regenerated from the body fragments
and is never edited by hand (JL 260907; this replaces the 260824
desk-room law, under which `<N>-<desk><year>/sections/*.tex` was the source of
record). A builder may refuse or watermark a build when a page's deliverable is
not bound to its current accepted version, but it must not silently replace
the source with prose mined from Word.

## 🏁 The milestone that admits a page

A Section Page enters the build when three things exist on it: an approved
outline table (`draft/<page>-draft-v*.md` with its tick), a preview PDF for
every display unit the page CITES and that is LIVE
(read on the page side, `results/<re-run>/payload/<unit>/preview.pdf`, the older form; § Stable Section identities), and its own compiled page PDF
(`delivery/latex/<page>.pdf`). A page missing any of
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

**A stale fragment stops the build (0.14.0, 261103).** The body fragment is
DERIVED from the page `.md` by the LaTeX lane; when the `.md` is newer than
`delivery/latex/<page>.tex` the build would print yesterday's words. That
happened silently on the MISQ paper: md2tex REFUSED to replace three Sections'
fragments because a citation key left each Section (a rewrite, a moved
paragraph), and the build printed their old text. Now, before it touches
`delivery/latex/`, the build checks every printed Section and stops (exit 1)
with one line per stale fragment, naming the keys md2tex would refuse:

```text
❌ build stopped: 1 printed Section(s) would carry OLD words
  stale fragment: t01_introduction (delivery/j11_writing_v1130_desk/t01_introduction/latex/t01_introduction.tex), not rebuilt since 2026-11-03 11:29: citation keys dropped: example2021one
  fix: re-export each Section through its LaTeX lane (page.py export <Section folder> --lane latex, ...)
  or build anyway: delivery/build.py --allow-stale (DRAFT, each listed as a G4 blocker)
```

```text
no key dropped         a plain re-export fixes it: page.py export <Section> --lane latex
a drop is intended     delivery/build.py --accept-dropped-keys: re-exports each stale Section
                       through its own LaTeX lane with md2tex's --accept-dropped-keys, then builds
build anyway           delivery/build.py --allow-stale: prints them, lists each under
                       stale_fragments in the manifest and as a G4 blocker
```

`--accept-dropped-keys` lets a key leave only when another Section in the
compile order still cites it, or a revise card in the Section's
`draft/records/<page>-revise.md` removed it (its `Original:` cites the key,
its `Expected:` does not). Any other key stays refused, named
`<key> (refused: unexplained)`, and the build still stops. Failing is the
default rather than a warning because a warning in a long summary is what let
three stale Sections through; `--allow-stale` covers the case where mtimes lie
(a fresh clone or a bulk rename sweep). The build never runs a bare md2tex: the
lane also places display floats and `\ref` labels. `build.py check` lists stale
fragments too and exits 1. The page manifest keeps its `fragment may be stale`
warning for the Paper Workbench.

Read the current outline's explicit `approved:` record, not merely its filename
or an older approved outline. When an `outline-version:` is declared, it must
match the file being admitted. An unsigned newer revision blocks admission;
a filename, successful test, or complete set of render files grants no approval.
The shared Page outline policy keeps `v0.x` unapproved; an inspection never
promotes it. Honor explicit `supersedes:` lineage before choosing a current
outline by numeric version, so a structural restart cannot revive an older
approval. Ambiguous lineage requires repair, not a guessed current plan.
Record the inspected outline path, version, and approval in the manifest (no
content hash). These mechanical milestones do not establish G4: missing checks for
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
| Page-level Delivery (`haipipe-delivery` `ref/page-delivery.md`, `page.py export --lane word`) | one Page's Markdown and Page-local evidence | `<Block>/delivery/<page-source-path>/word/` | coauthor review of one Section/Page |
| Paper-level `haipipe-paper-assemble` | every Section Page's `delivery/latex/<page>.tex` fragment, accepted display floats, merged `delivery/latex/selected-bibliography/<page>.bib` | `delivery/latex/` then `delivery/word/` | complete manuscript and supplement |

The Page's `delivery/latex/selected-bibliography/<page>.bib` is the citation
projection paired with its fragment: the Page export freezes it from the selected,
verified CITE Results (a Result's `payload.bibliography`; for an older paper-local
CITE Result, each cited key taken exactly from the `.bib` of a Supporting Result it
names). The accepted CITE Results remain citation authority. Both Bib homes stay: each Section keeps its
own `draft/evidence/bibex/<task>.bib`, and the build merges them into this file, which is generated and never hand-edited.
Regenerate stale Page delivery before assembly. An included, cited Page missing that Bib
fails with its exact path; excluded DRAFT stubs keep their not-ready status.
Retired `outline/evidence/bibex/` and flat `bibex/`
are never merged or used as fallback. A merged Bib does not prove acceptance.

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
   rewrites claims. One folder per venue, `venues/<venue>/` (`profile.toml`, a
   `venue.py` only for a Word shape no setting can say, its `.bst`, its test);
   the contract is [venues/README.md](venues/README.md), and the shared scripts
   never name a venue.
4. **Renderer and validators** — emit DOCX/PDF and review snapshots, calculate
   the source manifest, and run structural plus rendered visual checks.

The shared engine lives under this skill: `scripts/build_delivery.py` is the
ONLY delivery engine (regenerates `delivery/latex/`, compiles, converts
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

## 🔢 Build behaviors and their tests

Three behaviors every build must have · The expect-fail procedure: [ref/build-behaviors.md](ref/build-behaviors.md)

## 🔝 The Word lane

Word: every display at the top of a page · Tables must arrive in Word · Is the co-authors' Word the same as the build (`scripts/word_compare.py`): [ref/word-lane.md](ref/word-lane.md)

## 🗂 Stable Section identities and display unit folders

The Page has a stable semantic identity. The version face's compile-order
block and LaTeX determine printed order:

```text
t0N_<title> (Main)               t03_empirical-strategy · t04_results
t2N_<title> (Appendix, A = t21)  t21_instrumental-variables
the Abstract                     t00_abstract
legacy, still read               S-MISQ-Main-Results · S-MISQ-Appendix-Instrumental-Variables
<page>/results/<re-run>/payload/Display<n>-<slug>/         Display1-research-design · Display2-main-regression
delivery/latex/displays/<page-id>/<unit>/                  displays/t03_research-design/Display1-<unit>/
```

A display's one home is the Board's display Task (JL 261113; haipipe-paper-evidence rule 3). The build still reads
the unit on the page side, the older form (`results/<re-run>/payload/<unit>/` or `display/<unit>/`): its manifest, float,
assets, and preview, then projects the needed files into the generated Paper
delivery path; it never writes back into the unit.

Existing index-bearing Page IDs remain readable and retain their identity.
Inserting or moving a Section never renames its Page, Runs or display units.
The register compares the H1's declared printed number with actual LaTeX
numbering, not with a number embedded in the folder name. Legacy unit shapes
`S-Display-<code>-<slug>`, `<PageID>-Display<n>-<slug>` and
`Sec<N>-/App<L>-Display<n>-<slug>` remain naming findings. Every engine key is
`<page-id>/<unit>` because `Display<n>-<slug>` is unique only inside its Page.
Missing unit metadata remains a finding; it does not authorize an automatic
rename or modify the Page Result.

**Printed section numbers count what LaTeX numbers (0.7.6).** The register
counts every unstarred `\section{` in each placed fragment, in `\input` order,
and gives the page the first one; a fragment whose inner divisions use
`\section` (md2tex mapping `###` that way) prints several numbered sections,
shifts every later page, and is reported: `its fragment prints N numbered
sections; inner divisions should be \subsection`. A page whose fragment has only
`\section*` prints no number and is shown as `(unnumbered)`.

## 🎭 The venue's format

A venue's format is settled once · The venue template checklist · Venue profiles: [ref/venue-format.md](ref/venue-format.md)

## ✉️ The cover letter lane

The cover letter lane · run-delivery-coverletter: [ref/cover-letter-lane.md](ref/cover-letter-lane.md)

## 📮 The portal packet

The portal packet · what is uploaded as it is: [ref/portal-packet.md](ref/portal-packet.md)

## 🔍 The LaTeX diff

What changed since the last round · the LaTeX diff: [ref/latex-diff.md](ref/latex-diff.md)

## ⚙️ Configuration

Each version keeps one `delivery/jNN_<version>/paper-build.toml` at the Block. Paths are resolved relative
to that config file. The following is the minimum contract; fields may be
omitted only when the selected profile supplies a declared default:

```toml
[paper]
id = "Paper-Example-Misq"
desk = "misq2026"
source_format = "latex-room"
venue_profile = "misq"

[pages]
# where the words come from: the version folder that holds the Sections, and the face whose
# `haipipe:compile-order` block fixes the reading order. Each page contributes its body fragment
# <Block>/delivery/<page-source-path>/latex/<page>.tex, its delivery/latex/selected-bibliography/<page>.bib, and the float.tex +
# asset of every display unit its fragment \ref's. (An older Board names its Ba-/Bb- groups and its Story Page.)
main = "../../j11_writing_v<MMDD>_<desk>"
appendix = "../../j11_writing_v<MMDD>_<desk>"
order = "../../j11_writing_v<MMDD>_<desk>/j11_writing_v<MMDD>_<desk>.md"   # the version face's compile-order block

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
main_docx = "word/Paper-Example-Misq-draft.docx"
supplement_docx = "word/Paper-Example-Misq-supplement-draft.docx"
main_pdf = "latex/Paper-Example-Misq-draft.pdf"
supplement_pdf = "latex/Paper-Example-Misq-supplement-draft.pdf"
section_snapshots = "word/draft-sections"
assets = "latex/submission-assets"
manifest = "build-manifest.json"
```

The version face's compile-order block and declared Section groups determine the
current build inputs. A missing or ambiguous order is a repair requirement,
not permission to read a retired planning Page or silently choose another
desk room. Inspect older adapters before use and report unsupported checks;
this contract does not claim that all historical parser paths were removed.
For the single-target interface, require exactly one complete marker block.
Reject duplicate or malformed Section entries instead of silently omitting
them; candidate tellings are narrative plans, not additional active blocks.

The engine validates configuration before any write or cleanup.
`paper-build.toml` lives in `<Block>/delivery/` for a Block build, or
`<Block>/delivery/jNN_<version>/` for a version build; `source.room` is exactly
`latex`. Generated paths must remain inside their declared output directory,
with no `..`, absolute path, symlink escape or overlap with authored inputs.
Missing `[pages]` or required output keys is an error, not a legacy fallback.
Keep the copyable `ref/paper-build.toml.example` aligned with this contract.

For a commissioned Workflow build, use `compile.<paper>.<build>` from
`haipipe-paper-workflow/ref/run-workflow.md`: the caller allocates the native
Ticket/Result and freezes inputs before invoking the mechanical builder.
Its manifest is the current delivery receipt; a Result may retain an exact
historical snapshot. A bare build invocation does not invent a Run identity.

Configuration selects and names inputs/outputs. It does not duplicate prose,
claims, values, citations, captions, or table cells. If a paper needs a
special section boundary or a nonstandard supplement, that behavior belongs in
the venue profile or an explicitly named adapter, not in a second hidden Word
source.

### A grant: no abstract, page-limited, the team's Word file as template (JL 261112)

A Grant Board's send (`Grant-<Slug>/`, e.g. an LOI Project Statement) has no Abstract: the Word lane then starts the
text right after the title and prints no Abstract heading. Its page rules go in `[profile]`: `body_size` (default 12),
`body_line_spacing` (default 2.0), `heading_upper` (default true), with `word_template` pointing at the team's own
Word draft so its styles and margins carry over, `title_page_fields = ["title"]` and
`front_matter = "title-abstract-keywords"` so the title shares page 1; the LaTeX lane's margins, font and size go in the
paper's `preamble.tex`. First user: a grant Board's `Grant-<Slug>/delivery/j11_writing_v<MMDD>_<desk>/`.

### A paper that owns its LaTeX (0.9.1, 0.11.3)

All opt-in; a paper that sets none of these builds exactly as before. Used by
a preprint paper (a journal main + SI, and one arXiv file).

| Key | What it does |
|---|---|
| `[source] head = "<file>"` | the paper's own preamble, `\documentclass` and `\title` included, inlined in place of the engine's package head and title block; the `.sty`/`.tex`/`.cls`/`.bst` files beside it are copied into the room, so the room stays self-contained for arXiv |
| `[source] opening = "<file>"` | what follows `\begin{document}` (default `\maketitle`) |
| `[source] supplement_head`, `supplement_opening` | the same pair for `supplement.tex` (S-numbering, its title, its note and contents) |
| profile `appendices = "supplement"` | `master.tex` is the main article and its references, `supplement.tex` the appendix lane alone (each appendix on a new page, its own references), `combined.tex` both; outputs `main_pdf`, `supplement_pdf`, `combined_pdf`. The Word lane reads `combined.tex` and still splits at `\appendix` |
| profile `[latex] engine = "pdflatex"` | `latexmk -pdf` instead of `-xelatex`, for a head that loads no fontspec |
| `[source] store = "<dir>"` | a paper-level display store a fragment reads by path (`displays/Figure/x.pdf`): each file it reaches, and each stored `.tex` it `\input`s, is copied into the room at that path; every Page that reads it is a G4 blocker until its floats are DISPLAY Results |
| `[evidence] draft_citations = true` | a DRAFT merges a Page's `draft-bibliography/<page>.bib` (written by a `delivery: draft` Page) when it has no `selected-bibliography/<page>.bib`; `reference.bib` says UNVERIFIED and every such Page is a G4 blocker |

Independently of these keys, a `\ref` to a label the room itself defines (a
fragment's own float or equation, a stored table) is not counted as unresolved
(`drop_room_defined()`); the LaTeX logs remain the check for what LaTeX could
not resolve. Teeth: `tests/test_paper_owned_documents.py`.

### Evidence receipt boundary

The optional `[evidence] lock` is a materialized receipt generated from the
Section Pages. It may identify the Section source, Page evidence item, type
(`VALUE`, `CITE`, or `DISPLAY`), state, and source paths. The engine uses it
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

`delivery/build.py --pdf-only` (0.17.0, JL 261104) is the quick look while writing: the stale check, the LaTeX PDFs and
the manifest, about a minute, no Word app. Word, the cover letter, the portal and the shared folder stay as the last full
build left them, and `send` and `release` refuse until a full build runs. A plain `build.py` stays the full build, since
co-authors get real Word (JL 261023).

**The shared folder is a round.** `[publish] dir` names a round's `clean/` (`.../RoundN-vMMDD/clean`) and its `files`
use the round's names (`N-<Name>-vMMDD-<kind>.pdf`); any other folder gets nothing and a ❗ line. The working files,
track/, previous/ and submission/ are haipipe-delivery's round verbs (`adopt-round`, `open-round`, `refresh`,
`check`): `haipipe-delivery/ref/round-folder.md`. `scripts/delivery_publish.py` holds the step.

`delivery/build.py --word-draft` (0.18.0, JL 261104: "we can use method B, as long as the table is at the top of that
page") is the working Word copy: Word prints it, but no page is measured. Each display floats to the top of the page its
citing text reaches (`float_display_to_top`), so it may sit above that text, and a display too long for the page moves
to the next page with its citing paragraph, which can leave white space. A display that needs a whole page keeps a page
of its own. The shared folder stays as it was, and `send` and `release` refuse until a full build runs.

**Before the first build of a new version** (JL 261122, the JAMA AI version of Paper-LLMRecPhy-Jama printed
1,397 of 3,000 words because three Sections were never adopted):

```text
1 compile order   the face's block reads   main: / - t00_abstract / ... / appendix: / - t21_<title>
                  (paper_ladder.py task writes each line; a numbered "1. t00_abstract" list is refused)
2 citations       a version made from another is paper_ladder.py next --from <version> [--desk <desk>]: it
                  carries draft/ whole, evidence/bibex/<task>.bib included (never `version` and hand copies)
3 adopt           page.py adopt <Section> for each Section whose ## Content is still the placeholder,
                  then export, then build; build.py check and the build name each such Section (❗, ⚠)
4 subsections     Methods and Results print a \subsection per `- C<n> · <title>` of the draft's
                  Structure Overview; a part named like its Section (`- C1 · Discussion`) prints none
```

The public operation is `assemble`:

```text
resolve Paper and its delivery/
  → load delivery/paper-build.toml
  → read the [pages] groups · check each page's milestone (outline tick,
    display PDFs, page PDF) · read the version face's compile-order block for order
  → regenerate delivery/latex/ whole: master.tex · sections/ · appendices/ ·
    displays/ · reference.bib, all copied from the pages
  → verify source files and accepted bindings
  → parse source with the selected adapter
  → render main manuscript and online supplement
  → render optional section snapshots
  → write assets and the build manifest
  → render DOCX/PDF previews and inspect layout when requested
  → ON SEND (a person's act, the Send card): name the comments batch this send
    will collect into, the review Job jNN_review_<kind>_v<MMDD>/ (page-type: comments;
    `build.py send j31` or its full name; an older <version>/reports/qNN_…/ or Round RD<NN>-… still works), and copy every
    declared output (main/supplement PDF + DOCX when present) plus the manifest
    and display register into its sent/
  → ON ROUND CLOSE: rebuild, then copy into that Round's released/
```

`sent/` and `released/` are frozen copies and never rebuilt in place; the
Round's close receipt under `draft/` carries their paths and manifest `built` times.
`haipipe-paper-comments` owns the folder shape. A freeze fails if any declared
output is missing or if the destination already contains a prior snapshot;
this prevents a partial send from masquerading as a complete Round.

The paper-specific command is the thin wrapper `ref/build.py.wrapper`,
installed as `delivery/build.py`:

```bash
.venv/bin/python delivery/build.py            # build · DRAFT unless every page is ready; stops on a stale fragment
.venv/bin/python delivery/build.py --accept-dropped-keys  # re-export stale Sections, explained key drops pass
.venv/bin/python delivery/build.py --allow-stale          # build anyway, stale fragments listed as G4 blockers
.venv/bin/python delivery/build.py check      # find every Section and fragment, list stale ones; writes nothing
.venv/bin/python delivery/build.py send q02   # freeze the current build into that comments batch's sent/ (an older reports/qNN_ batch)
.venv/bin/python delivery/build.py send RD02  # (an older Board) into that Round's sent/
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
2. inspect `build-manifest.json` and compare its `built` time and recorded
   config/source/profile/output paths against the declared files on disk; a
   source newer than `built` (file time or `git diff`) makes the build stale;
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
  config path, source paths, output paths, and the `built` time;
- a machine-readable `build-manifest.json` containing page readiness, counts,
  unresolved references, missing assets, word-count results, renderer outcomes,
  and build status.

The manifest is the sole delivery receipt; Page-level acceptance remains the
`CHECK` controller judgment. The display register is a derived reader index whose findings
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
  the version face's compile order agrees with `[pages]`, and every listed Section meets
  the milestone or is reported as not ready;
- no generated DOCX/PDF/snapshot is read as an input;
- every `\\input`, citation, label/reference, table asset, and figure asset
  resolves or is listed as a visible failure;
- when an evidence receipt is declared, its source bindings are recorded and
  final/submission modes reject pending or non-accepted evidence;
- no raw TeX commands or parser sentinels leak into emitted prose/cells;
- main-text word count uses the selected venue profile and states what it
  excludes;
- source, config and output paths, profile and engine versions, and the
  `built` time are recorded;
- DOCX structure has the expected tables, figures, headings, and sections;
- when `[venue_template]` is declared, both lanes are compared with the venue's template (§ The venue template checklist, [ref/venue-format.md](ref/venue-format.md));
- rendered pages are visually inspected when the output is being handed off;
- if the build is run before G4, the result is visibly marked `DRAFT`.

## 🔁 The final read

The final read · before an author reads a build: [ref/final-read.md](ref/final-read.md)

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
