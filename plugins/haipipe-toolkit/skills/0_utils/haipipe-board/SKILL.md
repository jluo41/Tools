---
name: haipipe-board
description: Open and run a BOARD — one topic, one folder, one markdown file per open question, generated into a single self-contained HTML page you can read, project, share, and comment on inline. Use when a topic has several undecided questions that need to be laid out, discussed with someone, and closed one by one; when handing a few days of work to an RA; or when the user says board, 打开这块板, 开板, 加一题, 关板, /haipipe-board. "打开 <board folder>" means VIEW an existing board (rebuild + push the URL to the user's VS Code browser over the VS Code IPC socket) — NOT create a new one, and never `open board.html`/`file://` (Remote-SSH: the browser is on the user's laptop).
metadata:
  version: "0.9.2"
  last_updated: "2026-07-24"
  summary: "One topic = one folder of question .md files + one static HTML page. build.py for the static page; serve.py adds live comments/chat/terminal. SKILL.md = the board's settled questions, distilled."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board — 一个话题，一叠问题，一页看板

**一块板 = 一个文件夹。** 里面一题一个 `.md`，外加一页谁都打得开的 `board.html`。
问题一个个定完，这块板就关掉。

它取代了 `/haipipe-session`（那个是只有干活的人自己看的工作日志）。

**两条必须成立的（JL 定的）：**

- 打开就知道自己在干嘛 —— 靠 `spine`（主干）和 `## Topic`
- 知道什么时候能结束 —— 靠 `close`（关板条件）和每题的 `## Items to Finish`

## 🗂 形状

```
<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/
  board.md            标题 · spine · close · ## Topic · ## Pipeline · ## Roster
  QA1-<slug>.md       一题一个文件
  QA2-<slug>.md
  QB1-<slug>.md
  board.html          ← build.py 生成，别手改
  fig/
```

- **所属单位** = 这块板服务于谁（一个 plugin / 一个 task 文件夹 / 一篇 paper）。
  板是工作产物，skill 是交付包 —— 不放在同一个文件夹里。
- **日期是开板那天，之后永不改。** 一个文件夹一个话题，后来的讨论往里追加，不另开。
- **谁在这块板上，靠路径**：同目录所有 `Q*.md` 就是这块板的题。
  `## Roster` 只管排序和分组；漏登记的照样显示（归 ⚠️ 组）并在命令行提醒 —— **漏登记只会丑，不会丢题**。

## 🔨 动作

离线（只要 `build.py`）：**view · open · add · build · sync · link · close**
现场（要 `serve.py` 跑着）：**serve · comment**

> **「打开 <某块板>」= view（看已有的），不是 open（开新的）。** 用户给了一个已存在的
> 文件夹路径就走 view；只有要新建时才走 open。

### view — 打开一块已有的板（最常用）

用户说「打开 `<板文件夹>`」时做这三步，**别只丢一句「打开 board.html」就完事**：

1. **先重新生成**，免得页面是旧的：
   `python3 <skill>/build.py <板文件夹>`
2. **推到用户的 VS Code 浏览器**（下面那段是唯一真正有效的方式，见 ⚠️）：

```bash
BD=<板文件夹相对仓库根的路径>          # 例：Tools/plugins/.../diagram/01-boardform-260722
S=$(ls -t "$TMPDIR"/vscode-ipc-*.sock 2>/dev/null | head -1)
B=$(ls -t ~/.vscode-server/cli/servers/*/server/bin/helpers/browser.sh 2>/dev/null | head -1)
VSCODE_IPC_HOOK_CLI="$S" "$B" "http://127.0.0.1:5599/$BD/board.html#top"
```

3. 顺手报一句板的状态：几题、几条未解决评论、卡在哪。

⚠️ **为什么不能用 `open board.html` 或 `file://`**：这台机器是 Remote-SSH ——
**浏览器在用户的笔记本上，文件在服务器上**。`open` 只会在服务器桌面上打开，用户什么都看不到；
`file://` 指的是用户本机的盘，那儿没有这些文件。必须走上面那条 IPC，把 URL 交给用户那侧的 VS Code。

需要 `serve.py` 在 5599 上跑着（没跑就先起，见 serve 段）。`#top` 回目录、`#QA7` 直接跳某一题、`#all` 展开全部。

### open — 开一块**新**板

1. 问清三件事：**这块板要解决什么**（→ `spine`）、**什么时候算完**（→ `close`）、**有哪几个 Q**。
   Q 列表要用户点头才往下走 —— 这是唯一必须停下来问的地方。
2. 建 `<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/`。
3. 写 `board.md`：标题、`spine:`、`close:`、`## Topic`、`## Pipeline`、`## Roster`（三个都写上）。
4. 每个 Q 复制 `ref/q-template.md` → `Q<组字母><序号>-<slug>.md`。
   `<slug>` 用短英文小写（`access`、`scheduling`），跟 `ref/board-example.md` 一致。
   新开的 Q 一律 `state: 🔴 OPEN`。owner 按性质给：要拍板/授权的给 JL，动手干的给 RA/CC。
