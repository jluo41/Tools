---
title: Insight Studio bindings and current contracts
date: '2026-11-27'
aim: Use shared Bands and Studio types, preserve the three Insight Block contracts,
  and bind each Studio to real source content.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_studio_bands.md
  what: 记录本次原话、文件计划、确认、验收、共享接口缺口；在确认后创建。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/board.md
  what: 移除重复的 bands 覆盖，沿用共享 Band 来源；更新 Studio 导航说明，保留 Decisions。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: 更新生成源：Structure/Draw/Skills；各结构内容中嵌入对应真实例子；规则与实例分别标定，复用现有 mindmap。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
  what: 守护共享 Band 来源、三视图绑定、实例仍可达、来源与版本成员、人工 mindmap 修改及生成一致性。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
  what: 由更新后的生成器重建；规则与该类型的实际例子在同一内容项中展示。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json
  what: 由生成器绑定 Structure / Draw / Skills，不独立占 Examples 顶部视图。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md
  what: 更新当前 view 内容、实例入口和 owning skills；保留历史决定与来源。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
  what: 由更新后的生成器重建；规则与该类型的实际例子在同一内容项中展示。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json
  what: 由生成器绑定 Structure / Draw / Skills，不独立占 Examples 顶部视图。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.md
  what: 更新当前 view 内容、实例入口和 owning skills；保留历史决定与来源。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
  what: 由更新后的生成器重建；规则与该类型的实际例子在同一内容项中展示。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json
  what: 由生成器绑定 Structure / Draw / Skills，不独立占 Examples 顶部视图。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.md
  what: 更新当前 view 内容、实例入口和 owning skills；保留历史决定与来源。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_job_previews.py
  what: 新增轻量绑定生成器，只生成共享 Studio manifest，并提供 --check；不实现布局或读取患者数据。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview/studio-views.json
  what: 绑定真实 Block 内 Job/Task、合同、现有方案和人工画布；不独立占 Delivery/Instances。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview/s11-insight-job-preview.md
  what: 写清该类型的 Main/Task 内容和未实现项；Checklist 使用共享侧栏读取的章节；保留历史决定。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s12-questionbook-job-preview/studio-views.json
  what: 绑定真实 Block 内 Job/Task、合同、现有方案和人工画布；不独立占 Delivery/Instances。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s12-questionbook-job-preview/s12-questionbook-job-preview.md
  what: 写清该类型的 Main/Task 内容和未实现项；Checklist 使用共享侧栏读取的章节；保留历史决定。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s13-dataprep-job-preview/studio-views.json
  what: 绑定真实 Block 内 Job/Task、合同、现有方案和人工画布；不独立占 Delivery/Instances。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s13-dataprep-job-preview/s13-dataprep-job-preview.md
  what: 写清该类型的 Main/Task 内容和未实现项；Checklist 使用共享侧栏读取的章节；保留历史决定。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md
  what: 重写当前阅读入口与 Block 内导航、三种语义和 Studio 绑定；不混入历史 UI 比较。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/CONSTITUTION.md
  what: 保留默认所属 Block、共享 mindmap 规则；加入共同 Band 规则，撤销 Schedule 待办。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
  what: 同步当前类型/名字/分组边界、结构与实例关联、共享 views，以及验证要求。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
  what: 保留当前 topic 索引、原话、问题、状态与 guard；已有长篇事件记录移至技能外 Trace。
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_topics_evidence.md
  what: 完整保存 topics.md 现有事件记录，保持 topic ID 与来源可追溯。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md
  what: 当前三 Block 入口、版本组合、职责与签署边界；不新增 Job/Task schema 类型。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/ref/insight-ladder.md
  what: 当前三 Block 合同与 release 成员引用；保留执行、签署、问题编号和运行依赖规则。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/ref/dataprep.md
  what: 当前 code-only DataPrep 与 Board prep Run 合同；删除历史比较文字，保持签署与执行限制。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight-workflow/SKILL.md
  what: 当前 Run 路由、实际文件 gate 与人类签署；Run card 分类不再宣称是当前顶部 UI。
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-question/SKILL.md
  what: 当前 proposal→版本→问题定义合同；保留中立提问、评审与不复制来源；移除历史 UI 叙述。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_shared_mindmap.md
  what: 追加澄清：Schedule 已撤销；手机横向布局仍由共享组件负责，保留原事件记录。
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s99-guide/s99-guide.md
  what: 内容与目录保留，按 Work 落地的显式类型引用接口归入 Theme Guide；不重编号、不删除画布及来源。
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_studio_bands.md
- examples/Project-Ladder/blueprint/b11_theme_insight/board.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_job_previews.py
- examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview/s11-insight-job-preview.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s12-questionbook-job-preview/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s12-questionbook-job-preview/s12-questionbook-job-preview.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s13-dataprep-job-preview/studio-views.json
- examples/Project-Ladder/blueprint/b11_theme_insight/s13-dataprep-job-preview/s13-dataprep-job-preview.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_topics_evidence.md
- plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/ref/insight-ladder.md
- plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/ref/dataprep.md
- plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight-workflow/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-question/SKILL.md
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_shared_mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s99-guide/s99-guide.md
---


