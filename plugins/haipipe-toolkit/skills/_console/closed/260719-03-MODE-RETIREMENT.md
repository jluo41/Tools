# 260719 · `mode: light | full` 还留着吗 — ✅ CLOSED

> ## ✅ FINISHED · 2026-07-19
> **裁决 A(退役)已执行完毕。`mode: light | full` 不再是 probe 文件的字段。**
> 35 处活站点清零,三个 bucket 全部落地,残留扫描(字段 / 同义表述 / 路标)均为 0。
> 本文件从此是**只读记录**,不再有待办。执行明细见 §6。
>
> 本次退役**没有写进任何 CHANGELOG**(JL 裁决:直接跳过)——
> 这意味着 **§6 是「mode 去哪了」的唯一书面答案**。清理 `_console/` 时请先归档,勿直接删。

从 `260719-02-PHASE-BOUNDARY-REFACTOR.md` 的 D5 拆出来,因为它横跨 paper / application / probe 三个 skill 家族,不该塞在一次重构里顺手裁掉。


> JL: 宪法 don't use this name, just use "probe". 

起点:JL —— 「Do we still need this? Leave it. Maybe we don't need this mode.」/「for this one, maybe open a new review file to discuss about it only」


## 🎯 现在在哪 — 全部完成

```
  ✅ 已做   证据收齐(5 条独立线索,逐条落盘核实)          §2
  ✅ 已裁   JL 选 A. 退役                                  §4
  ✅ 已执行 35 处清零,probe → paper → application 按序      §6
  ✅ 已复扫 二轮宽扫补齐 10 处漏网,残留 0                   §6

  ⬜ 未做   commit —— Tools 工作区含大量【非本次会话】的改动,
            提交时须按本次实际改动文件逐个 stage,勿 `git add -A`。
```


## §1 它本来该干什么

```
  mode: light                          mode: full
  ─────────────────                    ──────────────────
  "stops at Read and returns           "the paper needs a COMMITTED
   evidence to the caller"              claim status"
  用于上下文型问题:seed landscape      → AUTHOR 把 supported|refuted|
  venue capability、section-edit 查     inconclusive 写进 1b-claims.md
                                       → (历史上)派 reviewer agent 去判
```

probe 里它是**文件级**字段:

```markdown
# PP<NN> — <topic>
**mode**: light | full
```


## §2 五条证据说明它已经死了

```
 (A) 条件句活过了它的结果句
     CHANGELOG 4.0.0 记着 full 当年买到的东西:
       "mode: full now actually reaches a judgment: INTERPRET dispatches
        Agent(haipipe-probe-reviewer-agent) and lands its return in 1b-claims.md"
     这个 dispatch 在 5.x 里【不存在】。改写删掉了结果句,留下 if full 悬空。

 (B) 它守的规则现在无条件成立
     per-stage-dispatch.md:36 — "the ONLY home of a claim's status
        (there is no review gate; a probe is communication, not judgment)"
     所以"claim status 只能进 1b-claims.md"在【任何】mode 下都成立。
     写成 `mode: full → ...` 就暗示 light 模式下可以反着来。从来不可以。

 (C) 它从不随 dispatch 传出去 —— executor 根本读不到
     probe 的 dispatch payload  action · project · question · task-folder
     paper 的 collector prompt  project_root · probe_files · dispatch · route
     两边【都没有 mode】。而且 per-stage-dispatch.md:53-61 直接把深度交给 executor:
       "the EXECUTOR picks the shallowest depth in its own clean context …
        the worker never learns which, and never asks."

 (D) 唯一看着承重的那处,其实由别的东西扛着
     per-stage-dispatch.md:99 把 resource BUILD 绑到 mode: full。
     但 BUILD 实际由 `state: commissioned` + owner/eta/blocks/cross-project 扛,
     而那四个字段 check-probe-cards.sh:535-559 是【真的在查】的。mode 贡献为零。

 (E) checker 早就不检查它了
     check-probe-cards.sh 从不测 **mode**:。
     它在执法层已经退役,只在散文层还站着。
```

**唯一支持保留的论点**,以及它为什么不成立:

```
  per-stage-dispatch.md:46-47 说 light 还有个名义含义
    "a light probe stops at Read and returns evidence to the caller"
  但当前模型下【每个】entry 都终于 state: read —— 那就是 ⑤。
  所以 light 也是普适的。两个取值都普适的字段,区分不了任何东西。
```


## §3 要动的话,顺序不能反

```
  probe 2 处 —— 字段的【声明】
        probe/haipipe-probe/SKILL.md:140
        probe/haipipe-probe/ref/probe-template.md:43

  paper 20 处
  application 23 处
        含 haipipe-application/PREFERENCES.md:19 (RELEASE MENU 要列 mode)
        含 1c-claims/SKILL.md:33 ("supported 只能来自 full-mode 答案")

  ─────────────────────────────────────────────
  probe  →  paper  →  application
```

⚠️ **反过来做会先杀掉解释**:`probe-citation/SKILL.md:269` 是全树**唯一**解释 probe 那个字段含义的散文。先删下游,等于在解释被删之后才去动被解释的东西。


## §4 三选一

```
  A. 退役
     45 处、3 个 bucket、按序。每个 `mode: X → 规则` 变成 `规则`,
     因为它们现在全都无条件成立。没有任何东西会读丢。

  B. 留着,给它一份新工作
     需要先想清楚:reviewer-agent dispatch 没了、claim status 无条件了之后,
     它还该 gate 什么?如果想不出来,那本身就是答案。

  C. 留着,但明确降级为"给人看的注释"
     文档里写死:"这是给读者看的预期深度提示,没有任何程序读它,没有任何机制强制它。"
     诚实,但它长得像个可执行字段却不是 —— (A) 和 (B) 就是这么来的。
```

