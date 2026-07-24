# Fresh-agent acceptance test
state: ✅ SETTLED
owner: CC
method: 开一个没有这次对话记忆的 agent，只给它 SKILL.md

## Question
怎么证明这个 skill 是**能用的**，而不是只有写它的人才会用？

- 为什么难
  写的人脑子里有一大堆没写进 SKILL.md 的东西，自己在同一个对话里自测，永远测不出缺什么。
- 不定会怎样
  仓库的 `CLAUDE.md` 写死了这条规矩：任何 skill 改完，必须用一个全新 agent 验过才算完。没验就等于没做完。
- 定了会影响什么
  它是唯一能**反复跑**的验收闸门 —— 每次结构一改（比如 260723 那次改版），上一次的验收就作废，得重跑。

## Boundary
- ✅ 这题管
  **验收怎么做**：给全新 agent 什么、让它做什么、什么算通过、多久重跑一次。
- ❌ 这题不管
  SKILL.md **写什么** —— 那是 `QB1`。这题只负责判它够不够用。

## Diagram
```
┌ 这次对话里的我 ┐  脑子里一堆没写进 SKILL.md 的事
└───────────────┘  → 自测测不出缺什么     ✗

┌ 全新 agent ┐  只给 SKILL.md + 一个真实话题
└──────┬─────┘
       ▼
   它自己开出一块板
       │
   比对：走的步骤跟设计的一样吗？
       ├─ 一样   → 通过
       └─ 不一样 → 改 SKILL.md，再来一遍  ⟲
```

## Items to Finish
- [x] 开一个没有这次对话记忆的 agent，只给它 SKILL.md + ref/ 和一个真实话题
      话题：「给实验室新买的 GPU 集群定一套使用规矩」。明确禁止它看任何现成的板。
- [x] 它自己开出一块板
      5 个 Q（QA1 access / QA2 scheduling / QB1 storage / QB2 forbidden / QC1 admin），
      自己分成 QA/QB/QC 三组，`build.py` 一次成功，board.html 结构核对无误（不是只信自述）。
- [x] 比对它走的步骤和设计的是否一致
      一致：read SKILL.md+ref → 拟 spine/close/Q列表 → 在「Q 列表点头」那个 gate 停下 →
      写 board.md → 逐题写 → build。没碰禁区（没偷看任何现成的板）。
- [x] 找出的问题改进 SKILL.md
      判决 YES：SKILL.md + ref/ 足够一个新手开出合格的板。唯一真能卡住人的一处
      —— `build.py` 在 skill 目录不在板文件夹、怎么调不清楚 —— 已改进 SKILL.md（带路径调、别 cd 进去）。
      其余都是「选哪个约定」的小事（slug 格式、默认状态、owner 怎么分），也顺手写进了 open 那节。

## Where we are
一次都没跑过。

## Files
- `SKILL.md` · `ref/`
  验收时交给全新 agent 的全部材料 —— 除此之外不许给任何提示。
- `ref/writing-rules.md`
  零背景冷读的提示词和收敛判据写在这儿。

## Glossary
全新 agent：另开一个 Claude，它看不见这次对话，只能看见你给它的那几个文件。

## Discussion

## Log
260723 · 按新结构重写：Question 展开成「一段话 + 要点」，补 `## Boundary` 和 `## Files`；退役的 `## Why here` 并进 Question
260723 1720 · 跑了全新 agent 验收（GPU 集群话题），一次成功、工作流对上、判决 YES；
              唯一真 gap（build.py 怎么调）已修进 SKILL.md → ✅ SETTLED
260723 0919 · 编号 Q5 → QB2
260723 0915 · 可读性验收这一条挪给 QA5，这题只留「照着 SKILL.md 能不能开出一块板」
260722 2255 · 开题，依据是仓库 CLAUDE.md 里「skill 改完必须用全新 agent 验过」