# Insight Studio bindings and current contracts

## Prompts and authorization

User: “好，我同意你现在就开始干嘛哈。”

The user approved the 32-file plan presented in this session. The reviewed plan and type inventory were prepared outside the repository before confirmation. Shared rules relayed by Work: Bands and Studio Types are distinct; themes reference shared types and may define their own; omit empty groups. s75 Task Procedure, s77 Studio Type and s79 Guide cease to be separate type definitions. Preserve actual content, directories, drawings and sources. s99 belongs to Theme Guide. Do not edit shared readers or restart the service.

## Plan

The front matter is the exact approved file list. Pre-edit copies and hashes are held outside the repository under /tmp/insight-studio-alignment-261127/before/. Existing dirty changes are preserved.

## Shared boundary

At the start, studio_types.py derives bands from s7N type faces and studio_tabs.py groups by directory decade. The explicit type reference interface and type retirement are not implemented. Record s99's semantic Theme Guide responsibility and source; do not invent an unsupported binding key or claim reclassification is live. The shared phone layout, retained Book member navigation and type-instance Checklist integration remain separate issues.

## Shared implementation accepted

Work reported its registry/readers accepted and 5623 reloaded under its existing parameters. b11 now inherits `b17_theme_work/delivery/page-spec/studio-bands.json`; no local Band override remains. The six content Studios and s99 keep their actual directories. Shared type definitions are referenced by source links. No unsupported instance-type field was introduced. s99's content contract is Theme Guide (s78), while its unchanged directory remains in the registry's s9N Guide Band. The two classifications are distinct.

This session did not change shared readers, registry, services, real example Jobs/Tasks, .mindmap.md, .excalidraw, structure.css or structure.js. The generator checked its unapproved outputs for identity before writing the approved outputs. Existing authored words and branches have a preservation check. The original 688-line topics file is preserved byte-for-byte in insight_topics_evidence.md.

## Check

### Source and generation

- `delivery/structure/check_structure.py`: pass. Shared renderer/grammar, native folds, actual parentage, question-release pins, nine v2 members including eight retained sources, prep execution ownership, authored map changes, source links, current skill bodies and generated freshness.
- `delivery/structure/build_job_previews.py --check`: pass. All preview manifest targets resolve to actual files and owning Block Job/Task selections; top views match the source generator.
- Approved 32-file baseline comparison: whitespace and readable-file length checks pass; original topics archive is byte-identical. Generated HTML is exempt from the readable-file length limit.
- Read-only HTTP verification: 43 unique Tailscale routes returned 200, including the b11 entry, Job/Task selections, contracts, all retained question sources, structure pages, QuickHtml, native mindmaps and Canvas endpoints. Initial sandbox network access was unavailable; the approved read-only check then ran outside that network sandbox. Receipt: `/tmp/insight-studio-alignment-261127/final-checks.json`.
- Run card structure/owner check: all 83 cards parse and reference real owners. The full scaffold-import check and next_run helper could not run in the host environment because pandas is absent. No shared environment was modified; do not count those two checks as passed.
- Validation used the running host's Python 3.13 environment. Shared UI imports require Python 3.10 or later; the system Python 3.9 cannot import them.

