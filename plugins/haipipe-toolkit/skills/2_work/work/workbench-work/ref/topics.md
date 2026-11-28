# Work theme topics

One entry per topic: its name, the words that raised it, the questions it raises, its state.

## Scoped plugin checks for Studio artifacts (2026-11-27) · fixed

User: "我觉得不仅仅是增加一个 Check PY，而是加一个 Check Folder。我们现在不是有 Skills、Service，还有这个这两个大类吗？那所以要不要再加一个 Checks 呢？你明白我的意思吗？"

User: "OK，行，呃，我们尽量比较晚但不要搞得太复杂。而且跑的时候应该也不会很 heavy吧。也不是说每次都要跑。你看看就是说怎么就是让它更……就有一些比较重要的一些路啊，就是我反复强调一直犯错那些路，你可以加一加。"

Questions: Can checks live beside skills and servers, stay small, reuse owning rules,
and reject bad artifacts without scanning unrelated work after every edit?

Implementation: `hai-studio/scripts/checks/run.py --target 〈topic-or-Block〉`; shared path/result
helpers and separate Studio binding, generation and placeholder modules. The Skills
views writer checks completed output. Check-view criteria remain in type elements.md;
its freshness check does not execute the criteria or change Not verified marks.
No CI, watcher or service restart. Other writers and semantic/UI acceptance are not
covered by this pilot. Validation and remaining findings are in b17's
`trace/261127/1833_plugin_checks_pilot.md`.

Guard: the checks tests (`hai-studio/tests/`) passed 29 tests; existing Skills/Check view suites passed 12.
Eight Skills topics plus S76 passed scoped checks in 0.148 seconds. A fresh-context
review reproduced and confirmed the fix for external symlink sources. The broader
Block check correctly reports stale S01/S72 outputs, outside this implementation.

## T01 · Three linked views: Folder, Element, Session (2026-11-17) · open

From tools-space-bc, relaying JL: "For the theme design, we should have three views. Folder Structure: how things are
stored in the file system. Element Structure: how the UI presents the Folder Structure on the website. Session
Structure: a view that records the important session history; the session keeps recording chat progress to the
history, and shows how each session episode relates to each Folder and Element."

Questions:
1. Which folder kinds does a work Block hold at Block, Job, Task and Run level?
2. Which view and section shows each kind today?
3. Where do work sessions already leave a trace, and in which folder?
4. What in the proposed shape (one shared Session view, episode = one goal, join key = folder path from the Block)
   does not fit the work theme?

Answered to tools-space-bc on 2026-11-17 (map below). No code change yet: the shared part is built once in
`servers/workbench/page` by its owner; the work theme fills its hook after.

```text
level  folder kind                         element today (view · section)
Block  board.md, records/, delivery/,      Overview (Goal, Requirements, MindMap, Work map);
       related/, sNN-<topic>/, runs/,      Delivery; Around the Work: Studio, Interactions,
       src/                                 Timeline, Files; records/ = cards (💬 📝 ✓)
Job    jNN_<job>/ + jNN_<job>.md, runs/,   Plan + Results: a Job row (marks, cards, 🙋 N)
       sNN-<topic>/
Task   tNN_<task>/ + face, scripts/,       Plan + Results: a Task row; Findings tabs
       runs/, draft/ (draft Task)          (Values tables.json, Maps runs/*/result/maps/)
Run    runs/rNN_<slug>/ run.yaml, result/, Plan + Results: a Run row; its pop-out (result,
       passes/pNN-<MMDD>/, ticket .html    card, ticket, passes); collect Run = 🙋 card
```

Session traces today: `passes/pNN-<MMDD>/pass.md` in a Run (`run.yaml` `passes:` and `source: chat`) or a Studio
topic; `Session:` chips on face cards (`## Plan + Results` items); `records/<stem>-comments.md` cards; git commits
(Timeline). None names the session that wrote it, and a Block or Job face keeps no episode list.

Contract merged by tools-space-bc: `servers/workbench/ref/three-views.md` (card addresses, several folders per
episode, collect Run passes read as episodes, page words). Still owed: a guard (test) once the shared Session view lands and the work hook fills it.

## T02 · A Run receipt said ok on 1% of the data (2026-11-18) · fixed

