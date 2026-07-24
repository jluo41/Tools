# How to design the haipipe-board folder structure?
state: ✅ SETTLED
owner: CC
method: 一题一个 md（照 1-probes/ 的做法），靠路径挂，不靠登记
session: c8603c47-0cd5-4a52-b708-37c617e82dd8
## Question
一块板就是一个文件夹。那这个文件夹里到底必须有哪些文件？更要紧的是：一个 Q 文件凭什么算「属于」这块板 —— 靠有人把它登记进名单，还是靠它躺在哪儿？

- 为什么难
  两种挂法差别很大：靠登记，漏登记就等于丢题；靠路径，丢个文件进去就自动算数，但顺序和分组又没人管了。
- 不定会怎样
  形状不定死，SKILL.md 就没东西可写，生成器也不知道该读什么 —— 后面每一题都悬着。
- 定了会影响什么
  直接决定 RA 能不能一个人认领一题去改而不跟别人撞车（一题一文件 vs 全塞进一个 board.md）。

## Boundary
- ✅ 这题管
  **文件夹里有什么、Q 怎么挂上来**：必须有哪些文件、路径认人还是名单认人、漏登记怎么办。
- ❌ 这题不管
  一个 Q 文件**内部**长什么样 —— 那是 `QA2`（模板）。也不管这个文件夹**放在仓库哪儿、叫什么名字** —— 那是 `QC1`。

## Diagram
```
NN-主题-YYMMDD/
├── board.md        全局：标题 · 主干 · 关板 · 主题 · 流水线 · 清单
├── QA1-xxx.md  ┐
├── QA2-xxx.md  ├─ 一题一个文件
├── QB1-xxx.md  ┘
├── board.html      ← build.py 生成，纯静态
└── fig/

谁在这块板上  →  靠路径：同目录所有 Q*.md，丢一个文件进来就算
什么顺序分组  →  靠 board.md 的 ## 清单：只写文件名，不抄标题
漏登记        →  照样显示（归 ⚠️ 组）+ 命令行提醒一句
```

## Items to Finish
- [x] 列出文件夹里必须有哪几个文件，每个一行说明管什么
      board.md · Q*.md · board.html · fig/ —— 写进了 SKILL.md 的「形状」节和 `ref/board-form.md`。
- [x] 写清 Q 文件怎么挂到板上（路径认人 + 清单排序，两层）
      同目录所有 Q*.md 就是这块板的题；`## Roster` 只管排序分组；漏登记归 ⚠️ 组不丢题。都成文了。
- [x] 照着这份清单能徒手搭出一块空板，不用翻现成的例子
      `ref/board-example.md` 就是一块两题的最小骨架；实测：subjective-label 那两块 + 这块，共 3 块板在用这个形状。
（一个 Q 文件内部长什么样，是 QA2 的事，这里不管。）

## Where we are
**形状已定死、写进 SKILL.md 和 `ref/board-form.md`，3 块板（这块 + subjective-label 两块）都照它建。**
文件夹里有什么，看上面 `## Diagram` 那张图；这里只记怎么挂、还差什么。

- 谁在这块板上 —— 靠路径
  同一个文件夹里所有 `Q*.md` 就是这块板的题。新开一题＝丢一个文件进去，不改别的。
- 什么顺序、怎么分组 —— 靠 `board.md` 的 `## Roster`
  只写文件名和分组标题，标题正文一概不抄。
- 漏登记只会丑，不会丢题（两种翻车都测过）
  清单漏写一个文件 → 那题照样出现在页面上，归 ⚠️ 组 + 命令行提醒一句；清单写了不存在的文件 → 也只是提醒。
- 还没定死的两条小事，边用边定
  `fig/` 是不是每块板都必须建（现在是空的）；文件名后半截用中文还是英文。

## Files
- `build.py`
  `parse_dir` 决定「同目录所有 `Q*.md` 就是这块板的题」，以及漏登记归 ⚠️ 组。
- `ref/board-form.md`
  §1 文件夹 · §2 编号 —— 这题的完整规格在那儿。