### Browser acceptance from the owning Block

Entry: `/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb11_theme_insight&layout=focus&section=studio#s01-insight-board-structure`, reached through the Tailscale origin used in this session.

- s01/s02/s03 expose Structure / Draw / Skills. Rule maps and inline actual examples use the native renderer; Open all expands the real Job/Task branches. No standalone Examples top view. Source chips retain actual source paths; Book v2 shows kept definitions from v1 without copying them.
- s03 Skills loads the actual hai-insight source. Structure and Draw use the same rule/example content.
- s11 selects Insight-Example j03 and t02; its question release and data/prep pins remain visible. s12 selects the Book's j02 and t09/K02 in the same Block identity. Neither opens a separate Job/Task page.
- s13 selects DataPrep j01 and t01 in its actual Block route/title. The live shared header incorrectly calls the Block Insight Board, and the selected step has no content. These are T34 gaps, not failed source bindings and not implemented by the proposal.
- QuickHtml loads Segment grid, Version changes, and Steps and Runs. These are proposals, distinct from the live Page-Job/Page-Task output.
- s13 Draw opens the existing native MindMap and preserved Canvas endpoint. The MindMap itself contains no authored content beyond its title; this round did not invent a drawing or overwrite the Canvas.
- At 390 × 844 the shared container clips horizontal map nodes. Text remains normal size; no theme-specific shrinking or layout was introduced. Viewport override was reset. T36 remains open.
- The retained browser deliverable is the owning b11 Block, not an internal HTML asset.

### Fresh-context skill invocation

The required independent reader loaded the current workbench-insight, hai-insight, question and workflow entries and checked actual example files. It confirmed:

- A Board Job pins a question release and data version, plus prep when used. j03 remains data-v2 × prep-v1 × question-v1; no fabricated v2 Board Job.
- Book v2 has nine release members, eight by source reference. DataPrep owns code; its execution is the Board prep Task's Run.
- K02's completed review Run contains a returned verdict and needs revision. Its collection placeholder is not a person's signature. Existing result Runs do not prove complete readings, answer pages, CHECK or signed close.

The reader found two instruction-layer problems, now corrected within the approved skills: card dispatch must check the owning DataPrep interface first, and command success must not be described as enforcing every review/signature gate. Its follow-up verdict was: “复核通过：两项发现已在技能指令层解决。” It explicitly kept the underlying Run-card conflict, sign() guards and example wording open. No analysis data or human signature was executed during validation.

## Outstanding work and boundaries

- **T34:** include retained Book members in live Job navigation; semantic prep grouping; DataPrep identity and step content. Main Brief / Plan + Results / Findings content remains the documented target, not a claim that every real fold is implemented.
- **T36:** shared phone horizontal layout and a regression check.
- **T11:** `hai-insight-workflow/ref/run-cards.md:542` requests per-dataset configs for a DataPrep step, conflicting with run(ctx). Current dispatch instructions prohibit following the conflicting card. The card, generated consumers and guard need their own approved update.
- **T06:** `hai-insight/scripts/insight_ladder_book.py:199–216` checks local agreement and named segments but lacks full review-verdict and segment-consent checks. The skill requires evidence and an actual human decision; command guards still need implementation and rejection tests.
- **T10:** `InsightDataPrep-Example/board.md:17` calls ready output a next data version; the current owner contract correctly keeps raw data and prep versions separate. Example correction is outside this file list.
- Shared automatic type-to-instance Checklist integration has no supported binding API here. Concrete checklist sections use the existing reader; do not claim automatic integration.
- Active documentation dependencies outside this plan remain caller-aware work: the table source used by `servers/workbench-insight/studio/insight-workbench-design.py` and cards_table.py, plus remaining old-page/register references. They were not deleted or declared migrated.
- Schedule is not a requested task; the user withdrew that interpretation.

## Summary

The approved Studio binding and current-entry contract batch is complete. T37 and T38 pass with source guards and browser evidence. T06/T10/T11/T34/T36 remain open with the specific owed work above. The overall Insight product is not declared complete. No directory migration, data execution, signature, shared-service restart or commit was performed by this session.
