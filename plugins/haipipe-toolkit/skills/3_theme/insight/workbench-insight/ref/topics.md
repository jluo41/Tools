# Insight topics

A topic records the current question, requirement and guard. fixed means its case passes with a guard; open names the work owed. Source prompts and event evidence are retained by topic id in the owning Block's [Trace](../../../../../../../examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1614_insight_topics_evidence.md). Consult the exact evidence before changing an existing verdict.

## Current index

```text
T01  what a question delivers                  fixed
T02  which check reads a ladder Board          fixed
T03  editing a version that is not signed      fixed
T04  an answer goes stale silently             open
T05  a refused Run looks like a missing Run    fixed
T06  Question Book gaps a check could catch    open
T07  a Question Book in /lab; host basics      fixed (host launch passed on)
T08  Executive questions on top of the map     fixed
T09  the Questions list: Executive first, closed  fixed
T10  data version provenance and ownership     open
T11  a step's worker reads a config nothing exports   open
T12  a prep Run can overwrite a folder made before    open
T13  audit could not read a DataPrep Block       fixed
T14  the step review's agent could not write agreed   fixed
T15  a step reads more than its raw export      fixed
T16  a step writes outside a folder of its own   fixed
T17  no prep step checks the stated experiment   fixed
T18  a page could show a record value            fixed
T19  the Board's Data view shows records        fixed
T20  a new prep version cannot order its steps  fixed
T21  three linked views: Folder, Element, Session  open (map sent, no code yet)
T22  a new prep version copies the Runs' notebooks  fixed
T23  a description from another pull stops a dataset  fixed
T24  a later step does not wait for the card    fixed
T25  a signature does not freeze a called library  fixed
T26  DataPrep holds code; the Board runs it     fixed
T27  a step cannot read a per-Board setting     fixed
T28  a cut key nobody reads is ignored          fixed
T29  a step's Result has no light summary       fixed
T30  a Board Job pins three versions           fixed
T31  a Run holds numbers and no reading        fixed
T32  a Run report cannot cite a row count      fixed
T33  structure needs its own types and names   fixed
T34  shared Job UI loses Insight distinctions  open
T35  organization must branch as a mind map    fixed
T36  shared map readability inside its Block   open
T37  shared Studio bindings and current contracts   fixed
T38  shared Bands and independent Studio Types     fixed
T39  explicit type catalogs and absent layers       fixed
T40  ordinary Work Studio scope and numbering       fixed
T41  shared type checker and member integration     open
T42  example face agrees with its question version  open
T43  Structure must use Folder Tree                 fixed
T44  Block Structure needs an owned Draw canvas      open
```

## T06 · Release prerequisites need executable checks · open

Rule: inspect the actual independent review verdicts and the person's segment/release decision before signing. A completed review can be returned; a collection placeholder is not consent. The workflow skill requires these checks even when a command accepts the files.

Gap: hai-insight/scripts/insight_ladder_book.py sign() checks local agreement, segment names and date format. Script-review verdicts, the full question review and actual segment consent need corresponding command guards and rejection tests.

## T10 · A prep output is not a new raw-data version · open

Rule: a Board pins raw data, question release and prep version independently. Its ready directory is the output of that combination.

Gap: InsightDataPrep-Example/board.md says the ready folder becomes the next data version. Align that example face with the current dataprep contract and add a source check before marking the topic fixed.

## T11 · Step cards must obey the preparation interface · open

Rule: a DataPrep step exposes run(ctx) and uses its declared context. The Board prep Task owns execution. Compare a Run card with the owning contract before dispatch; a conflicting prompt must not be dispatched.

Gap: hai-insight-workflow/ref/run-cards.md's Step script card requests a per-dataset scripts/config directory. The workflow skill prevents dispatch of that instruction, but the card, its generated consumers and a consistency check still need a coordinated update.

## T34 · Complete source membership in live Jobs · open

Questions: Can the shared reader include all retained release members, use semantic Board/Book/Prep groups and name each Block kind correctly?

Case: question-v2 includes eight kept members and K02; its local directory contains only the new Task. The structure adapter resolves release.yaml. The live reader must honor the same membership without copying questions. Prep step execution belongs to the Board prep Run.

Browser evidence: the Book title and selected K02 are correct, but retained members are absent from its Job navigation. DataPrep retains its Block route/title while the header says Insight Board and selected t01 displays no step content. Board preparation and DataPrep groups still use numeric labels.

Guard owed: shared-reader tests and real browser acceptance for all three Block kinds. A structure-render check alone does not close this topic.

