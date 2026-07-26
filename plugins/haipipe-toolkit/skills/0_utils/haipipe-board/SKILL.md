---
name: haipipe-board
description: >-
  Open and run a BOARD: one topic, one folder tree, and one markdown page per ruling (Q) or lifecycle stage (S), generated into a single self-contained HTML page you can read, project, share, and comment on inline. Use when a topic has several undecided questions or stages that need to be laid out and closed; when sharing work with colleagues; or when the user says board, 打开这块板, 开板, 加一题, 关板, or /haipipe-board. "打开 BOARD_FOLDER" means VIEW an existing board by rebuilding it and pushing its URL to the user's VS Code browser over the VS Code IPC socket. It does not mean creating a new board, opening board.html directly, or using file://.
metadata:
  version: "0.29.0"
  last_updated: "2026-07-26"
  summary: "A board's excalidraw round-trips, images included: the editor is seeded from fig/board.excalidraw and saves back into it one frame at a time, with pasted images kept as real files in fig/assets/ rather than base64 in the scene."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board — 一个话题，一叠问题，一页看板

**一块板 = 一个文件夹。** 里面一个 ruling/stage 一个 `.md` page，外加一页谁都打得开的
`board.html`。Q 是 ruling，S 是 lifecycle stage；两者共用一套版式，不共用关闭语义。

它取代了 `/haipipe-session`（那个是只有干活的人自己看的工作日志）。

**两条必须成立的（JL 定的）：**

- 打开就知道自己在干嘛 —— 靠 `spine`（主干）和 `## Topic`
- 知道什么时候能结束 —— 靠 `close`（关板条件）和每题的 `## Items to Finish`

## 🗂 形状

```
<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/
  board.md            标题 · spine · close · ## Topic · ## Pipeline · ## Pages
  QA1-<slug>.md       一题一个文件
  QA2-<slug>.md
  S-Seed-0-<slug>.md  命名过的 lifecycle page（有 lifecycle 才写）
  QB1-<slug>.md
  board.html          ← build.py 生成，别手改
  fig/
```

- **所属单位** = 这块板服务于谁（一个 plugin / 一个 task 文件夹 / 一篇 paper）。
  板是工作产物，skill 是交付包 —— 不放在同一个文件夹里。
- **日期是开板那天，之后永不改。** 一个文件夹一个话题，后来的讨论往里追加，不另开。
- **谁在这块板上，靠路径**：板文件夹**整棵树**里所有 `Q*.md` / `S*.md` 就是这块板的
  pages（`_`/`.` 开头的段和 `fig/` 除外）。
  `## Pages` 只管排序和分组（仍只写文件名）；漏登记的照样显示（归 ⚠️ 组）并在命令行提醒 —— **漏登记只会丑，不会丢题**。
- **Q/S 文件可以住进它讲的那个文件夹**：`4-display/QD2-….md` 和
  `4-display/S-Display-0-displays.md` 都会被发现。
  一棵已有的树（比如一篇 paper 的 `0-lifecycle/`）因此可以直接当一块板，题面贴着它讲的东西住 ——
  这种板**不套** `diagram/<NN>-…-<YYMMDD>` 的名字：树叫什么就是什么；NN+日期的规矩只管 `diagram/` 下新开的板。
- **`![[路径]]` / `![[路径#某节]]` 单独占一行**（QF1）＝把另一份文件的内容**按引用**嵌进这一题：
  生成时现读、零拷贝零漂移，板不学源文件的方言；嵌不到就地标红。详见 `ref/board-form.md` §5。
- **不要再用 Pages 里的 `doc:` 行**（原 QF2，260726 退役）：要展示别处的文件，就用上面那条
  `![[路径]]` 嵌进一个真正的 page —— 同样零拷贝，但页面有 state、有清单计数、有评论落点，
  而 doc 页三样都没有。parser 仍认 `doc:`，只是为了不让老板子炸；今天全 SPACE 一块板都没在用。
