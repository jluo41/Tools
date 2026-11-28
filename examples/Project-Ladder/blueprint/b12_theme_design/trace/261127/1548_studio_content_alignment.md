---
title: Design Studio content and shared Bands
date: 2026-11-27 15:48
aim: Align Design Studio content with shared Bands and publish the approved current skill contracts, preserving real examples and responsibilities.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1548_studio_content_alignment.md
  what: Record the approved page work, checks and outstanding skill scope.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/build_organization.py
  what: Embed examples with their rules, remove the separate Examples view, read shared Band names and guard the result.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-board.html
  what: Rebuild from the updated source.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-methodbook.html
  what: Rebuild from the updated source.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
  what: Structure contains the live Board example; Draw and Skills remain.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
  what: Structure contains the live Book example; Draw and Skills remain.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/s01-design.md
  what: Describe current views and the existing Task types accurately.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/s02-workbench-ui.md
  what: Describe current views; preserve the Book's absence of Tasks.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
  what: Align views, grouping and the actual task-type fields.
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
  what: Align views and shared Band source.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/hai-design/SKILL.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/hai-design-goal/SKILL.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/hai-design-unit/SKILL.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/hai-design-workflow/SKILL.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/hai-design-delivery/SKILL.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
  what: Approved current-contract skill batch; details below.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Approved current-contract skill batch; details below.
- do: add
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/CONSTITUTION.md
  what: Approved current-contract skill batch; details below.
- do: add
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/scripts/current_contract_check.py
  what: Approved current-contract skill batch; details below.
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1548_studio_content_alignment.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-board.html
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-methodbook.html
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/s01-design.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/s02-workbench-ui.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
- plugins/haipipe-toolkit/skills/3_theme/design/hai-design/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md
- plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/hai-design-goal/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/hai-design-unit/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/hai-design-workflow/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/hai-design-delivery/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/scripts/current_contract_check.py
---

# Design Studio content and shared Bands

## Prompts

Work owner relayed the user's clarification: “他们的这个 band，应该是一样的，但是他们可能会有自己的，比如说 studio type 呀，有自己的 job 呀，有自己的这个，对吧，种类的。”

The same instruction confirms approval to remove the independent Examples top view for Block Structure while retaining its real examples and owning Skills. Apply that existing approval to the previously authorized Structure source and bindings. New skill-body cleanup is a separate file plan awaiting confirmation.

## Findings

- The live migrated b12 already has shared Block Structure and Block Job UI Preview Bands. No shared server changes are required.
- The Structure builder hardcodes two Band names internally and still requires a separate Examples view.
- Board Task faces already use design-reason, design-item and design-whole. Groups Ideas, Designs and Review are not those types.
- The Book's method Jobs hold signed versions; there are no execution Tasks.
- Skill entries contain historical layouts and comparisons. This needs a separately reviewed current-contract rewrite; no skill file is changed in this page batch.
- The schedule request was withdrawn as a misunderstanding; no schedule work remains.

## Check

