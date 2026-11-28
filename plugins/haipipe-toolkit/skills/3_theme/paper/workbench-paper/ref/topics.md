# Paper topics

A topic is one current question or problem. `fixed` requires the reported case
and a continuing guard; `open` records the remaining work. Source reports and
wording are preserved in the [Blueprint Trace](../../../../../../../examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1548_studio_alignment.md).

## T01 · A Writing Job resolves its session prefix · open

- Recorded case: two Writing Jobs have no own `session-prefix`, while the Board
  names one; `/hai-lab` cannot resolve which prefix to use.
- Question: when may the Board prefix be used without sharing sessions between
  simultaneous Jobs?
- Owner: `hai-paper/scripts/create_section_sessions.py` `board_prefix()` and
  `open_writing_lab.py`; source report in the Trace.
- Owed: a precise fallback rule and tests for a single active manuscript versus
  simultaneous independent Writing Jobs.

## T02 · Lab prerequisites are checked before opening windows · open

- Recorded case: the lab opens windows without the terminal extension needed to
  start its sessions.
- Question: how does the plan report a missing extension and stop execution
  before opening unusable windows?
- Owner: `hai-paper/scripts/open_writing_lab.py` `extension_installed()` and
  `ref/writing-lab.md`.
- Owed: prerequisite checking in the plan and execution path, with an isolated test.

## T03 · The writing lab resolves a reachable origin · open

- Recorded case: a SPACE host runs but the lab resolves no page URL when its
  settings do not name an origin.
- Questions: what configured origin does the lab use, and how is a missing one
  reported before launch?
- Owner: `hai-paper/scripts/open_writing_lab.py` `board_origin()` and `page_url()`;
  shared launcher configuration belongs to Workbench.
- Owed: one generic configuration rule, a visible plan finding and a regression
  case. No deployment-specific prefix belongs in source code.

## T04 · Resuming a Section sends its required first prompt · open

- Recorded case: resumed Section sessions receive no first-turn prompt.
- Question: when is the next review prompt required, and how is an already
  answered review protected from duplication?
- Owner: `hai-paper/scripts/lab_launch.py` and `ref/writing-lab.md`.
- Owed: the resume rule, implementation and a regression check.

## T05 · Idea Jobs retain identity through Paper handoff · open

- User: “I’m thinking about to make the idea to be one specific block them self. And one idea will be a job and then in the task, they are a series of skills to evaluate it and check it. Do you get what I mean? I hope each idea will be developed to one paper later. What is your thoughts”
- Rule: one candidate Job owns its Card, assessments and reviewed selection;
  Paper links to that exact source revision.
- Guard: ideation ownership/selection checks and the source adapter.
- Verified: Idea-Example has three candidate Jobs, source Cards, assessment Tasks and live navigation.
- Owed: live acceptance of selection and Paper-handoff controls.

## T06 · Paper and Idea use shared Job navigation · open

- User: “那你知道你该去怎么去设计吗？然后你能不能比如说做一个 plan，然后设计一下这些东西呢？然后跟其他的保持一致，尤其是跟这个 work block 里面内容，就是说保持一致吧。你明白我意思吗？”
- Rule: Job and Task selection remain inside the owning Block. The shared
  framework supplies navigation and Main; the selected work supplies content.
- Sources: b16 s11 Idea preview, s13 Paper preview, `delivery/page-spec/job-ui-design.md`,
  and the shared `focus_jobs` content composition.
- Verified: Idea-Example and Grant-Example bind real Folder, Jobs and Studio views;
  Grant Draft Tasks render their authored application text.
- Owed: the remaining Main/Task controls, including the Job adapters in T13.
  Authored application content does not certify execution support.

## T07 · Block structure distinguishes groups, types and names · open