- **Paper lifecycle board 按 named S family 分组**：索引顺序固定为 `Seed → Work → Venue →
  Display → Main → Appendix → Submission`。Display 是独立的 evidence-presentation layer，
  不是 Work 的一个普通 item。这是 ownership/navigation order，不自动等于执行顺序；
  真实依赖写在 `## Pipeline`，例如 Narrative 后进入 Display，再分给 Main/Appendix。family 里的每个
  S page 是一个具体、可 CHECK 的 page；
  拦住它的 Q ruling 紧跟在该 S 后面。Seed 通常含 `S Seed` 和 `S Literature`；Main
  用数字 section；Appendix 用 `0, A, B...`；Submission 至少覆盖 reconcile、compile、
  review、submit。Submission 四页每一轮复用；外审意见让受影响的 Work/Display/Main/Appendix
  page reopen，再走同一组 reconcile → compile → review → submit，不为每轮复制一套页面。
  组标题仍以唯一 Q family 开头供页面写入按钮使用。
- **Group intro (QC2, 260724)**: in `## Pages`, plain lines between a `### ` heading and its first `.md` line introduce that group. Line 1 always shows under the group header on the index; further lines expand on click. The page's ＋Q / ＋Group / 🗄 buttons edit this structure through `POST /_board/structure` (serve.py `structure_op`); archive moves Q files to `_archive/`, never deletes.

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

⚠️ **为什么不能用 `open board.html` 或 `file://`**：Remote-SSH 的机器上 ——
**浏览器在用户的笔记本上，文件在服务器上**。`open` 只会在服务器桌面上打开，用户什么都看不到；
`file://` 指的是用户本机的盘，那儿没有这些文件。必须走上面那条 IPC，把 URL 交给用户那侧的 VS Code。
**本地机器**（不是 Remote-SSH：那两个 glob 找不到东西）就直接 `open "http://127.0.0.1:5599/<板>/board.html"` ——
走 http（评论层才活），照样不碰 `file://`。

需要 `serve.py` 在 5599 上跑着（没跑就先起，见 serve 段）。`#top` 回目录、`#QA6` 直接跳某一题、`#all` 展开全部。

### open — 开一块**新**板

1. 问清三件事：**这块板要解决什么**（→ `spine`）、**什么时候算完**（→ `close`）、
   **有哪几个 page**（几个 Q ruling；有 lifecycle 的话，还有几个 S stage）。
   这份 page 列表要用户点头才往下走 —— 这是唯一必须停下来问的地方。
2. 建 `<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/`。
3. 写 `board.md`：标题、`spine:`、`close:`、`## Topic`、`## Pipeline`、`## Pages`（三个都写上）。
4. 每个 page 都复制同一份 `ref/q-template.md`，改名决定它是哪种：
   ruling → `Q<组字母><序号>-<slug>.md`；paper lifecycle page →
   `S-<Family>-<unit>-<slug>.md`，其中 Family 是 `Seed|Work|Venue|Display|Main|Appendix|Submission`
   （例如 `S-Seed-1-literature.md`、`S-Main-3-theory.md`、`S-Appendix-A-prompts.md`）。
   普通旧板的 `S0-<slug>.md` 继续兼容。
   `<slug>` 用短英文小写（`access`、`scheduling`），跟 `ref/board-example.md` 一致。
   新开的 page 一律 `state: 🔴 OPEN`（Q 和 S 用同一套四个状态值，见下面「一个 Page」）。
   owner 按性质给：要拍板/授权的给 JL，动手干的给负责同事的姓名缩写或 CC。
   S 还必须有显式 `## Stage Contract` 和 `## Content`（Q 不写 Stage Contract，Content
   选填）。不要从 Pages 前后顺序猜上游；在 S 顶部显式写
   `requires: S-Work-1, S-Main-0`、`style-from: S-Venue-1`、`provides: ...`。
   用 `stage.py new` 创建，或 `stage.py sync` 刷新 managed contract；不要手抄上游全文。
   Pages 里 S 跟 Q 一样只写裸文件名 ——
   组标题是自由文本，单独给 stage 开一组（`### S · 这条 lifecycle`）或混进相关那组都行。
