# 260719 · DRAFT│PROBE 边界重构

三个 `probe-*` lane skill 不是放错了一层,是**每一条都横跨三个相位**。连带清出:sidecar 退役没传导、harvest 落点今天就断着、`mode` 是个活过了结果句的条件句、concern 无家可归。

起点:JL —— 「我觉得这个是不是说,我们应该把 probe citation 这些东西放到 draft citation 呢?……是不是我们都把它们变成 draft 的一种,然后 probe 就是纯粹的 probe?」

诊断来源:5 个 fresh-context 审计员并行跑 `paper/2-phase/` → 118 findings,trust gate 抽查 22 条全部落盘对上。




========================

## 🎯 现在在哪

```
  ✅ 已做   Batch 1  hub 核心           haipipe-paper-probe 5.3.1 → 6.0.0
  ✅ 已做   Batch 2  0-draft 三条 lane   3 个新 skill,已注册可调用
  ✅ 已做   Batch 3  revise-place        haipipe-paper-revise 1.5.1 → 1.6.0
  ✅ 已做   Batch 6  checker             PASS 2 复活 · PASS 4 新建 · concern carve-out
  ✅ 已做   Batch 7a 1-lifecycle 清扫    19 文件 · 6 个 skill bump
  ✅ 已做   Batch 7b 2-phase 文档层 + 路由 + 0-enter   1-probe/README.md 整体重写
  ✅ 已做   Batch 4  check-evidence      haipipe-paper-check-evidence 1.0.0
  ✅ 已做   Batch 5  删旧 lane skill       + 11 处失效引用全部改指
  ✅ 已做   Batch 8  RESOLVE             26 个 skill 的 version ↔ CHANGELOG 对齐

  ⚖️ 12 条裁决全部执行完毕。重构闭环。

  ⏳ 还等你的两件(都不属于本次重构):
       mode 三选一           → ✅ closed/260719-03-MODE-RETIREMENT.md §4 (裁决 A,已执行)
       PREFERENCES.md:11    → 是你的标准偏好,编码了已退役模型,要你亲手改
```


## 🔀 一句话说清这次改了什么

```
  BEFORE                                AFTER
  ═══════════════════════════════════════════════════════════
  0-draft/                              0-draft/          ◀ 提需求 + 挂主
    haipipe-paper-draft                   haipipe-paper-draft
                                          ├ -draft-citation  ✨
                                          ├ -draft-values    ✨
                                          └ -draft-display   ✨
  1-probe/                              1-probe/          ◀ 纯 ③④⑤
    haipipe-paper-probe                   haipipe-paper-probe
    ├ probe-citation   ✂️                   └ 吃进三块 ⑤ 残留 ~97 行
    ├ probe-values     ✂️
    └ probe-display    ✂️
  2-revise/                             2-revise/         ◀ 填洞
    revise + 3 workers                    + revise-place ✨(跑最前)
  3-check/                              3-check/          ◀ 投稿前走查
    check + proof-checker                 + check-evidence ✨(条件派发)
```

审计发现的关键事实:**三条 lane 的五个编号相位里,没有一个是 PROBE 的活**。但它们各自藏着真的 ⑤,藏的位置还都不一样 ——

```
  citation  ## Harvest mode  :109-175   第六节,压根不在五相编号里
                                        自称 "Called by haipipe-paper-probe at ⑤ INTERPRET"
  values    Phase3 前置块     :111-127   QA state 门禁(working→REFUSE)
  display   Phase3 LINK 正文  :119-125   六步全写 tex link,一步不碰 registry
```

所以 `1-probe/` 不会被清空,而是**收回**这三块。


## ⚖️ 裁决账本(append-only · 你的原话逐字保留)

```
D1 · harvest 写去哪
> JL: do A.
     >> CC0719: ✅ 已做。`### a-executor` 定为唯一落点。
                这条【今天就已经断着】,与重构无关:per-stage-dispatch.md:34 说落 a-executor,
                SKILL.md:116 和 harvest-acceptance.md:60,91 却还写 _CITATION_{stage}.md。
                可观测后果:每个 stage 的 cite/val/disp 状态条【永久红】,
                因为判据文件永远不可能存在了。

D2 · 幽灵执法者(我自己写的)
> JL: A
     >> CC0719: ✅ 已做(Batch 6)。我早上写的 "enforced by check-probe-cards.sh PASS 2"
                是假的 —— PASS 2 那时什么都不检查。现在它真的检查了:
                0-lifecycle/ 下出现任何 _CITATION_*/_VALUES_*/_DISPLAY_* 即 FAIL。
                ⚠️ 上线即抓到 11 个存量 sidecar,见下面「立刻要处理的」。

