# Board form — 完整规格

SKILL.md 是最短的操作说明；这一份是查得到细节的地方。

## 1. 文件夹

```
<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/
  board.md            全局：标题 · spine · close · Topic · Pipeline · Pages
  QA1-<slug>.md       一题一个文件
  QA2-<slug>.md
  S-Seed-0-<slug>.md  named lifecycle page（有 lifecycle 才写）
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
  0-seed/S-Seed-0-seed.md       lifecycle face 住在自己的 folder
  4-display/QD2-d01-….md        住在自己家里的题
  5-section-edit/6-results/QE5-….md      深度不限
  board.html
```

- 发现规则：板文件夹整棵树里所有 `Q*.md` / `S*.md`；路径里带 `_`/`.` 开头的段（`_archive/`、
  `_preview/`…）和 `fig/` 的不算。
- Pages 仍只写**文件名**；全板文件名唯一 —— 重名会在命令行警告并只认先到的那个。
- 页面回写（评论、归档）带的是**相对板根的路径**；归档时嵌套的题拍平进板根的 `_archive/`。
- 从页面新加的题仍生成在板根（要住进哪个文件夹，手动挪，Pages 行不用改）。
- Q 文件里写路径**仍然相对板根**（跟平铺时一模一样），不随题住到哪而变。

## 2. 编号与 Kind

文件名前缀就是这一题的编号：`Q` + 组字母 + 组内序号。

```
QA1  QA2  QA3      QA 组
QB1  QB2           QB 组
QC1                QC 组
```

排序按（字母，数字）。不分组就直接 `Q1 Q2 Q3`。加一组＝换个字母。
组内**下一号**（页面 ＋Q 用的规则）＝ 盘上全树 + Pages 里该组的最大号 + 1（QC3 之后全树数，别只看板根）。
`-<slug>` 只是给人认文件的短英文小写（`access`、`scheduling`），解析不看它，跟 `board-example.md` 一致。新开的 Q 一律 `state: 🔴 OPEN`。

Paper lifecycle 的 S face 用完整 family 名：`S-<Family>-<unit>-<slug>.md`。Family 固定为
`Seed`、`Work`、`Venue`、`Display`、`Main`、`Appendix`、`Submission`；unit 可用数字，也可在
Appendix 使用字母。例：`S-Seed-1-literature.md`、`S-Main-4-theory.md`、
`S-Appendix-B-validation.md`。Q 是 ruling；S 是 lifecycle page。两者共用段落 grammar，
首页分别统计 `questions settled` 和每个 S family 的 gate progress。旧板的 `S0` / `SM0`
/ `SA0` 命名继续可读，但新 paper board 不再生成这些缩写。

**S 的 `state:` 用同一套四个值**（没有第五个值，别自己造 `human-gated` 这种词）：
`🔴 OPEN` 没开始 · `🟡 PARTIAL` 在做 · `✅ SETTLED` = **这个 stage 的 human gate 过了**
（首页对应 family 的 `N/M` 数的就是 S face 里的 ✅）· `⏸️ ON HOLD` 明确搁置。
新开的 S 跟新开的 Q 一样，一律 `🔴 OPEN`。区别只在**凭什么翻到 ✅**：Q 要 checkbox 全闭合，
S 要它自己的 human gate 过了（`SKILL.md` 的 close 段说的 human-gated / explicitly parked
就是这两个值，不是两个新状态）。

**S face 在 `## Pages` 里跟 Q 文件一个写法**：一行一个裸文件名
（`S-Main-2-introduction.md`），放在哪个 `### ` 组下面就归哪组。普通 board 的组标题
是自由文本；**paper lifecycle board 默认按 named family 分组**：

```markdown
### QB · Work Group
Resources and claims become checkable lifecycle pages.
S-Work-0-resources.md
S-Work-1-claims.md
### QD · Display Group
The evidence-presentation layer serves both Main and Appendix.
S-Display-0-displays.md
QD1-figure-order.md
QD2-table-scope.md
```