Report from Proj-PD2D: "PD2D b03 r06 (CaseSet v2) died after 1 of 100 partitions and left no result, but the queued
b10 r08 r09 and b11 r06 r07 ran next, each wrote status ok, so their Deliverables would tick ✅ with test AUROC 0.7735
trained on 913 cases instead of about 90,000." Cause there: b10 t01 scripts/4_aidata_reachpd2d.py:56 globbed whatever
partitions existed (fixed in PD2D 0c931d7), and the chain kept going after a failed ticket.

Questions:
1. Can a work Deliverable tick ✅ when a Run its maker read never finished? It could: `item_state` checked only the
   maker's own receipt.
2. How does a Run say what it read? Only in words (`goal: ... (r06_prediabvisit_v261116)`); now also `reads:`.

Fix: `servers/workbench-work/work_progress_deliverables.py` `unfinished_upstream` follows `reads:` and rNN_ names in a
goal across the Project, through ok Runs to the one that never finished; such an item shows 🔶. On the real PD2D tree it
flags exactly b10 r08 r09 and b11 r06 r07. Rule: hai-run 0.37.0 (Result, evidence, and closure). Guard:
`servers/workbench-work/tests/test_deliverable_upstream.py` (3 tests).

## T03 · Elements as designs in b17 (2026-11-18) · fixed

JL: "should we change the Block UI to Block UI + element, so we have a Element Section at the first, right, and we can
understand what we will need. Because, otherwise, in the Element UI, we still need to group them into the block, Job,
and tasks."

Fix: each UI view of b17 opens with 🧩 Elements, from `delivery/page-spec/<level>-elements.md` (12 Block parts, 6 Job, 6 Task, 5 Run).
Walked on 5694: every Block tab outlines its part on the live b90 page. Guard: `workbench/page/element_marks/tests/test_ui_elements.py`.

## T04 · Fixed Block folder and one Tools tree (2026-11-24) · fixed

JL: "I want to update the Workbench-UI that make the folder to be the first and fixed one, do  you get it?"
On the Tools · UI screenshot: "could we make them together?"

Questions: Can Files always start at the real Work Block without displacing scoped sources?
Can Skills and UI stay open side by side without two tabs?

`servers/workbench/side_pane/files_tree/work_files.py` renders the Block first and restores expanded child folders
across views in the browser tab. Tools groups the view's Skills and UI as independent branches.
The contextual Blocks branch remains scoped. Guard: `workbench/page/job_task_views/tests/test_work_frame.py`.

## T05 · Floating Files and compact navigation (2026-11-24) · fixed

JL: "How do you think we can make the Files like a floating ball in the right bottom corner? Let's the status ball, do you get it?"
JL: "I want this the be the left and right half cicle, and save the spaces, do you get it?"

Questions: Can Files open without leaving the current view? Can Pages and Sections open without a row above the title?

`focus_shell.py` adds a floating Files button that opens the existing browser in place and replaces the
narrow-layout controls with left/right half-circle tabs. The full Files page and wide-screen rails stay available.
Verified on b17 in Chrome: both tabs open, Files loads the same folder tree, file previews open, and Escape
returns without navigation. Guard: `servers/workbench/page/job_task_views/tests/test_work_frame.py`.

## T06 · Skills inside general structure Studios (2026-11-27) · fixed

User: "I think skill might still be into one item in the top view list. No need to have a new studio for it."

User: "And for the work block structure. It should just be general. What are the job topic job name task topic and task name. 他们可以先general一下。 不需要给具体的名字,你知道吗?你直接就是 example 1，example 2，或 job 1，job 2，这样就行了。"

User: "然后你继续工作自己的这个 BO7的话你能覆盖就覆盖吧。我们现在就是说不要搞 scale 了，就是说 scale的话我们是放到 S0、0、2、0、3里面的 view 里面，你懂我意思吗。"

Questions: Where do Skills live? How do general structures and real examples stay distinct? Can themes reuse the shared renderer?

Rule: b17 s01 Work, s02 CoWork, s03 Discovery and s04 Theme own their structure design. Each offers Structure / Draw / Examples / Skills, following the user's format relayed by Design theme session. Structure and Draw cover both Job topic → Job → Task topic → Task and Studio organization. Use generic names in the model; do not invent Tasks for steps, versions or people records. Real examples open their Block; Skills read actual source files. Do not allocate separate skill Studios.

