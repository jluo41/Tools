# Insight Run workflow migration · 2026-09-20

The current model has no Phase object, phase state, or I0–I5 execution order.
The six existing resource owners retain their skill names, Folder kinds and
DIKW evidence rules. Their paths move from `insight/workflow-phases/` to
`insight/folder-kinds/`; all loaders resolve owner metadata rather than assume
the old grouping path. Skill names remain the invocation identities. Installers discover the new paths
recursively. Existing installed symlinks that point to the retired paths need
to be refreshed with the normal repository installer before invoking those
installed copies; this source update does not reinstall an external environment.

| Retired label | Current resource owner |
|---|---|
| I0 | Meta inventory |
| I1 | Question registration and settlement |
| I2 | Data observations |
| I3 | Information derivations |
| I4 | Knowledge claims and pooling verdict |
| I5 | Wisdom counsel and person-signed handoff |

No row in this mapping implies a Run. New work declares bounded Run Specs and
uses owner-native Tickets, Results and receipts under `run-workflow.md`.
GI0–GI6 remain stable assertion keys with explicit resource/Run owners.

## Persisted identity

New fixed-kind Folders use Page `folder-kind:`. If an identity record is needed,
write `workflow/folder.yaml` with `current.folder-kind`; it records resource
identity only. A valid canonical identity record takes precedence over an old
`workflow/phase.yaml`. An invalid canonical record is a routing error, never
permission to select the old one.

When no canonical record exists, the reader can extract only `folder-kind`
from the old file. Its `current.phase` and phase-transition history have no
execution authority. This is a read-only import adapter, not a new writer path.
If the declared Page kind conflicts with the selected identity record, report
the conflict rather than choose silently.

On the next authorized identity edit, write the canonical identity record,
keep Page `folder-kind:` consistent, and retain the old file only as history.
New writers never emit the legacy file or metadata.phase. Legacy read support
can be removed only after an explicit inventory proves no supported records
depend on it; do not impose a calendar deadline that makes unopened boards
unreadable. Page engine fields/functions whose physical names contain `phase`
remain adapter implementation details pending their own API migration; they
do not define Insight objects, Run ids, Folder ownership, or user-facing status.

## Existing boards and receipts

No live Board is rewritten by this skill update. Settled historical Queue marks
and exact Result references retain their history. At the next execution,
inventory actual native Runs and accepted Results and create the aggregate
runtime from them. Never manufacture past Tickets/receipts from an old I#
label, Page pass, or CELL mark. Missing provenance is a named blocker.

Apply new record requirements on next touch. Existing person-reserved release
and signature requirements remain binding immediately; this update adds no
new person gate. Prior settled work with missing current-contract records is
reported as historical with an owed migration finding, not silently reopened
or accepted as current evidence.

The repository-side blast radius is the six Folder owner skills, Insight door
and controller/references, Task Insight wording, Folder discovery/identity
readers, and the Page/Board callers of those readers. The shared reader still
discovers unmigrated sibling families at their existing paths. Historical
CHANGELOGs and evaluation snapshots retain the paths and terminology they
originally evaluated. No inventory of external live Boards is implied.

## 📜 Contract bumps have a blast radius

A version bump edits no page, yet it can move the frontier: a new closing check un-closes every page that fails it, and the register then contradicts its own pages with nobody having touched either. Two rules make that safe:

```text
① every bump SHIPS ITS MIGRATION NOTE, the way ../../haipipe-insight/ref/partition.md grandfathers
  9-X-cross/ by name: what happens to artifacts settled under the older version.
  The default is OWE-ON-NEXT-TOUCH — settled cells stay settled, the page owes the
  new check when next opened. The exception is a bump that ADDS A HUMAN GATE
  (a signature, a release): that blocks immediately, because the risk it guards
  is live from the moment it is law.
② the bumping desk COMPUTES THE BLAST RADIUS before shipping: grep the live
  boards for every artifact the new check fails, AND the sibling law for every
  version pin the bump stales, and list both in the migration note by id. A bump
  that names FW01 and silently un-closes FW02 shipped half a migration — and
  sibling citations are best written UNPINNED, so there is nothing to stale.
  A patch that lands a rule must grep the family for every sentence stating the
  OLD rule: two rounds running, a rule split across files was updated in some
  and contradicted by the rest.
```

The register never flips backward on a bump: an affected cell KEEPS its mark and gains the blocked reading at the gate the new check guards, so "settled under 0.2.0, owing under 0.3.0" is visible without rewriting history.

## 🧾 Marks, spelling and receipts

```text
token spelling     a mark's spelling INCLUDES its spacing: `🚫 F-only` is the token,
                   `🚫Fonly` is not it. Canonical forward; a live board is re-spelled
                   only in an authorized sweep, and its tables re-pad in the same
                   sweep — two spellings in one column defeats the mark
a mark is not an edit   🧊 and its kin annotate ADJACENT to a sentence; the sentence
                   itself stays byte-identical. Marking a fenced line is therefore
                   legal where editing it is not
🧊 lifecycle       the mark names its staling event AND its clearing condition; it
                   clears when that condition lands, and a 🧊 whose clearing
                   condition has already occurred is a finding, not a mark
🟡-final receipts  the flip leaves TWO receipts, whoever flips — a person, a lap, or
                   a charter: one record in the register's
                   outline/<register-stem>-log.md QUOTING the licensing sentence,
                   and one record in the ANSWERING Folder's
                   outline/<answering-stem>-log.md naming the QUESTION id and the
                   word final (the shape the checker scans) — staleness travels by
                   citation, and a citation invisible from the cited end cannot travel
```


## 1.3.1 corrections

- Canonical Folder identity uses strict YAML mapping semantics: ordinary two-
  or four-space indentation and quoted scalars work; duplicate keys, malformed
  quotes, missing `current.folder-kind`, and Page/canonical conflicts are visible
  errors in the checker, Page, Context and Board Ask routes. Invalid canonical
  files never fall back to a legacy identity. Board cache observes identity edits.
- Retarget an ask by creating a linked successor id in its destination register.
  Preserve old cells/receipts; do not move a QI id into QK ownership.
- Ask can register the first row and writes the canonical Outline receipt plus
  a zero-Run registration Runtime. Legacy Page Log text remains history.
- Signed Wisdom lacking current payload/dependency pins and GI5/GI6 records
  is historical/unverified for current Design binding. The viewer preserves its
  signature and Queue history. Materialize records from owner evidence on next
  authorized handoff use; this adds no new person gate. See `handoff-record.md`.
- Static local Data sources still owe frozen Local Input and ready typed local
  Evidence. They do not acquire a synthetic Supporting Run.
- Current Task discovery uses `scripts/config`, Job defaults, and recorded native
  Ticket/receipt addresses. Old layouts remain read-only discovery inputs.

The repository changes cover the Insight skills, Task Insight bind/freeze helper,
shared Folder identity reader and its callers, and Board/Design projections.
External boards were not inventoried or edited by this patch; record their exact
missing pins/receipts when they are next opened. Existing installed skill links
are refreshed separately through their normal installer.