- Rebuilt both pages and manifests from the source; `build_organization.py --check` passes with the SPACE Python 3.13 environment. System Python 3.9 cannot import the shared host's current annotations.
- Browser: b12 opens at its migrated Tailscale Block route; both shared Bands render, each Studio fold remains independent.
- s01: Structure / Draw / Skills only; Job rule expands through the three Task groups; the corresponding real example expands separately with all on-disk Jobs and Tasks.
- s02: Draw expands through Job name and has no Task layer; Skills opens the actual hai-design-method file; the real Method Book loads inside Structure.
- Both real Block embeds retain their own Block heading and navigation.
- Source links carry owning-Block Job/Task selections. Replaced popup targets locally with the current preview target. Browser verification: clicking M01 opens DesignMethodBook-Example Jobs with j01 selected, the Block heading and its Method / Steps / Versions / Used by content intact. A guard rejects popup targets in generated pages.
- Expanded maps can exceed the narrow frame width; text remains full size. No shared layout or server was changed or restarted.
- Approved skill batch: seven entry points, ladder, constitution, topics and current-contract guard updated; skill versions unchanged. Goal schema now includes the slug name required by the scaffold.
- Current-contract guard with --structure passes. Negative checks reject a missing goal name, superseded instructions and bare placeholders; fixture checks reject an invented Task type and execution Tasks in Method Book.
- Existing Design specialist suites: 111 passed, 4 skipped, 16 subtests passed. Design Job/focus reader suites: 23 passed. Total: 134 passed; the 4 skipped cases are opt-in Chrome rendering tests.
- README fresh-context invocation: both Design execution and Design UI reviewers pass the approved documentation scope. They checked specialist routing, input fences, actual Task types, Book without execution Tasks, human release gates and Block-owned navigation. No signing or release was performed.
- Actual browser after Work's shared rollout: s01 Skills shows the current workbench-design contract and goal-name schema; s02 Skills shows the current Method Book contract. Structure's Studio organization uses the shared registry, including its Skills Band. Only populated outer Bands render; folds remain independent.
- Rebuilt the two approved HTML outputs after the shared registry changed; freshness passes. Design changed no shared reader, registry or server and performed no restart.
- Scoped git diff --check passes. Pre-existing inputs.md and older-page.md changes were preserved. No repository cleanup, deletion or commit performed.

## Remaining

T08: serialized Job-type decision and explicit Task-type presentation in the structure graph. T17: Overview / Tasks / Findings Main implementation, s11/s12 highlight targets and Checklist comparison coverage. T19: writer enforcement and Job-local Delivery mismatch. T07: remaining page-word issues. Broader referenced historical documentation is outside this approved entry-point batch. These obligations remain open in workbench-design/ref/topics.md.

## Summary

The approved page and current-skill batches are complete and verified. Structure embeds its real examples, Draw and Skills remain, and Design reads the shared Band registry while preserving its own Board/Book contracts. Current entry-point rules and invocation checks are guarded; original topic history is preserved below. T16 and Design's T18 adoption are fixed. This closure does not certify the remaining Main, preview, type-presentation or writer changes listed above.

## Approved skill batch

These are additional files beyond the page batch. Preserve valid responsibilities and references; historical narrative belongs in Trace/Git. Do not change skill version numbers or delete called implementations.

- `plugins/haipipe-toolkit/skills/3_theme/design/hai-design/SKILL.md` — current Board/Book routing and naming; remove historical layout narrative.
- `plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md` — current folder and type contract, groups distinguished from types.
- `plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md` — current method identity, signed versions and no execution Task layer; reconcile version-governance wording without changing the version.
- `plugins/haipipe-toolkit/skills/3_theme/design/hai-design-goal/SKILL.md` — current goals, input versions and fences only.
- `plugins/haipipe-toolkit/skills/3_theme/design/hai-design-unit/SKILL.md` — current reason/generate/verify/revise/rank responsibilities only.
- `plugins/haipipe-toolkit/skills/3_theme/design/hai-design-workflow/SKILL.md` — current Run routing and gates only.
- `plugins/haipipe-toolkit/skills/3_theme/design/hai-design-delivery/SKILL.md` — current release ownership, conditions and sign-off contract.
- `plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md` — current Block-only navigation, two Job contracts, shared Bands and actual s01/s02/s11/s12 previews; distinguish live behavior from unimplemented Main design.
- `plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md` — record this topic and current unresolved obligations, with historical detail linked to this Trace.
- `plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/CONSTITUTION.md` — add the current-only contract and shared Studio ownership rules with their checks.
- `plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/scripts/current_contract_check.py` — guard current entry-point rules, valid owning links, Book without execution Tasks, and the shared Band source.
- `examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1548_studio_content_alignment.md` — record confirmation and results for this additional batch, separately from completed page checks.

Validation: run the focused guard and existing Design tests as applicable, then README's fresh-context subagent invocation checks. Audit remaining referenced files before proposing further cleanup; do not silently delete historical files that still have readers. Broader historical reference migration is not certified by this entry-point batch.

## Skill batch approval

User, 2026-11-27: “好，现在我允许你去进行更改，更改完你。”

The approved list above is now active. Skill versions and executable writers remain unchanged.