Implementation: each topic's `studio-views.json` uses `servers/workbench/studio/tabs/studio_views.py` and shared `studio_tabs.py`. File items use `name`, SPACE-relative `path`, optional `fragment`; examples use `name`, SPACE-relative `block` directory with board.md. Existing default Page/Effect/Draw topics are unchanged. Replaced faces are saved verbatim in each topic's result/structure-replaced-261127.md; drawings and annotations are untouched.

Verification: browser on Tailscale :5623 showed all four topic titles, Structure, interactive Draw, real Work example and actual hai-work skill reader. Theme Studio's left tab showed its Structure/UI/Guide organization independently of s01's selection. Guard: `studio/tabs/tests/test_structure_views.py` covers view composition, shared side tabs, independent topic IDs, default fallback, validated Block examples and path/symlink bounds. Existing Effect/reset tests also pass. Historical s05 and other old UI topics are retained outside this replacement scope.

## T07 · Authored Draw file types (2026-11-27) · fixed

Report from Design theme session: "Design 已接上共享 manifest，s01/s02 的 Structure、Examples、Skills 浏览器通过。验证发现 authored Draw 的 path 指向 .excalidraw 会原样显示 JSON，指向 PNG 则 iframe 里按原尺寸裁切。原因是 studio_views.read_views 对所有 file 调 frame._file_url、parts 第三位固定 False。请共享 owner 考虑对 .excalidraw 使用 _draw_url、PNG 使用原有图片预览能力；我不改共享模块，正在自己已批准的 structure.md 中用响应式图片作为 Draw 的回退。另共享 Studio 行仍显示 shaping/explore 状态字，属于共享 A01 后续清理。"

Questions: Can authored Draw reuse the canvas viewer and scale image previews in both one-item and multi-item views? Can the stage words be removed under shared A01?

Cause: studio_views.read_views used the generic file URL for every extension; studio_tabs.frame_of always made an iframe. The item tuple's third field means historical/earlier, not image metadata, and must retain that meaning.

Implemented: .excalidraw paths now use frame._draw_url; frame_of renders image URLs through responsive img and the existing open_dot. Single items and side tabs share that renderer. Regression guard: test_excalidraw_uses_canvas_viewer and test_images_render_responsively_alone_and_in_side_tabs. All 13 Studio tests pass. Existing HTML Draw sources keep their iframe behavior.

Real-page verification: Design session confirmed after the 5623 reload that s01/s02 show actual Excalidraw canvases in their iframes at 53% automatic zoom; screenshots checked. Both manifests use direct .excalidraw bindings and the Markdown workaround was removed. Structure / Draw / Examples / Skills passed. Verification receipt: `examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1009_design_structure_studios.md`. Drawing behavior is guarded by the tests above. Stage words are tracked separately in T08.

## T08 · Studio row stage words (2026-11-27) · open

Report from Design theme session: "另共享 Studio 行仍显示 shaping/explore 状态字，属于共享 A01 后续清理。"

Question: How should Studio rows follow hai-ui A01 without visible shaping/explore state words?

Cause: `servers/workbench/studio/tabs/studio_tabs.py` appends facts.stage as a row-stage span to each fold title. No change made in the Draw repair. Still owed: remove or replace the state words according to the shared A01 contract, add a regression guard, then check the real Studio page.


## Four structure Studios: folder content and organization (2026-11-27) · fixed

User: "第一个内容是 folder，第二个内容是我们 job，task organization，再个就是我们的 studio organization。"

User: "你接下来就直接去执行吧,然后我到时候我就起来我看看那什么样子。"

Questions: What belongs in each folder? How are Jobs and Tasks grouped? At which level does a Studio topic live?
The four content models are s01 Work, s02 Blueprint, s03 CoWork, s04 Discovery. Structure has Folder,
Job-Task, Studio; Draw covers those same models. S11–S13 retain UI design.
CoWork omits the Task level under its current contract. Skills remain a top view in the same topic.

