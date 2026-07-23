# Fresh-agent acceptance test
state: 🔴 OPEN
owner: CC
method: 开一个没有这次对话记忆的 agent，只给它 SKILL.md

## Question
怎么证明这个 skill 是能用的，而不是只有写它的人才会用？

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

## Done when
- [ ] 开一个没有这次对话记忆的 agent，只给它 SKILL.md 和一个真实话题
- [ ] 它自己开出一块板
- [ ] 比对它走的步骤和设计的是否一致
- [ ] 不一致就改 SKILL.md，再来一遍

## Why here
仓库的 CLAUDE.md 里写死了这条规矩：任何 skill 改完，必须用一个全新 agent 验过才算完。
在这次对话里自测没有用 —— 我脑子里有一大堆没写进 SKILL.md 的东西，测不出缺什么。
还要验第二件事：一个完全不懂这个话题的人打开 `board.html`，看不看得懂。上一块板试过一次，反馈是「像在解释一个菜谱的格式，却从头到尾没说这道菜是什么」。这条要变成 SKILL.md 里的硬要求。

## Now
一次都没跑过。

## Glossary
全新 agent：另开一个 Claude，它看不见这次对话，只能看见你给它的那几个文件。

## Discussion

## Log
260722 · 开题，依据是仓库 CLAUDE.md 里「skill 改完必须用全新 agent 验过」
260722 · 编号 Q5 → QB2
260722 · 可读性验收这一条挪给 QA5，这题只留「照着 SKILL.md 能不能开出板」