Additional coordination: shared Bands and Studio Types are separate. Work owns removal of the independent Task Procedure, Studio Type and Guide type definitions; preserve actual Task procedures and Guide content. No shared reader or server changes are authorized in this batch. Shared rollout is not claimed complete here.

## Topic record preserved before the skill rewrite

The following is the complete pre-edit topics record, kept outside skills. Its statements describe their recorded checks, not this batch’s current contract.

````markdown
# Design topics

The Design theme's topics, one section each (the repository's AGENTS.md § Report). A topic is the one thing
behind a message or a Report, not the case it showed up in. `fixed` means the case that raised it passes and
something keeps it passing (the guard); `open` names the work still owed.

```text
T01  three linked views: Folder, Element, Session   open
T02  current Design Job contract and documentation   fixed
T03  embedded Job Main, grouping and Task navigation fixed
T04  conversation and approval recorded in Trace     fixed
T05  Design content visible in Workbench             fixed
T06  one structure Studio per Design Block type      fixed
T07  page words in existing Design examples          open
T08  contract types and concrete names in Structure  fixed
T13  b12 Studio: Block Structure and Job previews    fixed
T14  Board Jobs grouped by method family             fixed
T15  structure Studios as b17's folder tree          fixed
```

## T01 · Three linked views of a theme: Folder, Element, Session · open

- **From**: the user, relayed by the session tools-space-bc, 261117: "For the theme design, we should have three
  views. Folder Structure: how things are stored in the file system. Element Structure: how the UI presents the
  Folder Structure on the website. Session Structure: a view that records the important session history; the
  session keeps recording chat progress to the history, and shows how each session episode relates to each Folder
  and Element."
- **Questions**: which folder kinds does a design Board, Job, Task and Run hold? Which view and section shows each
  kind? Where does a design session already leave a trace, and in which folder? What in one shared Session view
  would not fit Design?
- **Answer so far** (the map sent to tools-space-bc; no code changed):
  - Folder: `hai-design/ref/design-ladder.md` § The tree is the whole list, Board and Method Book.
  - Element: the focus page's views, `servers/workbench-design/design_focus_layout.py` (`BLOCK_VIEWS`, `JOB_VIEWS`,
    `TASK_STEPS`), `design_focus_block.py` (`BOARD_LAYOUT`) and `design_book.py` (`BOOK_VIEWS`). The join from a
    section to its folder is in code only; nothing on disk states it.
  - Session: a Run is the episode. A soft Run keeps one round per sitting in `passes/pNN-<MMDD>/`; a hard Run keeps
    one `result/`; the card's `by:` names the agent. A face's `session:` line names the session a copied prompt
    should run in (`design_focus_parts.py` `_session`). A Studio topic keeps `passes/`. At that review, no design folder held a
    chat transcript or digest; T04 now records this blueprint work in its Trace.