## T36 · Shared map readability inside the Block · open

Rule: Structure uses Folder Tree; Draw uses its own preserved drawing source. Both keep readable text and source references, with the owning Work Block as the default entry.

Guard: delivery/structure/check_structure.py covers source ownership and authored changes. Structure Folder Tree acceptance is tracked in T43. At 390 × 844 the shared top-view row and horizontal Draw content require separate layout acceptance; those shared guards remain open.

## T37 · Shared Studio bindings and current contracts · fixed

Date: 2026-11-27. Source: user in this session; Work coordination from 01a1bc86-ab96-7021-83ab-d4f9f137557a. User authorization, verbatim:

> 好，我同意你现在就开始干嘛哈。

Questions: Do Structure and Draw pair rules with real examples? Are owning skills current? Do Job/Task previews remain in real Blocks? Are proposals and actual behavior distinct? Are Findings and source files referenced once across levels?

Work: the approved file plan is in b11 trace/261127/1602_insight_studio_bands.md. s01–s03 bind Structure / Job types / Task types / Draw / Skills. s11–s13 bind live Block selections, contracts, QuickHtml and Draw. Checklist items stay in the shared side pane. Generated bindings have one generator; main skill entries and structure rules describe the current contract.

Guard: check_structure.py and build_job_previews.py --check pass. Real b11 browser acceptance verifies the Folder Tree in Structure, inline sources, live Job/Task selection routes, owning skills and all three QuickHtml proposals. T43 records the Structure guard; T44 records the separate Draw gap. Fresh-context invocation distinguishes all three Block contracts, retained members, execution ownership and human decisions. T34 and T36 track the live reader and phone gaps separately; active card/example dependencies remain T06/T10/T11.

## T38 · Shared Bands and independent Studio Types · fixed

Date: 2026-11-27. User wording relayed by Work, verbatim:

> 他们的这个 band，应该是一样的，但是他们可能会有自己的，比如说 studio type 呀，有自己的 job 呀，有自己的这个，对吧，种类的。

Questions: Does b11 read the common Band registry? Does it reference shared types rather than copying definitions? Can a theme supply an actual distinct type without empty groups? Does s99 retain its sources as a Theme Guide instance?

Rule: Band is the shared outer classification. Studio Type is a separate content contract. b11 references Block Structure, Block Job UI Preview and Theme Guide. Existing instances require no additional local type. Keep actual Task procedures with their Task type/skill and keep s99's directory and content.

Guard: check_structure.py rejects local Band overrides and checks shared type links. The live b11 page displays its nonempty shared Bands. s99 keeps its directory and references Theme Guide (s78); it remains in the shared Guide Band (s9N). These are source references, not an invented instance-type configuration field. Work owns the registry and reader checks.


## T39 · Explicit catalogs and absent layers · fixed

Date: 2026-11-27. User in this session, verbatim:

> 你觉得现在我们对Insight的这个block type的这个structure算是定好了吗，还是没有定好。
> 好，我确认了，现在你就进行更改吧。

Paper coordination source: 01a1bc86-c6c8-7bc2-b236-7944edb1d34e, 2026-11-27. Relevant requirement, verbatim:

> 每个实例有 types.md，分 Job group type / Job type / Task group type / Task type，并说明 for 与 holds、真实源字段和技能所有者；不存在的层级明确说明，不为通过检查发明类型。
> Job types / Task types 由清单生成。复用 hai-studio/gallery/block-structure/scripts/block_types_pages.py；不要只换标题或只验证自己硬编码的按钮列表。缺少所有 types.md 时不能把“0 types / 0 problems”当作通过。

Questions: Does each Block have a complete catalog? Are groups separate from types? Do missing layers stay absent? Can the generated view be traced to its catalog and actual members?

Rule: A07 and ref/block-structure.md define the four sections, source/owner requirements and valid absence. All three catalogs are required. The shared generator owns the type pages. Local checks resolve every Book member and Board pin, with Prep execution owned by the Board.

Guard: check_structure.py rejects missing catalogs, invalid absence and type/source mismatches, and preserves authored map content. Shared generator checks pass for all three instances. Fresh-context invocation distinguishes every responsibility. Browser acceptance inside b11 verifies the generated For/Holds pages, full Book membership and source links, Prep code steps, and all three source-backed Structure trees. T43 guards the tree presentation; T44 tracks Draw. Shared member integration remains T41.

## T40 · Ordinary Work Studio organization · fixed

