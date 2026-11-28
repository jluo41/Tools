---
title: Insight structure catalogs and Studio organization
date: '2026-11-27'
aim: Separate type from grouping and complete the three Block Structure contracts.
closed: true
plan:
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_structure_types.md
  what: 记录本轮原话、审批、共享要求差异、实际检查和剩余接口缺口。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/types.md
  what: 建立四类清单，注明 for/holds、真实来源和 owner；无分组明确 absent，不虚构类型。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/job-group-type--question-version.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/job-type--analysis.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-group-type--preparation.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-group-type--question-level.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-type--preparation-execution.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-type--question-answer.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json
  what: 由生成源加入 Job types/Task types；保留已批准的折叠 mindmap、内嵌案例和 Skills。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md
  what: 写清四类责任、实际 Work Studio 的 Band/编号设计、已确定规则和提案。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
  what: 经共享 refresh 同步分组与类型标签，按来源身份保留人工文字、节点与引用。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/types.md
  what: 建立四类清单，注明 for/holds、真实来源和 owner；无分组明确 absent，不虚构类型。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/delivery/types/job-type--question-set-version.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/delivery/types/task-group-type--question-level.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/delivery/types/task-type--question-definition.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json
  what: 由生成源加入 Job types/Task types；保留已批准的折叠 mindmap、内嵌案例和 Skills。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.md
  what: 写清四类责任、实际 Work Studio 的 Band/编号设计、已确定规则和提案。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
  what: 经共享 refresh 同步分组与类型标签，按来源身份保留人工文字、节点与引用。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/types.md
  what: 建立四类清单，注明 for/holds、真实来源和 owner；无分组明确 absent，不虚构类型。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/delivery/types/job-type--prep-code-version.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/delivery/types/task-type--prep-step.html
  what: 使用共享 block_types_pages 的页面生成函数，从 types.md 生成说明。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json
  what: 由生成源加入 Job types/Task types；保留已批准的折叠 mindmap、内嵌案例和 Skills。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.md
  what: 写清四类责任、实际 Work Studio 的 Band/编号设计、已确定规则和提案。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
  what: 经共享 refresh 同步分组与类型标签，按来源身份保留人工文字、节点与引用。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
  what: 从生成源重建 Folder/Job-Task/Studio 内容；保留正常字号与既有折叠交互。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
  what: 从生成源重建 Folder/Job-Task/Studio 内容；保留正常字号与既有折叠交互。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
  what: 从生成源重建 Folder/Job-Task/Studio 内容；保留正常字号与既有折叠交互。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/page-spec/example-types.json
  what: 从真实来源派生语义类型；DIKWX 分组不再混作 Task type。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: 读取类型清单并复用共享页面生成；补全普通 Work Studio Band/编号模型和正确目录规则。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure_contracts.py
  what: 薄内容适配：读取 types.md、核对来源与允许缺省层；不实现布局或替代共享 renderer。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
  what: 拒绝缺失清单；验证 for/holds、owner/来源、允许缺省、全量 release 成员、实际 Studio 与生成一致性。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md
  what: 同步当前结构入口与类型清单读取规则。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/CONSTITUTION.md
  what: 保留用户批准的简化呈现，补充类型清单与实际 Work Studio 的职责边界。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
  what: 完整定义四类语义、真实字段映射、普通 Work Band 编号与共享接口边界。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
  what: 登记本轮缺失类型清单、分组混作类型、Studio 规则不全，以及检查器的剩余缺口。
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_structure_types.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/types.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/job-group-type--question-version.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/job-type--analysis.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-group-type--preparation.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-group-type--question-level.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-type--preparation-execution.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/delivery/types/task-type--question-answer.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/types.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/delivery/types/job-type--question-set-version.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/delivery/types/task-group-type--question-level.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/delivery/types/task-type--question-definition.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/types.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/delivery/types/job-type--prep-code-version.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/delivery/types/task-type--prep-step.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/page-spec/example-types.json
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure_contracts.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
---

# Folder Tree correction

## Request

User, verbatim: “怎么还继续恢复用现有 meglimap啊，我们不是说用 full tree 吗？我操。”

The current request corrects the rendering within the already approved file scope. The reference is the existing Folder Tree: b17 trace/261127/1250_org_rule_as_tree.md, 1255_studio_rule_as_tree.md and 1802_studio_folder_tree_correction.md; s71 elements.md explicitly requires a folder tree for Job-Task. This supersedes this Trace's preceding acceptance of mindmap in Structure. The failure was in this theme's generator and its own check, both of which required the wrong presentation. Source membership/type work remains valid.