5. 生成：`build.py` 在 **skill 目录**里，不在板文件夹里，所以带上它的路径 ——
   `python3 <skill>/build.py <板文件夹>`（`<skill>` = `Tools/plugins/haipipe-toolkit/skills/0_utils/haipipe-board`）。
   **别 `cd` 进板文件夹再 `python3 build.py .`** —— 那样找不到 build.py。
   生成只往 `board.html` 写，不碰你的 `.md`（md 是唯一来源）。
6. **按 view 那一节把页面推到用户的 VS Code 浏览器** —— 不要只说「打开 board.html」。

### add — 加一题

复制 `ref/q-template.md` → 新文件名 → 写进 `board.md` 的 `## Roster` → 重新生成。
忘了写进 Roster 也不会丢，只会归到 ⚠️ 组。

### build — 生成

`build.py` 在 skill 目录里（不在板文件夹）。带路径调，别 cd 进板文件夹跑 `build.py .`：

```bash
python3 <skill>/build.py <board 文件夹>     # 生成一次（<skill> = .../0_utils/haipipe-board）
python3 <skill>/watch.py <board 文件夹>     # 盯着，改任何 .md 自动重新生成
```

**md 是唯一来源。** 永远不要手改 `board.html`。

### serve — 让板活起来（现场层）

一个服务器管所有板 —— 服务的是仓库根，不是某一块板：

```bash
.venv/bin/python <skill>/serve.py --root <仓库根> --port 5599
```

跑起来之后，板不只是能读，还能：**评论直接落盘**（下一节就靠它）、在某一题上**开 chat 或 terminal 当场干活**。
⚖️ 一题一 session · 一 session 一窗口 · N 题 N 终端 —— 详见板的 `QD1` 的 `## Law`。

> chat（受限抽屉，`QD2`）和 terminal（真 CLI，`QD3`）这套**还在 QD 组定型中**。
> 用法以那几题为准，别当成定死的规矩（见文末「板 ↔ SKILL.md」）。

### comment — 评论（要 serve.py 跑着）

- **页面上**：选中一句话 → 冒出「💬 Comment」→ 写评论 → 按 **Save**，
  `serve.py` 在**文件所在这台机器上**直接写进那题的 `## Comments`，顺手重新生成 html。
  **不存在「还没同步的评论」** —— md 永远是最新那份。署名下拉可现加新用户（任意 1–4 位大写缩写）。
  （serve.py 没跑时才退回浏览器兜底：面板的 Sync to md / Copy 手动送回。）
- **md 里**：`## Discussion` 写随手讨论（`> JL: …`），`## Comments` 写钉在某句话上的条目
  （`- [ ] JL 「原句」 · 260723 1100`，解决了改 `[x]`）。

被评论的原句会在正文里高亮；原文改动后引文对不上，那条会标 **⚠ anchor lost** —— 不会悄悄失效。

### sync — 干完活，同一轮里回写这一题

**板和产物必须联动，否则板就是一份过期的漂亮东西。**
在某一题名下做完任何实质工作（写了文件、跑了实验、拿到了结论），**在同一轮里**回写它：

| 回写哪 | 写什么 |
|---|---|
| `## Where we are` | 现在的实际状态。有数字给数字。 |
| `## Items to Finish` | 达到的条打勾。**没验过的不许打勾。** |
| `## Log` | 一行：`YYMMDD HHMM · 改了什么` |
| `state:` | 全部打勾 → ✅ SETTLED；有进展 → 🟡 PARTIAL；明确不做 → ⏸️ ON HOLD |
| `## Comments` | 这轮解决掉的评论，勾成 `[x]` |

然后 `python3 <skill>/build.py <板文件夹>`（或让 `watch.py` 自动跑；调法见上面 build 段）。

**还要清掉被这轮推翻的旧说法。** 板改了，别处正文里的旧描述立刻变成自相矛盾 ——
真实例子：版式早改成上下叠了，正文还写着「左右并排」；评论层已经引了 JS，另一题还写着「坚持零脚本」。
零背景读者第一眼挑出来的就是这个。

### link — 把板和它的产物连起来

板讨论的东西（一份 SKILL.md、一个脚本、另一块板）通常不在板的文件夹里。
在 `board.md` 加一段 `## Links`，声明反引号里的写法对应哪个真实路径：

```markdown
## Links
SKILL.md            ../../haipipe-board/SKILL.md
ref/q-template.md   ../../haipipe-board/ref/q-template.md
build.py            ../../haipipe-board/build.py
```

之后正文里任何 `` `SKILL.md` `` 都变成可点的链接，从板上一步跳到真东西。
也支持 `[写法](路径)` 这种普通 markdown 链接。声明过的路径不做存在性猜测 —— 写错了就是死链，自己负责。

### close — 关板

每一题都到 ✅ SETTLED 或 ⏸️ ON HOLD，这块板就关掉。
`close:` 那句话就是关板条件，写的时候要能验收，不是「差不多了」。

## 📐 一个 Q 文件