5. 生成：`build.py` 在 **skill 目录**里，不在板文件夹里，所以带上它的路径 ——
   `python3 <skill>/build.py <板文件夹>`（`<skill>` = `Tools/plugins/haipipe-toolkit/skills/0_utils/haipipe-board`）。
   **别 `cd` 进板文件夹再 `python3 build.py .`** —— 那样找不到 build.py。
   生成只往 `board.html` 写，不碰你的 `.md`（md 是唯一来源）。
6. **按 view 那一节把页面推到用户的 VS Code 浏览器** —— 不要只说「打开 board.html」。

### add — 加一题

复制 `ref/q-template.md` → 新文件名 → 写进 `board.md` 的 `## Pages` → 重新生成。
忘了写进 Pages 也不会丢，只会归到 ⚠️ 组。
文件夹题（QC3）：把新文件放进它讲的那个文件夹；Pages 仍只写文件名，全板文件名要唯一。
页面上的 ＋Q 一律把文件生成在**板根** —— 要住进哪个文件夹，自己挪（Pages 行不用改）。

### stage — 新建或刷新 lifecycle page

S page 的“上一阶段要求”和 writing style 只能来自显式引用，不能从 Pages 邻接关系猜。
`build.py` 永远只读 Markdown；真正写文件的是 `stage.py`：

```bash
python3 <skill>/stage.py new <board-dir> \
  --family Main --unit 7 --slug results --title "S Main 7 · Results" \
  --requires S-Work-1,S-Main-0,S-Display-0 \
  --style-from S-Venue-1 \
  --provides "reader-facing results section" \
  --directory 5-section-edit/6-results \
  --group "QE · Main Group"

python3 <skill>/stage.py sync <board-dir> S-Main-7
python3 <skill>/stage.py sync <board-dir> --all
python3 <skill>/stage.py check <board-dir>
```

`new` 生成 S file、加入指定 Pages group，并写入 managed `## Stage Contract`。
`sync --all` 按显式 `requires` / `style-from` dependency graph 做 topological sync，
不按 Pages 顺序同步。`sync` 只替换 `<!-- haipipe:contract:start -->` 到 `end` 之间的区块，不碰 Content、
Items、Where we are 或作者写的 `### Provides`。上游源文件一变，build/check 会报
`Stage Contract is stale`；显式 sync 后才清掉。上游最好在自己的 Stage Contract 写
短的 `### Provides`；writing source 写短的 `### Writing Style`。没有这些时，生成页
保留源链接并明确提示补 contract，绝不复制整页 Content 猜答案。

### build — 生成

`build.py` 在 skill 目录里（不在板文件夹）。带路径调，别 cd 进板文件夹跑 `build.py .`：

```bash
python3 <skill>/build.py <board 文件夹>     # 生成一次（<skill> = .../0_utils/haipipe-board）
python3 <skill>/watch.py <board 文件夹>     # 盯着，改任何 .md 自动重新生成
```

生成只用标准库，系统自带的 `python3` 就够（3.9 也行）。
**只有 `serve.py` 要仓库的 `.venv`** —— 它跑 `claude_agent_sdk`，那个要 3.10+。别把两条命令的解释器搞混。

**md 是唯一来源。** 永远不要手改 `board.html`。

### serve — 让板活起来（现场层）

一个服务器管所有板 —— 服务的是仓库根，不是某一块板：

```bash
.venv/bin/python <skill>/serve.py --root <仓库根> --port 5599
```

跑起来之后，板不只是能读，还能：**评论直接落盘**（下一节就靠它）、在某一题上**开 chat 或 terminal 当场干活**、给某一题的 🖼 Diagram **贴一张 excalidraw 画布**（写进 md 的就是作者手写的那一行；`QD7` 还在定型）。
⚖️ 一题一 session · 一 session 一窗口 · N 题 N 终端 —— 详见板的 `QD1` 的 `## Law`。

> chat（受限抽屉，`QD2`）和 terminal（真 CLI，`QD3`）这套**还在 QD 组定型中**。
> 用法以那几题为准，别当成定死的规矩（见文末「板 ↔ SKILL.md」）。