## Exact file plan

All paths below were in the user's confirmed 35-file scope. This correction does not expand file ownership or ask for another approval.

- `examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_structure_types.md` — Record the correction, exact file scope and acceptance without erasing earlier evidence.
- `examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py` — Restore existing Folder Tree for all Structure rules and inline examples; keep Draw on separate map fragments.
- `examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py` — Require Folder Tree in Structure and reject a reintroduced mindmap; keep source/identity guards.
- `plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md` — State current Folder Tree presentation.
- `plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/CONSTITUTION.md` — Make Structure Folder Tree authoritative and separate from Draw.
- `plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md` — Document Folder Tree rules and acceptance.
- `plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md` — Register this exact correction and its guard.
- `examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html` — Regenerate Structure as Folder Tree and keep Draw separate.
- `examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json` — Bind Draw to separate map fragments; Structure stays on rule-tree fragments.
- `examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md` — State the current Structure and Draw responsibilities.
- `examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html` — Regenerate Structure as Folder Tree and keep Draw separate.
- `examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json` — Bind Draw to separate map fragments; Structure stays on rule-tree fragments.
- `examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.md` — State the current Structure and Draw responsibilities.
- `examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html` — Regenerate Structure as Folder Tree and keep Draw separate.
- `examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json` — Bind Draw to separate map fragments; Structure stays on rule-tree fragments.
- `examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.md` — State the current Structure and Draw responsibilities.

## Check

Draw inspection found no owned Excalidraw files in s01–s03. The promised existing-canvas rebind is therefore not performed; no unrelated canvas is substituted and no new file is added outside this correction. T44 records the S71 Draw gap. Inline examples retain the explicit user-approved placement.

- Corrected all three Structure rule fragments and inline examples to the existing vertical Folder Tree. Native details/summary, branch lines, level colours and normal-size labels remain; role/type meanings are on hover. The tree adapter retains source links and source identities. No layout renderer, CSS or shared service was changed.
- check_structure.py passes. For each Block kind, one negative probe replaces the Job-Task tree with mindmap markup; another binds Structure to a Draw fragment. Both fail as required. Preserved semantic membership, authored-node merging and generated-output checks also pass. Draw separation is checked without declaring its current map fragments the required S71 format.
- README fresh-context invocation through validate_insight_folder_tree passes, including the follow-up review of role hovers and T44. It independently identifies the missing owned Draw canvases; no Draw-completion claim is made.
- Built-in browser opened the verified Tailscale b11 Work Block. Folder, Job-Task and Studio were selected in all three structure Studios. Board rule and Data group expansion worked; Book version and actual-example expansion worked; Prep actual Jobs/steps matched the source. Source hrefs still target authoritative records. Inline actual Studio content is omitted for Prep, which has no Studio source.
- At 390 × 844, the expanded Board tree shows every branch at normal text size, without the mindmap's clipped root. Deep indentation still narrows labels (the content measurement was 224 px client / 233 px scroll width); the shared top-view row also overflows. T36 stays open rather than claiming complete phone acceptance. The viewport was reset and the owning Block tab marked as the deliverable.
- Job-preview generation remains current. git diff --check passed for this scope. The broad preservation audit finds no unplanned change/addition, no missing approved file, and keeps all protected example sources, existing decisions and canvases. This correction touches only the listed 16 paths from the approved 35-file scope; readable files stay below 700 lines.
- T43 is fixed with browser evidence and regression guards. T44 (S71 owned Draw canvas) remains open. T34/T36/T41 and the example contract gaps retain their independent state. No shared renderer, registry, server process, research source, signature or commit was changed.

Entry: http://100.121.165.84:5623/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb11_theme_insight&layout=focus&section=studio#s01-insight-board-structure



# Current approved round

## Request and authorization

User, verbatim: “好，我确认了，现在你就进行更改吧。”

This confirms the 35-file plan at /tmp/insight-structure-types-261127/PLAN.md. Paper coordination requested the current shared A06/A07 and s71 requirements. The theme keeps the explicitly approved native folding mindmap and inline examples; the shared s71 standalone Examples / Excalidraw-only Draw wording does not silently replace those choices. This round changes only the listed files.

## Plan and preservation

The front matter lists the exact approved files. Their hashes still matched the reviewed plan before execution. Pre-edit copies are at /tmp/insight-structure-types-261127/before-execution/. Existing decisions, folders and source references stay. The earlier Trace record is preserved below, including its original front matter; this round's conclusions supersede only its claims about the current presentation.

## Check