- `SKILL.md`
  「🗂 形状」那一节。

## Glossary
一题一个文件：借 haipipe-probe 的做法 —— `1-probes/` 下面每个问题是一个单独的 md 文件。好处是两个人同时改两个问题不会撞车。

## Discussion

## Comments
- [x] XZ 「挂接方式分两层，已经跑通并测过两种翻车」 · 260723 2023
      this Now section. is not easier to read.
      >> CC0723: `## Now` 重写成「小标题 + 缩进解释」的要点式（QA4 定的形式）；删掉了跟 `## Diagram` 重复的那份文件夹图和散句长段。
- [x] JL 「📍 Now」 · 260723 1240
      I want to make each section name to be more salient, and also make it can be callapsed.
      >> CC0723: QA4 在这条之后（260723 1400–1720）已做进 build.py：节标题 18px + 底下一条线 + 右边 expand all；item 解释收进 `<details>` 默认折叠、点名字才展开。QA1 这次把 Now 改成要点式，折叠才真正生效。
- [x] JL 「260722」 · 260723 1240
      also add the time as well.
      >> CC0723: `## Log` 已全部带 HHMM（260723 0919 起的格式）。原句已改，所以这条显示 anchor lost。
- [x] JL 「260722 开题。原题「文件夹里有哪些文件 + 文件里有哪些段落」两件事混在一起 260722 拆题：段落归 QA2，这题只管文件夹 260722 挂接方式定成两层（路径认人 / 清单排序），两种漏登记都测过 260722 编号 Q1 → QA1；标题 28 字压到 9 字 260722 完成线改成勾选清单；补 ## 图」 · 260723 1240
      For here, also add the time, not only the date. 
      
      and the newest things to the top.
      >> CC0723: 两条都已生效：Log 每行 `YYMMDD HHMM ·`，最新在最上面。
- [x] JL 「📜 Log (5) 260722 开题。原题「文件夹里有哪些文件 + 文件里有哪些段落」两件事混在一起 260722 拆题：段落归 QA2，这题只管文件夹 260722 挂接方式定成两层（路径认人 / 清单排序），两种漏登记都测过 260722 编号 Q1 → QA1；标题 28 字压到 9 字 260722 完成线改成勾选清单；补 ## 图」 · 260723 1240
      for the logs, I want it to add the date and time as well.
      >> CC0723: 同上，已生效。
- [x] JL 「QA1」 · 260723 1240
      I want all the section name to be more salient.
      >> CC0723: 同「📍 Now」那条 —— QA4 的节标题放大 + 下划线已覆盖所有 Q 的所有节。
- [x] JL 「Board folder shape」 · 260723 1240
      maybe make it a bit longer, make it more like a question, like
      
      How to design the haipipe-board folder structure.
      >> CC0723: 标题已改成 `How to design the haipipe-board folder structure?`，用的就是这条里的原话。

## Log
260723 · 按新结构重写：Question 展开成「一段话 + 要点」，补 `## Boundary`（跟 QA2 / QC1 划清）和 `## Files`；退役的 `## Why here` 并进 Question
260723 2036 · 清掉全部 7 条评论：标题改成问句（JL 原话）；`## Now` 重写成要点式、删掉跟 Diagram 重复的图（XZ）；「节标题醒目 + 可折叠」两条由 QA4 已落地的版式覆盖；「Log 带时间 + 最新在上」三条早已生效，补勾
260723 1710 · 全局回顾时补勾：形状早定死并写进 SKILL.md/board-form.md，3 块板在用 → ✅ SETTLED
260723 0919 · 段落名改英文（## Now / ## Done when / ## Why here …）
260722 2320 · 完成线改成勾选清单，补 ## Diagram
260722 2310 · 编号 Q1 → QA1；标题从 28 字压到 9 字
260722 2255 · 挂接定成两层（路径认人 / Roster 排序），两种漏登记都测过
260722 2250 · 拆题：段落归 QA2，这题只管文件夹
260722 1706 · 开题。原题「文件夹里有哪些文件 + 文件里有哪些段落」两件事混在一起
