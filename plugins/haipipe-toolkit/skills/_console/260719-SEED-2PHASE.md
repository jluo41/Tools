# 260719 · seed + paper/2-phase · 契约自相矛盾

**问题不是词汇漂移,是文档之间(以及文档自己内部)对相位契约的说法互相打架。**

③⑧⑨⑩ 那一串扫的是【同一个概念的不同措辞】。这份板子记的是【同一个概念的不同**规则**】——
两份文件对同一件事给出相反的指令,agent 读哪一行就照哪一行做。扫词汇治不了这个。

来源:2 个 fresh-context 审计员,分别读 seed 四件套 和 paper/2-phase 全部 in-scope 文件。

---

## 🔴 P0 · 同一份文件里写着两种契约(最毒:无法靠"读仔细点"避开)

```
  paper/2-phase/README.md:6    DRAFT 🤖              (纯 agent)
  paper/2-phase/README.md:54   DRAFT 🤖→🧑 ⛔HARD STOP  (硬人闸)
  ────────────────────────────────────────────────────────────────
  paper/2-phase/USAGE.md:3     "…then stops at CHECK for you"   → 一个闸
  paper/2-phase/USAGE.md:21    "Two human gates: structure      → 两个闸
                                review after DRAFT, quality
                                review at CHECK"
  ────────────────────────────────────────────────────────────────
  3-check/haipipe-paper-check/SKILL.md:3    DRAFT structure review 是第二个闸
  3-check/haipipe-paper-check/SKILL.md:9    CHECK 是 "the ONLY human-involved phase"
  3-check/haipipe-paper-check/SKILL.md:18   "DRAFT, PROBE, REVISE run fully automatic"
  ────────────────────────────────────────────────────────────────
  1-probe/haipipe-paper-probe/SKILL.md:65   ENTRY 建在 "GATE-1-approved Q<n>" 之上,
                                            但同段又说 DRAFT 先开 ENTRY、人再在 GATE 1 批。
                                            批准发生在开条目之后 —— 因果倒置。
                                            同样的倒序复制在 0-draft/…/SKILL.md:36
                                            和 1-probe/…/ref/per-stage-dispatch.md:82
```

> ⚠️ `paper-check:18` 这条,application/HANDOFF.md:62 早在 07-17 就作为 "paper F2" 记过,一直没修。

## 🟠 P1 · 跨文件矛盾(相位边界)

```
  ②MATCH 到底在哪个相位
    WIRING.md:41             PROBE 跑五步 ORGANIZE→MATCH→…      ❌
    1-probe/README.md:9-13   ①② 在 DRAFT                        ✅
    1-probe/…/SKILL.md:16,50-51 · 0-draft/…/SKILL.md:163  同 ✅

  citation / values / display 三条 lane 归谁
    WIRING.md:42             PROBE 扇出                          ❌
    WIRING.md:23(同一文件)  DRAFT Step 4a                       ✅
    0-draft/…/SKILL.md:145-153, :300  "not PROBE tracks"        ✅

  DISPATCH 走哪扇门
    WIRING.md:42-44   直呼 task/discovery orchestrator          ❌ 违反 LAW 1
    1-probe/…/SKILL.md:35,85,89  必须过 q-executor-agent,
                                 worker transcript 里不许出现 orchestrator  ✅

  revise 的 -place
    WIRING.md:45 漏了 -place;humanizer/SKILL.md:111-118 也漏,还称顺序 "Typical"
    2-revise/haipipe-paper-revise/SKILL.md:86-87  place 跑第一,顺序是硬的   ✅
```

## 🟡 P2 · seed(两个 family 各说各话)