- `check_structure.py` passes: all three catalogs required, four sections with for/holds/source/owner, documented absent layers, semantic group/type separation, Board release pins, full Book membership, code/execution ownership, real Studio source owners/bands, shared writer ranges and generated consistency.
- Preservation checks exercise edited node words, notes, added descendants and reparenting with stable source identities. Renamed Job labels survive wrapper removal; repeated refresh does not duplicate or move authored nodes. The actual pre-edit maps had no authored nodes, and all protected source files/canvases were hash-compared.
- `block_types_pages.py --check` passes independently on s01/s02/s03: 6, 3 and 2 generated type pages. Each manifest's two type views are obtained from that shared generator, rather than an expected hard-coded list.
- `build_job_previews.py --check` passes. The existing s11–s13 files are unchanged.
- Shared `block_types_check.py` exits 1 with three missing-list findings: Book Job group, Prep Job group and Prep Task group. These are the documented absent layers. This is an unresolved shared interface, not a passed check. The local guard rejects missing catalogs and invalid absence without fabricating types.
- README fresh-context invocation completed through `validate_insight_structure_types`: the agent selected workbench-insight, read its dependencies and actual records, ran the checks read-only, identified all type/group distinctions, resolved v2's eight retained members plus K02, and distinguished Prep code from Board execution. It independently confirmed the shared member-reader limitations and the example-face conflicts tracked in T10/T42.
- Real built-in browser acceptance opened only the owning b11 Work Block as the design entry, through Tailscale. All three type views show their actual For/Holds pages. Native Structure and Draw expansion works on Board, Book and Prep. The Book v2 source link opens the authoritative j01 D01 question.md, while K02 resolves to j02. That temporary source tab was closed; b11 remains the deliverable.
- Browser checks found and corrected escaped Markdown in first-level version labels and omitted data pins in the actual Studio tree's Job names. The content adapter now normalizes visible card titles while retaining the shared source chip, raw source text and shared renderer. Regression checks cover both cases. No theme layout/CSS/JS or shared renderer was introduced or changed.
- Studio acceptance shows ordinary Work band ranges and proposed responsibilities in 〈〉, with actual Board studios under their source scopes and actual Other grouping. Prep has no fabricated actual Studio. Book/Prep version groups are omitted as contracted; segments remain Run detail.
- Skills preview reads workbench-insight 1.7.0. The Tailscale Block title and route remain b11_theme_insight throughout the Studio selections.
- Phone acceptance at 390 × 844 reproduces T36: top-view overflow and map content clipping in shared containers. Font size was not reduced. Viewport was reset after inspection. This round does not claim phone acceptance passed.
- File scope audit: all 35 approved files changed or were added; no missing approved file, no unplanned change/addition in b11 or its three example Blocks. Existing face decisions/history and protected canvases remain unchanged. All readable changed files stay below 700 lines. No shared registry/reader was edited, no server was restarted, and no research signature or commit was created.

## Summary

This approved structure-contract batch is complete. s01/s02/s03 each have a source catalog, generated Job types/Task types, correct native grouping and ownership, and ordinary Work Studio organization separate from Blueprint categories. Their Structure and Draw share content; inline examples and owning Skills remain in the Block. T39/T40 are fixed with local guards and browser evidence.

The broader Insight system remains incomplete: T41 shared absent-layer/member matching and Block-owned member routes; T34 live retained Book membership, DataPrep labeling/content and semantic grouping; T36 phone clipping; T06/T10/T11 execution/signing or example dependencies; T42 Book example naming. These require their own applicable file plans. The shared s71 presentation discrepancy is preserved in this Trace rather than added to current skill instructions.

Verified default entry:
http://100.121.165.84:5623/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb11_theme_insight&layout=focus&section=studio#s01-insight-board-structure

## Earlier record (preserved)