- User: “你这里面不能用index了，哎呀我操，这个就是你是具体的paper，你的paper你的block，你还有一二三四吗？你应该就是有具体的名字了呀。 就是你不要再用那个 drop 1、drop 2、drop 3 了，你应该是找 Q的 example。你比如说我刚才讨论的那什么，第一个 drop group 是 story 啊，第二个是那个 evidence 啊，这个应该写这个呀。”
- Rule: Paper/Grant use Story, Evidence, Display, Writing and Presentation;
  Review/Submission belong within Writing. Variable instance names use `〈 〉`.
- Question: which semantic roles have an explicit execution contract and a
  verified source face?
- Owed: reconcile Paper value/citation type fields with the shared Task owners,
  and define Story/consolidated Evidence/Presentation execution boundaries.
  Real Idea/Grant examples are bound; their content grants no execution authority.

## T08 · A simple structure tree · fixed

- User, 2026-11-27: “他们有那个studio type，你的studio type是啥呀？不是说不要用 mind map 了吗。”
- Rule: A04. Structure uses S71's folder-style trees; the four Job-Task levels
  carry the common colours. Purpose stays on hover and unused levels are omitted.
- Guard: `check_block_structures.py` checks the actual bindings, rendered rows,
  parents, hover text, level classes, palette and default expansion.
- Verified, 2026-11-27: all three live Studios show expandable Folder and
  Job-Task trees. Paper's shared colours are visible; Writing expands to Review
  and Submission. Independent fresh-context review and the guard pass.

## T09 · Shared Studio Bands with theme-owned content · fixed

- User request relayed from Work theme design, 2026-11-27: “他们的这个 band，应该是一样的，但是他们可能会有自己的，比如说 studio type 呀，有自己的 job 呀，有自己的这个，对吧，种类的。”
- User approval in this session: “你确定你整好了吗？你也就是按照这个方案去更新了吗？你有什么计划？如果你有计划的话，你就按照计划去执行吧。”
- Link request: “然后你要把这个链接给我一下，我打开看一看，好吧。”
- Questions: does b16 read shared Bands, keep its own real types, retain the
  simple structure, embed its verified example and open owning skills?
- Current rule: A05; s01–s03 follow the shared Block Structure type. Paper-Example
  appears in Examples with its live Folder, Jobs, Studio and Block views.
  Idea-Example and Grant-Example bind the same live views.
- Guard: `check_block_structures.py --bindings-only`, shared Studio rendering
  tests and actual-page acceptance. Verification is recorded in the Trace.
- Verified, 2026-11-27: the live Block opens its Paper structure, the real
  Paper-Example and owning skill files. The bindings guard, shared rendering
  tests and fresh-context skill invocation pass. T07 retains the separate
  execution-contract gaps.

## T10 · Block Structure instances follow their shared Studio Type · open

- User, 2026-11-27: “我觉得首先你对这个你的这个Blueprint这个block呢，就是你的这个S01、S02、S03，并没有按照，就是说这个Studio Type去设计。你能不能check一下skill和check一下B17里面的设计啊。”
- Authorization: “那你赶紧就是执行一下，把他们给拉起来，好吧？要align with this。”
- Coordination request: “然后你怎么把相同的要求发给其他的那些block，其他的三十他们也 follow 这个 block 呢。”
- Cause: the Paper manifest, skill A05 and binding guard all repeated a private
  three-view definition. That guard did not check the shared s71 requirements,
  four type lists, Folder models or numbered Studio Band definitions.
- Rule: s01 Idea, s02 Grant and s03 Paper are instances of one Block Structure
  Studio Type. Type catalogs distinguish semantic proposals from current fields.
- Check: shared type pages and local conformance guard; actual Studio navigation;
  fresh-context workbench-paper invocation. Execution gaps remain T07.
- Verified: three catalogs and all bindings pass the strengthened guard;
  twelve shared rendering tests pass. Fresh-context review found and then
  verified the fixes for Draw omissions, child-path links, Example Studio Bands
  and Idea-owned Folder records. Browser acceptance confirms the shared views,
  source inventories, live Folder/Studio, one Draw canvas, owning Skills, and a draft
  member selecting its Task inside Paper-Example.