Implementation and guard: b17 `delivery/structure/build_organization.py`, the four topic manifests, and
`delivery/structure/check_organization.py`. Original faces and canvases are retained. Validation is recorded in
`trace/261127/1021_structure_folder_organization.md`. The guard, actual browser checks and fresh-context review passed; the reviewer’s two missing-folder findings were corrected and added to the guard.


## Folder preserves existing storage (2026-11-27) · fixed

User: "No!!!! The folder will still be what we have now. No topic folder"

Question: does Folder describe the current disk layout or propose new storage?
Answer: it reads existing names and parentage. Job topic / Task topic are grouping labels in Organization,
never new directories. Existing sNN folders are retained in place. The previous schematic Folder template
is superseded; no work directories are renamed, scaffolded or migrated.
Guard: `delivery/structure/check_organization.py` verifies every rendered path exists. Evidence:
`trace/261127/1041_folder_existing_only.md`.


## Organization follows the Block type (2026-11-27) · fixed

User: "For this, the topic type should be attached to the block type. Like for the blueprint work block, we should have block structure and the block UI, do you get it?"

User: "The job topic and job name should be relevant to the block type as well! If it is general, then use the place holder of example 1 example 2"

User: "Go ahead and make the plan and then update them"

Questions: which Studio topic types belong to this Block type, and what Job topics and names fit it?
Answer: Blueprint has Block Structure and Block UI Studio types. Job organizations use meaningful, type-relevant
examples; general Work slots use Example 1 / Example 2. CoWork and Discovery use coordination and inquiry
examples. These are illustrative organizations, not additional canonical Job types. Small role labels distinguish
Job topics, Jobs, Task topics and Tasks. The old Owning level diagram is superseded. Folder inventory stays intact.
Guard and evidence: b17 `delivery/structure/check_organization.py` and `trace/261127/1048_organization_by_block_type.md`.

## Explicit Job and Task kinds and names (2026-11-27) · fixed

User: “我觉得你这个犯了一个很大的错误，就是怎么所有的 block type 都是变成 job1，job2，job3了，它们应该有具体的自己的名字呀。啊，你这搞的他妈什么东西啊。”

User: “那这里面最重要的每一个 blog，之所以跟其他 blog 不一样，那就是它们的 job，name，job type，name，job name，还有什么 task name，它们应该有自己的这个名字。那这样才能区分它们是怎么 organized 的。你先给我放在这个地方，就是这个 block structure，它里面那个 job 种类是什么，对吧？然后 job 的 name 是什么，task 的种类是什么，task name 是什么。那这个一定要把它给弄出来。你这个就是都是模糊化了这样都行吗。 然后就给每一个session都去发个message，让他们就是重新再去更新一下他们的plan，然后去执行。”

Question: Can a reader tell what work each Block contains and how its kinds and named Jobs/Tasks relate?
Rule: Show Job Type / Job Name / Task Type / Task Name explicitly in Block Structure, and the same relationships in Draw. A generic topology or backend field list alone is insufficient. Name responsibilities with domain meaning; distinguish the structural proposal from existing machine type fields, and bind actual names to source records. Do not infer a canonical Job type for every use case. A generic placeholder does not count as a completed structural design.

Implementation: build_organization.py binds four distinct responsibility models to existing Job/Task files. Source names open their records; actual declared fields are inspectable on source links. Existing Folder sections are preserved. check_organization.py guards all four columns, meaningful names, parentage, distinct trees and the real Discovery type fields.

Verification: Chrome on Tailscale :5623 showed all four embedded four-column tables and the Work Draw with matching typed relationships. The source/parentage/placeholder/Folder checks passed. Remaining separate contract debt: CoWork UI/example contains a Data-use plan Task while hai-cowork forbids a Task level; that mismatch is shown and not silently resolved. code/ui in old examples are not a newly registered task skill taxonomy.

## Horizontal type/name mind map (2026-11-27) · fixed

User: “你这个地方能不能不要画成表啊？你能不能画成一个 tray啊，第一列是，对吧，第一列是 type，job type，第二列是 job name，第三列是 task type，第四列是 task name。这这么简单东西你却做不出来，卧槽。”

User: “不是，我意思是做一个mind map一样的炊，你懂吗。”

Question: how do the four levels show branching membership without repeating parents as table rows?
Rule: Job Type → Job Name → Task Type → Task Name is a left-to-right mind map with connecting branches. Each parent appears once within its own parent; a Job without Tasks ends at its Job node. Preserve meaningful names and source links. This supersedes the table presentation above.

