# Board form — 完整规格

SKILL.md 是最短的操作说明；这一份是查得到细节的地方。

## 1. 文件夹

```
<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/
  board.md            全局：标题 · spine · close · Topic · Pipeline · Roster
  QA1-<slug>.md       一题一个文件
  QA2-<slug>.md
  S0-<slug>.md        lifecycle stage（有 stage 才写）
  QB1-<slug>.md
  board.html          生成的，别手改
  fig/                截图
```

- **所属单位** = 这块板服务于谁：一个 plugin、一个 task 文件夹、一篇 paper。
  板是工作产物，skill 是交付包，两者不混在一个文件夹里。
- **NN** 每个 `diagram/` 各自从 01 开始。
- **YYMMDD** 是**开板那天**，之后永不改。

**文件夹题（QC3，JL 260724）**：Q 文件也可以住进它讲的那个文件夹 —— 板于是能直接
盖在一棵已有的树上（第一个消费者：一篇 paper 的 `0-lifecycle/`）：

```
0-lifecycle/                    ← 整个文件夹就是板
  board.md
  QA1-frontier.md               顶层的题照旧
  0-seed/S0-seed.md             stage face 住在自己的 stage folder
  4-display/QD2-d01-….md        住在自己家里的题
  5-section-edit/6-results/QE5-….md      深度不限
  board.html
```

- 发现规则：板文件夹整棵树里所有 `Q*.md` / `S*.md`；路径里带 `_`/`.` 开头的段（`_archive/`、
  `_preview/`…）和 `fig/` 的不算。
- Roster 仍只写**文件名**；全板文件名唯一 —— 重名会在命令行警告并只认先到的那个。
- 页面回写（评论、归档）带的是**相对板根的路径**；归档时嵌套的题拍平进板根的 `_archive/`。
- 从页面新加的题仍生成在板根（要住进哪个文件夹，手动挪，Roster 行不用改）。
- Q 文件里写路径**仍然相对板根**（跟平铺时一模一样），不随题住到哪而变。

## 2. 编号与 Kind

文件名前缀就是这一题的编号：`Q` + 组字母 + 组内序号。

```
QA1  QA2  QA3      QA 组
QB1  QB2           QB 组
QC1                QC 组
```

排序按（字母，数字）。不分组就直接 `Q1 Q2 Q3`。加一组＝换个字母。
组内**下一号**（页面 ＋Q 用的规则）＝ 盘上全树 + Roster 里该组的最大号 + 1（QC3 之后全树数，别只看板根）。
`-<slug>` 只是给人认文件的短英文小写（`access`、`scheduling`），解析不看它，跟 `board-example.md` 一致。新开的 Q 一律 `state: 🔴 OPEN`。

S face 用 lifecycle 自己的 stage order：`S0`、`S1a`、`S1b`、`S2a`、`S2b`、`S3`、
`S4`、`S5`。Q 是 ruling；S 是 lifecycle stage。两者共用段落 grammar，但首页分别统计
`questions settled` 和 `stages gated`。

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
One sentence shown under the group header on the index (optional intro).
More plain lines: the click-to-expand body, what this group is for and why.
QA1-form.md
QA2-qtemplate.md
### QB · 另一组
QB1-skillmd.md
```

**Roster 只管排序和分组**，标题正文一概不抄（抄了就会不同步）。

**`doc:` 行（QF2，JL 260724）**：`doc: notes/readme.md` ——
把列出的源文件**直接**渲染成一页（id = 第一份文件**所在文件夹**名，顶层文件才取文件名主干 ——
这样 `2b-pitch/PITCH_LOG.md` 的页叫 `2b-pitch`，两个 `README.md` 也不会撞；标题取第一份文件
自己的 `#`/setext 标题，没有就用 id）。
没有 Q 文件包着，所以也没有 state、没有清单计数、没有评论落点；doc 页是「看」，不是「题」，
不进 settled 计数和进度条。只保留它兼容旧板；lifecycle stage 要参与 checklist、gate 和评论，
就写成 S face。

