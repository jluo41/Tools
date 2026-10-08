# Corpus preparation for labeling

This is the design and implementation contract for preparing structured
transcript corpora before Data → Contract. The five source-owned Corpus Runs,
their file checks, the group-aware reservation, and Data → Preparation are
implemented for transcript JSONL. The Labeling job catalogue has 26 Run
Types; corpus-contract remains its first job-scoped Run. Other raw formats,
conversation-level and span-level units, and stratified group draws remain
extensions that need their own workers and validation.

## Decision and ownership

A labeling item is derived from a versioned source and a versioned unit recipe.
Preparation is an upstream, reusable work object with native Runs and Results.
Its logical owner is the Corpus Preparation folder for that source snapshot;
its Runs use full `run-corpus-...` names. New Labeling job Runs use full
`run-labeling-...` names. Their owners and folders
distinguish the two kinds of work without abbreviated family codes.
The source folder is a local metadata anchor even when raw bytes remain in
remote custody; its manifest binds the immutable source identity and digest.
The Labeling Workbench projects those Runs in a Data → Preparation
View on a Page after a source owner is attached. The View does not own or duplicate the upstream Runs. A Board
may link to the Page, but the Page folder and upstream receipts are the source
of truth.

This boundary matters when the same transcript source supports several label
questions. Normalization, unitization, and the partition of source groups can
be reused. Each Labeling job still has its own corpus-contract, human semantic
authority, G0 confirmation, and later Labeling Runs. A prepared item set says what
is judged and what context is visible; it does not decide the class meanings.

The first held-back reservation is an upstream custody Run before Contract.
The existing Quality → Test test-reserve Run Type is a separately commissioned
supersession of a job's frame, not a second name for that initial reservation.
A frame change after a job is created needs a new lineage and explicit
invalidation of dependent work.
When test-reserve is implemented, it must use the same group and custody law;
the present item-level draw cannot serve as its worker for multi-item groups.

## One labeling unit

A unit recipe freezes these choices before any candidate item is released:

| field | decision |
|---|---|
| source snapshot and normalizer | exact immutable raw version; parser and turn-order rule |
| target selector | final assistant reply or every assistant reply; conversation and span recipes require a future worker |
| target text | the exact field/span a human judges |
| context policy | earlier turns only, role-marked, with an explicit window and rendering version |
| leakage group | conversation, encounter, patient, or a larger linked group that must never cross partitions |
| exclusions | malformed order, missing target, empty text, duplicates, and declared scope rules |

For user U1 → assistant A1 → user U2 → assistant A2, a final-reply recipe
produces one item whose target is A2 and whose context is U1, A1, U2. An
every-reply recipe produces two items: A1 with U1 as context, and A2 with U1,
A1, U2 as context. Both items carry the same split_group_id. A
conversation-level recipe instead produces one item with the whole declared
conversation as its target. Neither the parser nor the UI decides this
granularity implicitly.

The prepared row projected into the current engine has at least:

~~~json
{
  "item_id": "c17:t4",
  "source_snapshot_id": "source-v1",
  "item_set_id": "items-v1",
  "conversation_id": "c17",
  "split_group_id": "c17",
  "target_turn_id": "t4",
  "text": "A2",
  "context_prev": "user: U1\nassistant: A1\nuser: U2",
  "unit_recipe_id": "assistant-every-v1",
  "source_ref": "transcript-17"
}
~~~

item_id is unique within one item set. item_set_id distinguishes different
recipes or parser versions that may reuse an item_id. split_group_id is stable
across recipes of the same source and partition scope. A private lineage map
resolves each item to source record and target span; public rows carry only
source references permitted for development. The configured text_field is the
target, and context_field is the rendered prior context. Structured turns may
also be retained under custody, but the current engine consumes these string
fields.

