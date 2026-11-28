# Labeling UI contracts

## Shared Studio Bands and type references · open

Current request, relayed by chat `01a1bc86-ab96-7021-83ab-d4f9f137557a`, 2026-11-27:

> 他们的这个 band，应该是一样的，但是他们可能会有自己的，比如说 studio type 呀，有自己的 job 呀，有自己的这个，对吧，种类的。

Which source owns Bands? The shared `studio_types` and `studio_tabs` readers provide Band names and order.
Bands group folds; Studio Type definitions specify content. Labeling supplies content, with no local Band override.
Each Band groups independent topic folds; empty Bands are omitted.

Current refinement, same sender and date:

> 共用 Band 与 Studio Type 是两件事；保留 Studio Type 分组，但取消 b17 的 S75 Task Procedure、S77 Studio Type、S79 Guide 三个独立类型定义。

The shared registry is `examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json`,
read by the shared reader separately from type definitions. Keep actual process topics and their folders; ordinary
Work Blocks show instances without mandatory type-definition topics. Source and browser grouping checks pass.
Work's Block Structure definition still declares Structure / Job types / Task types / Draw / Examples / Skills;
its requirements need reconciliation with the approved embedded-example contract. That shared-definition
integration remains open; Labeling does not edit the shared reader or type definitions.

Which topics belong here? b15 s01–s03 are Block Structure topics for Itemization, Guideline Generation and
Labeling at Scale, referencing Work's Block Structure definition. s41 Items and s42 Building remain process
instances owned by their corresponding Task skills; they do not require a separate Task Procedure definition.
No additional Labeling Studio Type definition is needed for this inventory. A workflow or Studio topic does not
establish a Block type. A theme's Job types do not establish Bands.

How do instances show? A Block Structure topic keeps Structure / Draw / Skills with applicable type views
generated from `types.md`. Structure and Draw each contain Folder, Job-Task and Studio. Verified examples stay under their corresponding content;
the owning Block opens through the shared preview and pop-out. Skills reads the family door, responsible Task
skills and workbench reader from their actual files. Changes to Block Job UI Preview's Delivery/Instances controls
apply to that Studio type only.

Guard: `examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py --check` verifies shared
Band sources/order, omitted empty Bands, catalog-derived views, separate Structure/Draw bindings and real source
files. `hai-studio/scripts/topic_titles_check.py` checks topic names against their shared Band.

## Type and name boundaries · fixed

Current request, relayed by chat `01a21d6c-cdee-7580-aeda-b1852ffb4a14`, 2026-11-27:

> 每一个 block，之所以跟其他 block 不一样，那就是它们的 job name、job type、task name，它们应该有自己的名字……先放在 block structure，它里面 job 种类是什么、job name 是什么、task 种类是什么、task name 是什么，这个一定要弄出来……给每一个 session 发 message，让他们重新更新 plan，然后执行。

What is fixed? Itemization uses `items`; Guideline Generation uses `labeling-meaning` and `labeling-expression`;
Labeling at Scale uses `labeling-scanning` and may have an independently authorized `eval` Task. Describe/build/check,
expression methods/rounds and Test/Scan/Audit are operations within those Tasks. They do not create Job or Task types.

What varies? Job and Task names follow source/recipe, construct/scope or release/population. Slots and undecided
names use `〈 〉`. Job topics are grouping metadata; no separate Task topic layer is defined. A Job without Tasks
ends at its Job node. Independent Job Type values remain unspecified until supported by an owning contract.

How are relationships shown? Structure uses Work’s shared `tree_html` and CSS for collapsible folder trees.
Job Type → Job Name → Task Type → Task Name preserves unique parents and evidenced names. Studio ownership
and embedded examples use that tree presentation too. Draw uses `frame.mindmap_module()` through separate
fragments. Both read the same content model. Folder shows actual storage paths without changing them.

Guard: the structure builder checks source excerpts, placeholder labels, unique parents, multiple names of one
Task type, Jobs without Tasks and the identity of shared renderers. Each Structure fragment must contain a
folder tree and no mindmap; Draw must use its own drawing fragment.

## Independent Block contracts and production UI · open

Which boundaries are agreed? Itemization accepts a source snapshot and recipe and produces immutable Items;
Guideline Generation binds Items, a construct and human authority and produces signed guidance; Labeling at Scale
binds Items, a signed release and executor configuration and produces audited labels. The Block is the only page;
Jobs, Tasks and Runs remain internal selections and records.

