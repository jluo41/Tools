# Board form — 完整规格

SKILL.md 是最短的操作说明；这一份是查得到细节的地方。

## 1. 文件夹

```
<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/
  board.md            全局：标题 · spine · close · Topic · Pipeline · Roster
  QA1-<slug>.md       一题一个文件
  QA2-<slug>.md
  QB1-<slug>.md
  board.html          生成的，别手改
  fig/                截图
```

- **所属单位** = 这块板服务于谁：一个 plugin、一个 task 文件夹、一篇 paper。
  板是工作产物，skill 是交付包，两者不混在一个文件夹里。
- **NN** 每个 `diagram/` 各自从 01 开始。
- **YYMMDD** 是**开板那天**，之后永不改。

## 2. 编号

文件名前缀就是这一题的编号：`Q` + 组字母 + 组内序号。

```
QA1  QA2  QA3      QA 组
QB1  QB2           QB 组
QC1                QC 组
```

排序按（字母，数字）。不分组就直接 `Q1 Q2 Q3`。加一组＝换个字母。
`-<slug>` 只是给人认文件的短英文小写（`access`、`scheduling`），解析不看它，跟 `board-example.md` 一致。新开的 Q 一律 `state: 🔴 OPEN`。

## 3. board.md

```markdown
# 板的标题 —— 一句话说清这块板在干嘛
spine: 主干。这块板在解决什么，一句话。没解决之前，题目不许漂移。
close: 关板条件。什么时候这块板可以关掉。
source: 可选，这块板的来源（会议记录路径之类）

## Topic
给一个完全没背景的人读的：这是什么项目、谁是谁、在解决什么。
零背景审查最常挂的就是这一段缺失。

## Pipeline
这些 Q 之间是什么关系 —— 并列？流水线？分几组？

## Roster
### QA · 组标题
QA1-form.md
QA2-qtemplate.md
### QB · 另一组
QB1-skillmd.md
```

**Roster 只管排序和分组**，标题正文一概不抄（抄了就会不同步）。

**必填**：`# 标题`、`spine:`、`close:`、`## Topic`、`## Pipeline`、`## Roster` —— 这三段都要写，别省掉 `## Pipeline`。`source:`、`## Links` 选填。

## 4. Q 文件

段落名与页面位置一一对应：

```
# 短标题        → .h2       聚焦时 38px，前面挂编号
state:          → .pill     ✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD
owner:          → 状态条    JL 显示 🧠 拍板，其他显示 🔧
method:         → 状态条    一句话说怎么做

## Question        → .ask       一段话 + 几个要点；第一段是大字领句
## Boundary        → .bnd       这题管什么 / 不管什么，灰边
## Diagram         → .dia       ascii 图
## Items to Finish → .col.goal  绿色边，栏头自动数出 5/6
## Where we are    → .col.now   黄色边
## Files           → .fls       这题牵动哪些文件，蓝边（路径自动变可点链接）
## Why here        → .folds     折叠（已退役，见下）
## Discussion      → .folds    折叠
## Comments     → .folds    折叠，有未解决的会默认展开
## Law          → .folds    折叠 · 这题拍定的规矩
## Lesson       → .folds    折叠 · 这题踩过的坑
## Glossary     → .folds    折叠
## Log          → .folds    折叠
```

**必填**：`# 标题`、`state:`、`owner:`、`## Question`、`## Items to Finish`、`## Where we are`。
`## Boundary` 和 `## Files` 选填但**强烈建议写**；其余（`method:`、`## Diagram` 和所有折叠段）**选填**，用不上就整段删掉。
折叠段在页面上的顺序由 `build.py` 固定（Why here · Discussion · Comments · Law · Lesson · Glossary · Log），跟文件里写的顺序无关。

**台面上的顺序是定死的**（260723 改版）：`Question → Boundary → Diagram → Items to Finish → Where we are → Files`。
先给意图（在问什么、边界、什么算完），再给状态（现在到哪）。改版前是 Now 在 Done when 上面 ——
零背景的人先撞上一堵实现细节，还没搞懂目标就淹了。

**`## Why here` 已退役。** 它的活（为什么难 / 不定会怎样）并进 `## Question` 的要点里，
好让「光读第一节就 orient」。老板子里还写着这段的照常解析，只是收进底部折叠区，内容不丢。

**老段名一律还认**，老板子不用改就能重新生成：中文名（`## 问题` `## 现在什么样` …）、
以及改版前的 `## Done when`（＝`## Items to Finish`）和 `## Now`（＝`## Where we are`）。

## 4b. `## Links` —— 板和产物的连线

板讨论的东西通常不在板的文件夹里。在 `board.md` 里声明：

```markdown
## Links
SKILL.md            ../../haipipe-board/SKILL.md
ref/q-template.md   ../../haipipe-board/ref/q-template.md
haipipe-board/      ../../haipipe-board/
```

左边是正文里反引号的写法，右边是相对 `board.html` 的路径。
之后所有 `` `SKILL.md` `` 都变成可点链接。

