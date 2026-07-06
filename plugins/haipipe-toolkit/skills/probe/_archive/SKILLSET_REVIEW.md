> **HISTORICAL (2026-07-05).** Folder-era document. probes/ folders, the Probe Console, and creator agent are retired; current contract = haipipe-probe/SKILL.md 6.1.1 + agents/. Kept as rationale-of-record (SKILLSET_REVIEW is the diagnosis that motivated going folderless).

# probe skill-set review

Date: 2026-07-05 · Reviewer: haipipe-skill-diagnose 1.0.0 · Scope: `Tools/plugins/haipipe-toolkit/skills/probe/` (1 skill `haipipe-probe` 5.0.1, 3 agents, 4 root docs, 53 files, ~5.3k lines; whole core read in the main session, no auditor panels). Paths below are bucket-relative.

Status: Phase 4 FIX in progress (2026-07-05). B1 RESOLVED + executed (gather-only, legacy table deleted). E1 RESOLVED + executed (SKILL.md 481→286, one sentence per line). D2 RESOLVED (redraw), execution queued. C1 OPEN: my answer to your light/heavy question is in the thread below, waiting on your `> JL:` reply. [M] fixes applied so far: A1, A4, A6, A7, A8, B2, C3, C4, D1; still queued: A2/A3 (DESIGN + PHILOSOPHY sweep), A5/C2 (agents + copies), C5 (root changelog), D2 redraw, final grep-zero verification.


## Part 1 · Root causes (先看这个)

1. ① 🚚 搬家没改地址 (9 findings, 4🔴/4🟡/1🟢): three recorded migrations never reached all their readers. (a) The **Return→Deposit rename** (4.0.1/4.2.0) updated SKILL.md + fn/ + schema but skipped the three root docs, so DESIGN/PHILOSOPHY/MENTAL_MODEL still teach `return.md`, `fn/return.md`, `probe.yaml.return`, and SKILL.md sends every new reader to PHILOSOPHY.md FIRST. (b) The **agent merge** (2026-06-23: 3 Judge reviewers → unified haipipe-probe-reviewer-agent, Codex dropped) never reached `fn/judge.md`, which still dispatches all three retired agents via Codex. (c) The **probe-ref letter convention** (4.1.0, `P.T0605`/`P.D0622`) never reached the procedures that CREATE probe folders, which still scaffold legacy letterless names.
2. ② 📄 路由层失真 (2 findings, 1🟡/1🟢): `/haipipe-probe file` is the "front door" in probe-attach.md, the dashboard, MENTAL_MODEL and DESIGN, but SKILL.md's Commands block only knows it as a legacy alias.
3. ③ ⚔️ 内部矛盾 (5 findings, 1🔴/3🟡/1🟢): the CHANGELOG 4.3.0 anti-monolith decision (orchestrator loses Write/Edit) was recorded but never applied to the file; the reviewer agent's verdict yaml disagrees with the canonical schema field names; two docs address `deposit_target` at different yaml paths.
4. ④ 🪝 层间耦合 (2 findings, 1🔴/1🟢): probe-attach.md and DESIGN.md claim `haipipe-data`/`haipipe-discovery` auto-invoke the filing judge on create. Zero such references exist in the task/ or discovery/ buckets (grep verified), and the claim contradicts this bucket's own one-way-dependency rule (MENTAL_MODEL Rule 3) and the settled upper-unaware architecture.

Healthy parts, for calibration: the 3 agent files are current and mutually consistent (orchestrator 1.6.0 freshly maintained, copies in `.claude/agents/` in sync); stage-strip.sh is sound (syntax-checked) and matches the dashboard doc; fn/feedback.md + fn/digest.md are current; feedback inboxes are healthy (16 fixed / 4 open); schema, gather, read, deposit, console procedures are internally consistent.


## Part 2 · Findings

### ① 🚚 搬家没改地址