**Group intro (QC2, 260724)**: plain lines between a `### ` heading and that group's first `.md` line are the group's intro. Line 1 is always visible under the header on the index page; any further lines open on click (rendered as a native `<details>`, so the no-script invariant holds). Intro lines must not end in `.md`. The index page's ＋Q / ＋Group / 🗄 buttons write exactly this grammar through `POST /_board/structure` (`structure_op()` in serve.py, imported by the console): `add_question {group, title}` seeds a stub Q file and lists it under its group; `add_group {title, letter?, hook?, body?}` appends a `### QX · title` heading (letter auto-picked); `archive_question {q}` moves that file to `_archive/` inside the board folder (never deletes; since QC3 build.py DOES glob subfolders, so it is the `_` prefix that hides `_archive/` from discovery — archived files leave the page for that reason); `archive_group {group}` removes a group only when it lists no questions. Over HTTP the payload also carries `path` (the page's own location.pathname); called directly it is `structure_op(board_dir, payload)`, and importing serve.py is side-effect free (`serve_forever` sits behind `__main__`).

**必填**：`# 标题`、`spine:`、`close:`、`## Topic`、`## Pipeline`、`## Roster` —— 这三段都要写，别省掉 `## Pipeline`。`source:`、`## Links` 选填。

## 4. Q/S Face

段落名与页面位置一一对应：

```
# 短标题        → .h2       聚焦时 38px，前面挂编号
state:          → .pill     ✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD
owner:          → 状态条    JL 显示 🧠 拍板，其他显示 🔧
method:         → 状态条    一句话说怎么做

## Question        → .opening .ask + kind 路由  第一段问句在 Opening；解释段见下
## Boundary        → .opening .qbd  这题管什么 / 不管什么，收进 Opening
## Diagram         → .diagram-section > .dia  独立一节，默认折叠
## Content         → .content / .opening-context  S 必填、Q 选填；见下
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

**两种 face 都必填**：`# 标题`、`state:`、`owner:`、`## Question`、
`## Items to Finish`、`## Where we are`。S 另外必填 `## Content`；Q 可省 Content。
`## Boundary` 和 `## Files` 选填但**强烈建议写**；其余（`method:`、`## Diagram` 和所有折叠段）**选填**，用不上就整段删掉。
折叠段在页面上的顺序由 `build.py` 固定（Why here · Discussion · Comments · Law · Lesson · Glossary · Log），跟文件里写的顺序无关。

**台面上的五层顺序是定死的**：
`Opening → Diagram → Content → Items to Finish → Where we are`（Files 跟在状态后面）。
Opening 是 Question lead + optional Boundary；optional Diagram 是独立一节，默认折叠，
点节名才展开。Q 的 Question 解释段自动成为 Content 首节。S 的解释段放进 Opening；
S 的显式 Content 里若有直接 `### Stage Record`，也提进 Opening、默认折叠，其余
subsections 留在 Content。Q 的显式 Content 可省。
先给意图（在问什么、边界、什么算完），再给状态（现在到哪）。改版前是 Now 在 Done when 上面 ——
零背景的人先撞上一堵实现细节，还没搞懂目标就淹了。

**`## Why here` 已退役。** 它的活（为什么难 / 不定会怎样）并进 `## Question` 的解释段，
并渲染成 “Why this matters”：Q 放在 Content 首节，S 放在 Opening。老板子里的旧段仍收进底部折叠区。

**老段名一律还认**，老板子不用改就能重新生成：`## Opening` 也可代替 `## Question`，
中文名（`## 问题` `## 现在什么样` …）、
以及改版前的 `## Done when`（＝`## Items to Finish`）和 `## Now`（＝`## Where we are`）。