- Verified: all three catalogs now bind real examples; the shared checker reports
  no missing examples. Idea and Grant Folder, Jobs and Studio open inside b16.
- Owed: type-page membership currently uses explicit single-token fields;
  inferred Idea/Writing kinds do not populate every member list. T07 tracks
  execution contracts, and T13 tracks the remaining Grant Main adapters.
- Coordination: the same requirement was delivered to Work, Insight, Design,
  Labeling and Knowledge's owning chats. The shared type generator's child-path
  defect was reported to Work; this theme adapts its destinations locally.

## T11 · S71 presentation is checked, not just its view names · fixed

- User, 2026-11-27: “我觉得你做的不对吧，你他妈错了啥玩意儿。你这个，不是啊，我让你，哦靠，等一下，你这个做对吗？你看一下这个B17的这个S71是怎么设计的。”
- Clarification: “他们有那个studio type，你的studio type是啥呀？不是说不要用 mind map 了吗。”
- Authorization: “你现在就是说去整整吧，好吗？去，啊，check一下啊，更新一下吧。”
- Cause: the guard checked manifest names and source parity but omitted S71's
  folder-tree presentation. A04 also specified the wrong component.
- Rule: the three Studios reference one shared Block Structure Studio Type.
  Structure uses the b17 folder tree, with S71's common level colours. The
  authored outline is data; it must not choose the visible UI component.
- Guard: active Structure bindings reject focus-map content; rendered nodes,
  parents, purpose hovers, level classes and default opening are verified.
- Verified, 2026-11-27: browser acceptance opened all three instances inside b16
  and expanded their Job branches. Fresh-context review checked the rendered
  hierarchy, bindings, shared component and skill. Isolated mutations confirm
  the guard rejects missing hovers, wrong levels, closed Folder roots and
  mind-map content. T10 retains the separate type-member mapping gap.


## T12 · Idea and Grant examples are actual Blocks · fixed

- User, 2026-11-27: “再去生成一下idea和grant的那个example吧,不要再等了。”
- Questions: do both Examples bind real Blocks, and do their Jobs, Tasks and
  Studio topics contain readable content?
- Rule: Idea-Example holds one candidate per Job with source Cards and assessment
  Tasks. Grant-Example uses Story, Evidence, Display, Writing and Presentation
  groups; Review and Submission are Task groups within each Writing Job.
- Sources: `examples/Project-Ladder/paper/Idea-Example`, `Grant-Example`;
  b16 s01/s02 `types.md` and `studio-views.json`.
- Guard: `check_examples.py` checks ownership, current Draft parsing, source links,
  Task registers and the absence of fabricated scientific execution or selection.
  `check_block_structures.py` checks the live bindings against the shared type.
- Verified: browser navigation inside b16 opened Idea Cards, assessment Tasks and
  its Landscape; Grant Writing → Submission → Cover letter displayed the actual
  Draft sentences, and the Aims Studio displayed its comparison table. These are
  illustrative content examples; T07 and T13 remain separate execution/UI work.

## T13 · Grant Main respects each Job's semantic role · open

- Trigger, 2026-11-27: browser acceptance for the T12 request.
- Question: can the shared Paper adapter show Story and Presentation Main without
  treating them as manuscript versions?
- Cause: `servers/workbench-paper/board_read.py:384` classifies unmatched Job names
  as Writing versions; `paper_version.py:178` consequently supplies their Main.
  Grant-Example's Presentation Main shows a Story/Sections template and
  “No story yet.” despite authored Job content.
- Verified scope: Grant's Writing navigation, Draft Tasks and Studio content work.
  Story/Evidence/Presentation execution types still require the T07 contracts.
- Owed: role-aware Main adapters and a regression check against these real examples.
  This example-creation change does not modify shared routing or restart the service.