- [ ] **A1** 🔴 `[M]` `haipipe-probe/fn/judge.md:39-55` dispatches the three RETIRED agents (`probe-structural-reviewer-agent`, `probe-integrity-auditor-agent` "(Codex, Task)", `claim-verifier-agent` "(Codex, Task)"), all merged into `haipipe-probe-reviewer-agent` on 2026-06-23 (agents/README.md:43-57). judge.md also never mentions `fn/g2_integrity_check.py` or `ref/probe-caveats-checklist.txt`, even though the reviewer agent names judge.md as its canonical gate-logic source (agents/haipipe-probe-reviewer-agent.md:31-37) - the canonical file is staler than its consumer. Fix: rewrite steps 3-5 as gates G1/G2/G3 delegated to `haipipe-probe-reviewer-agent` (inline fallback kept), G2 = deterministic `fn/g2_integrity_check.py`, add the caveats-checklist pointer.
- [ ] **A2** 🔴 `[M]` `DESIGN.md:284-302` Judge section: same three retired agents as a live table, "Codex reads the files and rules", plus two dead paths - "Real agent files live in `haipipe-probe/agents/reviewers/`" (real home: bucket `agents/`) and "the plugin top-level `agents/` holds flat symlinks" (real registration: copies in `.claude/agents/`, per agents/README.md:73-77). Also `DESIGN.md:185` lists `fn/return.md` (does not exist; it is `fn/deposit.md`). Same stale Judge story at `MENTAL_MODEL.md:141-152`. Fix: rewrite both Judge sections around the unified reviewer + correct registration note.
- [ ] **A3** 🟡 `[M]` Return→Deposit rename never reached the root docs: `DESIGN.md` (~12 live sites: lifecycle listing :64, Return-vs-Report :72, command `/haipipe-probe return` :137, fn table :203, folder model :225, file schema :249, block ownership :274, filing/insight notes :277) · `PHILOSOPHY.md` (~8 sites: :30, :49-51, :95-101, :116, :193, :206) · `MENTAL_MODEL.md` (~10 sites: :37, :56, :119, :170, :214-216, :250, :275). Decision Log / changelog entries quoting v4.0.0 history stay as history. Fix: mechanical rename sweep (Return→Deposit, return.md→deposit.md, probe.yaml.return→probe.yaml.deposit), keeping "legacy alias return" notes.
- [ ] **A4** 🟡 `[M]` `haipipe-probe/ref/lifecycle-map.md:15` Judge external calls = "reviewer agents / Codex when available"; Codex was removed from the reviewer on 2026-06-23 (reviewer 1.1.0 changelog). Fix: "haipipe-probe-reviewer-agent (G1/G2/G3; G2 via fn/g2_integrity_check.py)".
- [ ] **A5** 🟡 `[M]` `agents/haipipe-probe-creator-agent.md:66` and `agents/haipipe-probe-reviewer-agent.md:68` still write/check `source.return_target`; the schema field is `source.deposit_target` (ref/probe-yaml-schema.md:117). A creator following its own doc writes a field the Deposit step never reads. Fix: rename both; bump both agents + sync `.claude/agents/` copies.
- [ ] **A6** 🟡 `[M]` `haipipe-probe/ref/probe-dashboard.md:51` shallow-check field list ends "...`verdict`, and `return`" (schema block is `deposit`); `ref/probe-yaml-schema.md:216` "Insight may be called by Return after the verdict is judged". Fix: rename both mentions.
- [ ] **A7** 🟡 `[M]` Letter convention (4.1.0, `probes/<LETTER><MMDD>_<slug>/`) missing exactly where probes get CREATED: `haipipe-probe/fn/plan.md:72-73` writes `probes/<MMDD_slug>/` (and step 6 defines no `id:` even though step 5 classifies the T/D letter); `haipipe-probe/fn/gather.md:145` and `ref/probe-attach.md:147` materialize letterless folders; `haipipe-probe/SKILL.md:236-257` "Recommended project layout" shows only legacy letterless examples; `agents/haipipe-probe-orchestrator-agent.md:54` input spec `probes/<MMDD_slug>/`; `MENTAL_MODEL.md:271` one-line rule. Fix: `<LETTER><MMDD>_<slug>` at all six sites + plan.md step 6 gains `id: P.<LETTER><MMDD>`; leave the legacy worked example in probe-dashboard.md (it is labeled as literal legacy-probe output).
- [ ] **A8** 🟡 `[M]` Old subagent-tool name `Task` in `haipipe-probe/SKILL.md:5`, `fn/judge.md:5`, `fn/gather.md:5` allowed-tools (and judge.md prose "(Task)"); the dispatch tool is `Agent` (the three agent files' own `tools:` lists already say Agent). Fix: Task→Agent in the three frontmatters; prose fixed inside A1.
- [ ] **A9** 🟢 `[M]` `MENTAL_MODEL.md:22` "read these" list opens with `../PHILOSOPHY.md`, but MENTAL_MODEL.md sits NEXT TO PHILOSOPHY.md at the bucket root (the other three entries in the same list are bucket-root-relative). Fix: `PHILOSOPHY.md`.

### ② 📄 路由层失真

- [x] **B1** 🟡 `[J]` **RESOLVED per JL 2026-07-05 ("我们就用一个gather得了，把legacy去掉好了。"): gather is the single filing entry; the whole legacy-alias table is deleted; file verb retired; 4 front-door sites reworded to gather. Executed, see the confirm block in the thread.** Original finding: `/haipipe-probe file` status is contradictory: `haipipe-probe/SKILL.md:114-131` Commands block omits it and :143 classes `file` as a LEGACY alias ("gather link / plan, depending on input"), while `ref/probe-attach.md:26` calls it the FRONT DOOR, `ref/probe-dashboard.md:117` renders it in the no-arg panel ("Un-probed: 2 GAP → /haipipe-probe file ..."), `MENTAL_MODEL.md:81-103` and `DESIGN.md:131` list it as a first-class entry point. Arbitration (newest deliberate design beats leftovers): probe-attach.md is a v4.0.0 deliberate design, so promote `file` to the Commands utility block (`/haipipe-probe file "<work>"  filing judge: attach/new/standalone, ref/probe-attach.md`) and route it in step 1d before probe-ref resolution. Thread mirrored below (same thread also sits at `haipipe-probe/SKILL.md:147`; 回哪边都行, 先写的为准):

  > {CC->JL}: `file` 要不要从 legacy 别名升级为正式命令 (review finding B1)
  > 背景: SKILL.md 的 Commands 区是 /haipipe-probe 命令的权威清单。`file` 现在只在 legacy 表里, 说明文字是"旧动词, 视输入映射到 gather link 或 plan"。但同一个桶里有四处把它当正式入口: ref/probe-attach.md 第 26 行叫它 "Front door", 无参 dashboard 的面板模板会打印 "Un-probed: 2 GAP -> /haipipe-probe file ...", MENTAL_MODEL.md 和 DESIGN.md 的命令表也都单列了它。
  > 原文: "file     -> gather link / plan, depending on input"  (只出现在 Legacy aliases 表)
  > 提议: Commands 块新增一行 `/haipipe-probe file "<work>"    file scattered work: ATTACH / NEW / STANDALONE (ref/probe-attach.md)`, Routing 增加 1d (file 首 token 先于 probe-ref 解析, 直读 ref/probe-attach.md), legacy 表删去 file 行。
  > 例子: 你在 dashboard 看到 "Un-probed: 2 GAP -> /haipipe-probe file ...", 于是输入 `/haipipe-probe file "tasks/R02_Reg_TraitDiabetesNDC"`。现状: 路由器把 file 当 legacy 别名, 先猜该走 gather link 还是 plan, probe-attach 的三分支判决 (ATTACH / NEW / STANDALONE + FILING.md 记一行) 不保证被触发。升级后: 第一跳就进 ref/probe-attach.md, 稳定产出 "NEW P.T0622_trait-diabetes (confirm?)" 这样的判决行。
  > 证据: probe-attach.md 是 v4.0.0 的成品设计 ("Front door" 是原话), dashboard / MENTAL_MODEL / DESIGN 三处一致; 只有 SKILL.md 的别名表把它归为遗留。按仲裁序: 最新的深思设计 > 残留清单。
  > 风险: 如果你的本意其实是让 file 退役 (统一走 gather link), 那升级就走反了, 正确动作变成改掉那四处的 front-door 措辞。
  > 问你: A = 升级 file 为正式命令 (我的建议); B = 维持 legacy, 反过来清洗那四处措辞。
  > JL: 我们就用一个gather得了，把legacy去掉好了。
  >
  > {CC->JL}: ✅ 已执行 (你选了第三条路: 不升级 file, 也不留 legacy, 只用 gather)
  >
  >     改动前                                改动后
  >     ┌─────────────────────────────┐      ┌─────────────────────────────┐
  >     │ Commands 正式动词           │      │ Commands 正式动词 = 全部    │
  >     │ + Legacy 表 9 个旧别名      │      │ (legacy 表整个删除 ❌)      │
  >     │   design/bridge/.../file/   │      │ 散工填档入口 = gather       │
  >     │   return                    │      │   (link 路径自动跑          │
  >     │ + 4 处文档教 /probe file    │      │    probe-attach 三分支判决) │
  >     └─────────────────────────────┘      └─────────────────────────────┘
  >     动过的文件: SKILL.md (5.1.0) · ref/lifecycle-map.md · ref/probe-attach.md
  >     (front door 改 gather) · ref/probe-dashboard.md (面板提示改 gather) ·
  >     MENTAL_MODEL.md。旧 probe 文件夹里的 yaml 数据 (status: returned 等) 不受
  >     影响, 只是命令词没了。



- [ ] **B2** 🟢 `[M]` `haipipe-probe/SKILL.md:4` argument-hint `[console|plan|gather|read|judge|deposit|status]` omits the utility verbs the skill actually routes (`feedback`, `digest`, `file`, `link`, `call`). Fix: extend the hint.

### ③ ⚔️ 内部矛盾

- [ ] **C1** 🔴 `[J]` Orchestrator tools contradict a recorded decision: `haipipe-probe/CHANGELOG.md:33` (4.3.0 item 7) records "Orchestrator agent: Write/Edit removed from tools (structural anti-monolith enforcement)" - backed by `agents/feedback/2026-06-23_orchestrator-collapses-to-monolithic.md` and siblings - but `agents/haipipe-probe-orchestrator-agent.md:6-8` has carried Write+Edit since its FIRST commit (86eb7c2, 2026-06-23) and no later commit removed or re-added them (git verified). The recorded decision was never applied. Nothing in the orchestrator's 1.6.0 workflow needs Write/Edit (creator/reviewer own all writes). Arbitration: recorded deliberate decision + feedback evidence beat the (apparently accidental) file state → remove Write/Edit, sync the `.claude/agents/` copy. Thread mirrored below (same thread also sits at `agents/haipipe-probe-orchestrator-agent.md:33`; 回哪边都行, 先写的为准):

  > {CC->JL}: orchestrator frontmatter tools 里的 Write/Edit 是不是该按 4.3.0 的记录删掉 (review finding C1)
  > 背景: 这个 agent 是非交互派发目标, 设计上只协调: creator 写 probe.yaml / evidence.md, reviewer 写 verdict.md, 它自己不产出文件。skill 的 CHANGELOG 4.3.0 第 (7) 条白纸黑字记录: "Orchestrator agent: Write/Edit removed from tools (structural anti-monolith enforcement)", 即用拿走写权限的方式, 从结构上防止它独干不派发 (agents/feedback/ 里有 4 条独干投诉支撑这个决定)。但 git 显示: 该文件从首次提交 (86eb7c2, 2026-06-23) 起就带着 Write/Edit, 之后没有任何提交删过或重新加回。决定被记录了, 从未被执行。
  > 原文: "tools: - Read - Write - Edit - Grep - Glob - Bash - Skill - Agent"
  > 提议: "tools: - Read - Grep - Glob - Bash - Skill - Agent"  (删 Write/Edit; .claude/agents/ 副本同步)
  > 例子: 派发它跑 P.T0605 的 gather+read。带 Write 的实际事故模式 (agents/feedback/2026-06-23_orchestrator-collapses-to-monolithic.md): 它自己读回归表格, 自己写了 evidence.md, creator/reviewer 一次没派, 一条上下文既当运动员又当裁判。删掉 Write/Edit 后: 它写 evidence.md 的工具调用会被权限层直接拒绝, 唯一能走通的路就是 "Dispatch haipipe-probe-creator-agent", 防线从"提示词求它别干"变成"物理上干不了"。
  > 证据: 4.3.0(7) 是有 feedback 佐证的深思决定; 本 agent 自己的 changelog 1.1.0-1.6.0 从未记录重新加回; 1.6.0 工作流逐步看也没有任何一步需要它自己写文件 (SWEEP 只读, REUSE 是纯读返回文本, 建文件夹和写状态都归 creator)。
  > 风险: 若存在未写明的路径需要 orchestrator 直接落盘 (我在 1.6.0 文本里没找到), 删掉后那条路径会 blocked, 需要补派发。
  > 问你: A = 删 Write/Edit, 执行 4.3.0 原决定 (我的建议); B = 保留现状, 并在 CHANGELOG 补记一条 "4.3.0(7) 撤销, orchestrator 恢复写权限"。
  > JL: 我现在考量的是probe是不是有个轻量版和heavy版，有的时候我就是想从现在的existing evidience里去找一些证据，如果再用很heavy的creator或者reviewer这样好吗？你想想怎么帮我解决这个问题。
  >
  > {CC->JL}: 你要的轻量版已经存在, 而且删 Write/Edit 恰好不伤它, 图解如下
  >
  >     你的两种场景, probe 已经分了两条路:
  >
  >     🪶 轻量 (mode: light + SWEEP REUSE)      🏋️ 重量 (mode: full)
  >     🧑 "从现有证据里帮我找 X"                🧑 "H1 要一个正式 verdict"
  >        ↓                                       ↓
  >     🎯 orchestrator 一个 agent 搞定          🎯 orchestrator 派发:
  >        ├─ SWEEP: 纯读 discoveries/              ├─▶ ✍️ creator  写 probe.yaml
  >        │  tasks/ insights/ 里已有的东西          │            + evidence.md
  >        └─ 直接返回带锚点的 takeaways            ├─▶ 🔍 reviewer 跑 G1/G2/G3
  >        ✅ 不派 creator, 不派 reviewer           └─ verdict.md + deposit
  >        ✅ 不建 probe 文件夹, 零写盘          只在要"落笔的结论"时才上重杠杆
  >
  >     关键连接: REUSE 这条轻路径本来就零写盘 (读完直接把 takeaways 返回给
  >     caller), 所以把 orchestrator 的 Write/Edit 删掉, 轻量场景一点都不受
  >     影响; 受约束的只是重路径里它"抢 creator 的活自己写文件"这种事故。
  >     这正是 4.3.0 想要的: 轻查询照样轻, 独干被物理封死。
  > 问你: 这样解释后, C1 还按 A 执行吗? A = 删 Write/Edit (轻量路径不受影响, 我的建议); B = 你觉得轻量路径还不够轻 (比如连 orchestrator 都不想过一道), 那我们先另开一条 finding 讨论轻量入口, Write/Edit 暂缓。
  > JL: 所以light的时候，他只是return一个查出来的结果，对吗？


- [ ] **C2** 🟡 `[M]` `agents/haipipe-probe-reviewer-agent.md:163-173` final verdict yaml uses `claim:`, `scope_supported`, `scope_unsupported`, and `structural: pass|fail`; the canonical schema (`ref/probe-yaml-schema.md:249-268`) and `fn/judge.md:96-111` agree on `status:`, `supported_scope`, `unsupported_scope`, `structural: pass|warn|fail`, plus `next_needs`/`judged_at` which the reviewer omits. The reviewer's own 1.1.0 changelog says "restore warn tier in verdict yaml schema" yet its block lacks warn on structural. Fix: align the reviewer block to the schema; bump + sync copy.
- [ ] **C3** 🟡 `[M]` `haipipe-probe/fn/deposit.md:31` resolves the target from `probe.yaml.deposit_target`; the schema defines it as `source.deposit_target` (ref/probe-yaml-schema.md:117). Fix: `probe.yaml source.deposit_target` in deposit.md.
- [ ] **C4** 🟢 `[M]` `haipipe-probe/CHANGELOG.md:4` header says "Newest first" but entries run 3.1.0→5.0.1 oldest-first. Fix: reorder entries newest-first (matches every other skill changelog).
- [ ] **C5** 🟡 `[M]` Root `CHANGELOG.md` (bucket-level rollup) stops at 4.0.0 (2026-06-22); bucket-level changes since are unrecorded: the agent-triad merge + retirement of the 3 Judge reviewers to `agents/_old/` (2026-06-23), mode full/light (5.0.0), Return→Deposit completion. Fix: add one rollup entry pointing to the per-skill changelog + agents/README.
 
### ④ 🪝 层间耦合

- [ ] **D1** 🔴 `[M]` `haipipe-probe/ref/probe-attach.md:26-28` ("Also auto-invoked by `haipipe-data` (on task create) and `haipipe-discovery` (on discovery create)"), its Hook-points block `:196-206`, and `DESIGN.md:398` claim the lower layers call probe-attach at creation time. False on disk: zero references to probe-attach / `haipipe-probe file` anywhere in `skills/task/` or `skills/discovery/` (grep verified), and the claim contradicts `MENTAL_MODEL.md:170` / `DESIGN.md:350` Rule 3 (one-way dependency: probe reads tasks, tasks never reference probes) and the settled lower-layers-upper-unaware architecture. A reader waits for auto-filing that never happens. Fix (mechanical because the architecture ruling already decided direction): drop the auto-invoke claims; state that the front door is `/haipipe-probe file` at creation time by the USER/probe side, and strays are caught by the no-arg dashboard UNLINKED sweep + FILING.md.
- [ ] **D2** 🟢 `[J]` `haipipe-probe/diagram/03-probe-aware-entrypoint.txt` sketch still shows the retired `minimap` stage in the paper spine and v3 `arms->` vocabulary. It is labeled "[design sketch]". Proposal: add one header line "(historical, v4.0-era sketch; lifecycle wording predates 4.0.1 Deposit rename)" rather than redrawing. Thread mirrored below (same thread also sits at `haipipe-probe/diagram/03-probe-aware-entrypoint.txt:1`; 回哪边都行, 先写的为准):

  > {CC->JL}: 这张旧草图是加历史横幅、重画、还是删掉 (review finding D2)
  > 背景: 这是 v4.0 时代的入口设计草图。里面画着 paper 流水线的 minimap 阶段 (已裁撤, 现行流水线是 folder->seed->pitch->claims->narrative->display->editing), 用着 v3 的 "arms->" 词汇 (已退役), lifecycle 用词也早于 4.0.1 的 Return->Deposit 改名。
  > 原文: "seed -> pitch -> claims -> [narrative] -> figs -> minimap"  和  "|     |   arms->          refs->            files->"
  > 提议: 顶部加一行横幅 "(historical, v4.0-era sketch: minimap / arms / Return 词汇已过时, 仅作设计历史)", 图本身不动。
  > 例子: 新会话按文档索引翻到这张图, 看到 minimap, 会以为 paper 层还有 minimap 阶段, 去找 /haipipe-paper minimap (不存在), 白跑一趟。加横幅后, 第一行就声明这是历史草图; 而图的主旨 (collapsed architecture: evidence core + delivery siblings) 今天仍然成立, 值得留。
  > 证据: 图自标 [design sketch]; banner-保历史 是 SUPERSEDED 横幅惯例的轻量版, 成本一行。
  > 风险: 横幅方案留着过时词汇, 只看截图不看首行的人仍可能被误导; 删图则丢掉唯一一张 collapsed-architecture 总览。
  > 问你: A = 加历史横幅 (我的建议); B = 按 5.x 词汇重画; C = 删掉这张图。
  > JL: 重画吧。
  >
  > {CC->JL}: ✅ 收到, 按 B 重画: 保留 collapsed-architecture 主旨, 词汇全部换成现行版 (paper 流水线去 minimap, arms-> 换 evidence_refs, Return 换 Deposit, probe 例子用 P.T/P.D 字母命名)。重画完成后这条线程和图顶的旧线程一起撤掉。


### ⑤ 📏 重复膨胀 (added mid-review by JL)

- [x] **E1** 🟡 `[J]` **RESOLVED per JL 2026-07-05 ("这个怎么这么长，是不是有很多重复的地方" / "一句话一行 不要break lines"): SKILL.md slimmed 481 → 286 lines.** The feedback/digest rules were stated 4 times inside SKILL.md (Commands one-liners, Skill Procedures block, Routing 1b/1c full detail, Feedback section full detail) on top of their canonical homes fn/feedback.md + fn/digest.md; Gather detail duplicated fn/gather.md; full/light chains stated 3 times; intro duplicated Boundaries. Fix applied: SKILL.md is now the entry contract (commands, routing order, boundaries, pointers), all rule bodies live once in fn/ or ref/, formatting is one sentence per line with no manual wrapping. Nothing was deleted that lacks a canonical body elsewhere.

## Part 3 · Coverage honesty

- `fn/g2_integrity_check.py` (781 lines): header, number-extraction regex families, and output surface read; not line-audited, not executed.
- `ref/stage-strip.sh`: logic read + `sh -n` syntax pass; not executed against a live probe folder.
- `agents/CODE_REVIEW.md`: dated point-in-time review (2026-06-23), treated as history; its retired-agent mentions are in-context, not flagged.
- `agents/_old/` (3 retired agents): not audited, retired by design.
- feedback inboxes (20 files): frontmatter statuses scanned (16 fixed / 4 open); bodies are inputs, not contracts, not audited.
- Cross-bucket claims (D1) verified by grep over `skills/task/` and `skills/discovery/` only; those buckets were not re-read line-by-line.
- Live `examples/*/probes/` project folders: out of scope (skill docs only).