- **Does not fit**: a design Job's `inputs/` is a fence (the reasoning may read only what `manifest.yaml` lists),
  and a verify or rank must run in a context that generated nothing in the Job; an episode record written inside
  the Job must stay out of `inputs/` and must never be read by a maker or reviewer Run. A frozen folder
  (`inputs/inputs-vN/`, `observed/eNN_<exp>/`, a method's `mK.md`, a released Job) takes no new file, so its
  episodes are recorded beside it, not in it. One sitting often spans several Runs (generate, verify, revise), so
  an episode lists Runs, not one Run.
- **Owed**: the shared Session view and episode record (`servers/workbench/page`), then Design's hook: a
  folder-kind to section table read from the layout tables above, and a test that every folder kind in the tree
  has a section.

## T02 · Current Design Job contract and documentation · fixed

- **Date:** 2026-11-26.
- **From:** user: “所以你觉得现在的话你应该怎么去，比如说先做一些你能够做的，先更新一下。然后你觉得我们这些对话，就是说能够存到Trace 里吗”
- **Confirmation:** “好，我同意，你去这样做吧。” The approved scope is six documentation/Trace files, not a UI implementation.
- **Questions:** what is a real Job type; where do actions live now; which source content is actually rendered?
- **Answer:** a Board execution Job pins goal × method version × inputs version; a Book method Job owns one method type and its signed `mK.md` versions. Current focus routing redirects old Work links to Report; `design_focus_parts._views` combines actions and results. The updated skill, Job matrix, structure and dialog guide describe this distinction.
- **Evidence:** `servers/workbench-design/design_reader.py` (`is_job`, `is_method_book`, `method_book`), `design_focus_layout.py`, `design_focus_parts.py` (`_views`), and `servers/workbench/page/block_index_page/focus_render.py` (`page_route`). Source files take precedence over older Studio descriptions.
- **Guard:** this skill requires checking the current renderer and separating implementation from proposals before reporting coverage. The evidence checks and fresh-context review for this documentation change are recorded in the linked Trace.
- **Check:** direct rendering of the two example Blocks and six Job/Task bodies, old Work routes, Job matrix and guide parsing passed. Fresh-context skill validation passed after legacy naming and approval-location wording was corrected.
- **Owed:** no work remains for this documentation correction; T03 remains open for the UI implementation.

## T03 · Embedded Job Main, grouping and Task navigation · fixed

- **Date / source:** same user request and confirmation quoted verbatim in T02; cross-theme inventory request from the coordinating session `01a21515-ca66-7871-a100-1f2dc9dc17cd` prompted the preceding read-only review.
- **Questions:** what should Main aggregate; how should Design Jobs and Tasks be grouped; can an embedded Task expose every step?
- **Observed before the frontend change (historical):** `focus_jobs.job_topic` uses release or decade; `task_topic` uses DIKW or decade, without Design roles. `job_pane` embeds `page_ctx(...).body` only. The Board example's Main is Setup; t00/design/t99 show Inputs/Draft/Rank. A Book method Job returns an empty-map fallback because it is excluded from execution `is_job` and has no dedicated Job renderer.
- **Original proposal, now implemented for embedded Jobs:** goal-based Board Job groups, Ideas / Designs / Review Task groups, complete role navigation, and the two distinct Main presentations described in `delivery/page-spec/job-views.md`. Method families are used only if authored. No fabricated Tasks or version-as-Job conversion.
- **Implementation:** `design_jobs.py` now supplies Main, goal/role groups and complete Task step tabs to the shared selector. The existing approval handler is reused. Method Main is embedded; its standalone route remains generic.
- **Check:** automated real-example regressions and browser acceptance pass; details are in `trace/261126/1741_design_jobs_frontend.md`. The original documentation-only update made no renderer changes; that approved frontend Trace records this implementation.
- **Owed:** none for the embedded Jobs contract. Standalone method Job routing remains generic; its supported Main is the Book Jobs section, linked explicitly from the Job definition and Studio Page.

## T04 · Conversation and approval recorded in Trace · fixed

- **Date / source:** the user's request and confirmation are quoted verbatim in T02 and in `examples/Project-Ladder/blueprint/b12_theme_design/trace/261126/1719_design_job_alignment.md`.
- **Questions:** can dialogue be retained; what is exact quotation versus retrospective summary; does it save automatically?
- **Answer:** `hai-trace` records one piece of work in its Block, with prompts, aim, confirmed file plan, changed files, Check and Summary. This trace is created through its script before the approved documentation edits. Earlier context is explicitly retrospective and missing timestamps are not fabricated. Assistant reasoning and decisions are summarized, not presented as user quotations.
- **Check / guard:** the Trace retains the five available user messages and the coordinating review request, labels unavailable message times, records the confirmed six-file scope, and closes with Check and Summary through `hai-trace`. Its `trace.py check` validates the record. Future work follows the same plan → confirm → changes → check loop.
- **Owed:** none for this work record. Automatic capture of every future chat message is not implemented or promised here; the shared hook remains separate work. The broader Session view in T01 remains open.


## T05 · Design content visible and operable in Workbench · fixed

- **Date:** 2026-11-26.
- **From:** user: “好，你继续做呀，现在已经做完了吗？能不能就是进行一个前面的更新。然后我最终想要看到就是说我打开你这个五个半之后呢，我可以看到你这些内容，明白我意思吗。”
- **Confirmation:** “那你现在要不要试一下，去完成一下。那你去执行吧。”
- **Questions:** can Main expose the complete Job; can selected Tasks expose all steps; can Studio show the actual page; can this conversation be read in Trace?
- **Implementation:** design_jobs.py supplies the two embedded Main contracts and role steps to the existing shared selector. The s12/s13 Page routes read live examples; the frontend Trace records this confirmed twelve-file scope.
- **Guard:** test_design_jobs.py checks real example content, all Task roles, original Runs, no rendering writes, approval controls and the shared fallback. Browser acceptance must confirm switches, live previews and the Trace before this topic closes.
- **Check:** the Tools host on port 5623 was reloaded with its existing flags. Chrome verified Board Main, Design → Verify → Main switching, Method Versions, the live s13 Design preview selecting t01, and Files → Trace showing the two user prompts and associated files. No approval was submitted. Automated checks and fresh-context skill validation are recorded in the frontend Trace.
- **Owed:** none within the confirmed scope. Standalone method Job routing remains generic and is outside this embedded-Main change; enter through the Book Jobs section.

## T06 · One structure Studio per Design Block type · fixed

- **Date:** 2026-11-27.
- **From:** user: “你不应该设计S01和S0二吗?”; “OK，你这有structure, example, skill，没有draw吗？”;
  “OK，好，你现在做一个plan，然后看看该怎么去设计它，好吗。”;
  “然后你也把这个要求呢 发给其他的session，让他用一样的格式。”
- **Confirmation:** “OK，我同意，那你现在就开始去整吧，好吗。”
- **Questions:** which types need a structure Studio; what is generic versus an example; where do
  Skills and Draw sit; does a Method Book own Tasks; can the same shared format serve every theme?
- **Cause:** `b12_theme_design/s01-design/s01-design.md:1` previously named the whole Design ladder;
  `s02-workbench-ui/s02-workbench-ui.md:1` named the older workbench drawing. Neither had an authored
  four-view manifest. The old five-Task method proposal could be mistaken for the current Book contract.
- **Change:** s01 now describes Design Board and s02 Design Method Book. Each has Structure / Draw /
  Examples / Skills, a generic branching drawing, the actual example Block and existing skill owners.
  The Book has method-type Jobs and signed versions, with no invented execution Tasks. Both prior
  faces remain verbatim under Historical decisions and references; the older canvases and Guide
  source keep their paths. No shared renderer or skill implementation changed in this scope.
- **Guard:** `examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py --check`
  validates the view order, real source paths, example Block identity, drawing IDs, Book Task boundary,
  preview files and historical canvas presence. Builders never overwrite an existing canvas. Before
  marking future Studio changes fixed, open every authored view in the actual Workbench; a valid
  path alone does not prove that a drawing is visible or that the example stays in its Block.
- **Check:** both manifests resolve through the shared reader; the old faces match their pre-edit
  copies byte-for-byte as retained suffixes. A rebuild with an added human mark in a temporary
  canvas preserves all canvas bytes. Ten existing Design Job regressions pass. Chrome at the
  Tailscale origin opens both types, their skill views, and their live examples; Board Task selection
  retains the Block heading, and Book Jobs show versions without a Task selector. The final preview
  check and delivery are recorded in `trace/261127/1009_design_structure_studios.md`.
- **Owed:** the separate Job Main consolidation remains the earlier 0921 plan, not part of this fix.

## T07 · Page words in existing Design examples · open

- **Date / source:** the user's request for consistent theme UI, tested during T06.
- **Question:** do the embedded real examples meet the current page-word rules?
- **Observed:** Design-Example's Report still prints “waiting for you” and release progress as
  prose; Job Main retains state words in legacy section hints. `servers/workbench-design/design_jobs.py:118`
  passes “waiting for you” to Review and approve and `:120` passes “done” to Delivery.
  The shared Studio row also prints shaping/explore; that shared issue was reported to the Work owner.
- **Owed:** a separately scoped page-word cleanup and repeated browser scan. The new structure
  manifests do not make the embedded legacy content compliant by themselves. This topic stays open.

## T08 · Contract types and concrete names in Structure · fixed

- **Date:** 2026-11-27.
- **From:** user, relayed by Work owner `01a21d6c-cdee-7580-aeda-b1852ffb4a14`:
  “每一个 block，之所以跟其他 block 不一样，那就是它们的 job name、job type、task name，它们应该有自己的名字……先放在 block structure，它里面 job 种类是什么、job name 是什么、task 种类是什么、task name 是什么，这个一定要弄出来……给每一个 session 发 message，让他们重新更新 plan，然后执行。”
- **Questions:** what are this theme's Job and Task types; what are their names; which are groups;
  do method versions imply Tasks; do Structure and Draw show the same relationships?
- **Cause:** the earlier generic labels in `b12_theme_design/delivery/build_structure_studios.py`
  (`diagram`, formerly lines 30–58) illustrated a hierarchy but hid Design's role distinctions.
  The previous `s01-design/delivery/structure.md:9–16` used placeholder names where four explicit
  type/name columns were needed. T06's generic-placeholder requirement is superseded by this correction.
- **Resolution:** Board's structural Job role is Design execution; the actual example Job is
  “Confirm by reply, by Overall performance”, pinned to M02 m1 and inputs-v2. Reason ideas → reason
  ideas; Design → reply-first-short and reminder-one-ask (two Tasks); Review whole → review whole.
  Book's structural Job role is Method type, with registered M01 and M02 identities named
  “M01 · goal only” and “M02 · overall performance”; their signed versions are m2 and m1 respectively.
  Book has no Task Type or Task Name. Job/Task topic groups are described separately.
- **Evidence:** `hai-design/ref/design-ladder.md:26–65,77–97`; `hai-design-method/SKILL.md:24–29`;
  `hai-design-unit/SKILL.md` reason/generate/verify/revise/rank; the actual example Job and Task
  faces named by both structure documents; `design_reader.py:202,218,300` and `design_jobs.py:25–52`.
- **Guard:** the structure builder's check requires all four fields in both documents and drawings,
  rejects the old placeholder names, verifies names and versions against the actual example files,
  and fails if the Method Book gains Task folders without revisiting its diagram. The four top views,
  real Block examples, source paths and Excalidraw route remain checked. No Folder is renamed.
- **Check:** details and live browser acceptance are recorded in
  `b12_theme_design/trace/261127/1054_design_type_names.md`. Both drawings were synchronized, not
  merely relabeled: Board's Design role branches to separate actual Task names; Book's two registered
  types have their own Job names and versions, without the former generic two-version branch.
- **Unresolved:** no explicit serialized `job_type` / `task_type` enum exists in these faces. Labels
  here name contract roles, not a newly invented storage field. A future enum and the older s05
  proposal for method-development Tasks require an owning-contract decision; neither is implied.

## T09 · Structure is a branching tree · fixed

- **Date:** 2026-11-27.
- **User:** “你这里的 structure能不能变成一个 tree啊？你画了一个表，他妈谁看得好啊？你看别人怎么做的，你画了一个 tree不行吗。”
- **Questions:** can readers follow the Job/Task relationship directly; can both Block types use
  the same tree presentation as peer themes while keeping their own contract boundaries?
- **Cause:** both `s01-design` and `s02-workbench-ui` manifests sent Structure to Markdown;
  their `delivery/structure.md` four-column tables required readers to reconstruct the hierarchy.
- **Change:** both Structure views now embed `delivery/structure.html`, with native expandable
  trees, initially expanded. Job types contain named Jobs; Board Tasks branch by type and name.
  Book Jobs lead to signed versions without inventing Tasks. Folder and Studio are separate tree
  entries in the existing shared left tabs. The Markdown sources also use trees. Work's existing
  organization tree was the presentation reference; Draw and the actual folders retain their paths.
- **Guard:** `delivery/build_structure_studios.py --check` rejects HTML tables, requires open
  tree nodes and the exact generated Job hierarchy, and checks the three Structure fragments.
  Its existing source checks retain the real names, versions and Book Task boundary.
- **Check:** Chrome displayed both trees at the Tailscale origin. The Board Design branch
  collapsed and expanded its two named Tasks; Folder and Studio entries displayed their trees.
  A refreshed page showed the default expanded tree. See
  `b12_theme_design/trace/261127/1110_design_structure_tree.md` for the file plan and checks.

## T10 · Structure is a left-to-right mind map · fixed

- **Date / source:** 2026-11-27, Work owner `01a21d6c-cdee-7580-aeda-b1852ffb4a14`
  relayed the user's correction: “不是，我意思是做一个mind map一样的炊，你懂吗。”
- **Questions:** do connected branches show ownership; does each parent appear once; do Jobs
  without Tasks end at Job Name; do Structure and Draw agree?
- **Cause:** T09's `delivery/build_structure_studios.py::tree_html` rendered an indented outline.
  It exposed hierarchy, but did not provide the requested horizontal mind-map presentation.
- **Change:** `organization_map` places parents between their children and draws curved SVG
  connections from left to right. Board retains the verified Job and four named Tasks under three
  Task types. Book ends at its two Job names; versions remain in Folder and Main. Both manifests
  bind Structure and Draw to the same map; the prior editable canvas remains a separate Draw entry.
  Fit to width and Actual size follow the Work theme pattern. Actual folders are unchanged.
- **Guard:** the builder checks node roles and branch totals, rejects tables, compares generated
  relationships with the rendered HTML, and requires both views to bind the same map. Existing
  source/name/version checks remain. A parent appears once within its branch, and a Book map has
  no Task or signed-version node. T09's outline requirement is superseded for Jobs / Tasks.
- **Check:** live Chrome showed Board branches and Book's Job Name endpoints. Actual size yielded
  scale(1), Fit to width scale(0.630208) in the tested embedded viewport; Draw showed the same map.
  Screenshot and validation details are in `trace/261127/1120_design_structure_mindmap.md`.

## T11 · Reuse the existing mindmap skill inside the Block · fixed

- **Date / source:** 2026-11-27, Work coordinator relayed the user request to use the existing
  mindmap rules and default to the owning Work Block. The requirements are recorded in the Trace.
  The user then supplied the raw-Markdown screenshot: “你自己不解释拿你干啥东西吗？”
- **Questions:** can Design use the existing renderer without another SVG layout; can readers
  start folded, expand readable names and distinguish naming rules from actual examples?
- **Cause:** T10 implemented another `organization_map` layout in the Design builder. This
  duplicated the existing `hai-mindmap/scripts/mapview.py` and `mmmap.py` responsibility.
- **Change:** each Studio now owns authored `delivery/organization.mindmap.md`,
  `example.mindmap.md` and `studio.mindmap.md`, using stable IDs and source links. Structure
  expresses fixed names and naming rules; Examples preserves actual named records and the live
  example Block. Both Structure and Draw bind to the same organization source. A small
  `delivery/mindmap.html` entry redirects its own iframe to the already supported focus-map route;
  it contains no map markup, CSS or renderer. This also works while an older service still treats
  direct .mindmap.md manifest paths as Markdown. The checker never
  overwrites authored maps or canvases. Existing HTML is retained only for the Folder entry;
  its earlier Jobs view is historical, not an active binding or a recommended entry point.
- **Guard:** the Design checker verifies the native `focus-map` route, `fit=1`, shared mapview
  CSS/JS, folding controls, read-only rendering, source files, node roles and the Book's no-Task
  boundary. The skill's own grammar checker validates all six maps. Delivery links point to the
  Design blueprint Block, never to standalone content as the default entry.
- **Check:** the user's in-app browser was refreshed on the owning Design Block at the Tailscale
  origin. It showed the native folded graph without root/node markers. Opening the type revealed
  the named Job rule, then Task types; Examples opened all verified names and its Job source file
  in the existing document pop-out. Draw showed the same graph. Method Book expanded to Job Name
  and stopped there. The final reload showed a readable closed map. No shared service was restarted
  by Design. T10's custom SVG is superseded by the existing skill's folded map.
- **Trace:** `trace/261127/1156_native_design_mindmaps.md`.

## T12 · Identify the requested schedule component · open

- **Date / source:** the same 2026-11-27 relay says the screenshot requests the existing schedule.
- **Question:** which existing component and call site does that screenshot identify?
- **Evidence:** searches of current workbench and mindmap sources found scheduling helpers for
  chat polling and autosave, plus the Files/Trace timeline. An old CoWork timeline and display
  gantt/timeline templates exist, but none establishes that it is the requested component.
- **Owed:** identify the screenshot's actual component before binding it. No new schedule,
  timeline or gantt implementation is introduced on the strength of its name.

## T13 · b12 Studio reads as b17's: Block Structure and Job previews · fixed

- **Date / source:** the user, 2026-11-27, two screenshots: s03 to s05 under Structure ("I want to remove this out
  of the structure"), then b17's Studio ("I want you to update the studio strucutre basd on this"; "you know b12 is
  actaully the blueprint block, right?"; "what is the emoji, please have the same name").
- **Question:** which topics does a theme's blueprint Block keep in its Studio, under which bands?
- **Answer:** b12 is a blueprint Block; its own Jobs follow b17 s02 and s14. Its Studio describes the design Blocks:
  `bands: j0N 🗄️ Earlier design · s0N 🧱 Block Structure · s1N 👀 Job previews` (b17's names and emojis);
  s01 Design Board and s02 Design Method Book under Structure; s11 Design Job and s12 Method Book Job UI previews
  live over the design examples; every older topic in `_archive/20261127/` (trace 261127/1212).
- **Guard:** `hai-ui/scripts/ui_preview_check.py` checks both previews have a live view and name no host;
  hai-studio `ref/ui-preview-topic.md` lists them in the Job UI Previews table.

## T14 · Board Jobs grouped by method family · fixed

- **Date / source:** the user, 2026-11-27, on s01's mind map: "we jus t have one type of job here? for the design?";
  "but we can still group the design by the design types, how do you think? or we just have one job type?"; "go ahead adn try it."
- **Question:** does a Design Board need more Job Types, or a different grouping?
- **Answer:** one Job Type (every Board Job holds the same folders). Its Job topics group by the pinned method's
  family from the method registry, not by goal; a Board usually has one or few goals, so goal groups showed one
  group. The goal moves into the label: `j03 · G01 · M02 m1 · inputs-v2` (trace 261127/1235).
- **Guard:** `servers/workbench-design/tests/test_design_jobs.py`
  `test_board_groups_by_method_family_and_names_pins`.

## T15 · Structure Studios as b17's folder tree · fixed

- **Date / source:** the user, 2026-11-27, after reading b17's Folder and Job-Task views: "could you
  update yours to this folder-tree structure as well?"
- **Question:** how do s01 (Design Board) and s02 (Design Method Book) show Folder, Job / Task and Studio
  organization the way every blueprint Block does?
- **Answer:** `b12_theme_design/delivery/structure/build_organization.py` imports b17's shared drawing code
  (`tree_html`, `organization_map`, `STYLE`) and adds design's trees: naming rules under Structure and Draw, the real
  example Blocks under Examples. Job Type and Task Type become Job group (the method family, from the registry) and
  Task group (Ideas, Designs, Review); the Book stops at Job name. Book Jobs with no authored `family:` now take the
  registry family on the live page too (`design_jobs.topic`), so page and tree agree (trace 261127/1305).
- **Guard:** `build_organization.py --check`: both pages carry all six sections and no table, match a fresh build,
  and both topics' `studio-views.json` match the builder; the Book has no Task group. It replaces the mind-map
  checks named in T06, T09 to T11 (`build_structure_studios.py`, now in `b12_theme_design/_archive/20261127/`).


````

## Skill batch completion

The user's approved file list has been executed. Shared rollout was subsequently reported complete by the Work owner and Design verified its own page after that rollout. The historical approval/coordination notes below remain as recorded.

Verified Block entry: http://100.121.165.84:5623/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb12_theme_design&layout=focus&section=studio&group=Structure#s01-design

This Trace records decisions, authorization, changed files and checks; it does not claim automatic capture of all conversations.