D3 · 三块 ⑤ 残留归谁
> JL: A.
     >> CC0719: ✅ 已做,但**我原方案错了一处**:values 那 17 行 state 门禁【不该搬】。
                它守的是 lane skill 那个公开直呼入口,skill 一删入口就没了;
                而 hub 的 ④ POINT 本来就会打开 target 读 state。搬过去纯属重复。
                实际折叠 ~97 行,不是我估的 114。

D4 · harvest lane 存废
> JL: A. the principle is everything now in the Quetions of 1-probes and the stages's Q-consumer.
     >> CC0719: ✅ 已做。ref/harvest-acceptance.md 删除。
                这机制的第一条指令就是自伤:它要你先写 `harvest: OWED`,
                而 checker 规则 7 对 OWED 直接 FAIL,唯一合法出口是写一个已退役的 sidecar。
                我今天亲自踩了这个坑(PP01 被我写红了),所以这条是实证不是推理。
                ✅ 救出:harvest-acceptance.md:30-32 的防造假 grep
                   `grep -F '<value>' <source>`,没命中就 REJECT
                   —— 全 bucket 唯一一颗防造假的牙,差点跟着 cleanup 一起没。

D5 · mode
> JL: Do we still need this? Leave it. Maybe we don't need this mode.
> JL: for this one, maybe open a new review file to discuss about it only
     >> CC0719: ✅ 已单独立案 → `closed/260719-03-MODE-RETIREMENT.md`(裁决 A 退役,已执行完毕)。本文件不再讨论。

D6 · cite/val/disp 状态条
> JL: Delete.
     >> CC0719: ✅ 已做。整块换成四态 `probe ⬜/🚀/✅/--`,从 checker 推导,
                不从存值也不靠肉眼。

D7 · PLACE 去 REVISE
> JL: Follow your recommendation.
     >> CC0719: ✅ 已做。新 worker `haipipe-paper-revise-place`,顺序 place → content
                → humanizer → results,**顺序是硬的**:先跑文风再替换,等于把 key 和数字
                塞进 humanizer 刚封好的句子里,最终出版那个句子从没被审过。
                你 07-10 其实已经裁过一半(revise/CHANGELOG [1.5.1]),只是没进 SKILL 正文。

D8 · DRAFT 提位置的模型
> JL: ok. The whole idea now is in the draft, we propose where to put the value, and
      references and display, and the Q-consumers are linked to them. And then will fill them.
     >> CC0719: ✅ 已建成 = 那三个新 lane skill。DRAFT 提位置 → PROBE 填 → REVISE 放。

D9 · 占位符所有权不变式
> JL: ok, follow you recommendation.
     >> CC0719: ✅ 已做(Batch 6)。新 PASS 4。它关掉的缺口:
                {VAL:?} 此前【没有任何机制】管(checks.sh 和 check-probe-cards.sh 都不查),
                而唯一被查的 % TODO 早已被 check/CHANGELOG 1.8.1 退役 ——
                checker 在守一个死标记,放着两个活的不管。

D10 · concern 机制
> JL: I agree.
     >> CC0719: ✅ 已做(Batch 6)。{CONCERN:<risk>} [Q-<Stage>-<n>] + 1-probes/ 里
                route: none · state: concern。每闸 ⚠️ 报一次不算 FAIL;
                终闸(--final)必须有 `discussed:` 指向承载它的 limitation 句,否则 FAIL。

D11 · check 归谁
> JL: I think check should be in executor side.
     >> CC0719: ⛔ **我不敢猜,两种读法差太远** ——
                (A) 窄:那个 checks.sh 调用归 CHECK 相 → 照原计划建 check-evidence
                (B) 宽:核验本身归 executor 侧,paper 不再复验墙那边送来的东西
                       → check-evidence 根本不该存在;QA 文件到手时就该自带核验,
                         CHECK 只确认它这么说了。这会重开 D8,并改动 bank 的 qa 门契约。
                我倾向 (A),因为 (B) 改的是 executor 契约,超出本 bucket。
     >> CC0719: ✅ 你裁了 (A)。haipipe-paper-check-evidence 1.0.0 建成:
                三轴(存在性 / 元数据 / 上下文)· 每个数字重新推导 · 报告-only,
                像 proof-checker 那样【条件派发】(仅投稿前),不是每个 section 闸都跑 ——
                每个闸解析全部 DOI 是跑不起的,而跑不起的 pass 等于从不跑。