七个 group 的索引顺序固定为 `Seed → Work → Venue → Display → Main → Appendix → Submission`，
但这是稳定的 ownership/navigation order，不是执行器自动推导的线性流程。真实 stage
edges 必须写在 `## Pipeline`；一个 flow 可以在 Narrative 后进入 Display，再分给
Main 和 Appendix。Display 独立成组，因为它拥有 claim-to-display map、approved assets、
captions、statistical labels 和 placement，不是 Work 的普通 item。
Seed 里 `S Seed → S Literature`；Main 里 narrative control 后接每个 manuscript section；
Appendix 里 control 后接 A/B/C；Submission 里 reconcile → compile → review → submit。
收到 external review 后，reopen 受影响的 Work/Display/Main/Appendix pages，再复用同一组
Submission pages 记录下一轮，不复制 `S-Submission-R2-*` 页面。
某个 S 的 Q ruling 紧跟在它后面。标题开头仍放一个唯一 Q family（如 `QD`、`QBa`），
让页面的 ＋Q / archive controls 有稳定 writer key。漏登记的照样显示，归 ⚠️ 组。

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

## Pages
### QA · 组标题
One sentence shown under the group header on the index (optional intro).
More plain lines: the click-to-expand body, what this group is for and why.
QA1-form.md
QA2-qtemplate.md
### QB · 另一组
QB1-skillmd.md
### QB · Seed Group
S face 跟 Q 一样只写裸文件名。
S-Seed-0-seed.md
S-Seed-1-literature.md
```

**Pages 只管排序和分组**，标题正文一概不抄（抄了就会不同步）。

**`doc:` 行（原 QF2，JL 260724；**260726 退役**，别再用）**：要展示别处的文件，改用 §5 的
`![[路径]]` 嵌进一个真正的 face —— 同样零拷贝，但页面有 state、有清单计数、有评论落点。
下面这段只为老板子留着，parser 仍认它（今天全 SPACE 无人使用）：`doc: notes/readme.md` ——
把列出的源文件**直接**渲染成一页（id = 第一份文件**所在文件夹**名，顶层文件才取文件名主干 ——
这样 `2b-pitch/PITCH_LOG.md` 的页叫 `2b-pitch`，两个 `README.md` 也不会撞；标题取第一份文件
自己的 `#`/setext 标题，没有就用 id）。
没有 Q 文件包着，所以也没有 state、没有清单计数、没有评论落点；doc 页是「看」，不是「题」，
不进 settled 计数和进度条。只保留它兼容旧板；lifecycle stage 要参与 checklist、gate 和评论，
就写成 S face。

**Group intro (QC2, 260724)**: plain lines between a `### ` heading and that group's first `.md` line are the group's intro. Line 1 is always visible under the header on the index page; any further lines open on click (rendered as a native `<details>`, so the no-script invariant holds). Intro lines must not end in `.md`. The index page's ＋Q / ＋Group / 🗄 buttons write exactly this grammar through `POST /_board/structure` (`structure_op()` in serve.py, imported by the console): `add_question {group, title}` seeds a stub Q file and lists it under its group; `add_group {title, letter?, hook?, body?}` appends a `### QX · title` heading (letter auto-picked); `archive_question {q}` moves that file to `_archive/` inside the board folder (never deletes; since QC3 build.py DOES glob subfolders, so it is the `_` prefix that hides `_archive/` from discovery — archived files leave the page for that reason); `archive_group {group}` removes a group only when it lists no questions. Over HTTP the payload also carries `path` (the page's own location.pathname); called directly it is `structure_op(board_dir, payload)`, and importing serve.py is side-effect free (`serve_forever` sits behind `__main__`).

**必填**：`# 标题`、`spine:`、`close:`、`## Topic`、`## Pipeline`、`## Pages` —— 这三段都要写，别省掉 `## Pipeline`。`source:`、`## Links` 选填。

## 4. Q/S Face

段落名与页面位置一一对应：

