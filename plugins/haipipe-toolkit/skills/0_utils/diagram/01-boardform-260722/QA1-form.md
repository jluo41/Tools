# Board folder shape
state: ✅ SETTLED
owner: CC
method: 一题一个 md（照 1-probes/ 的做法），靠路径挂，不靠登记

## Question
一块板是一个文件夹。这个文件夹里必须有哪些文件？一个 Q 文件是怎么「属于」这块板的？

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

## Done when
- [x] 列出文件夹里必须有哪几个文件，每个一行说明管什么
      board.md · Q*.md · board.html · fig/ —— 写进了 SKILL.md 的「形状」节和 `ref/board-form.md`。
- [x] 写清 Q 文件怎么挂到板上（路径认人 + 清单排序，两层）
      同目录所有 Q*.md 就是这块板的题；`## Roster` 只管排序分组；漏登记归 ⚠️ 组不丢题。都成文了。
- [x] 照着这份清单能徒手搭出一块空板，不用翻现成的例子
      `ref/board-example.md` 就是一块两题的最小骨架；实测：subjective-label 那两块 + 这块，共 3 块板在用这个形状。
（一个 Q 文件内部长什么样，是 QA2 的事，这里不管。）

**已经定死、在用了。** 形状写进了 SKILL.md 和 `ref/board-form.md`，
3 块板（这块 + subjective-label 两块）都照它建。
剩的只是两条无关紧要的小事，边用边定：`fig/` 是不是每块都必须建、文件名后半截中文还是英文。

## Why here
文件夹形状不定死，SKILL.md 就没东西可写，生成器也没法读。
而且「一题一个文件」还是「全部塞在一个 board.md 里」，直接决定 RA 能不能一个人认领一个 Q 去改，而不跟别人撞车。

## Now
已经跑通一版：

```
NN-主题-YYMMDD/
  board.md      全局：标题 · spine（主干） · close（关板条件） · ## 主题 · ## 流水线 · ## 清单
  QA1-xxx.md     一题一个
  QA2-xxx.md
  board.html    生成的，纯静态
  fig/          截图放这儿
```

挂接方式分两层，已经跑通并测过两种翻车：
① **谁在这块板上** —— 靠路径：同一个文件夹里所有 `Q*.md` 就是这块板的题。新开一题＝丢一个文件进去，不改别的。
② **什么顺序、怎么分组** —— 靠 `board.md` 的 `## Roster`：只写文件名和分组标题，标题正文一概不抄。
清单漏写一个文件，那题照样出现在页面上（归到 ⚠️ 组）+ 命令行提醒一句；清单写了不存在的文件，也只是提醒。**漏登记只会丑，不会丢题。**

还没定死的：`fig/` 是不是必须建（现在是空的）；文件名后半截用中文还是英文。

## Glossary
一题一个文件：借 haipipe-probe 的做法 —— `1-probes/` 下面每个问题是一个单独的 md 文件。好处是两个人同时改两个问题不会撞车。

## Discussion

## Comments
- [ ] JL 「📍 Now」 · 260723 1240
      I want to make each section name to be more salient, and also make it can be callapsed.
- [ ] JL 「260722」 · 260723 1240
      also add the time as well.
- [ ] JL 「260722 开题。原题「文件夹里有哪些文件 + 文件里有哪些段落」两件事混在一起 260722 拆题：段落归 QA2，这题只管文件夹 260722 挂接方式定成两层（路径认人 / 清单排序），两种漏登记都测过 260722 编号 Q1 → QA1；标题 28 字压到 9 字 260722 完成线改成勾选清单；补 ## 图」 · 260723 1240
      For here, also add the time, not only the date. 
      
      and the newest things to the top.
- [ ] JL 「📜 Log (5) 260722 开题。原题「文件夹里有哪些文件 + 文件里有哪些段落」两件事混在一起 260722 拆题：段落归 QA2，这题只管文件夹 260722 挂接方式定成两层（路径认人 / 清单排序），两种漏登记都测过 260722 编号 Q1 → QA1；标题 28 字压到 9 字 260722 完成线改成勾选清单；补 ## 图」 · 260723 1240
      for the logs, I want it to add the date and time as well.
- [ ] JL 「QA1」 · 260723 1240
      I want all the section name to be more salient.
- [ ] JL 「Board folder shape」 · 260723 1240
      maybe make it a bit longer, make it more like a question, like
      
      How to design the haipipe-board folder structure.

## Log
260723 1710 · 全局回顾时补勾：形状早定死并写进 SKILL.md/board-form.md，3 块板在用 → ✅ SETTLED
260723 0919 · 段落名改英文（## Now / ## Done when / ## Why here …）
260722 2320 · 完成线改成勾选清单，补 ## Diagram
260722 2310 · 编号 Q1 → QA1；标题从 28 字压到 9 字
260722 2255 · 挂接定成两层（路径认人 / Roster 排序），两种漏登记都测过
260722 2250 · 拆题：段落归 QA2，这题只管文件夹
260722 1706 · 开题。原题「文件夹里有哪些文件 + 文件里有哪些段落」两件事混在一起
