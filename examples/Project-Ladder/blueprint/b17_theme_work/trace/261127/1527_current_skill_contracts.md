---
title: Current skill contracts
date: 2026-11-27 15:27
aim: Apply the approved first batch of current skill contracts and Files checks.
closed: true
plan:
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-workbench/SKILL.md
  what: 重写当前打开与阅读流程；删除历史操作说明，不宣称 CLI 子路径问题已修好。
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-workbench/ref/work-pages.md
  what: 新增当前共享 Work/Blueprint 页面规则。
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/hai-work/SKILL.md
  what: 保留 propose/update 职责，阅读入口改用 workbench，移除历史布局叙述。
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/update.md
  what: 对齐当前更新、只读检查、Files 与证据验收规则。
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/propose.md
  what: 保留提案流程，核实当前作者脚本，移除历史案例叙述。
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md
  what: 只写当前 Job 记录、脚手架、类型与分组职责。
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-job/ref/job-contract.md
  what: 统一 Block 产出目录归属，移除旧六 Spaces 和历史比较。
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/task/hai-task/SKILL.md
  what: 统一当前目录与命令，准确描述 authored Tasks 的脚手架例外。
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/task/hai-task/ref/task-folder.md
  what: 保留当前 Run/结果目录合同，不再指导旧目录兼容。
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: 首批重写 A06 为当前 Files 角色、路径与排序规则，历史依据保存到 Trace。
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
  what: 写当前角色与验证规则，不保留 Before/Now 叙述。
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
  what: 检查当前角色、真实路径与嵌套，不要求编号标题。
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
  what: 替换过时标题断言，验证当前角色和路径。
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
  what: 验证排序变化不会改变路径或点击目标。
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1527_current_skill_contracts.md
  what: 新增本次用户要求、确认后的计划、文档移出的依据与实际验证结果。
changed:
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-workbench/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-workbench/ref/work-pages.md
- plugins/haipipe-toolkit/skills/2_work/work/hai-work/SKILL.md
- plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/update.md
- plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/propose.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-job/ref/job-contract.md
- plugins/haipipe-toolkit/skills/1_base/task/hai-task/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/task/hai-task/ref/task-folder.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1527_current_skill_contracts.md
---

# Current skill contracts

## Prompts

用户要求：“一定要把他们就是说不要有任何，在 skill 里面不要加任何的 legacy，不要说之前是怎样怎样的，这个是绝对绝对禁止的。”

用户要求：“我觉得可以把 workbench-work 这些东西，把它给融入到那个 skill of workbench 里面。”

用户批准了已展示的逐文件清单：“好，我同意，你现在开始对它进行更新吧，好吧。”

The confirmed first batch contains exactly the 15 files in this plan. Three Codex workers own disjoint file sets; the coordinating session owns this trace. Claude's quota-limited sessions have not received a successful new handoff for this batch.

## Check

- Job scaffold suite: 13 passed; Task vocabulary/type suites: 10 passed.
- Files role-parts suite: 5 passed; work-frame suite: 27 passed.
- Read-only Tailscale b17 Files A06 check passed against the running 5623 service: roles, real source paths and role-local numbering.
- Scoped diff whitespace check passed. The 15 changed paths match the confirmed plan; attribution compares pre-edit bytes, not pre-existing dirty Git state.
- Updated Markdown links and named implementation paths resolve; all changed files remain below 700 lines.
- Full folder-icons checker still reports 11 pre-existing A07 trace-format/moved-path issues; not changed or hidden by this batch.
- Fresh-context Job/Task invocation: PASS. Temporary Block/Job/data-Task/draft-Task scaffolds, schema/register mutation probes and Block delivery resolution behaved as documented. Receipt: /tmp/codex-skill-audit/fresh-job-task.md.
- Fresh-context Workbench invocation: PASS. Actual example Task resolved to its Block; bounded update --check stayed read-only; source inspection and offline rendering matched the reading rules. Receipt: /tmp/codex-skill-audit/fresh-workbench.md. No new browser or physical-device validation was performed by these reviewers.
- Reviewers recorded separate existing gaps: authored-task ticket checks and lifecycle child-path instructions, s02 Task binding/pop-out child routes, and unresolved canonical Work Job-type source. These were not silently filled with guesses or declared fixed.

## Summary

The approved first batch is complete and verified. Workbench now owns shared page reading instructions; hai-work retains propose/update record coordination. Job/Task docs state the current record contract. Files A06 and its checker match the current role-based pane. Historical instruction comparisons removed by this batch are kept as provenance below, not as live skill rules.

Still owed outside this batch: retirement of the duplicate workbench-work skill after runtime data/callers/Studio bindings move; CLI child-path correction; Studio source-generator and S71/S72 synchronization; remaining UI/history cleanup; type checker applicability/missing-field fixes; Trace dirty-file attribution. The Files touched-by Job link uses a child path today; the tests here establish source-path identity, not a fixed embedded Job route. Full-system completion is not claimed.

