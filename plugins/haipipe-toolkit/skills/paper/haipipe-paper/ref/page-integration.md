# Paper–Page integration contract

This reference is the Paper family's adapter boundary to the shared Page
contract. It records only Paper-specific consequences; the Page skill and
Page-workflow skill remain authoritative for the base Face, lifecycle, Runs,
Evidence Workspace, and Page release.

## 1. Ownership boundary

```text
haipipe-page
  Page Folder · Page Face · Page Run names · Page Runs · Evidence Workspace
  Page release · Page delivery · Page CHECK

haipipe-paper
  Paper Run Workflow · G0–G5 · Story C1–C8 · Story/Section bindings
  Venue library · Round routing · complete-paper assembly
```

Paper Page Types extend the Page Face; they do not reorder or replace
`Opening → generated Outline → Content → Aims`. A Paper Page may keep a fixed
`page-type:` declaration when its self-owned Page Type is the first matching
owner. This migration does not introduce a parallel `folder-kind:` system.

This adapter follows the current canonical Page Workflow, Page Run families,
and interactive-writing contract. On upstream changes, compare ownership,
loading order, IDs, release and Result boundaries before adopting them. The
2026-09-13 hash pin is retired because those sources changed; a hash alone
cannot establish compatibility. The Paper update record documents the checks.

## 2. Paper and Page routing

`haipipe-paper` selects the Paper operation. `haipipe-page` resolves an actual
Page's Folder/Face owner and `haipipe-page-workflow` loads the current Run Spec,
Paper Workflow, exact Paper PageType, and relevant references in its canonical
order. Load the Paper-specific owner only for that Page. A generic Page never
loads every Paper skill.

`page-type: ideation` resolves to `haipipe-paper-ideation`, which loads
`haipipe-ideation` for semantic generation/testing/selection or sync. The
semantic owner keeps the cards, sync schema and sole I3 decision; the adapter
owns the Paper presentation. Direct Ideation-only audits need not run Page.
Story, Section, Round and Venue likewise load their exact self-owned contract.
See `haipipe-paper-workflow/ref/run-workflow.md` for the Run Spec list.

Page controller `Run/cycle/next_cycle` fields are compatibility labels, not
Workflow units, Run Specs or Steps. Paper PageTypes are direct
`paper/haipipe-paper-*` entrypoints. One Page pass is a Workflow
Runtime/control record; only independently commissioned work gets a native Run
identity.

## 3. Run boundary

New Page interaction and evidence follow the shared RP/RE/RD contract:

```text
rp-struct-01               whole-Page SHAPE + SURVEY
rp-sec-01                  one Section writing session
rp-para-01_P01-P03          fixed paragraph-group goal
re-cite-01_<slug>           local citation Evidence Item
re-display-01_<slug>        local display Evidence Item
rd02_latex                 one Page delivery target/version
```

Local Evidence/Display work is Page-owned; its selected Task/Display worker
does not change that ownership. Independent Supporting Runs remain with their
Task/Discovery owner and full native identity. The historical `pm-/pa-/pr-`,
`pj...` and compact `rp00/rpNN` forms are read-only compatibility inputs, never
new allocation templates. See `run-naming.md` beside this file for the
ownership table and Paper judgment profile. Evidence does not satisfy human
writing acceptance, and a judgment never replaces I3 or G3.

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

## 6. Ideation projection route

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

Each successful surface transition writes the normal Page controller receipt under
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
a writing Run. Human prose feedback still uses the normal Writing Step/Page Run
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
and allocate current typed RP identities only when real Page interaction is
commissioned. Keep historical IDs unchanged.
Do not modify `_archive/`, frozen `sent/`/`released/` snapshots, or generated
delivery by hand.