### excalidraw — 一块板一个 scene，一题一个 frame

**一块板只有一个 `fig/board.excalidraw`，每个 page 在里面占一个 frame。**
绝不拆成一题一个文件：只有同一张画布才说得清 page 之间的**关系**，
而那正是画图唯一比 ASCII 强的地方（`QA4a`）。

```bash
docker run --rm -d -p 5610:80 excalidraw/excalidraw     # 编辑器，跑一次就行
python3 <skill>/xcal.py <board 文件夹>                   # 按 board.md 重建 scene
python3 <skill>/xcal.py <board 文件夹> --wire            # 顺手把每个 frame 的 URL 写进它那题的 ## Diagram
```

`board.md` 声明一次编辑器地址：`excalidraw: http://127.0.0.1:5599/_excalidraw`
（`serve.py` 把容器代理在这个路径下，这样它走的是**唯一被转发的那个端口**，见 `QE6`）。
两种 URL 指的是同一个文件：不带 `?frame=` 是整块板，**画关系就在这儿画**；
带 `?frame=<题号>` 是那一题的 frame，由 `serve_frame()` 现算，页面上嵌的就是它。

**画的东西会存回仓库**，靠的是 `serve.py` 往它代理的那个 app 里注入 `assets/xcal-boot.js`：
开源版 Excalidraw 没有「存到服务器」这回事，它从 `#url=` 读、存进浏览器 ——
所以那个脚本干脆把浏览器的 storage 接管了：进来时按文件把场景喂进去（因此**不再弹
「Replace my content」**），编辑时每 1.5 秒把变化 POST 到 `/_board/excalidraw-save`。
带 `frame=` 的保存**只换那一个 frame 的那一片**，其余 27 个原样不动 —— 这才是
「一块板一个 scene」能被任何一页编辑的原因。

⚖️ **页面里嵌的那个是只读的，写只发生在 ✏️ 那个标签页。**
一块板一页一个 iframe，它们同源同一个 storage key，可编辑的话就是 28 个编辑器互相覆盖。
所以：iframe 用内存 storage（能拖能缩放，什么都不存）；
点「✏️ Edit this frame」开的新标签页才是唯一能写的，并且会上锁，第二个标签页自动退回只读。

**贴进去的图片也存得下来**，但不塞进 scene 里：字节写到 `fig/assets/<fileId>.<ext>`，
scene 里只留一个指针（JL 260726 提的这个文件夹）。
Excalidraw 自己是把 base64 塞在文档里的 —— 一张截图就是几 MB，之后每挪一个框 git 都要重 diff 一遍，
版本库扛不住。读的时候 `serve.py` 再还原成 dataURL，所以**从服务器取到的 scene 是自包含的**，
编辑器完全不知道这回事。
⚠️ 代价：**直接用 VS Code / Obsidian 插件打开磁盘上那个文件，图片是空的**（只有指针）。

⚠️ 两个已知边界：**种子文本改了会被下次 `xcal.py` 覆盖回去**（画在旁边的东西不受影响）；
**删掉图片元素，它的文件还留在 `fig/assets/` 里**（不自动删，删了就没法撤销）。