**S face 的 Q-consumer 规则**：不另开顶层 `## Q-consumer`。每个 consumer 是
`## Items to Finish` 里的 checklist item，标题保留 `Q-<Stage>-<n>`，折叠详情保留
Description / Reason / Probe / Answer。只有 Answer 已落地、已解释、已织回 Content 才勾
`[x]`；deferred 只有写下 forward pointer 才能闭合。`## Where we are` 只总结 stage，
不复述每个 consumer answer。

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
| `- [ ]` / `- [x]` + 缩进解释 | 勾选清单，栏头自动数出 `3/5`；S 的 Q-consumer 也用这一行形 |
| ` ``` ` 围栏 | 原样输出的 `<pre>`（ascii 图、代码、目录树） |
| item 解释行里**缩进的** ` ``` ` 围栏 | 收进**这个 item 的折叠区**（不 flush 成兄弟块）：dedent 后原样 `<pre>`，位置随你放（摘要后、正文段之间都行）。顶格的围栏照旧是兄弟块（JL 260724，QC10 CABG 板首用） |
| 单独一行 `![[路径]]` / `![[路径#某节]]` | **嵌入**（QF1）：把另一份文件（整份或某一节）按引用嵌进这一题，生成时现读。路径相对板根，找不到再逐级向上找（≤8 级）；只吃 `.md`/`.txt`；`#某节` 认 `##` 标题**和** setext（下划线）标题；嵌不到 / 找不到那节 → 就地一块红色警告，绝不悄悄空掉；嵌进来的内容里再写 `![[…]]` 不展开（防环）。钉在嵌入文字上的评论仍写进**这一题**的 `## Comments`，重建时在新渲染的嵌入块里重新锚定 —— 源文件删了那句话才会显示 unanchored |
| 单独一行一个 excalidraw 分享链接 | 嵌成可交互画布（iframe）+ 一条「↗ 在 Excalidraw 打开」兜底链接 |
| 裸 `https://…` | 自动变成可点链接（不会把已在 `href=` 里的再套一层） |
| `` `code` `` `**粗**` `![](fig/x.png)` | 行内代码 / 加粗 / 图片 |
| `> JL: 文字` | 讨论行，按署名分颜色 |
| `>> CC0723: 文字` | 回复 |
| `> JL 「原句」: 文字` | 讨论行 + 把「原句」在正文里高亮 |
| `260723 1030 · 文字` | Log 一行，时间可省 |

署名认任意 1–4 位大写字母（`JL` `ZW` `CC0723`）。`JL/CC` 有固定颜色；每位同事用自己的缩写，按名字自动分配颜色。

## 6. Comments 段

```markdown
## Comments
- [ ] JL 「被选中的原句」 · 260723 1100
      评论正文，缩进两格，可多行。
      > CC0723: 回复也写在缩进里
- [x] ZW 「另一句」 · 260723 1130
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

- **平铺**（默认）：主干 + Q settled / S gated 两个进度信号 + 索引 + 所有 faces，滚着读。
- **聚焦**：点索引任意一行，`:target` + `:has()` 纯 CSS 把其余全收起来，屏上只剩那一题；
  去掉边框圆角底色，标题 38px，底部 `← 上一题 · ☰ 全部 · 下一题 →`。投屏用这个。

**聚焦时什么上台面、什么收起来**（QA4 定的）：

- **上台面**（从上到下）：标题 → `🧭 Opening`（Question lead + optional Boundary；S 另含
  open 的 Why this matters 和 collapsed 的 optional Stage Record）→
  `🖼 Diagram`（optional，只有节名上台面，内容默认折叠）→
  `📚 Content`（Q 先放 Why this matters；S 只放 Stage Record 以外的显式 subsections）→
  `🎯 Items to Finish` → `📍 Where we are` → `📁 Files`。
- **三级层级**：节标题（🧭/📚/🎯/📍，底下一条线）＞ **组标题**（整行加粗 → 🔹 默认，开头写 emoji 就用那个，领着一串 item）＞ item 的名字（`▸`）。
- **默认收起**（点名字 / 按节标题右边的 `expand all` 才现）：整个 `## Diagram`、item 的解释（收进 native `<details>`）、正文里的代码块（收成一行 `</> code · N 行`）。
- **沉到底部折叠区**：Why here · Discussion · Comments · Law · Lesson · Glossary · Log。
- 一屏第一眼 = 一列干净的节名和 item 名；Diagram 自己点开，`expand all` 一键把其他节的 item / 代码铺开（纯增强，脚本剥掉后每条仍能单独点开）。

**别的定死的**：现在 vs 算做完**上下叠**不左右分栏（长短不齐时并排会空半边）；长题**滚动**不截断不拆屏；**不锁 16:9** 随窗口高走（锁画幅归投屏 deck）；大标题 id 后面留一个**真空格**，复制才不会粘成 `QA4Single…`。

**不变量：把页面里所有 `<script>` 删掉，每一题和全部正文仍然在。** `build.py` 每次生成都断言这一条。脚本只能做增强（现在只有评论层），不能是内容的来源。
