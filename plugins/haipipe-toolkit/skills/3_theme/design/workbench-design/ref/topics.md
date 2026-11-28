# Design topics

Current rules and unresolved work. Source messages and detailed receipts are retained in the
[Block Trace](../../../../../../../examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1548_studio_content_alignment.md).
A topic is fixed only when its case passes and a guard keeps it passing. The IDs below retain their recorded
identity; their evidence is linked from the Trace.

## T01 · Folder, element and session mapping · open

Question: can every work folder be reached through its page element and work episode?
The folder contract is `hai-design/ref/design-ladder.md`; current layout tables are in `design_focus_layout.py`
and `design_focus_block.py`. Trace records work episodes; it is not automatic full-chat capture.
Owed: a shared, checked folder-to-element/session mapping. Keep traces outside the frozen input fence and Results.

## T02 · Design Job contracts · fixed

Board execution pins one signed goal, method version and inputs version. Book Jobs own a method identity and
signed version files. The ladder and this skill describe that contract. Guards: `current_contract_check.py`
and the scaffold and method registry tests.

## T03 · Embedded Main and Task navigation · fixed

`design_jobs.py` supplies Board Main, Method Main, role-specific Task step tabs and original Runs to the shared
Jobs selector. Main hides Task selection; picking a Task retains the Block. Guards: `test_design_jobs.py`.
The separate Overview / Tasks / Findings consolidation remains open under T17.

## T04 · Conversation in Trace · fixed

Record prompts, approved concrete file plans, changed paths and checks in the owning Block's Trace. Missing
message times are not fabricated; a summary is not an exact quotation. Guard: `hai-trace/scripts/trace.py check`.

## T05 · Content visible in the Workbench · fixed

Enter through the real Board or Book. Embedded Job content and its actions come from the shared reader;
preview validation never submits release approval. Guards: real-example Design Job tests and browser checks
recorded in Trace. New source edits require a new running-page check before claiming deployment.

## T06 · Structure Studio per Block kind · fixed

s01 describes Design Board; s02 describes Design Method Book. Structure includes rules and real examples,
Draw uses shared drawing code, Skills opens the owners. Guard: b12 `build_organization.py --check`.

## T07 · Page words · open

The real Board Report and release sections print redundant state words. `design_jobs.py` passes “waiting for you”
to Review and approve and “done” to Delivery. Owed: scoped reader changes and another actual page scan against
`hai-ui`. A Studio or skill edit does not make those embedded pages compliant.

## T08 · Types and concrete names · open

Verified Task values are `design-reason`, `design-item`, `design-whole`. The Board's single execution Job contract
and the Book's method Job contract remain distinct. No serialized Job enum is declared by the current examples.
Owed: an owning-contract decision if a `job-type:` field is required, plus type presentation in the shared scheme.
Do not turn method family or Ideas / Designs / Review into new execution types. Guard: current contract check.

## T09 / T10 / T11 · Shared structure drawings · fixed

Structure uses the shared folder-style tree; each parent appears once in its branch and Book branches end at
Job name. The shared S71 colors distinguish levels; meanings sit on hover. Expand branches without shrinking
text. Default entry is the owning Block; source selections stay in its preview. Guard: b12 builder's
check_structure() and actual-browser expansion checks; T21 records the current acceptance.

## T13 · Blueprint Studio organization · fixed

b12 contains s01/s02 Block Structure instances and s11/s12 Block Job UI Preview instances. Outer Bands come from
shared Studio definitions. Each topic fold remains independent. Guards: shared Studio tests and the b12 builder.

## T14 · Method-family grouping · fixed

Board Jobs group by their pinned method's registry family; the goal remains in the label. Book Jobs use authored
family, registry family, then Methods. Guard: `test_board_groups_by_method_family_and_names_pins` and the Book
cases in `test_design_jobs.py`. The Board fallback to a goal remains supported when no method family is present.

## T15 · Rules and their actual instances · fixed

The b12 generator imports the shared folder tree for Structure and drawing code for Draw. Each Structure entry includes its real example;
its named Block entry uses the shared live renderer. Skills remains a top view. Guard: `build_organization.py --check`.

## T16 · Current skill instructions and shared Studio ownership · fixed

Date: 2026-11-27. Source: Work owner `01a1bc86-ab96-7021-83ab-d4f9f137557a` relayed the user:
“他们的这个 band，应该是一样的，但是他们可能会有自己的，比如说 studio type 呀，有自己的 job 呀，有自己的这个，对吧，种类的。”
User confirmation: “好，现在我允许你去进行更改，更改完你。”

Questions: do entry points state one current contract, preserve writer/gate ownership, distinguish type from
family, and point at actual Studio sources? Does skill invocation lead to the correct Block and specialist?

Scope: seven entry points, the ladder, this topics file, the owning constitution and current-contract guard.
Evidence: scaffold Task writer; actual example faces; `design_jobs.py`; two manifests; b17's shared Studio source.
Guard: `scripts/current_contract_check.py`, relevant Design tests and fresh-context invocation checks.
Checks: current-contract guard and structure freshness pass; existing skill/reader suites pass; both fresh-context
invocations pass after correcting the goal-name schema and caller-owned gates. Browser Skills previews show the
current contracts. Documentation changes do not imply executable writer changes; T19 records the remaining gap.