每个 frame 会**用那题 `## Diagram` 里第一段 ``` ASCII 图当种子**填进去 ——
frame 空着的话，读的人分不清是「还没画」还是「功能坏了」（JL 260726 就是这么撞上的）。
种子是**单向**的：md 永远是唯一来源，画布里改了不会回流。

重跑是安全的，这也是它敢做成脚本的原因：id 稳定（`frame-QA4a`），
人挪过的 frame 保住位置，人画的东西原样带走，**页面已经退休的 frame 会被删掉**。
`--fresh` 是唯一会毁东西的模式（重排全部、丢掉手画内容），所以它永远不是默认。

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

⚠️ **触发条件是「这一轮做了实质的活」，不是「这一轮打开了某个 page」。**
一整段 /haipipe-board 会话里做的每件实质工作，都归属于某一个 page —— 哪怕这活是从
聊天里的一句话开始的，从头到尾没提过题号。所以顺序是：**先认领是哪一题，再干活，
干完在同一轮回写**；一件活如果哪一题都不归，那它本身就是一道该开的新题。

真实事故（JL 260726）：QA4a 的整条本地 excalidraw 路线当天建完并跑起来了，`QA4a` 却还写着
`state: 🔴 OPEN` 和「Nothing is built and nothing is decided」。活是对的，回写没做，
于是板上写的和机器上跑的是两件事 —— 这正是「过期的漂亮东西」。
`check.py` 的 `open-with-done-items` / `partial-with-nothing-open` 就是抓这个的，
但它只看得见 state 和勾，看不见正文，所以它是兜底，不是替代。

**「做完了」= 回写完了。** 没回写就跟 JL 报完成，等于报了一件板上不存在的事。

在某个 page 下做完任何实质工作（写了文件、跑了实验、拿到了结论），**在同一轮里**回写它：

| 回写哪 | 写什么 |
|---|---|
| `## Where we are` | 现在的实际状态。有数字给数字。 |
| `## Items to Finish` | 达到的条打勾。**没验过的不许打勾。** |
| `## Log` | 可选的一行历史：`YYMMDD HHMM · 改了什么`；没有历史需求就不建 |
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

每个 page 到 `✅ SETTLED` 或 `⏸️ ON HOLD`，并满足 `close:`，这块板才关掉。
Q 和 S 用的是同一套状态值，翻到 ✅ 的凭据不同：Q 要 checkbox 全闭合，S 要它自己的
**human gate 过了**（⏸️ 则是明确搁置）。首页按 named family 分别统计 S 里的 ✅。
`close:` 那句话就是关板条件，写的时候要能验收，不是「差不多了」。

## 📐 一个 Page

```markdown
# 短标题（短语，≤14 字）
state: 🔴 OPEN          ✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD
owner: CC               JL 显示 🧠 拍板，其他显示 🔧
method: 一句话说怎么做

## Question        第一段是真问句；后面一段解释为什么重要                     ┐ 🧭 Opening
## Boundary        这题管什么、更要紧的是不管什么（选填但强烈建议）          ┘
## Stage Contract  S 必填；上游 inputs + writing style，managed block          ┐
## Diagram         ascii 图（可省）；独立一节，默认折叠                       │
## Content         S 必填、Q 选填；`###` 一块能单独折的 division，`####` 一个段落  │
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

**台面上的层次顺序是定死的**，Q 和 S 一样：
`Opening → Diagram → Content → Items to Finish → Where we are`（Files 跟在状态后面）。
Opening 放 Question 的第一段问句和 optional Boundary；optional Diagram 是独立一节，
默认折叠，点节名才展开。Q page 的 Question 解释段自动成为 Content 的第一个
“Why this matters” subsection（默认展开）。S page 的 Opening 里还有 “Why this matters”、
optional 的 `### Stage Record`、以及整个 `## Stage Contract` —— **这几行全部默认折叠**
（JL 260725：台面上只留那句问句），所以 Stage Contract 不再单独占一节。S 的其余
Content 仍在 `📚 Content`，节标题显示 stage 名（`📚 Content · Main 7 §6 Results`）而不是数
subsection；Q 的显式 Content 选填、标题仍显示数量。这个标题是从 `# 短标题` 推出来的，
所以 artifact 自己的编号跟板上的 index 对不上时，标题写成 `S Main 7 · §6 Results`，两个号
都摆出来。
**S 的 `## Content` 只放这个 stage 自己产出的东西**（JL 260725）：继承来的 venue/writing
contract 归 `## Stage Contract`（写在 managed 标记之后，sync 不会动），已定的更正归
`## Where we are`，还欠的归 `## Items to Finish`。旧板仍可写 `## Question`，也认
`## Opening` 这个别名。

**一套版式，两种工作流：**