Date: 2026-11-27. Same user approval and Paper coordination as T39. Relevant requirement, verbatim:

> Structure 里的 Folder / Job-Task / Studio 是否齐全：Folder 是带〈变量〉的命名规则；Job-Task 分组与类型分开；Studio 写清该实际 Block 的 Band 名称、编号和主题组织。不能拿 Blueprint 的 Band 当作实际 Block 的全部设计，也不能只有几个主题示例。

Questions: Does Studio show applicable ordinary Work categories and shared numbering? Are proposed purposes distinct from actual topics? Do the actual examples keep their real Block/Job/Task owners and grouping?

Rule: A08 requires shared numbering for new topics, proposed purposes in 〈〉, and real examples derived from source owners/configured bands/group order/tags. Existing identifiers remain; no empty topic is created.

Guard: check_structure.py checks the shared writer ranges, source owners/bands, proposal distinction and no invented Prep Studio. Fresh-context invocation and browser acceptance confirm those distinctions; Board Studio instances retain data-version names. Source-label display and authored-node reparenting have regression checks. Phone layout remains T36; its clipping is reproduced at 390 × 844.

## T41 · Shared type-check and member interfaces · open

Date: 2026-11-27. Source: the T39 approval and shared-generator inspection in b11 trace/261127/1057_insight_structure_types.md.

Questions: Can shared checking represent absent layers and reject an empty catalog inventory? Can type pages resolve Insight release members and open selections within their Block?

Gap: hai-studio/gallery/block-structure/scripts/block_types_check.py requires all four sections to contain types and succeeds with no catalogs. block_types_pages.py matches only explicit job-type/task-type fields and builds child-path member routes. Insight source semantics and retained membership need a shared adapter/selection interface. The local guard and inline examples cover this theme; they do not repair those shared interfaces.

Guard owed: shared rejection tests for missing catalogs, valid-absence cases for Book/Prep, complete release-member matching and Block-owned routes, followed by browser acceptance. Research records must not gain invented fields just to make these checks pass.


## T42 · Example face agrees with its question version · open

Date: 2026-11-27. Source: fresh-context skill invocation for the T39 approved change, agent validate_insight_structure_types.

Question: Does the actual Book's introductory face describe the same version naming rule its source Jobs and skill use?

Gap: examples/Project-Ladder/insight/InsightQuestionBook-Example/board.md:9 writes jNN_pN/; the current contract and actual folders use jNN_question-vN_〈slug〉. The structure resolves actual release.yaml members correctly. The example face and a consistency guard need a separate approved change. The DataPrep ready/data wording is tracked in T10. Neither example source was modified in this structure-only file plan.


## T43 · Structure must use Folder Tree · fixed

Date: 2026-11-27. User in this session, verbatim:

> 怎么还继续恢复用现有 meglimap啊，我们不是说用 full tree 吗？我操。

Questions: Are all Structure items and their inline examples vertical Folder Trees? Are Draw content and bindings separate? Does a regression check reject replacing Structure with a mindmap? Do source links and actual memberships survive the change?

Rule: A02 and shared s71 Job-Task require Folder Tree in Structure. The source model remains authoritative across views; types/groups and actual folders do not change. Native details/summary, branch lines, existing level colours and normal-size labels supply the presentation.

Acceptance: check_structure.py passes and rejects both restored mindmap markup and a Draw fragment selected by Structure, for each Block kind. The fresh-context invocation confirms these checks and the current rule. Actual b11 browser acceptance exercises all three Structure items across s01–s03, expanded rules and actual examples, source hrefs, normal-size labels and hover responsibilities. At 390 × 844 the tree is visible and expandable; deep indentation still leaves narrow labels and the shared top-view row overflows. T36 stays open for phone layout. T44 separately tracks the missing owned Draw canvases. Evidence and scope audit are in b11 trace/261127/1057_insight_structure_types.md.


## T44 · Block Structure needs an owned Draw canvas · open

Date: 2026-11-27. Source: fresh-context Folder Tree review and current S71 Draw contract, corroborated by Paper's coordination notice.

Questions: Does each of s01–s03 own one Excalidraw canvas? Does Draw show that canvas full width without left tabs?

Gap: these three actual folders contain no Excalidraw file. Draw still binds separate map fragments. Preserve their sources, but do not call this S71 Draw acceptance or reuse a Job UI Preview canvas for another Studio type. The current approved correction changes Structure; adding three canvases and validating their structural patterns needs its own exact file plan. Inline real examples remain the user's explicitly approved placement; the shared standalone Examples wording needs reconciliation.