Implementation: the shared local organization generator lays out nodes and SVG branches for all four Block models, in both Structure and Draw. Fit-to-width shows the overview; actual-size allows scrolling to read nodes. Folder remains byte-identical.

Verification: check_organization.py checks four headings, node/edge counts, absence of tables, controls, source relationships and preserved Folder hashes. Chrome showed the embedded Work map in Structure and Draw. Actual-size was exercised; 390 × 844 viewport showed the fitted four-level map, then the viewport override was reset. Contract gaps recorded above remain separate from this presentation fix.

Cross-theme reuse: `build_organization.organization_map(tree=..., sources=...)` accepts a Block root containing four levels of `(label, children)` nodes. `organization_document(title, tree=..., sources=...)` wraps it for an embedded Studio file using exported `STYLE` and `MAP_SCRIPT`. Sources use full label-path tuples as keys and `(absolute face Path, field description)` as values, so names in distinct branches do not collide. Existing `organization_map(kind)` calls remain compatible. This is an authoring helper, not a new server or Job/Task route. The guard covers external trees, source disambiguation, escaped labels, absent Task levels and rejected extra levels.


## Concrete examples before dense organization (2026-11-27) · fixed

User: “你能不能把structure给我先给出来一些example出来？你现在做啥东西啊，我看都看不懂，看不清楚，不simple，太complicated了。你就不能就直接把那东西弄好吗？我操。”

Question: can a reader understand one concrete Job and its Tasks without first decoding a whole Block taxonomy?
Rule: begin with a named, source-bound example. Show one Job at a time; switching its name changes the entire connected diagram. Retain Job Type → Job Name → Task Type → Task Name. Use the existing hai-mindmap renderer with readable text, initial folding and horizontal scrolling; do not shrink all branches to fit. Keep detailed source/contract notes on hover.
Implementation: example_maps in the b17 authoring helper and its four generated files; the reusable all-tree API remains available. Example selection, source links, one initially visible panel and shared rendering are guarded by check_organization.py.

Verification: the four-model guard passes, including one initially visible example, all source-bound options and minimum scale. Chrome showed the actual Work Structure example with Read CSV / Print report and successfully switched to First docs / README. Jobs has no repeated heading; Studio is a short topic list. Final node typography uses 15px text with normal word wrapping and a 90% scale floor. Folder hashes remain unchanged.


## Fixed names, variable slots and concrete examples (2026-11-27) · fixed

User: “那你想想怎么就是把这个东西表达得更清楚一些。 就是说要么就是说你有两个，一个是指example，另外一个version，就是有的时候我们这个block就是说它的job name就是说是 至于当下的具体的任务 的，有的时候它的job name或job group name它是固定的。我想说你怎么就是区分它们？”

User: “要不然你再重新再更新一下。”

Question: which names are required by a contract, which are chosen for the current work, and which are merely examples?
Rule: Structure/Draw show naming rules; Examples shows actual named records. Plain names denote fixed names; 〈…〉 denotes a name chosen for this work. Classify each level independently; an optional group is not a Job type or a folder. Fixed names require an owning contract or explicit type-specific design decision. CoWork j00_people is fixed by hai-cowork; other Job names follow the request. Work Block (Blueprint) Structure/Block UI are the user's explicit Studio types, not prescribed Job names. Preserve the real example inventories.
Verification: check_organization.py passes the rule/example manifest split, fixed CoWork people Job, no CoWork Task in the rule, Discovery inquiry/Task grouping, Blueprint Studio names, absence of sample names in rules, source relationships and unchanged example Folder hashes. Four generated scripts pass node --check. The running Work page shows 〈Job group〉 / 〈Job name〉 / 〈Task group〉 / 〈Task name〉 in Structure; Examples shows the existing CSV folder inventory and source-linked First command line Tasks. Canonical trace: 1150_structure_rules_and_examples.md.


## Trace registration must reach the Files pane (2026-11-27) · fixed