```
# 短标题        → .h2       聚焦时 38px，前面挂编号
state:          → .pill     ✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD
owner:          → 状态条    JL 显示 🧠 拍板，其他显示 🔧
method:         → 状态条    一句话说怎么做
requires:       → contract  显式上游 S ids / paths，comma-separated（S only）
style-from:     → contract  显式 writing-contract sources（S only）
provides:       → contract  本页给下游的短交付说明（S only）

## Question        → .opening .ask + kind 路由  第一段问句在 Opening；解释段见下
## Boundary        → .opening .qbd  这题管什么 / 不管什么，收进 Opening
## Stage Contract  → Opening 内 .csec.contract 折叠行  S 的 inherited inputs + writing style（JL 260725：收进 Opening，不单独占节）
## Diagram         → .diagram-section > .dia  独立一节，默认折叠
## Content         → .content / .opening-context  S 必填、Q 选填；见下
                     S 只放这个 stage 自己产出的东西（JL 260725）：venue/writing contract 归
                     `## Stage Contract`，已定的更正归 `## Where we are`，还欠的归
                     `## Items to Finish`。节标题在 S 上显示 stage 名（`📚 Content · Main 7
                     §6 Results`，从 `# 短标题` 推出来，所以 artifact 自己的编号跟板上的
                     index 对不上时，标题写成 `S Main 7 · §6 Results` 把两个号都摆出来），
                     不再数 subsection；Q 仍显示数量。
                     里面**只有两级**（JL 260725）：`###` = 自己有内容、能单独折的一块
                     （division），`####` = 它里面的一个段落，永远是 `####`。深浅靠编号
                     （`§6` vs `§6.1`）而不是靠标题级数 —— 页面只折一层，再多一级就把
                     整节压成一个盒子、丢掉逐 division 折叠。一块 division 只在自己确实
                     有内容时才写出来：flat 的节写一个 `### §1 Introduction` 领着它的段落，
                     有 subsection 的节直接从 `### §6.1` 开始，绝不开一个点开是空的盒子。
                     好处是可校验：带点的 `###` 个数就是 subsection 数，不读正文就能跟
                     venue blueprint 对。
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
`## Items to Finish`、`## Where we are`。S 另外必填 `## Stage Contract` 和
`## Content`；Q 删除 Stage Contract、可省 Content。
`## Boundary` 和 `## Files` 选填但**强烈建议写**；其余（`method:`、`## Diagram` 和所有折叠段）**选填**，用不上就整段删掉。
折叠段在页面上的顺序由 `build.py` 固定（Why here · Discussion · Comments · Law · Lesson · Glossary · Log），跟文件里写的顺序无关。

**台面上的顺序是定死的**：
Q 是 `Opening → Diagram → Content → Items to Finish → Where we are`；
S 相同：Stage Contract 折叠在 Opening 里，不再单独占一节（JL 260725）
（Files 跟在状态后面）。
Opening 是 Question lead + optional Boundary；optional Diagram 是独立一节，默认折叠，
点节名才展开。Q 的 Question 解释段自动成为 Content 首节。S 的解释段放进 Opening；
S 的显式 Content 里若有直接 `### Stage Record`，也提进 Opening、默认折叠，其余
subsections 留在 Content。Q 的显式 Content 可省。
先给意图（在问什么、边界、什么算完），再给状态（现在到哪）。改版前是 Now 在 Done when 上面 ——
零背景的人先撞上一堵实现细节，还没搞懂目标就淹了。

**`## Why here` 已退役。** 它的活（为什么难 / 不定会怎样）并进 `## Question` 的解释段，
并渲染成 “Why this matters”：Q 放在 Content 首节（默认展开），S 放在 Opening 且**默认折叠**
（JL 260725：Opening 里除了问句本身，其余每一行都收起来）。老板子里的旧段仍收进底部折叠区。

**老段名一律还认**，老板子不用改就能重新生成：`## Opening` 也可代替 `## Question`，
中文名（`## 问题` `## 现在什么样` …）、
以及改版前的 `## Done when`（＝`## Items to Finish`）和 `## Now`（＝`## Where we are`）。

**S face 的 Q-consumer 规则**：不另开顶层 `## Q-consumer`。每个 consumer 是
`## Items to Finish` 里的 checklist item，标题保留 `Q-<Stage>-<n>`，折叠详情保留
Description / Reason / Probe / Answer。只有 Answer 已落地、已解释、已织回 Content 才勾
`[x]`；deferred 只有写下 forward pointer 才能闭合。`## Where we are` 只总结 stage，
不复述每个 consumer answer。

**S face 的 Stage Contract 规则**：依赖只读顶层 metadata，不从 Pages 顺序或 filename
数字猜：

```markdown
requires: S-Work-1, S-Main-0, S-Display-0
style-from: S-Venue-1, STYLE.md
provides: reader-facing results section

## Stage Contract
<!-- haipipe:contract:start sha256=... -->
### Required Inputs
...上游 `### Provides` 的短摘要、路径和 gate state...
### Writing Style
...writing source 的短 contract...
<!-- haipipe:contract:end -->

