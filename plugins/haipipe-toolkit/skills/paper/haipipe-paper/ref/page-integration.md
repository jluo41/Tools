# Paper–Page integration contract

This reference is the Paper family's adapter boundary to the shared Page
contract. It records only Paper-specific consequences; the Page skill and
Page-workflow skill remain authoritative for the base Face, lifecycle, Runs,
Evidence Workspace, and Page release.

## 1. Ownership boundary

```text
haipipe-page
  Page Folder · Page Face · Page phases · Page Runs · Evidence Workspace
  Page release · Page delivery · Page CHECK

haipipe-paper
  paper journey · G0–G5 · Story C1–C8 · Story/Section bindings
  Venue library · Round routing · complete-paper assembly
```

Paper Page Types extend the Page Face; they do not reorder or replace
`Opening → generated Outline → Content → Aims`. A Paper Page may keep a fixed
`page-type:` declaration when its self-owned Page Type is the first matching
owner. This migration does not introduce a parallel `folder-kind:` system.

This adapter is frozen against the current shared Page baseline as of
2026-09-13: `haipipe-page` 0.89.0 (`SKILL.md` SHA-256
`64cca86d33b52a3a51ed5019d9cd84cb44555a4e8ec0acd5f15d5bef505982d`),
`haipipe-page-workflow` (`e1eee1209ab87cd1e076fdf89cd573dc359c560002b2a92ffdf9977975a8a1a`),
and `haipipe-page-content`
(`20eefbc8122c8c22560d989a0363adda92243b5ca0bb95aeb640c0f7476d1ef`).
If any of these sources changes, rerun the Paper compatibility audit before
adopting another Page migration.

## 2. Page phases inside the Paper journey

The Paper journey and the Page lifecycle are different axes:

```text
Paper: P0 Ideation → P1 Story → P2 Evidence/Execution → P3 Section
       → Compile → P4 Round

Page:  00 CONTEXT → 01 OUTLINE → 02 EVIDENCE → 03 CONTENT → 04 CHECK
```

P2 remains an external work lane. A Story releases Discovery/Task work;
owner-native receipts return to Story rows. A Section then runs the shared
Page lifecycle. Paper never invents a private Page lifecycle.

## 3. Run boundary

Human feedback and acceptance use the Page-owned namespace:

```text
rp00_mermaid-structure
rp01_p01
rp02_p02-p03
```

Delegated writing, Discovery, analysis, rendering, and other output-producing
work remain owner-native Task Runs (`rNN`, `rlNN`, or the owning global
identity). Paper-local typed Evidence/Display work may use `pm-`, `pa-`, or
`pr-` identities, but these remain Task-lane Runs and never satisfy a Page Run
prerequisite. The old `pj...` and `rNN_page-writing...` records are read-only
history and are never bulk-renamed.

The Page-global paragraph sequence is `P01…PN` across all Content divisions.
`C<n>.P<m>.B<n>` remains the readable Bullet address, with `P` never resetting
at a new `C`.

## 4. Page release and Paper gates

Closing a Page Run does not adopt prose into the Page source and does not
refresh delivery. Page CONTENT/release happens only after all planned Page
Runs and required Evidence Results are ready and bound; Page CHECK then judges
that released version.

- G3 releases a Story Section Narrative row for a Section to work on. It does
  not substitute for Page Shape approval, Page release, or Page CHECK.
- G4 admits only current Section outputs whose outline, cited display previews,
  Page delivery, accepted evidence, and Page CHECK version are all resolvable.
- Assembly may run before G4, but its manifest must say `DRAFT` and name the
  missing Page or Paper obligations.

## 5. Source and projection law

The Page Markdown and its `outline/` records are authoritative. A Section's
`delivery/latex/<page>.tex` is the Paper assembly input; the Paper-level
`delivery/` tree is generated from those fragments and the Story compile order.
No generated Word/PDF, retired room, or Round snapshot becomes a wording
source.

The current Page product exposes only its Page Face. Logs, discussions, files,
requirements, evidence records, and historical drafts stay under `outline/`
or an explicit archive. `## Diagram`, `## Outline`, `## Files`, `## Log`, and
`## Discussion` are not new authored Page sections. A diagram belongs in a
Content division map or the Page's visual lane.

## 6. Ideation P0 projection route

The Paper Ideation Page is a generated projection consumer. Its semantic source
is `projection/paper-ideation-sync.yaml`, owned by `haipipe-ideation`; the Page
does not copy Result Cards, create a second portfolio, or write an I3 decision.
The sync packet identifies a `sync_revision`, `source_hash`, and
`projection.change_class`:

| Change class | Page route | Page Run |
|---|---|---|
| `state` | refresh the generated working projection | none |
| `portfolio` | refresh by stable `idea_id`, then inspect shell impact | none unless human prose feedback is requested |
| `structure` | route through OUTLINE/SHAPE and stop if a shape decision is open | only when human interaction is required |

Each successful surface transition writes the normal Page phase receipt under
the Page's `workflow/` receipt lane. Its Paper-specific `paper_projection`
extension names the source packet, consumed revision/hash, Page path, surface
(`working`, `release`, or `delivery`), output hash, and timestamp. The three
surfaces are independent:

```text
working projection  → Outline/preview/Bullet Workspace
release             → adopted Page Content
delivery            → generated web/LaTeX/Word/PDF output
```

Working projection refresh is not an interactive Page Run and never allocates
`rpNN`. Human prose feedback still uses the normal Writing Step/Page Run
contract. Release and delivery remain behind the Page release barrier and
cannot be claimed current from a sync packet or working receipt alone.
The adapter reads Page receipts on its next sync and is the only writer of the
sync packet's nested `paper_page` state; Page never edits the semantic packet.
Portfolio order is an attention aid; `idea_id`, not list position, is the
stable projection identity and must not cause silent Page-global paragraph
renumbering.

## 7. Migration rule

Migrate current active Pages in place. Preserve stable Story, Section, claim,
Evidence, and historical Run identities. Use the Page migration command for
Page-global paragraph addresses, classify old Runs rather than renaming them,
and create `rp00_mermaid-structure` only when real Page interaction begins.
Do not modify `_archive/`, frozen `sent/`/`released/` snapshots, or generated
delivery by hand.