User: “为什么我发现你的这个 Trace 没有更新啊？”
Question: why did written structure work not appear in the Trace UI?
Cause: organization_by_block_type.md lacked the numeric filename prefix consumed by trace_view.traces() and omitted aim/do/changed metadata. Appending prose did not register it. The follow-up also started with reads before its Trace was written.
Fix: retain the history; register 1150_structure_rules_and_examples.md using hai-trace's script and record the late registration honestly. Future requests use that script before implementation. Verify both trace.py check and actual Files-pane discovery, rather than only file existence.
Verification: canonical trace check passes; the real Files pane shows its title and file marks, and clicking its title displays the user's current request and aim. Guard: trace.py new creates the discoverable filename and schema; trace.py check verifies closure fields.


## Studio Band groups topic folds (2026-11-27) · fixed

User: “我们可不可以在这个这里也加上 B A N D 的呢？就是按照不同的组来分它们。你懂我意思吗？”
User: “你懂我的意思吗？我的意思是说你这个办的当作一个group，你把这些 fold给组织起来。”
User: “啊，你还等啥呢？”

Question: can Studio show the group containing each existing fold, while each fold still opens independently?
Implementation: shared studio_tabs.render wraps existing topic folds in named section/h2 Bands. Uses topic Tags and _studio_groups.txt, preserves sNN sorting inside each group and selects one group for multi-tag topics in the complete list; explicit filters keep all matching topics. No theme names or alternate schemas are introduced. Empty groups are omitted. Rule and guard: hai-ui A11 and test_focus_studio.py. Trace: 261127/1202_studio_bands.md.
Verification: 14 focus Studio tests and 15 Studio tab tests passed. After reloading the existing service, Chrome showed b17's Structure/All pages/Block UI/Other Bands. Opening s01 then s02 left both independently open. The screenshot's b12 page showed Workflow/Structure/Levels/Run and Skill/Guide headings containing their existing folds; empty configured groups were absent. Scoped diff check passed.


## Reuse the existing structure mind map (2026-11-27) · fixed

User clarification: “我不知道你啥意思。慢慢慢普，我不知道啥schedule。”
Relayed requirement from coordination chat 01a21d6c-cdee-7580-aeda-b1852ffb4a14: “复用已有 scripts/mapview.py 的 CSS/JS/render 与 mmmap.py 的 draw/fragment（由现有 workbench mindmap_module 接入）”.
Questions: which renderer owns structure diagrams; where do readers open examples; was schedule requested?
Rule: use frame.mindmap_module().draw for a verified data tree or fragment for an authored .mindmap.md. Preserve IDs, actual Folder content and human edits. Structure gives naming rules; Examples gives real names. Deliver the owning Block entry. Job links use group=jNN and Task links add task=tNN on that Block; never pass the whole Job directory as group. Schedule was a misunderstanding, not requested work.
Implementation: b17 delivery/structure/build_organization.py adapts the existing models to MT.MindMap; no custom SVG layout, scaling or connector script. Shared fold controls and source chips remain. The previous 576px/90% scale design is superseded. Initial folding and horizontal scrolling preserve readable text.
Verification: check_organization.py covers all four models, model ancestry, shared CSS/JS, rule/example separation, source routes, reproduction and unchanged Folder hashes. The actual Tailscale Block page showed initial folding, opened all levels, switched First command line to First docs/README, and opened Read CSV inside b01_example_work with j01/t01 selected. No shared server restart was performed by this chat. Registered Trace: 261127/1157_shared_structure_mindmap.md.

## Native mindmap Studio binding (2026-11-27) · open

Report from Design chat 01a1bc86-defc-7600-9d10-469cb2f36576: “请在你负责的共享入口支持 manifest 中 .mindmap.md 原生嵌入（Structure/Draw/Examples），复用现有 mapview/mmmap 并默认折叠。”
Question: can theme manifests bind the existing viewer without a private renderer?
Implementation: studio_views.read_views routes a contained .mindmap.md path to the existing focus-map route with fit=1. Manifest format stays {name, path}. Existing containment and symlink checks apply. Authored nodes currently require stable IDs: the existing read-only fragment does not assign missing IDs; this constraint was sent to Design.
Guard: test_structure_views.py passes eleven tests, including all three views, readonly folded rendering and outside-SPACE symlink rejection. Still owed: verify a consuming theme's actual native manifest binding in its Block; current Design manifest still points at its fragment-based HTML adapter. Code tests do not count as that live acceptance.


