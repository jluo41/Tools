haipipe-paper — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.4.1] — 2026-07-03

Fixed
- Marker rule tightened from "at most one 🔥 and one 🚀 per line" to EXACTLY one of each, never zero (live seed run rendered `draft 🔥` with no 🚀 anywhere). "Reached" defined as entered-not-completed, so a virgin paper's first phase renders `draft 🔥🚀`; a line with 🔥 but no 🚀 is a rendering defect.

## [2.4.0] — 2026-07-03

- create verb RETIRED, absorbed into enter as GET-OR-CREATE (JL: 直接去掉create，enter的时候没有就call create): a missing path CONFIRMS first (repo creation is outward-facing, never off a typo), then runs the same flow (org resolved per invocation, papers-inside recipe, folder scaffold, double-bump) and continues straight into the console. Verbs block, dispatch notes, examples, chooser, argument-hint updated; lifecycle + folder-skill + wiki/04 cross-references repointed. The create flow itself is unchanged and was validated live (Paper-PhyPatSim run) before the re-homing.

## [2.3.0] — 2026-07-03

- stage-strip.sh moved from wiki/10-stage-strip.sh INTO this skill folder (co-located with the Closing Block spec it renders; JL: 为什么 strip 在 wiki 里有这里也有); all 8 references repointed, wiki has no strip content left.
- Resolved > JL: / > CC: comment threads archived below verbatim and removed from SKILL.md (comment lifecycle: working doc stays clean, resolved threads move to the log). Companion changes landed in their owners: wiki/08 Gate Modes (copilot|autopilot) + APPROVAL step + ledger Actor column + Stage Exit Invariant; haipipe-paper-check 1.4.0 (Gate Modes + invariant); haipipe-paper-probe 1.7.0 (From-buffer entry).

### Archived comment threads (verbatim)

**@ Verbs / Dispatch notes**

> CC: write/edit 的老路由目标 haipipe-paper-edit-write / edit-weaving 在重构后已不存在（对应能力并入 2-phase/2-revise workers，由 stage 内部调用）。我把 write/edit/polish 这些词全部路由到 section-edit stage 了，对吗？还是这组动词干脆退休不再出现在 Verbs 块里？
> JL: 是的，旧词不要再出现了，省的误导
> CC: 已退休全部旧词（write/edit/polish/draft/写初稿/整篇润色），section-edit 行只留 section-edit|section|sec|§N。
> JL: 好，done

**@ Closing Block (end every reply)**

> JL: 这个应该有两层吧 一个是stage，一层是phase
> JL: <--- 这里可以弄的再简单一些吗。比如paper root不要了，然后status和current layer放到一起。
> JL: 我们是不是也有其他的file也在讲这个，要不把他调到这里，我们single source of truth
> CC: 三条都已落：两层 strip（stage+phase）、tail 简化为 status·stage + next 两行、wiki/01 语义并入本节并删除原文件（enter skill 的引用已改指这里），此节即唯一出处。
> JL: 我想说你这个跟wiki里的strip的关系是什么，会冲突吗？
> CC: 不再冲突：wiki 里剩的只是渲染脚本，现已把 10-stage-strip.sh 也搬进本 skill（./stage-strip.sh，与 spec 同住），8 处引用全部改指，wiki 里已无任何 strip 内容。

**@ Gate-aware (Closing Block)**

> JL: 你要想着我们有两个mode，一个co-pilot 在check phase的时候，人加上comments，一个是auto pilot，在check的时候，call一个subagent，然后让他给comments 你想想这个我们怎么做。但是是的，必须要有一个judgment，就是这个gate-aware，进入下一个stage要非常的明白，要有confirm，要有一个approval的动作（人或者代替人的subagent）
> CC: 方案在 chat 里：CHECK 增加 mode=copilot|autopilot，autopilot 派 reviewer subagent 给 comments + approve/revise verdict，gate ledger 记 approval actor；你点头后我改 wiki/08 + haipipe-paper-check。
> JL: 可以的，你整吧。
> CC: 已整：wiki/08 加 Gate Modes 节 + APPROVAL 步骤 + ledger 增 Actor 列；haipipe-paper-check 加 Gate Modes 节（autopilot 派 fresh reviewer subagent 落 > REVIEWER: comments + verdict；bibtex 等人类专属项标 DEFERRED 进 human queue，绝不静默放行）。

**@ Composing with Evidence Workers**

> CC: 原文这张图上游还列了 /idea-discovery /run-probe /auto-review-loop /result-to-claim 四个入口，skill 清单里已找不到，我删了。如果它们有新名字（或还想保留占位），告诉我补回。

**@ Composing with Evidence Workers**

> CC: 原文头部还有一处孤立引用（"读 lifecycle 参考时也读 ../1-lifecycle/haipipe-paper-display-figure/SKILL.md"），看不出为什么单点名 figure 渲染器，我也删了。有特殊用途的话说一声。

**@ Composing with Evidence Workers**

> JL: 我们要不要把所有的wiki的内容也都移到这里来。然后随后把wiki的东西删掉。skill最好还是self-contained
> CC: 建议不整体搬：wiki/ 本就在 paper 家族内部（家族级 self-contained），02/04/08/10 各有 5-10 个 skill 共用，搬进 umbrella 会让每次调用重新变胖；折中方案已执行 wiki/01（并入本文件）+ 单消费者页可逐个并入唯一消费者，详见 chat。

