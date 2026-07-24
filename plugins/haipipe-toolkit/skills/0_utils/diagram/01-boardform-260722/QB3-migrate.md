# Migrate the two old boards
state: ✅ SETTLED
owner: CC
method: 重写成新格式 + 重新生成 html + 清掉旧中间产物

## Question
`subjective-label/diagram/` 下面已经有两块旧格式的板。要不要迁到新格式？迁到什么程度算够？

- 为什么难
  迁多了是白工（那两块板的话题已经过去了），迁少了它们又打不开、当不成例子。
- 不定会怎样
  这两块板是这个 skill 目前唯一的**实物证据**。它们要是还停在打不开的旧版本，SKILL.md 里写的东西就一个能指的例子都没有。
- 定了会影响什么
  也顺带验证一件事：生成器对老板子到底兼不兼容（`ALIAS` 那套多段名的机制成不成立）。

## Boundary
- ✅ 这题管
  **老板子怎么办**：迁哪几块、迁到什么程度、还是就地重新生成。
- ❌ 这题不管
  新板的格式本身 —— 那是 `QA1`/`QA2`/`QA4`。这题只管存量。

## Diagram
```
01-sublabel-license-260722/  ──折──►  02-method-260722/（新格式，13 题）
  验证内核 ①②⑤            ─►  QB3 拿一个不是自己打的分数
  ③ auto-lexicon          ─►  QD4 词表别写死
  ④ objective             ─►  QC3 用什么标准挑构念
  ⑥ b02-naming            ─►  QC2 的 ZD 评论
  Di 的 note-update/audit  ─►  02/_source/（存档，不销毁）
  board.md/html/bak · deck.html · render.py  ─►  删
```

## Items to Finish
- [x] `02-method-260722/` 改成 QA1 定下的格式：拆成一题一文件（13 个 `QX-slug.md`）、中文段名→英文段名、`[Q1]`→`QA1`、补 Diagram/Log
- [x] `02-method` 的 `board.html` 重新生成，打开能看（13 个 Q、零脚本仍有 20450 字正文）
- [x] `01-sublabel-license-260722/` 完全迁入：验证内核→QB3、③→QD4、④→QC3、⑥→QC2 评论；Di 的 F1–F8 分发成 12 条锚定评论；Di 设计原文移到 `02/_source/`
- [x] 旧的中间产物清掉：整个 `01-sublabel-license-260722/`（含 `render.py`/`deck.html`/`board.html.bak`）已删

## Where we are
**两块旧板都迁完了，`02-method-260722/` 成了唯一一块 subjective-label 板**（13 题、四组 QA/QB/QC/QD、彩色索引按 Roster 排、零脚本静态）。
- `02-method` 内容：7 个方法 Q（QA1–QA3 / QB1–QB2 / QC1–QC2）+ 折进 01-license 验证内核的 QB3 + JL 当场提的 QD 引擎组（QD1 embedding · QD2 cascade · QD3 训分类器 · QD4 auto-lexicon）+ 从 01-license 的 ④ 折出的 QC3 objective。
- `01-license` 处置：6 件事全部安家（①②⑤→QB3 · ③→QD4 · ④→QC3 · ⑥→QC2 评论）；Di 的 F1–F8 方法学缺陷分发成 12 条锚定 `## Comments`（署名 ZD，12/12 命中高亮）；Di 的 `note-update-v3` + `workflow-audit` 移进 `02/_source/` 存档；旧文件夹已删。

## Files
- `build.py`
  `ALIAS` 决定老段名还认不认 —— 老板子能不能一个字不改就重新生成，全看它。
- `Tools/plugins/subjective-label/diagram/`
  那两块老板子所在的地方。

## Glossary
白屏：旧版页面的正文全靠页面里一段 JS 现场生成，而 VS Code 的预览窗口不许跑这段 JS，所以打开就是一片白。新版把正文直接写死在 HTML 里、一个脚本都没有，因此不可能白屏。

## Discussion

## Log
260723 · 按新结构重写：Question 展开成「一段话 + 要点」，补 `## Boundary` 和 `## Files`；退役的 `## Why here` 并进 Question
260723 1620 · 关板 🟡→✅：01-license 六件全安家（③→QD4 ④→QC3 ⑥→QC2 评论）、Di F1–F8 分发成 12 条锚定评论、Di 原文移入 `02/_source/`、旧文件夹删除；02 现 13 题
260723 1605 · `02-method` 迁完：拆成一题一文件（11 题）+ 折入 01-license 验证内核（QB3）+ 新增 QD 引擎组；state 🔴→🟡（剩 01-license 的 ③④⑥ 和清理，等 JL 拍）
260723 0919 · 编号 Q6 → QB3
260722 2340 · 完成线里加「删掉旧的 deck.html / render.py」
260722 2255 · 开题
260722 2129 · 02-method 改成静态版（7 题、零脚本），但还没拆成一题一文件