```markdown
# 短标题（短语，≤14 字）
state: 🔴 OPEN          ✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD
owner: CC               JL 显示 🧠 拍板，其他显示 🔧
method: 一句话说怎么做

## Question        一段平白话 + 2–4 个要点：在问什么 · 为什么难 · 不定会怎样  ┐
## Boundary        这题管什么、更要紧的是不管什么（选填但强烈建议）          │ 台面
## Diagram         ascii 图（可省）                                        │ 顺序
## Items to Finish 勾选清单 ＝ 什么算做完，栏头自动数出 3/5                 │ 固定
## Where we are    现在的实际状态，有数字给数字                             │
## Files           这题牵动哪些文件（选填但强烈建议）                        ┘
## Law          这题拍定的规矩      ┐
## Lesson       这题踩过的坑        │
## Glossary     这一页的生词        ├ 选填 · 折叠，不上台面
## Discussion   随手讨论            │  用不上就删整段
## Comments     钉在某句话上的评论   │
## Log          260723 1030 · 改了什么 ┘
```

**台面顺序是定死的**：先给意图（问什么 · 边界 · 什么算完），再给状态（现在到哪、动哪些文件）。
`## Question` 一节读完，一个零背景的人就该明白这题在干嘛 —— 这是这套版式的验收标准。

正文里长内容一律写成 **`- 小标题` + 缩进两格的解释**，不要一段接一段的散句；
整行加粗 `**…**` 是**组标题**（领着一串 item）。
加一题直接复制 `ref/q-template.md`（每段都标了必填/选填）；完整语法表见 `ref/board-form.md`。

> 老段名一律还认：`## Done when`＝`## Items to Finish`、`## Now`＝`## Where we are`、中文名同理。
> `## Why here` 已退役 —— 它的活并进 `## Question` 的要点，老板子里写着的收进折叠区。

## ✍️ 写法（这条最容易被跳过）

**「如果不易读，写那么多都是 rubbish。」** 详见 `ref/writing-rules.md`，最要命的三条：

1. **不许造词** —— 每个说法要么是源文档的原话，要么在 `## Glossary` 里解释过。
2. **过期的话要清掉** —— 板改了，正文里的旧说法就成了自相矛盾，零背景读者一眼就挑出来。
3. **改完要用全新 agent 冷读** —— 自己在同一个对话里读测不出问题，因为你知道太多没写进去的事。

## 🚫 不许做的

- 手改 `board.html`
- 给板重新起日期
- 删掉 `> JL:` 开头的行（解决了就在 `## Comments` 里勾 `[x]`）
- 让页面依赖 JS 才能读 —— 脚本只能做增强。
  **不变量：删掉页面里所有 `<script>`，每一题和全部正文仍然在。** `build.py` 每次生成都断言这一条。

## 📖 板 ↔ SKILL.md：怎么保持同步

这份 SKILL.md 不是凭空写的 —— 它是一块板（这个 skill 自己的
`diagram/01-boardform-260722/`）里**已定问题的结晶**。

```
   那块板（每题 Question/Now/Law/Lesson/Log）           SKILL.md
   ┌──────────────────────────────────┐   一题 ✅   ┌──────────────┐
   │ 完整设计记录：为什么、怎么来的、还没定的 │ ────────► │ 只留结论，照着做 │
   └──────────────────────────────────┘           └──────────────┘
        working record（含 🟡/🔴）                    settled 的蒸馏
```

**毕业机制**：一条 Q 到 `✅ SETTLED`，就把它 `## Law` 那段的规矩抄进 manual 对应位置 —— 操作规矩进 SKILL.md 正文，显示 / 语法这类**规格**进 `ref/`（SKILL.md 保持最短，QB1 的 Law）。

- 没定的题（🟡/🔴）**不进** manual —— 免得把「随手定的」写成铁律。
  （真踩过：`QD1` 的权限规则我一开始随手写死「只能改这一个文件」，后来被 JL 推翻成「跟 CLI 一样」。）
- 所以 SKILL.md 永远 = **已定规矩之和**，不多不少。改它之前，先看那题 `✅` 了没。
- 现在已毕业的：`QA2`（Q 文件模板）· `QA4`（幻灯片版式 → `ref/board-form.md §8`，显示规格不塞进这里）· `QA6`（评论落盘）· `QC1`（板放哪）。
  现场层的 chat/terminal（`QD1`/`QD2`/`QD3`）还 🟡，上面只放了指针，没写成规矩。

## 📚 ref/

| 文件 | 看它做什么 |
|---|---|
| `ref/q-template.md` | 加一题时直接复制的空模板 |
| `ref/board-form.md` | 完整规格：文件夹、编号、段落↔页面对应、语法表、Comments 格式、`## Links` |
| `ref/writing-rules.md` | 怎么写才是人话 + 零背景审查的提示词和收敛判据 |
| `ref/board-example.md` | 一块两题的最小示例 |

活的例子：`Tools/plugins/haipipe-toolkit/skills/0_utils/diagram/01-boardform-260722/` —— 这个 skill 自己的板。
