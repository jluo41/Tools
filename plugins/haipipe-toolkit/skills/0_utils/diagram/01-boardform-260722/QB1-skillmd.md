# What SKILL.md must say
state: 🔴 OPEN
owner: CC
method: 三件事说清楚：怎么开板、怎么加题、什么时候关板

## Question
别人（或者以后没有这次对话记忆的我）敲下 `/haipipe-board`，要照着做什么？

## Diagram
```
用户敲  /haipipe-board
          │
          ▼
      SKILL.md  ──►  必须答清楚三件事
          ├─ ① 怎么开一块新板   建文件夹 → board.md → 第一个 Q
          ├─ ② 怎么加一个 Q     抄 ref/ 模板 → 改文件名 → 进清单
          └─ ③ 什么时候关板     每个 Q 到 ✅ 或 ⏸️

现在：文件夹在，build.py 在，ref/ 在 —— SKILL.md 一个字没写
```

## Done when
- [ ] `SKILL.md` 写完
- [ ] 里面答清楚：怎么开一块新板
- [ ] 里面答清楚：怎么往板上加一个 Q
- [ ] 里面答清楚：这块板什么时候该关掉

## Why here
现在这套流程只活在这次对话里。换个 agent 进来，看到的只有一个 `build.py` 和两块试验板，它猜不出该怎么走。
skill 的全部价值就是把流程写下来 —— 不写，这次做的东西下次就没了。

## Now
文件夹 `skills/0_utils/haipipe-board/` 已经建好。
里面只有 `build.py` 和 `ref/board-example.md`。
`SKILL.md` 一个字都还没写。

## Glossary
SKILL.md：Claude Code 里一个 skill 的入口文件。用户敲 `/haipipe-board` 的时候，被读进去的就是它。

## Discussion

## Log
260722 · 开题
260722 · 编号 Q4 → QB1；标题压到 12 字
260722 · 完成线改成勾选清单（三件事各一条）
260722 · 技能文件夹从 skills/board/ 搬到 skills/0_utils/haipipe-board/