```yaml
title: Insight Block types and names
date: 2026-11-27
aim: Each Insight structure Studio distinguishes Job Type, Job Name, Task Type and Task Name, with real folders and one source for Structure and Draw.
closed: true
plan:
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_structure_types.md, what: request, plan and acceptance record}
- {do: edit, path: examples/Project-Ladder/blueprint/b11_theme_insight/board.md, what: index three structure Studios alongside existing UI topics}
- {do: edit, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/page-spec/example-types.json, what: complete canonical semantic type mappings}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py, what: read examples and build linked organization views}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py, what: validate semantic types, membership, source paths and generated views}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css, what: responsive content layout inside the shared Studio}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.js, what: draw the same organization models and select manifest fragments}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html, what: generated Board structure and drawings}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html, what: generated Book structure and drawings}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html, what: generated Prep structure and drawings}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md, what: Board structure topic and history references}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md, what: generated semantic map}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json, what: shared Structure Draw Examples Skills manifest}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.md, what: Book structure topic and history references}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md, what: generated semantic map}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json, what: shared Structure Draw Examples Skills manifest}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.md, what: Prep structure topic and history references}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md, what: generated semantic map}
- {do: add, path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json, what: shared Structure Draw Examples Skills manifest}
- {do: edit, path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md, what: point to current structure law}
- {do: add, path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md, what: define semantic types separately from names and grouping}
- {do: edit, path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md, what: record user correction and acceptance guard}
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_structure_types.md
- examples/Project-Ladder/blueprint/b11_theme_insight/board.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/page-spec/example-types.json
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.js
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
```


# Insight structure types

## Prompts

The user in this session:

> 这里的话你不应该再用 general name 了吧，因为你现在我们是 insight，是一个具体的 blog。那你这个 job topic 什么的，这名字应该都是要具体一些了吧，不能是 topic 1234。我之前那个是给 Walk 讲的，Walk 是 general 的嘛，Walk 那个 blog type 是 general structure。然后你这个是具体到一个 insight，那你这个 structure 应该是要具体一些，比如说 job group 什么名字呀，然后 path 什么名字啊，就是说应该是 propose 1234，propose 一下，你知道吗。

The user in Work theme design: block skill, verified by read_thread on thread
01a21d6c-cdee-7580-aeda-b1852ffb4a14, user message 01a21db4-ea6f-7291-bbc9-2bb13727fb54:

> 那这里面最重要的每一个 blog，之所以跟其他 blog 不一样，那就是它们的 job，name，job type，name，job name，还有什么 task name，它们应该有自己的这个名字。那这样才能区分它们是怎么 organized 的。你先给我放在这个地方，就是这个 block structure，它里面那个 job 种类是什么，对吧？然后 job 的 name 是什么，task 的种类是什么，task name 是什么。那这个一定要把它给弄出来。你这个就是都是模糊化了这样都行吗。 然后就给每一个session都去发个message，让他们就是重新再去更新一下他们的plan，然后去执行。

The specific file plan was shown in this session before editing. The verified instruction
to update the plan and execute authorizes this revision. No shared server or other theme is edited.

## Preservation

Old s01-insight-ladder, s02-insight-workbench and s03-insight-methods are already absent
from the working tree. Their existing Git deletions, original decisions, tracked canvas blobs,
and staged history are untouched. The new s01/s02/s03 structure titles follow the user's
requested numbering; no old decision is renumbered or treated as a new decision.
Current s05, s11, s12, s13 and s99 remain. No example Job, Task or Studio is renamed.

## Check

- `python3 -B delivery/structure/check_structure.py`: passed. Actual Block kinds, Board
  question IDs/levels against pinned releases, Book retained references, prep execution
  ownership, real source paths, shared manifests and generated freshness are checked.
- `python3 -B delivery/structure/build_structure.py --check`: current.
- `node --check delivery/structure/structure.js`: passed.
- Scoped `git diff --check`: passed. All planned human-readable files remain below 700 lines.
- README fresh-context validation: the reviewer independently confirmed all three mappings
  and live/proposed boundaries. Its two source-guard gaps were closed: pinned Board members
  and every Book member's source ID. A mismatched retained D01→D02 reference now raises the
  intended error without modifying an example.
- Existing shared host: b11 Studio and the three generated pages returned HTTP 200. No new
  server, origin, permissions, or shared server file was introduced.
- Actual browser: s01 four-field table and Draw; s02 question-v2's retained references and
  new K02; s03's same-type experiment/source/prepare steps, connected Draw, Skills and live
  Examples embed. At 390 × 844, the mapping becomes readable label/value rows and the drawing
  fits its content frame. Viewport reset; the b11 Studio tab is retained for the user.

## Summary

Completed s01 Insight Board Structure, s02 Question Book Structure and s03 DataPrep Structure.
Each has Structure / Draw / Examples / Skills; the same source model drives table and drawing.
No real Job, Task or Studio folder was renamed or copied. The current file tree remains visible.
T33 is fixed with a guard. This completes the specialized structure design, not all Insight UI.

T34 remains open: the shared Jobs reader omits retained Book questions, its fallback grouping
still needs Book/Prep/Preparation names, and the embedded DataPrep header still says Insight
Board. Those shared integration changes, as well as the separate s11/s12/s13 UI Effects and
Job Overview work, were not included in this file plan.