## T17 · Main consolidation and preview comparison · open

Board Main currently has Brief, Tasks, kept designs, Ranking, observations, release/Delivery, Workflow and Runs.
The approved target is Overview / Tasks / Findings. Owed: implement the separately scoped reader plan and test
all actions and original Runs; verify s11/s12 highlight targets and Checklist comparison coverage on real pages.
Method Main keeps its method-specific content and does not gain Tasks merely to match the Board.

## T18 · Shared Studio Type refinement · fixed

Date: 2026-11-27. Work owner relayed the instruction to separate Bands from Studio Type definitions, retain
needed theme-specific types, and place procedures with Task types/skills and guidance with Theme Guide.
Questions: have the shared definitions and reader landed, and does b12 still match their current contract?
Design reads `b17/delivery/page-spec/studio-bands.json` through the shared adapter and defines no redundant
catalogue. The generated pages pass the shared-source freshness check. Browser verification after the shared
owner's rollout shows the registry's Band names in b12 and only populated outer Bands. Actual topics and drawings
remain in place. Guard: `current_contract_check.py --structure`; shared type coverage belongs to the Work owner.


## T19 · Writer enforcement and Delivery ownership · open

Date: 2026-11-27. Source: fresh-context invocation check of the approved Design contracts.
Question: do writers fully enforce the invariants the caller must preserve?
`hai-design/scripts/design_ladder.py:320` creates Job-local `delivery/`; the storage contract requires Block
Delivery. The allocator does not reject every competing open Run; the Job gate checks input-directory existence
without validating the frozen manifest; the draft projection does not check generation closure. The entry points
now assign those checks explicitly to the caller and distinguish workflow projections, delivery's `released`
and a person's `dropped` state writes.
Owed: separately scoped writer and regression changes, including the Job-local Delivery mismatch. Do not claim
these implementations fixed by the passing documentation guard or remove existing output by hand.


## T20 · Block Structure inventories and absent layers · open

Date: 2026-11-27. Paper owning session `01a1bc86-c6c8-7bc2-b236-7944edb1d34e` relayed:
“然后你怎么把相同的要求发给其他的那些block，其他的三十他们也 follow 这个 block 呢。”
User approved this session's four-file inventory plan: “好，现在我确认了，然后现在就进行这个更改吧。”
Coordination scope, authorization and validation are in the
[inventory Trace](../../../../../../../examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1727_block_structure_types_alignment.md).

Questions: does each real Block kind have an inventory, do groups remain distinct from types, can an absent
Task layer be represented without fabrication, and does Studio organization describe the actual Block kind?

Sources: b12 s01-design/types.md and s02-workbench-ui/types.md; Design ladder; example faces; design_jobs.py
`topic()` / `task_topic()`; shared hai-studio block_types_check.py and block_types_pages.py.
The inventories state the semantic Design execution and Method type Job contracts, the three serialized Board
Task types, grouping inputs, owning skills and names. No separate group-type enum or serialized Job enum is
established by the current contract. Book execution Task groups and types are absent, not pending creation.

The shared checker requires a nonempty list at every level and accepts a scan finding zero inventory files.
It also skips missing job-type/task-type fields. Until that contract is extended, explicitly require both
inventory files and compare every real Task face; record expected absent/undefined-list diagnostics without
calling the shared check passed. Shared generation reads only for/holds, matches serialized types, and links
members via their folder paths; owning sources and semantic-only Job membership need verified presentation.

Owed: shared support for absent versus undefined lists and nonempty inventory coverage; inventory-driven
Job types / Task types views; actual Board/Book Studio Bands and numbering; render/expansion/source-link
acceptance. Preserve expandable Structure trees, embedded real examples and manual drawings. This four-file batch changes
no page binding, shared renderer, execution record or service. T08 keeps the serialized Job-type decision.


## T21 · Structure uses folder trees · fixed

Date: 2026-11-27. User: “现在是什么情况？要进行下一步了吗？然后你的这里的这个 的这block，S01，S02，你那个东西都要，那个 structure 都要变成 folder tree啊，不要用 mind map。”
Question: do all s01/s02 Structure models use readable expandable folder trees, including embedded record outlines?
Rule: use b17 tree_html and the common S71 level stylesheet. Keep Job group → Job → Task group → Task
parentage, omit absent Book Task levels, put meanings on hover and keep source selections inside their Block.
Scope: six approved files; Draw bindings, manual canvases and actual execution records remain outside this edit.
Guard: build_organization.py check_structure() validates tree rows, parent links, level classes, actual source
URLs and absence of a mind map in Structure. Actual Block-page expansion and source navigation must also pass.
Receipt: [folder-tree Trace](../../../../../../../examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1832_structure_folder_tree.md).
Checks: both builders and the current-contract guard pass; negative mutations reject a mind map in Structure,
wrong hierarchy colors and altered source URLs. Fresh-context skill invocation passes. Actual Block browser
acceptance verifies both Folder trees, Job/Task and Studio trees, branch expansion, common colors and hover,
Method Book ending at Job, and actual Board/Book Job plus Board Task links inside their owning Block previews.
The existing Draw bindings and manual canvases are preserved. T20's type-view and Studio-contract work remains open.