## Studio types are independent of shared Bands (2026-11-27) · fixed

User: “s75 s77 s79 我觉得这三个studio type没必要存在了吧。你觉得呢？”

User: “然后还有一个点就是说，我们其他的几个block，The Studio页面也要有这个Studio Type。 他们需要有吗？还是没有呢？我这里我也不是很清楚啊。”

Questions:
- Can the three independent type topics be removed without losing their Bands or actual content?
- Which Work Blocks (Blueprint) define types, and which reuse shared definitions?
- Do actual Work Blocks need type-definition topics?

Rule: shared Bands are independent of type definitions. Work Blocks (Blueprint) reference common types and define only
theme-specific types. Actual Work Blocks show instances without a required Studio Type group. Task procedures
and specific Block Guides remain usable content. Original type records are preserved in
`examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2250_studio_type_scope.md`.

Verification: shared registry and removal regression suites passed (12 tests); fresh-context agent scaffolded a theme-specific type and an ordinary Work topic, verified titles and actual rendered groups. The Tailscale Block page was opened after the coordinated reload: six retained types under Studio Type; s75/s77/s79 absent; S71 Studio requirement and S99 Guide opened successfully. The actual-content migrations in other themes remain their owning sessions' work.


## Studio bands for five Work-theme Block types (2026-11-27) · open

User: “现在我们就 focus 在沃克主题。在沃克主题下面不是这个 block 不是多了一个 Knowledge 吗？你怎么没有把它加进来呢？然后这里面，就是我们就 focus 在沃克主题，沃克主题里面 block 有五个，对吧？然后这五个里边他们的 Studio，那个页面的那个 banner 定好了吗？还是没有定好。”

Questions: Which Bands are fixed for each type? Which Studio names depend on the work? Where does Knowledge Sources belong?

Work, CoWork and Discovery have content Bands; Blueprint references its shared registry. Knowledge has Concepts,
Methods, Applications, with a shared Knowledge Sources Studio whose records individual topics reference.
S01–S04 native mind maps and Structure/Draw bindings are this batch; S05 and source-record implementation belong
to the Knowledge design chat. Definition changes do not migrate real work Blocks or create example work records.

Verification: four native map checks and the contract/binding guard passed, including negative probes for a wrong Band and an unbracketed example. The actual Block page rendered all four maps and expanded Work, CoWork and Discovery branches; S01 Draw uses the same source. Baseline comparison preserves existing views and drawings.

Still owed: S05/Knowledge Sources acceptance by its owner; mobile map usability (390px viewport clips the initially visible right branches); numeric Trace filename registration (the approved filename is currently excluded by the Files-pane selector). Keep this topic open. Record and exact file plan: `examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1705_studio_bands_by_block_type.md`.


## Structure Studio uses Folder Tree (2026-11-27) · open

User: “你给我解释一下为什么我们的S01里面那个 Studio Structure它还是 Mind Map啊？它不是我不是说一直要用那个 Folder Tree吗？你给我解释清楚，到底是什么原因。”

Cause: Structure → Studio was rebound to focus-map, replacing the existing Folder Tree. The new check asserted
that mistaken binding instead of the user's requested representation.
Rule: Structure → Studio renders Block → Band → 〈Studio topic〉 through the existing collapsible Folder Tree.
Authored data format does not determine the renderer. Band grouping adds no actual directory layer.
Guard: check_studio_bands.py requires the tree fragment and semantic tree markup, rejects mindmap binding;
check_organization.py checks the full manifests, original Draw entry and reproducible output.
Verification: S01 desktop and 390px phone viewport display the Folder Tree; expanding Work Design reveals its two topic slots. Four-instance guard passes and rejects the wrong mindmap binding. Real Folder sections match the baseline. Overall S71 acceptance stays open: the explicit tree requirement is now in elements.md; Band emoji/number requirements are not fully represented. Broader organization checking still reports a pre-existing historical Folder-hash mismatch.


## Type-owned Check view (2026-11-27) · fixed

User: “Work Skills Studio 你读一读这个吧，你读一读这个。然后我觉得，无论是S，无论是就是说S7，还是说是S，还是比如Skill Type，我们都先再加一个Top View，Bottom，再加一个新东西叫做Check。就是说在这里我们需要Check什么啊。”