```
  Q-consumer 三字段名          application  Ask / Why / Answer
                               paper        Description / Reason / Answer
  template 是不是规则唯一家    paper  是(内联 <!-- RULE -->)
                               application  否(规则搬进 SKILL)
  PROBE 怎么调                 paper  Skill("haipipe-paper-probe", from-buffer …)
                               application  只说 "one worker call",还写成
                                            Agent(haipipe-probe-q-executor-agent)
                                            ← 那是 worker 内部,不是 stage 的调用

  application seed 把 ②MATCH / target: 都算给 PROBE 相(SKILL.md:42,44,55,61)
     ← 和 probe/haipipe-probe/SKILL.md:89「DRAFT now writes target」直接冲突

  🐛 模板缺字段:application/…/ref/seed-template.md:46-54 的 Q-Seed 块【没有 Answer: 行】,
     而 SKILL.md:79,85 的 Done 闸要查 Answer 的 __TO_BE_FILLED__ 状态
     → 照模板生成的 seed 永远过不了自己的闸

  两个 template 都缺 probe 要求的 `→ 1-probes/PPnn · QX<n>` 指针(probe SKILL:89)

  seed 自相矛盾:paper seed:228「两个问题是常态,提八个说明没想清楚」
                vs 同文件 :184/:187 原则 5/5a「RAISE freely,数量不设限」
                ← 5a 是 D12 刚裁过的,:228 是漏网的旧句
```

## 🪦 墓碑 + 版本号(低危,顺手清)

```
  墓碑    WIRING.md:28 · 0-draft:315,:253,:211 · revise-content:3,9,54(同一句说三遍)
          per-stage-dispatch:35,36,75-76,117 · proof-checker:27,303,361
          paper-seed:35,171,205-206 · app-seed:34,38,63

  版本号  humanizer  last_updated 07-07,正文还是三 worker、无 -place
          results    last_updated 07-08,无 -place,且 :25 把 REVISE 的改写踢回 DRAFT
          proof-checker 1.1.2 / 07-07,summary 只描述独立跑法
          paper-probe 6.0.1 ← 相位切分是破坏性契约变更,不该是 patch 号

  路径错  USAGE.md:6  examples/ProjB-PhyTrait-OpioidRx/paper/…  盘上不存在
                      实际是 examples/Project-Personality-OpioidRx/papers/…
```

## 🧾 清账表(**闭集**:全部来自这一次审计,不再新增编号)

```
  编号  项目                                    规模   状态
  ──────────────────────────────────────────────────────────
  P0-1  README.md 自相矛盾 DRAFT 闸              2 行   ⬜
  P0-2  USAGE.md 自相矛盾 闸数                   2 行   ⬜
  P0-3  paper-check 三处互斥(:3/:9/:18)         3 行   ⬜  ← 07-17 就记过
  P0-4  GATE-1 因果倒置                          3 处   ⬜
  P1-1  WIRING.md 四条(MATCH/lane/dispatch/place) 4 行  ⬜
  P2-1  seed 两 family 四处分歧                  4 组   ⬜  需你裁哪边对
  P2-2  app seed-template 缺 Answer: 行          1 处   ⬜  🐛 真 bug
  P2-3  两个 seed-template 缺 → 1-probes 指针     2 处   ⬜
  P2-4  paper-seed:228 vs 原则 5a                1 行   ⬜  D12 漏网
  T-1   墓碑                                     ~20 处 ⬜
  V-1   版本号/路径                              5 处   ⬜
  ──────────────────────────────────────────────────────────
  0 / 11        全 ✅ 本文件才算 clean
```

## 📝 为什么这份板子不会变成跑步机

```
  旧账本  ③→⑧→⑨→⑩   每扫一轮生出新编号,分母跟着分子涨
          原因:~14 份文件各自【复述】probe 解剖,grep 只抓得到猜到的措辞

  这份    编号来自【一次全量审计】,不是一次 grep。清完就是清完。
          要让它永久不复发,还得做上一轮提的那件事:
          删掉复述 → 每个 skill 只留一行指针 → probe/haipipe-probe/SKILL.md:23
          的 "COPY … then propagate" 改成 "POINT here"
```