### Provides
本页作者拥有的下游交付说明；sync 不覆盖。
```

`python3 stage.py new` 建页面，`stage.py sync` 只更新 marker 之间，`stage.py sync --all`
按显式 dependency graph 的 topological order 刷新（不看 Pages 顺序），`stage.py check`
检查 source hash。`build.py` 也把 missing/stale contract 放进 warnings，但永远不修改
Markdown。上游全文保持在上游；contract 只带 acceptance conditions、writing rules 和链接。

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
| `### 标题`（`## Content` 里顶格） | **division**：能单独折的一块内容。深浅靠编号（`§6` vs `§6.1`）不靠标题级数；只在自己确实有内容时才写（见 §4） |
| `#### 标题` | **段落标题**（`.ph`）：一个 division 里的一个段落，永远这一级。**没有图标**，比组标题小一号 —— 以前被压成 `**…**`，于是套上组标题的 🔹，把「一个段落」说成「领着一串 item 的一句话」（JL 260725） |
| 紧跟 `####` 的整行 `(…)` | 这一段**要干的活**（`.pj`）：灰斜体，留在台面上当扫读钩子，不折起来（折起来就扫不了）。只认紧跟标题的那一行，长度按 venue template 大约 80–120 字符 |
| `**整行加粗**`（单独一行） | 组标题：略大，领着下面一串 item。开头写个 emoji（`**🎨 版式落地**`）就用它当记号；不写用默认 🔹。**只有真的领着一串 item 才用它** —— 一个段落用 `####` |
| `- 小标题` + 缩进两格的解释行 | 要点块：▸ 加粗小标题 + 灰色解释 |
| `- [ ]` / `- [x]` + 缩进解释 | 勾选清单，栏头自动数出 `3/5`；S 的 Q-consumer 也用这一行形 |
| ` ``` ` 围栏 | 原样输出的 `<pre>`（ascii 图、代码、目录树）。**两棵树别并排画**：列的边界是空白，一复制就没了，右边那列会读成左边的分支 —— 板本来就是拿去贴进聊天和邮件的。要对比就竖着叠，一次一棵完整的树 |
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

- **上台面**（从上到下）：标题 → `🧭 Opening`（这一行不折，永远在）→ 领句（永远在，
  【可点】：点开它，抽屉里 Boundary、以及 S 的 Why this matters / Stage Record /
  Stage Contract（Required Inputs · Writing Style · venue）全是【平的】，一次全看见，
  里头不再套第二层 ▸。抽屉里的小标题一律是【光秃秃的词，不挂图标】—— 之前 7 个里
  只有 2 个有图标，这就是 JL 说的不一致，JL 260725）→
  `🖼 Diagram`（optional，只有节名上台面，内容默认折叠）→
  `📚 Content`（Q 先放 Why this matters；S 只放 Stage Record 以外的显式 subsections）→
  `🎯 Items to Finish` → `📍 Where we are` → `📁 Files`。
- **三级层级**：节标题（🧭/📚/🎯/📍，底下一条线）＞ **组标题**（整行加粗 → 🔹 默认，开头写 emoji 就用那个，领着一串 item）＞ item 的名字（`▸`）。
- **默认收起**（点名字 / 按节标题右边的 `expand all` 才现）：整个 `## Diagram`、item 的解释（收进 native `<details>`）、正文里的代码块（收成一行 `</> code · N 行`）。
- **沉到底部折叠区**：Why here · Discussion · Comments · Law · Lesson · Glossary · Log。
- 一屏第一眼 = 一列干净的节名和 item 名；Diagram 自己点开，`expand all` 一键把其他节的 item / 代码铺开（纯增强，脚本剥掉后每条仍能单独点开）。

**别的定死的**：现在 vs 算做完**上下叠**不左右分栏（长短不齐时并排会空半边）；长题**滚动**不截断不拆屏；**不锁 16:9** 随窗口高走（锁画幅归投屏 deck）；大标题 id 后面留一个**真空格**，复制才不会粘成 `QA4Single…`。

**不变量：把页面里所有 `<script>` 删掉，每一题和全部正文仍然在。** `build.py` 每次生成都断言这一条。脚本只能做增强（现在只有评论层），不能是内容的来源。