- `Q*.md` = ruling。checkbox 全闭合后才可 `✅ SETTLED`。
- `S*.md` = lifecycle stage。`## Content` 是 stage substance（S 必填）；former Q-consumer questions
  become recognizable `Q-Stage-n` checklist records inside `## Items to Finish`; stage closes only
  at its human gate —— 也就是 S 的 `✅` 表示 gate 过了，首页按 family 据此计数。
- S 的 `## Stage Contract` 不属于 Content。它只带显式 `requires` 的上游 acceptance
  conditions 和 `style-from` 的写作规范；managed 部分由 `stage.py` 写，作者拥有
  `### Provides`。Pages 顺序绝不是 dependency inference。
- 两种 page **共用同一套 `state:` 四个值**，没有第五个：新开的都是 🔴 OPEN，🟡 在做，
  ⏸️ 明确搁置，✅ 的凭据按上面两条各自算。别在 `state:` 里写 `human-gated` 这种自造词。
- Q-consumer checkbox means the answer landed, was interpreted, and was woven into Content. A
  deferred item closes only after its forward pointer is recorded.
- `## Where we are` summarizes the actual stage state. It does not copy every consumer answer.

正文里长内容一律写成 **`- 小标题` + 缩进两格的解释**，不要一段接一段的散句；
整行加粗 `**…**` 是**组标题**（领着一串 item）。

**`## Content` 里只有两级，深浅靠编号不靠标题级数**（JL 260725）：`###` 是一块能单独折的
division，`####` 是它里面的一个段落、永远是这一级。页面只折一层，再深一级就把整节压成
一个盒子。一块 division 只在自己确实有内容时才写：flat 的节写一个 `### §1 Introduction`
领着段落，有 subsection 的节直接从 `### §6.1` 开始。好处是不读正文也能校验：带点的 `###`
个数就是 subsection 数。`####` **没有图标** —— 🔹 是组标题的，别拿 `**…**` 当段落标题写；
紧跟 `####` 的整行 `(…)` 是这一段的活儿，灰斜体留在台面上当扫读钩子。
加一题直接复制 `ref/q-template.md`（每段都标了必填/选填）；完整语法表见 `ref/board-form.md`。

> 老段名一律还认：`## Done when`＝`## Items to Finish`、`## Now`＝`## Where we are`、中文名同理。
> `## Why here` 已退役 —— 它的活并进 `## Question` 的解释段并渲染到 Content；
> 老板子里写着的旧段仍收进底部折叠区。

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
- 现在已毕业的：`QA2`（Q/S 共用源模板 → `ref/q-template.md`）· `QA4`（Q/S 共用 page 版式 → `ref/board-form.md §8`，显示规格不塞进这里）· `QA6`（评论落盘）· `QC1`（板放哪）· `QC3`（Q 可住进自己的文件夹）· `QB5`（Python 按页拆进 `src/`）。
  现场层的 chat/terminal（`QD1`/`QD2`/`QD3`）还 🟡，上面只放了指针，没写成规矩。嵌入语法（原 `QF1`）已定进 `ref/board-form.md §5`；QF1 这个 page 本身 260725 退役，见板上 QF 组的说明。

## 📚 ref/

| 文件 | 看它做什么 |
|---|---|
| `ref/q-template.md` | Q/S 共用 page 模板（历史文件名保留，避免旧链接失效） |
| `ref/board-form.md` | 完整规格：文件夹、编号、段落↔页面对应、语法表、Comments 格式、`## Links` |
| `ref/writing-rules.md` | 怎么写才是人话 + 零背景审查的提示词和收敛判据 |
| `ref/board-example.md` | 一块两题的最小示例 |
| `stage.py` | 显式创建/同步 S page 的 inherited requirements 与 writing style |
| `check.py` | 结构自查（`QA9` 的机器那一半）：段落、state、引用、渲染出的 html、模板覆盖 |
| `xcal.py` | 一块板一个 `fig/board.excalidraw`，一题一个 frame；`--wire` 把 URL 写回各题 |

活的例子：`Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/` —— 这个 skill 自己的板（平铺形）。
嵌套形（Q rulings + S stages）的活例子：`examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/`。