**@ Composing with Evidence Workers**

> JL: 这个的话，我在想，还都是有haipipe-paper-probe 来进行probe calling？不要让haipipe-paper直接call了，他在一个stage的一个phase的阶段来call。
> CC: 已改：umbrella 不再直连 /haipipe-probe，probe run 交给 haipipe-paper-probe（stage 的 PROBE phase worker）消费 1-probe-plans/ 再向下分发；Verbs 行、dispatch note、上图已同步。
> JL: 好，再确认一下。
> CC: 已确认并补齐另一端合同：haipipe-paper-probe 新增 "From-buffer entry" 节（from-buffer <paper_root> [PPNN]：读 planned 项 → reuse-before-create → 分发 /haipipe-probe → 回写 status/probe_ref → 返回 dispatch summary），两端调用签名一致。

## [2.2.0] — 2026-07-03

- JL in-file comment round applied (> JL: / > CC: threads kept in SKILL.md): (1) retired write/edit/polish/draft alias words entirely (省得误导); (2) closing block now TWO-LINE focus strip (stage + phase) with the simplified tail (status·stage merged, paper_root dropped, next only); (3) wiki/01-focus-strip-markers ABSORBED into the Closing Block section as the single source of truth (file deleted; enter skill + 10-stage-strip.sh + wiki README repointed; wiki numbering gap kept); (4) umbrella no longer calls /haipipe-probe directly -- probe run hands 1-probe-plans/ to haipipe-paper-probe (the PROBE phase worker inside a stage's phase), composing diagram + dispatch note + description updated; (5) gate-aware line now names the two approval modes (copilot human / autopilot reviewer subagent), full design pending JL confirm (wiki/08 + check skill).

## [2.1.0] — 2026-07-03

- Dedup rewrite (JL: "会有比较重复的地方吗", same treatment as discovery 2.6.0): say each thing ONCE. Command table + keyword map + positional aliases + Routing Step 2 (the same dispatch stated 4 times) merged into one Verbs block + one 6-rule Routing pass; feedback/digest full spec (written twice + fn/) reduced to one pointer section; create recipe (written twice + owner fn) reduced to one dispatch note; probe/venue-coupling/folder-tree/skill-tree restatements replaced by pointers to their owners (fn/probe-plans.md, wiki/03, paper-folder-anatomy.md, wiki/06). ~545 -> ~200 lines.
- Stale fixes swept in: 2-claims -> 1-claims backfill refs; 3-narrative.tex -> .md; phantom top-level 2-section-edit/ dir removed from the skill tree (real homes: 1-lifecycle/5-section-edit + 2-phase/); write/edit rerouted to section-edit (old targets haipipe-paper-edit-write/-weaving no longer exist); stage list gained section-edit; "phase skills" wording corrected to stage skills (DPRC phases are internal); retired upstream workflow names dropped from the composing diagram.
- Three open questions embedded as > CC: markers for JL review (write/edit verb fate, retired upstream workflow names, dropped display-figure reference).

## [2.0.2] — 2026-07-03

- create verb added to the front door (JL: should be /haipipe-paper create, not a sub-skill invocation): routes to haipipe-paper-lifecycle folder; repo-backed inside Project-* repos per project/haipipe-project/fn/repo-project.md papers-inside recipe; --org resolved per invocation (paper owner may differ from project owner). Retired prospectus verb/aliases removed (seed replaced it); haipipe-paper-bootstrap specialist entry replaced by haipipe-paper-folder; paper-folder contract tree fixed to current spine (1-claims, 2-pitch, 5-section-edit, .md early stages).

## [2.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; phase workers probe/ and revise/).

## [2.0.0] — 2026-06-22

- cross-cutting protocol wiring. All stage skills now reference ../wiki/08-stage-gate.md (confirm-before-advance), ../wiki/09-stage-illuminate.md (Socratic taste elicitation), ../wiki/13-tex-quality.md (self-contained compilable tex), ../wiki/12-evidence-routing.md (\needprobe macro + probe handoff). Stage strip end-of-reply convention enforced. Enter dashboard restructured (pitch summary first). 22 feedback items addressed.

## [1.5.0] — 2026-06-22

- probe buffer (1-probe-plans/). Claim-related evidence needs accumulate as probe plans during lifecycle work, then batch-dispatch to /haipipe-probe. Probe is the universal evidence gateway for claims; it calls task/discover during Gather. Direct task/discover verbs kept for non-claim utility work. See fn/probe-plans.md.

## [1.4.0] — 2026-06-22

- added probe/discover/task verbs as evidence-worker dispatchers. Paper orchestrator can now route directly to /haipipe-probe, /haipipe-discovery, /haipipe-task with project context resolved from the paper path. Paper stays story layer; evidence workers do the work.

## [1.3.0] — 2026-06-21

- renamed paper working-memory layer from feedback to rounds; added lifecycle, rounds, and skill-structure references.

## [1.2.0] — 2026-06-21

- made paper lifecycle the delivery-side owner of story/claims and routed GAP/NEED items through the shared delivery-need interface.

## [1.1.0] — 2026-06-21

- added enter/status paper-session loader routing.

## [1.0.0] — 2026-05-31

- baseline metadata added.