D12 · principle 5a
> JL: Yes.
     >> CC0719: ✅ 已做(Batch 7a)。改写为 **RAISE freely; DISPATCH narrowly**。
                原文 "DO NOT open a seed probe for it" 字面上禁的是【提问】,
                于是 agent 会压掉真问题,那句 prose 永远没有 anchor。
                成本其实在 dispatch,不在 Q-consumer 里多一行。
```


## 🧾 清账表(每有进展就在这里划掉)

```
  编号  项目                        规模      状态
  ────────────────────────────────────────────────────────────────────────
  ①    存量 sidecar                11 → 0    ✅ 已归档 _archive/260719-sidecars/
  ⑤    WIRING.md 的 lane 映射       1 → 0     ✅ Batch 5 顺手修
  ⑧    serves: 仍被指令写           4 → 0     ✅ 新发现,已修(venue/pitch/narrative/lifecycle)
                                              和 ③ 同一条 checker 规则 FAIL
  ─── 以上已清 ───────────────────────────────────────────────────────────
  ③    a-consumer: 词汇漂移        19 → 0    ✅ 全仓退役字段形式归零
                                              保留 25+ 处【活概念】(stage doc 的 station ②)
                                              📜 probe/{HANDOFF,MERGE-HANDOFF}.md 零改动,已核
  ⑥    "constitution" 绰号          29 → 0    ✅ 全仓清零(含 4 处两个 agent 范围外的漏网)
                                              1 处保留:0_utils/haipipe-session:149 的
                                              「04 CONSTITUTION」是笔记骨架的槽位名,
                                              不是指 probe —— 换掉它得连带重命名骨架文件
  ②    无主占位符(论文侧)          19        ⬜ 待你指定先做哪一节
                                              4-llmtrait 3 · 5-empirical 4
                                              6-results 10(全是数字,最硬)· 7-discussion 2
  ④    PREFERENCES.md:11            1         ⬜ 你的标准偏好,要你亲手改
  ⑨    ## Verdict / verdicted 禁令表  13       🟡 paper 侧 6 处已抹(SKILL:371 · probes:106,108
                                                 · claims:27 · lifecycle:183-184 · per-stage:36,76)
                                              application 侧 agent 扫描中
                                              保留判断:migration 对照表 + SUPERSEDED 横幅【不算墓碑】
                                                 前者是可执行指令,后者是 owner 裁决的记录
  ⑩    "section" → "entry" 漂移      18+      ⬜ probe 文件里是 ENTRY 不是 SECTION
                                              paper 3:03-paper-lifecycle:89,96 · 04-lifecycle-map:37
                                              application 15:SKILL.md:3,9,48,349 · 1c-claims:9
                                              · 5-section-edit:9 · 1b-themes:53 · venue:68
                                              · PHILOSOPHY:41,108 · README:193 · EVALUATION:35 · USAGE:26
                                              ⚠️ 其中 4 处在 summary:/description: 上 —— 必须用
                                                 文件级过滤 grep -v '/CHANGELOG\.md:' 才看得见
  ⑦    mode                        35        ✅ 已退役 closed/260719-03-MODE-RETIREMENT.md §6
  ────────────────────────────────────────────────────────────────────────
  已清 5 / 10     目标:全部 ✅ 本文件才算 clean
```

⚠️ **我给 agent 的验证命令自己有洞** —— agent 发现并修正了:
```
  我写的  grep -v CHANGELOG          过滤【行】。而每个 skill 的 frontmatter
                                      summary: 都以 "History: ./CHANGELOG.md." 结尾
                                      → 整行被吃掉,藏住了真幸存者
                                      (haipipe-paper-claims/SKILL.md:9)
  正确的  grep -v '/CHANGELOG\.md:'   过滤【文件】
```
和今早 `_CITATION_0-seed` 那次同源:**过滤条件写窄了,然后信了自己的零结果**。

## 📝 顺带记下的两条方法论

```
  「无墓碑」  JL:「不需要留退役告示,直接抹除任何痕迹」/「follow this rule to do all
              the following changes」
              → skill 文档只写【当前契约】。历史归 CHANGELOG,强制归 checker。
                这条【压过】"留个禁令免得下个 agent 又造出来"的本能。
              → 已写进 haipipe-paper/PREFERENCES.md(可移植,换机器不丢)

  「扫概念,不扫文件名」  我今早翻过一次车:grep 的是 `_CITATION_0-seed`,
              而真正执行 DRAFT 的那个文件写的是泛称 `_CITATION_`,于是漏了,
              还在 CHANGELOG 里写下"live references are now zero" —— 假的。
              是同日的 fresh-context 验证 agent 抓出来的。
              → 教训已记进 haipipe-paper-seed/CHANGELOG 4.4.0 的 ROUND 2 段。
```