- 没声明的路径也会自动试一次：从板的文件夹逐级往上找同名路径，找到且**真实存在**才链。
  找不到就还是普通 `<code>`，不会变死链。
- 声明过的**不做存在性检查** —— 写错就是死链，自己负责。
- 也支持普通 markdown 链接 `[写法](路径)`。

## 5. 正文语法

| 写法 | 效果 |
|---|---|
| `**整行加粗**`（单独一行） | 组标题：略大，领着下面一串 item。开头写个 emoji（`**🎨 版式落地**`）就用它当记号；不写用默认 🔹 |
| `- 小标题` + 缩进两格的解释行 | 要点块：▸ 加粗小标题 + 灰色解释 |
| `- [ ]` / `- [x]` + 缩进解释 | 勾选清单，栏头自动数出 `3/5` |
| ` ``` ` 围栏 | 原样输出的 `<pre>`（ascii 图、代码、目录树） |
| 单独一行一个 excalidraw 分享链接 | 嵌成可交互画布（iframe）+ 一条「↗ 在 Excalidraw 打开」兜底链接 |
| 裸 `https://…` | 自动变成可点链接（不会把已在 `href=` 里的再套一层） |
| `` `code` `` `**粗**` `![](fig/x.png)` | 行内代码 / 加粗 / 图片 |
| `> JL: 文字` | 讨论行，按署名分颜色 |
| `>> CC0723: 文字` | 回复 |
| `> JL 「原句」: 文字` | 讨论行 + 把「原句」在正文里高亮 |
| `260723 1030 · 文字` | Log 一行，时间可省 |

署名认任意 1–4 位大写字母（`JL` `RA` `ZW` `CC0723`）。`JL/RA/CC` 有固定颜色，其他人按名字自动分配。

## 6. Comments 段

```markdown
## Comments
- [ ] JL 「被选中的原句」 · 260723 1100
      评论正文，缩进两格，可多行。
      > CC0723: 回复也写在缩进里
- [x] RA 「另一句」 · 260723 1130
      已解决的，勾上。
```

- `[ ]` 未解决 → 引文在正文里**黄底高亮**，折叠块默认**展开**。
- `[x]` 已解决 → 整条变灰、引文划掉，高亮也变淡。
- 引文在正文里找不到（原文被改过）→ 那一条标 **⚠ anchor lost**，折叠块标题也会写出来。**不会悄悄失效。**
- 折叠块标题：`💬 Comments (2 open / 5) · ⚠ 1 anchor lost`

这一段通常不用手写 —— 页面上选中文字加评论，再点 Sync to md 就会写进来。

## 7. 生成

`build.py` / `watch.py` 都在 skill 目录里（不在板文件夹）。带路径调，别 `cd` 进板文件夹跑 `build.py .`：

```bash
python3 <skill>/build.py <board 文件夹>     # 生成一次（<skill> = .../0_utils/haipipe-board）
python3 <skill>/watch.py <board 文件夹>     # 盯着，改任何 .md 自动重新生成
```

**别手改 `board.html`** —— 下一次生成就覆盖了。md 是唯一来源。

## 8. 页面

一个文件两种模式，没有第二份 deck：

- **平铺**（默认）：主干 + 进度条 + 两个全局入口 + 索引 + 所有题，滚着读。
- **聚焦**：点索引任意一行，`:target` + `:has()` 纯 CSS 把其余全收起来，屏上只剩那一题；
  去掉边框圆角底色，标题 38px，底部 `← 上一题 · ☰ 全部 · 下一题 →`。投屏用这个。

**聚焦时什么上台面、什么收起来**（QA4 定的）：

- **上台面**（从上到下）：标题 → `❓ Question`（大字领句 + 要点）→ `🚧 Boundary` → `## Diagram`（招牌图，不折）→ `🎯 Items to Finish` → `📍 Where we are` → `📁 Files`。
- **三级层级**：节标题（❓/🚧/🎯/📍，底下一条线）＞ **组标题**（整行加粗 → 🔹 默认，开头写 emoji 就用那个，领着一串 item）＞ item 的名字（`▸`）。
- **默认收起**（点名字 / 按节标题右边的 `expand all` 才现）：item 的解释（收进 native `<details>`）、正文里的代码块（收成一行 `</> code · N 行`；`## Diagram` 除外）。
- **沉到底部折叠区**：Why here · Discussion · Comments · Law · Lesson · Glossary · Log。
- 一屏第一眼 = 一列干净的名字 + 招牌图；`expand all` 一键把这一节的 item / 代码全铺开（纯增强，脚本剥掉后每条仍能单独点开）。

**别的定死的**：现在 vs 算做完**上下叠**不左右分栏（长短不齐时并排会空半边）；长题**滚动**不截断不拆屏；**不锁 16:9** 随窗口高走（锁画幅归投屏 deck）；大标题 id 后面留一个**真空格**，复制才不会粘成 `QA4Single…`。

**不变量：把页面里所有 `<script>` 删掉，每一题和全部正文仍然在。** `build.py` 每次生成都断言这一条。脚本只能做增强（现在只有评论层），不能是内容的来源。