Question: can types and instances expose the same required checks, instead of checking an implementation against itself?
Rule: type elements.md owns criteria; check_type binds the instance to that source. Check is a final top view;
Skills generation treats it as a managed view, not a skill. A definition is not a result; instance checks remain
unverified until actual execution evidence exists. This pilot displays requirements and methods only.
Scope: S71→S01 and S76→S51. No shared server changes or check execution endpoint.

Guard: hai-studio tests/test_check_views.py; generator --check validates generated UI freshness only.
Verification: ten unit tests, all four generated Check views, both type generators and the S51 Skills generator pass. Fresh-context fixtures confirmed inheritance, bad binding rejection and regeneration. Browser acceptance opened all four Check views, switched skills, expanded Verify and opened its source; 390px phone rendering was inspected. This fixes the presentation pilot only. Automated results are not implemented; SKILL.md reference discoverability remains owed. Full check_organization.py still fails on its pre-existing historical Folder hash, recorded rather than suppressed. Trace: 261127/1814_studio_check_pilot.md.


## Examples beside requirements and element-scoped Check (2026-11-27) · fixed

User: “你像这些 Studio Type，S7，S7二，就是我们要加 Check，能不能也加一些，比如说那个 Example。你比如说我每次都是上边是上，对吧，Top，然后 left，right，right 现在是我们的 right 的一些路。那能不能把一些 right 的一些，比如说 Example 也列一下。然后再就是 Check。我觉得这个 Check 的话，你也可以用这种模式，Top，Left，Right，然后说一定要 Check 什么什么什么。嗯。但这东西，比如说我的 Mars 里面写都有啊，你这都是睁不开你的狗眼啊。”

Questions: can each right-side requirement show its corresponding example, and can Check identify its exact
Top/Left location without independently copying or losing criteria?
Cause: type_requirements.py rendered descriptions only; S72's separate parser used a different Markdown syntax,
so the shared Check reader could not read its inline must fields or identify its Top views.
Change: S71/S72 bind examples by instance topic/view/item; shared requirement_examples.py resolves the existing
content, uses shared open-dot/file/draw routes, and normalizes child Job/Task examples to Block selections.
S72 now uses the shared element reader. Check's element layout retains parent-view and selected-element criteria.
S71 explicitly requires Folder Tree for Structure/Studio; S01's inherited Check was refreshed under its earlier
approved file scope. Unexecuted checks remain definitions, never claimed passes.
Guard: tests/test_requirement_examples.py and tests/test_check_views.py cover missing sources/fragments/selectors,
canonical Block navigation, a full-Block example accidentally bound to a Folder snapshot, criteria coverage and
source changes. Both type generation checks pass; existing Skills-view tests pass.
Verification: actual b17 Block opens S71 Structure/Studio Folder Tree, S72 Job Overview and Task Runs examples;
Overview Requirements switches, the open dot opens the same Block example, and Check/Task Runs includes parent
criteria plus its own method/source. The right-content page at 390px has 390px scroll width and readable wrapping.
Fresh-context skill validation discovered both references and exercised independent temporary fixtures; its
incorrect full-Block binding finding was corrected and guarded before completion.
Boundary: fixed means example/Check presentation and binding, not certification of every example's content.
Existing S01 Band emoji/number completeness and the historical organization Folder-hash failure remain open.

## Examples stay beside their requirements (2026-11-27) · fixed

User: “这个盐泡我记得不是说不要了吗?直接不是把它去掉吗?” (screenshot: S71 Examples top view).
Cause: the example/Check implementation incorrectly preserved the separate Examples top view despite the user's
decision to show examples beside the corresponding right-content requirements.
Change: removed S71's Examples definition, its bindings and generated pages; regenerated the manifest and Check.
The corresponding inline examples remain. Ref/type-examples.md and Constitution A06 now explicitly exclude a
separate top view for these examples. S01 inherited Check was refreshed from the changed type source.
Guard: test_s71_examples_stay_inline_without_a_top_view checks regenerated top views, Check items and inline content.
Verification: eight binding tests, generation freshness, fresh-context skill validation and actual refreshed
Block page pass: Structure / Job types / Task types / Draw / Skills / Check; right content still has Example.