## Preserved provenance

The excerpts below preserve decision provenance outside active skill instructions. They describe source history, not the current operating contract. Full pre-edit bytes and audit receipts are in /tmp/codex-skill-audit/approved-before and the three audit folders; existing Git history remains untouched.

### plugins/haipipe-toolkit/skills/1_base/workbench/hai-workbench/SKILL.md

> ## 🚪 Open: /wb and /hai-workbench (JL 261009)

> **One share door per SPACE** (JL 261012; b10 s52-D17): a second host on the same SPACE, `--share`,
> 127.0.0.1 only, behind its public name through the tunnel; people sign in with an emailed code
> and see only what the SPACE's `.server_config/access.yaml` grants them. The table names its door
> (`public_url:`, `port:`, for example `https://share.example.test` and a port of its own): each SPACE keeps
> its own values in its git-ignored `.server_config/` (`access.yaml`, `settings.env`), never in this repo. A SPACE with no table has no
> door, and `/wb share` refuses it. A share door is never one of the SPACE's own hosts to `/wb`.

> **What a door can reach** (JL 261012: "will this make my mac studio unsafe?"): only 127.0.0.1 on this Mac,
> so the tunnel is its one way in; only emails in the allowed domains get a code; a grant opens its folder and below, every
> other path is 404; for everyone but an owner it is read-only, with no terminal and no chat. The tables, the cookie
> secret and the mail key are git-ignored and mode 600, so a clone of this repo carries the code and no way in.