> {CC->JL}: A。五条证据全指同一个方向,而且具体损害已经看得见:paper hub 里有两条规则
> 被写成 `mode: full →`,于是暗示 light 模式下可以把 claim status 写进 probe 文件 ——
> 从来不允许。**死掉的条件句不会安静地待着,它会凭空发明权限。**
> 若走 A,我会按 bucket 各跑一轮 diagnose,probe 先行。
> JL: A. 退役
> >> CC0719: 裁决已收。执行顺序 probe → paper → application,见 §6。 A. 退役


## §5 披露:已经动了 2 处,以及为什么那不算动 mode

执行 `260719-02-PHASE-BOUNDARY-REFACTOR.md` 的裁决时,我在本文件存在之前改了 20 处 paper 站点中的 2 处 —— `haipipe-paper-probe/SKILL.md:38` 和 `:111`。

改它们**不是为了退役 mode**,是因为它们把一条无条件规则写成了条件句:

```
  before  `mode: full` → the claim STATUS goes in 1b-claims.md, NEVER in the probe file
  after   A claim's STATUS goes in 1b-claims.md, written by the AUTHOR, NEVER in the probe file
```

这个修法在 A 和 B 下都成立(规则本身普适),顺带少了 2 处 mode 引用。

*(写于裁决之前。当时其余站点一处未动;裁决 A 落地后已全部清零 —— 见 §6。)*


## §6 执行记录(A. 退役 · 2026-07-19)

按 probe → paper → application 顺序执行完毕,残留活站点 **0**。

```
  probe        2 处   声明行删除(SKILL.md · ref/probe-template.md)
  paper       12 处   fn/probes.md · 0-seed/SKILL.md · per-stage-dispatch.md ×9
                      1-probe/README.md
  application 20 处   fn/probes.md · PREFERENCES.md · 5 个 stage SKILL(含 venue)
                      1c-claims/SKILL.md ×2 · 0-draft/SKILL.md ×2
                      1-probe/SKILL.md ×4 · per-stage-dispatch.md ×9
  ─────────────────
  合计        34 处
```

⚠️ **第一轮只清掉 24 处,漏了 10 处** —— 第二轮宽扫才补齐。漏网原因(记下来防再犯):

```
  ① grep 用了大小写敏感的 `\bmode\b`  ─▶ 漏掉 "Mode FULL is the norm here"
  ② 只匹配 mode 紧邻 light/full 的写法 ─▶ 漏掉 "PROBE   light, and often skipped"
                                          (venue stage SKILL,与另外 4 个 stage 同构)
  ③ 完全没想到【路标】这一类      ─▶ 5 处 "which rung runs which mode"/"rung→mode map"
                                          仍在给一份已不存在的 mode map 打广告
```

**与 §3 的三点出入(执行时发现,已按实际处理):**

1. §3 说 45 处 —— 实际**活站点 24 处**。差额是 CHANGELOG 条目(probe 4 · 各 bucket 若干)和
   两份已标 SUPERSEDED 的 `SOP-*.md`。两类都是**历史记录,不改写**。
2. §3 的排序理由**已失效**:`probe-citation/SKILL.md:269` 不存在了 —— 该 skill 现名
   `paper/2-phase/0-draft/haipipe-paper-draft-citation/SKILL.md`,仅 118 行,全文不含 mode。
   「先删下游会杀掉唯一的解释」这个风险自己先消失了。排序仍按 probe 先行(声明先于用法)。
3. `light | medium | full` **不是这个字段** —— 那是 venue 的 `claims_settlement` 结算档
   (6 处,application/venue/_SCHEMA.md:47 等)。**全部保留未动**。

**三处判断题(超出「删词」的机械范围):**

```
  ① 两份 per-stage-dispatch.md 的 Dispatch rule 1 整条删除,rule 2 顺延为 1。
     理由:rule 1 通篇是 mode 规则;其非-mode 内容("claim status 进 1b/1c-claims.md")
     已在同文件的 claims 行陈述,深度归属已由 rule 2「the DEPTH is the EXECUTOR's」承担。
     留着会变成一条纯重复的规则。

  ② application/.../per-stage-dispatch.md:57 的 "light data probe" → "quick data probe"。
     这里的 light 是普通形容词、不在 §3 清单内,但它紧挨 probe,留着会让退役的取值
     以词汇形式复活 —— 正是 §4 {CC->JL} 说的「死掉的条件句会凭空发明权限」。

  ③ paper/1-lifecycle/ref/08-stage-gate.md:175 整行删除。
       删掉:④  probe light reuse (zero-write => zero ceremony);
       ④ 现在只剩:discovery ENRICH (no new folder, creator folded, one review pass)
     我原判断它属 cost ladder 而非 mode 字段,提请裁决;JL:「delete that」。
```

> {CC->JL}: 未动 CHANGELOG。三个 bucket 各自的版本号该怎么记、这次是否合成一条,
> 是你的决定,不是我该猜的。
> JL: delete them all. → 澄清后确认为:**不写 CHANGELOG,直接跳过**。
> >> CC0719: 三个 bucket 都不记版本号、不写条目。本次退役的唯一书面记录就是上面的 §6。
> >> 各 CHANGELOG 里既有的 mode 历史条目、两份 SOP-*.md、本 _console 文件,一律未删。