Derive item_set_id from the immutable source snapshot, normalizer, recipe and
canonical item-set digest. Derive partition_id from the source snapshot,
grouping rule, source group universe and versioned draw frame, independently
of how many target items a later recipe emits.

## Run graph and completion results

Only independently closable work receives a Run. Individual transcript edits,
turns, items, previews, retries under unchanged inputs, and a person's bare
approval are Steps or evidence inside a Run. A Run Type is a reusable operation
such as `unit-materialize` or `corpus-contract`; a concrete Run is one Ticket
and its matching Result for a specific target. Use the same readable stem on
disk and in the Workbench:

| owner | concrete Run name | example |
|---|---|---|
| Corpus Preparation | `run-corpus-<operation>-<MMDD>-<target>` | `run-corpus-unit-materialize-0929-assistant-replies` |
| Labeling Page | `run-labeling-<operation>-<MMDD>-<target>` | `run-labeling-corpus-contract-0929-job-v1` |

The `<operation>` segment is the stable Run Type key; the whole `run-corpus-...`
or `run-labeling-...` stem is the concrete Run's full name. `MMDD` is the opening date, not an
input version; the Ticket binds exact input versions. Append `-2`, `-3`, etc.
if a name is already taken in its owner's `runs/`. The words `run-corpus` and
`run-labeling` identify the family, but are not complete instance names. This
follows the Page Workbench's readable `run-<kind>-<MMDD>-<slug>` direction;
the Paper Workbench likewise shows full `run-...` names, though some older
Paper files still have short internal IDs.

| upstream Run Type | frozen target and result | close rule |
|---|---|---|
| source-normalize | one raw snapshot → normalized conversations plus reject ledger | stable IDs, roles, ordering, and source lineage; unresolved records excluded with reasons |
| unit-recipe | one source contract and target/context policy → versioned recipe | target, context cutoff, grouping and exclusions accepted by the named preparation owner |
| unit-materialize | one normalized source × recipe → private candidate item set and lineage | deterministic IDs and counts; full candidate text stays under custody |
| unit-check | one candidate item-set version → QA report | schema, unique IDs, context cutoff, lineage, exclusions, duplicates and group rules pass or fail explicitly |
| initial-group-reserve | one accepted item set × source-level frame → fenced development package and protected reservation | whole leakage groups assigned once; counts and custody receipt reconcile |
| existing corpus-contract | one accepted fenced package × label question → Page-local job and `run-labeling-corpus-contract-...` Result | the engine verifies custody and group disjointness under the protected file boundary, copies eligible rows and an opaque reservation, then waits for G0; the UI never shows protected IDs |

Any upstream operation can reuse an exact accepted Result. The current transcript
worker requires a source-normalize Result, including when the input is already
structured transcript JSONL; a future source adapter may accept an existing
versioned normalized snapshot instead. No placeholder Run is allocated. A changed source, normalizer, recipe, group policy or
reservation frame creates a new version/Run and preserves the old Result.
A failed check blocks reservation;
a failed reservation or binding check blocks corpus-contract without creating
a successful Labeling Contract Result. The source-normalize worker may be an
existing data pipeline when it actually supports that source format; a transcript parser is
not assumed to exist merely because haipipe-data exists.

## Partition and custody law

Reserve complete source-level leakage groups, never independent item IDs. Use
one stable partition scope for jobs derived from the same source snapshot and
group policy, so a conversation cannot be development data for one label and
sealed test for another. A recipe may change which items exist without
silently changing that group's partition. If the group definition or frame
changes, mint a new partition version and invalidate dependent jobs.

The reservation request specifies a number or fraction of groups, not an
exact number of items. Group sizes vary, so an exact item count and whole-group
assignment cannot both be promised. A seeded draw over sorted, unique group
IDs makes the result invariant to input row order. Optional stratification
uses one declared source-level value per group; conflicting values are refused
unless a versioned aggregation rule resolves them. Record source/development/
sealed group counts, resulting item counts, seed, strata, and group inclusion
probabilities. Check that no group or item appears on both sides. Duplicate or
linked sources that could expose the same target across groups must be merged
under the declared grouping rule or rejected before reservation.
If the resulting sealed item count cannot support the declared test plan,
acceptance fails. Select a new frame before development release; after release,
a new frame requires a new lineage and invalidation of dependent jobs.