> **One host per SPACE, the board is a path in it** (JL 261011: "when we use the /wb we will
> just start from the SPACE, and then we pickup the board"). Every row above goes through the
> one host rooted at the SPACE; a Project, Block, Job or Task is picked up inside it by its
> path. Never start a host rooted at a Project or a board folder: such hosts outlive renames
> and serve gone folders (three such hosts once did, stopped 261011). A Tools
> blueprint Block belongs to the Tools SPACE, so it opens on the host rooted at `Tools/`.

> **A renamed folder keeps its old links** (JL 261012: "I cannot open you anymore"). Whoever renames a Block,
> Job or Task writes the old name into its face, `renamed-from: <old name>` (or a list); the host then answers
> an old `path=` with a 302 to the new one, the Space and subspace kept (`frame_view.renamed`). A name that never
> existed still says Not found.

> 1. **Run the script** from inside the SPACE: `.venv/bin/python <this skill's folder>/cli/wb.py <input>`
>    (from the SPACE root, `Tools/plugins/haipipe-toolkit/skills/1_base/workbench/hai-workbench/cli/wb.py`).
>    A path may be SPACE-relative or relative to where you are; a file inside a folder opens that folder.
> 2. **It checks before it hands out**: it finds this SPACE's running `servers/_host/serve.py --root <SPACE>`
>    (the lowest port when several run), starts one from `.server_config/settings.env` when none does,
>    loads the link, and restarts a server that drops the request (a server started before another
>    session renamed something in Tools holds old paths). Then it opens the browser and prints the link,
>    the folder, its level and the skill for its theme. `--no-open` only prints; `--no-restart` never restarts.
>    A running host keeps the code it started with, so after a Tools change run `wb.py restart` in each SPACE.
>    It starts serve.py with the SPACE's `.venv/bin/python` when that has PyYAML (Python 3.10+), else
>    `~/.cache/haipipe/host-venv/bin/python`, made once with uv (`launcher` in cli/wb.py).
>    A Project, Theme folder, Block, Job or Task opens on its focus page (`layout=focus`: Report · Studio ·
>    Delivery · Interaction · Related, the page picks its opening section; Work is retired in every theme; JL 261030: "Why not using the UI that we discussed
>    previously?"); `--classic` opens the old screens (Project Home view, the frame on its Studio).
> 3. **Words**: it ranks every Project, Theme folder, Block, Job and Task by folder name, title and
>    `spine:`/`goal:`/`status:` lines, using the server's own lists (`home.discover_boards`,
>    `frame.children`, `frame.theme_of`), so a found place and the screen agree. Level words
>    (project, block, job, task) and theme words (paper, cowork, discovery, insight, design,
>    labeling) narrow the search. When one place clearly wins it opens it.
> 4. **No clear winner** (`🙋`): read the listed titles and pick by meaning (`CGM-FM` is the CGM
>    foundation model), then run `wb.py <that path>`. Do not ask the person to choose: open the best
>    one and name the next two as links. `--find` only lists.
> 5. **Then route**: load the printed skill when the person wants the screen explained or worked in:
>    `workbench-work`, `workbench-cowork`, `workbench-discovery`, `workbench-paper`, `workbench-insight`,
>    `workbench-design`, `workbench-labeling`, or this skill when the folder has no theme. Reply with
>    the printed link; its Tailscale address also opens on a phone.

> ## 🔧 Update: /wb update <Block> (b10 s10, JL 261012)

> One door that takes any Block, old or new and of any theme, to today's rules (JL 261012: "I want it work
> like /wb update-to-date path to the block"). `cli/wb.py update <Block>` hands it to `cli/wb_update.py`.
> A new Block starts on `hai-block`'s `new_board.py`, which writes today's face, so this door then says
> "today ok"; run it again as Jobs and Tasks arrive. `workbench-work` only shows a Block; it never changes one.

> `ref/roster.md` is the single list: name · kind · storage · surface · writer · status.
> Every optional surface, including the Page Runs stepper, appears in the one
> Workbench picker. A surface may use its own panel layout after opening, but that
> never creates a second top-level menu.
> A generic Page Workbench's OPERATING knowledge lives in one of exactly two
> public skills: `workbench-task-draft`, beside this one in `skills/1_base/workbench/` (the 📃 Page
> tab with its Draft, Evidence and Delivery Spaces and their Runs panels, the 📤
> Delivery tab, and the 📂 Folder tab: everything
> `servers/workbench/workbench-task-draft` renders) or `hai-studio`. Internal lanes
> live as references under their owning category skill; they never mint
> duplicate callable skills. Page owns Citation/Bib, Value, Display, the ranked
> Skill record, the All-runs view (`ref/run-space.md`), LaTeX, Word, Slide, and Render
> (`ref/delivery.md`), and the Folder inventory (`ref/folder.md`); Studio owns
> Chat and Draw. PageX is legacy migration input only.
> Every other workbench skill lives in the family that owns its lanes and its
> writer, never in the Page family: `skills/3_theme/design/workbench-design`
> (the Design Folder; the Design Board grain is its `ref/design-board.md`),
> `skills/3_theme/insight/workbench-insight` (one InsightBoard page; the board
> grain is its `ref/insight-board.md`), `skills/3_theme/paper/workbench-paper`
> (the Paper Board), and `hai-labeling`'s `workbench-labeling`. Each
> pairs by name with `servers/workbench-<x>`; a workbench that serves two grains
> keeps the board grain as a ref, never as a second top-level skill, and none
> promotes an internal lane to a duplicate top-level workbench.
> One lane inverts the shape: `workbench-task-draft/ref/folder.md` is the 📂 meta-surface over the roster itself — no subfolder, no storage, no roster row (JL 260816).
> This contract stays the base every one of them loads on top of; the board pages (`QPf2`-`QPf8`) stay the design records; the engine keeps only routes and machinery.

### plugins/haipipe-toolkit/skills/2_work/work/hai-work/SKILL.md

> The work theme runs bounded execution work: code, data, models, calculations.
> It is one of the themes in `skills/3_theme/` (beside cowork, design, discovery,
> insight, labeling and paper). Its current focus pages use the shared
> `servers/workbench/page/block_index_page/focus_page.py` and `work_frame.py`; `servers/workbench-work`
> also retains the classic workbench. It was
> called the task theme until 2026-10-07; the Task as a ladder level (Block ->
> Job -> Task -> Run) belongs to every theme and keeps its name.

> ## Plan new work on the Plan + Results view (JL 261109)

### plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/update.md

> | View | Inspect and align | Do not invent |
> |---|---|---|
> | Overview | Goal from the level's face; Requirements and close conditions; MindMap from existing topics, Questions and work | Goals or requirements inferred only from folder names |
> | Plan + Results | One section per Job type (face `bands:`, else the Job's `use-case:`, else its Tasks' task-type); each Job row its state and a bar of its Tasks done, opened to its Tasks and Runs; authored Dependencies | New Job types, synthetic Runs, or a generic Next Steps list in place of the Job rows |
> | Findings | A Block first shows 🗄️ Data, its stores from board.md's `data:` block (`hai-block` board contract; counts read from a Result, never typed). Then, at every level and nothing else (JL 261111): 🔢 Values, the value Jobs' newest tables.json and the values.json numbers the text can quote (`hai-evidence`, VALUE catalog); 🖼️ Displays, the display Tasks' preview.pdf (`hai-display`, display unit). Each keeps its slot when empty. Last, 🧠 Maps, only when the work drew maps (result/maps/). Studio topics and ❓ questions are not Findings (CoWork and Discovery keep their questions) | Findings copied from a template or completion inferred from a file's existence |
> | Delivery | Actual artifacts, recorded acceptance and usage | Acceptance, release, or delivery merely because a build exists |
> | Blueprint UI views | Configured real example pages, type/view matrix, walkthroughs, review evidence | Block UI / Job UI / Task UI / Run UI on an ordinary Work Block, or an unsupported level's example |
> | Title line | The type and use case under each title come from the records: a face's `use-case:`, a work Task's `task-type:`, a Run's `type:` | A `use-case:` guessed from a folder name, or one copied from the Block to its Jobs |

### plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/propose.md

> 1. **Sections are files a script writes**: a build script writes one Markdown file per section, `# <emoji> <title>` on
>    its first line, so a rebuild keeps them in step with the material. Do not hand-write what the material already says.
>    A long list of entries (a decision log) is one list item per entry with its detail as sub-items: the page shows
>    each entry as a card that opens. Write the sub-items as labels: `Session:` and `Area:` become chips, `Decided:`,
>    `JL asked:` and `Built:` tinted blocks. A list whose items start with a bold time (`**12:53** · title`) is drawn
>    as a timeline; an item bold all through (`**12:39 to 13:51 · title**`) is a phase on it, and the entries under a
>    phase come after it.
> 2. **The face names them**: `board.md` gets `## Review Content` (the Overview), `## Plan + Results` (after the
>    Jobs, numbered on: what happened when, such as one section per day) and `## Findings`. Each
>    `### <emoji> <title>` is one numbered section; a line `embed: <path>` brings in a `.md`, rendered, or an `.svg` drawing, inline (hover titles work, scripts are stripped). When the material is many people or sessions over time, draw it first as a transit map (one line per person or session, a station per entry in time order, a shared entry joining the lines; the method of trace-canvas), as Overview's section 1. In those sections, a line `each: <glob>` makes one section per matching `.md`, titled by its `# ` line.
> 3. **Native sections, never a website**: page content maps to the Block's own sections as Markdown. A standalone
>    `.html` page (a replay site, a dashboard) is never framed into a section, a Deliverable card or a Service
>    (JL 261114: "map the content to the website structure of the workbench UI"); its content becomes sections.
> 4. **Jobs on the ladder**: `jNN_<job>/jNN_<job>.md` (`state:`, `goal:`, `emoji:`, `use-case:` and `## Tasks`), its Task
>    faces, and the Runs from step 2. The face's `## Jobs` lists them in order. `use-case:` names the Plan + Results
>    section that Job falls under.

### plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md

> Delivery belongs to the Block (JL 261010). Only the Block has a physical
> `delivery/` folder. A Job writes `delivery/jNN_<job>/`, a Task writes
> `delivery/jNN_<job>/tNN_<task>/<lane>/`, and a Report writes
> `delivery/reports/qNN_<report>/<lane>/`, all relative to its Block. Child
> Delivery views select their own source subtree. Runs and Results remain at
> their source; a build grants no acceptance or release. Use
> `hai-draft/src/common.py` for the path, never create Job/Task-local delivery.
> Standalone Pages without a Block retain their own output root.

> A Job's title is its folder's words: `j01_work_ladder_contract` is `# j01 · Work ladder contract`,
> so the name on every page row matches the folder; give `new_job.py` that `--title`, and rename the
> title with the folder. Its face carries an `emoji:` line (after `close:`); a Block's Status shows
> each Job as that emoji, its jNN, its name and how far (b17 s04-D19, JL 261108).

### plugins/haipipe-toolkit/skills/1_base/project/hai-job/ref/job-contract.md

> JL 261020: "I want it like the TODO list ... for each job, what are the delivery and outcome to
> provide ... make the Goal to be the first one". The face's `## Deliverables` holds one fenced
> `yaml` block; the workflow layout's Goal view (workbench-work `work_progress.py`) draws it as one
> folded tree, Goal → Job → Task → item, and ticks each item from disk, never from a person's word.

### plugins/haipipe-toolkit/skills/1_base/task/hai-task/SKILL.md

> > ⛔ **Generated files: never modify them directly; change the code that writes them, then rerun it**
> > (JL 260928; the SPACE's AGENTS.md § Working rules). Here: a ticket a `gen_*.py` writes, a notebook, a figure, a Table
> > Card, everything in a Run's `result/`.

> The twelve type skills are hidden from the skill listing (`disable-model-invocation: true`,
> JL 261026): read the type's SKILL.md by the path below and follow it. A person can still type
> `/hai-task-for-<type>`; `/hai-task <type> …` reaches the same file through this door.

### plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md

> > "these two are more like the topic, right? they are not the real folders, is that correct?" (JL 261124, Files pane groups)
> > "for each section, could you also give the full path from this SPACE? do you get hwta I mean here>" (JL 261124)
> > "we still wnat to keep the relative structure here, do you get it?" (JL 261124)

### plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md

> > "these two are more like the topic, right? they are not the real folders, is that correct?" (JL 261124, Files pane groups)
> > "for each section, could you also give the full path from this SPACE? do you get hwta I mean here>" (JL 261124)
> > "we still wnat to keep the relative structure here, do you get it?" (JL 261124)