What is evidenced? b02_labeling_walkthrough has a Job with Items, Meaning and Expression Tasks and their Studio
records. b03_itemization, b04_guideline_generation and b05_labeling_at_scale are synthetic design previews without
corresponding Job/Task folders. Their custom preview shell does not meet the shared Report / Studio / Jobs contract.
The b04 model's expression-method Jobs and operation Tasks conflict with the Meaning/Expression Task ownership.

What is owed? Register the three independent Job types in their owning contracts; implement folder writers and
shared Block content adapters; persist operations through guarded writers; migrate the preview models; verify
production inputs, receipts and custody. On the running host, the combined b02 example opens at its Block,
but `section=work` resolves to Report and its section picker exposes no Jobs entry. The embedded example therefore
does not prove internal Job/Task selection. The workbench skill and CLI must return owning Block URLs for child
selections. `delivery/page-spec/shared-framework-plan.md` records the implementation scope in b15. Structure
presentation checks cannot close these production requirements.

## Block Structure type catalogs and actual Studio Bands · open

Current request, relayed by chat `01a1bc86-c6c8-7bc2-b236-7944edb1d34e`, 2026-11-27:

> 然后你怎么把相同的要求发给其他的那些block，其他的三十他们也 follow 这个 block 呢。

Each of the three Block Structure instances needs its own `types.md`, with Job group type, Job type,
Task group type and Task type; for, holds, actual source fields and owning skills. An absent level is declared
without inventing a type. The shared `block_types_pages.py` supplies the type pages. Missing catalogs and
empty Task inventories fail the Labeling coverage guard; a shared zero-file success is not acceptance.

The independent examples contain preview designs, not executed Jobs. Their Job identifiers and actual Work
Studio Band names/numbering remain unregistered. The model preserves those gaps with bracketed slots, rather
than copying Blueprint Bands. The combined walkthrough supplies real record evidence only. The optional `eval`
adapter reads final labels/external gold, while its owning scaffold expects ModelInstance/AIData; align inputs
before creating that Task. Scanning qualification is a different operation inside `labeling-scanning`.

The common requirements specify an Examples view and a single Draw canvas. This chat's approved variant embeds
examples with their subject. Structure uses folder trees; Draw retains the shared diagram presentation through
separate bindings. Shared type-definition reconciliation is open. Human canvases and actual Folder records are preserved.

Shared interfaces still owed: `block_types_check.py` flags every empty group or Job list as missing, including
explicitly absent levels; it also succeeds with no catalogs. `block_types_pages.py` currently makes child-page
links for real members and does not render owner/source metadata. This theme does not patch either shared helper.
Its preview examples have no members; actual evidence opens through the embedded Block and canonical file links.
The shared checker also skips membership validation when a real face omits its type field; this remains a shared
coverage requirement, distinct from the catalog presence and provenance guards.

Acceptance needs a real Block browser check plus fresh-context skill invocation, as well as generated-page and
catalog coverage checks. Passing presentation checks does not close these contracts or establish execution.

## Structure uses folder trees · fixed

Current user request, 2026-11-27:

> 现在是什么情况？要进行下一步了吗？然后你的这里的这个 labeling 的这三个 block，S01，S02，S03，你那个东西都要，那个 structure 都要变成 folder tree啊，不要用 mind map。

What changes? In s01 Itemization, s02 Guideline Generation and s03 Labeling at Scale, Structure’s Folder,
Job-Task and Studio subjects, including their embedded examples, use the shared collapsible folder tree.
The tree keeps role labels, evidenced names, source links and notes. It changes presentation only.

What owns the view? Work’s `tree_html` and CSS supply the tree. Labeling adapts its existing verified hierarchy.
Draw’s Job-Task and Studio use separate drawing fragments; its Folder keeps the tree. Both views read the same
generated document and content model. File storage, type
catalogs, the actual example records and human canvases retain their ownership and names.

Guard: `delivery/structure/build.py --check` requires a folder tree and forbids a mindmap in every Structure
fragment; it checks dedicated Draw bindings, parentage, names and source files. Browser acceptance must expand
Job-Task and Studio trees in all three Studios and confirm their Block route remains.

Acceptance: all three Structure entries opened from the Labeling Work Block (Blueprint) in Chrome; Job-Task and Studio
branches expand, example trees and source links remain, and the Block route is retained. The builder, scoped topic
titles, three generated type-page checks and 12 shared Structure tests pass. Fresh-context skill invocation confirms
the folder-tree rule, shared renderer identity, Draw’s Folder exception and unchanged work-record ownership.