Before the reservation closes, raw and full candidate text are available only
to authorized preparation and custody workers. Development-facing Page files,
prompts, previews, embeddings and search receive no candidate text. After it
closes, only eligible item text may enter the Page's labeling/corpus/items.jsonl.
Sealed text stays in source custody; protected IDs, group IDs, and hashes are
confined to the protected reservation manifest. Public receipts show counts,
rules, versions and digests, not protected IDs or text. Review candidate
units under custody, including multi-turn and exclusion cases, before
acceptance.

## Files and Workbench projection

Inside a SPACE (the nearest folder holding `env.sh`), two storage rules hold. Every path a
record keeps (a Run's `raw_path` and `config_path`, a package receipt's `owner` and
`package`, a Page's `preparation-owner.yaml` and `preparation-ref.yaml`) is written relative
to the SPACE root, never as `/Users/<name>/...` (AGENTS.md rule 7), and read back with
`resolve_stored`; an older absolute record still reads, and two records that differ only in
how a path is written agree (`same_reference`). Every `*.private.*` artifact (normalized
conversations, rejects, candidate items, lineage) is written to and read from
`_WorkSpace/LabelingStore/_custody/<its path from the SPACE root>`, so the corpus text never
sits in a git-tracked folder; the Run's Result still lists it by its path in the owner.
Outside a SPACE both rules fall away and the files stay where the paths say.

Space and View are interface locations, not required folder names. The
upstream owner keeps canonical Tickets, Results, full candidate data and
custody artifacts in its own native locations. The Labeling Page stores a
non-sensitive owner attachment followed by a reference to one accepted version:

~~~text
<source folder>/corpus-preparation/
  source.yaml
  runs/run-corpus-<operation>-<MMDD>-<target>.yaml
  results/run-corpus-<operation>-<MMDD>-<target>/runtime.yaml, result.yaml
  versions/<snapshot>/normalized.private.jsonl, rejects.private.jsonl, manifest.public.json
  versions/<snapshot>/recipes/<recipe-id>.yaml
  versions/<snapshot>/itemsets/<item-set-id>/items.private.jsonl,
    lineage.private.jsonl, manifest.public.json, qa.public.json
  partitions/<partition-id>/frame.public.json, frame.protected.jsonl
  packages/<item-set-id>-<partition-id>/config.yaml, corpus/items.jsonl,
    corpus/manifest.json, test/sealed/*, preparation-receipt.json

<Page>/
  <page>.md
  labeling/preparation-owner.yaml     source owner and source ID; may exist before any Run
  labeling/preparation-ref.yaml       source, recipe, item-set, QA and partition
                                     IDs/digests plus the five upstream Run names
  labeling/corpus/items.jsonl         eligible text, only after corpus-contract
  labeling/test/sealed/               opaque protected manifest and public status
  runs/run-labeling-corpus-contract-0929-job-v1.yaml
  results/run-labeling-corpus-contract-0929-job-v1/...
~~~

The `--page-file` for attach, link, and Contract must be the canonical
`<Page>/<Page>.md` file. A flat Board source has no isolated `labeling/` lane;
create its Page folder before attaching a source. The Workbench may read a
flat Board source as a bridge to an existing Page folder, but never uses the
flat group's shared directory as the destination for a new job.

`attach --owner <source>/corpus-preparation --source-id <source> --page-file
<page.md>` first writes a small, immutable Page reference. The Workbench then
shows source-owned Tickets and Results as they close, before a package exists.
This attachment is not a Run and contains no candidate or protected content.
The accepted-package reference binds source snapshot, recipe, item-set, QA,
partition and fenced-package identities with content digests and upstream Run
names. It contains no raw or sealed text. The Workbench's Data →
Preparation View follows those references to show actual upstream Run states,
QA and custody summaries. Linking occurs after an accepted reservation; the
Page shows progress from the earlier owner attachment and then narrows the
panel to the five Runs bound to its accepted package. Its Run prompts route to
the upstream owner; its panel never invents Page-local Labeling Tickets. Data → Contract offers a
copyable setup request only after the accepted preparation and reservation
binding exists; the request names the accepted package and asks for the target
and named authorities before creating a Page-local job. A Page can
show Preparation before labeling/config.yaml exists, so Board discovery must
recognize a preparing Page as well as an established job. A standalone
Workbench uses the same Page files; Board navigation is optional.
Upstream Results are light receipts with digests and pointers, not copies of
the row-level corpus.

The Run Type's reusable worker and Result defaults belong to its native owner.
The Run Spec × Workbench cell binds the Skills needed on this surface. The
View has one primary context Skill, haipipe-labeling-preparation; its
supporting Skills vary by operation:

| Preparation Run | primary View Skill | supporting guidance when relevant |
|---|---|---|
| source-normalize | haipipe-labeling-preparation | haipipe-data only if its source pipeline actually owns the input |
| unit-recipe | haipipe-labeling-preparation | haipipe-labeling-building for the human target/context boundary |
| unit-materialize | haipipe-labeling-preparation | source-processing Skill when the selected worker requires it |
| unit-check | haipipe-labeling-preparation | haipipe-labeling-building when a semantic unit judgment is needed |
| initial-group-reserve | haipipe-labeling-preparation | haipipe-labeling-building for custody and sealed-test restrictions |

The native owner consults haipipe-run when allocating or auditing these Runs;
that does not turn every code-worker call into a Skill invocation. Do not mechanically attach the current four
Labeling Skills to these upstream Runs. The existing 26-row job catalogue and
its four-entry bindings remain unchanged.

## Implementation boundary and acceptance checks

`engine/corpus_preparation.py` implements the five source-owned Runs for
structured transcript JSONL, including deterministic reply/context units,
QA, source-group reservation, a fenced eligible-only package, and a Page link.
`engine/job.py create` verifies the accepted package's digests and group-frame
receipt before writing a Labeling Contract. The Workbench has Data →
Preparation and Board discovery recognizes an attached Page before
`labeling/config.yaml` exists. New Labeling writers use full names; readers
still recognize old short-named Tickets. The browser continues to copy Run
prompts; it does not silently execute them.

New preparation packages write a v2 receipt binding the source, recipe,
candidate set, QA, group frame, and delivered config/status/manifest bytes.
Early v1 packages remain readable through their original narrower digest
checks and can be linked without changing their accepted receipts.
The shared host blocks direct static access to JSONL, `corpus-preparation/`,
and `labeling/` files. Other private raw formats must remain outside its served
root.

`engine/fence_source.py` remains an item-level path for already-unitized,
single-unit legacy sources. Its outputs have no source-group safety proof.
The Contract validator still parses supported protected ID/hash records under
the protected file boundary to reconcile source counts, although the UI never
renders those IDs. The protected group frame stays with the source owner.
Conversation/span recipes, additional raw formats, source-level group
stratification, and a group-aware implementation of the later job-local
`test-reserve` Run Type remain unimplemented; do not claim those operations
ran from a catalogue entry alone.

Acceptance requires: every assistant reply has the declared earlier context
and no future turn; all items of c17 and every other leakage group stay in one
partition for every seed and input order; the same source-level partition is
reused across compatible recipes and label questions; public Page output has
no sealed text or protected IDs; counts and digests reconcile; a changed input
mints a new version; and a missing or mismatched proof prevents
corpus-contract from allocating a successful Labeling Contract Result.
