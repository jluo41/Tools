# haipipe-board · v0.51.0
state: 🟡 in flux
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Question
haipipe-board is a shipped skill: what does it still owe, and is it healthy?

Write here what this skill is for in one paragraph a stranger could follow, why it exists as its own skill rather than as part of its neighbour, and what would have to be true for it to be considered finished.
The generated sections answer what it IS; only this one can answer whether it is any good.

## Diagram
<!-- haipipe:skill:tree:start d551d6c8ba2a8eed board/haipipe-board -->

```
haipipe-board/
  assets/
    board-mark.svg            44 ln
    board.css               1113 ln  palette + type follow html-ppt's academic-report; layout is body.single
    board.js                2238 ln  Comment layer — PURE ENHANCEMENT. The prose is already real HTML;
    xcal-boot.js             264 ln  Injected by serve.py into the proxied Excalidraw app (QA4a).
  ref/
    board-example.md         111 ln  最小示例 —— 一块两题的板
    board-form.md            389 ln  Board form — 完整规格
    q-template.md            278 ln  Short title (a phrase, not a sentence)
    writing-rules.md          80 ln  Writing rules — how to write so it reads like human language
  src/
    __init__.py                3 ln  haipipe-board src/ (QB5): build.py and serve.py are thin entries; the code
    body.py                  951 ln  The board's body grammar -> html (ref/board-form.md §5): inline marks, link
    common.py                109 ln  Shared constants + tiny helpers (QB5). Used by every page module AND by
    dialect_paper.py        1004 ln  The `paper` dialect: resolve a manuscript's inline markers at BUILD time.
    page_board.py            238 ln  The cover + index + whole-page assembly (QB5: render(), asset inlining,
    page_question.py         582 ln  One question -> one <section class="slide q"> card (QB5: the card chunk of
    page_stage.py            262 ln  Stage/source content on a slide (QF1, JL 260724): the `![[path]]` /
    parse.py                 328 ln  md -> data (QB5): board.md, Q files, folder discovery, legacy blocks.
    stage_contract.py         98 ln  Managed requirements and writing-style contracts for S pages.
  vendor/
    xterm/
      addon-unicode11.js       2 ln
      xterm.css              285 ln  * Copyright (c) 2014 The xterm.js authors. All rights reserved.
      xterm.min.js             2 ln
  build.py                   127 ln  board folder -> board.html (static content; scripts are optional enhancement).
  CHANGELOG.md              1227 ln  haipipe-board — Changelog
  check.py                   519 ln  check.py — the structural half of QA9, run against one board.
  refs.py                     73 ln  Render a paper's real bibliography, once, into a cache the board can read.
  regroup.py                 142 ln  Move a board's root pages into one named folder per Q group (QA1, JL 260726).
  serve.py                  2478 ln  Serve boards AND accept comment writes — from the machine the files live on.
  SKILL.md                   546 ln  /haipipe-board — 一个话题，一叠问题，一页看板
  skillpage.py               728 ln  One skill folder -> one Q page on a board (QC5, opened by JL 260726).
  stage.py                   378 ln  Create and synchronize lifecycle S pages with explicit inherited contracts.
  status.py                  240 ln  Render the three-line closing block for one Board-attached session.
  test_activity.py           176 ln  Focused regression tests for QD8 board activity timing.
  test_sentence_chat.py       80 ln  Contract checks for render-local sentence addressing and focused Q chat.
  test_sentence_editing.py    85 ln  Regression tests for sentence-local comments and tracked edits.
  test_status.py             150 ln
  watch.py                    55 ln  Watch a board folder and rebuild board.html whenever a .md changes.
  xcal.py                    324 ln  board.md + the pages' ASCII figures -> ONE `fig/board.excalidraw` (QA4a).
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)

  A BOARD IS A FOLDER.  md is the only source; board.html is output.
  ─────────────────────────────────────────────────────────────────
  board.md          spine · close · Topic · Pipeline · Pages
  QA-<group>/       one .md per ruling (Q) or lifecycle stage (S)
        │
        │  build.py          md -> ONE self-contained board.html
        ▼                    asserts: strip every <script>, all prose remains
  board.html
        │
        │  watch.py          rebuild on any .md change
        │  serve.py          the LIVE layer, one server for the whole repo
        ▼
  http://…:5599/<board>/board.html
        │
        ├── comments land back in the md            (QA6)
        ├── ＋Q / ＋Group / archive edit board.md    (QC2)
        ├── an excalidraw frame per page            (QA4a · QD7)
        ├── chat + terminal per page                (QD1-3)
        └── ACTIVITY counts updates from ## Log     (QC2 §8)

  WRITERS, all of them into markdown, never into board.html
  ─────────────────────────────────────────────────────────
  stage.py      new/sync/check   an S page + its managed Stage Contract
  skillpage.py  new/sync/check   a skill folder -> this very page
  regroup.py    [--apply]        root pages -> one folder per Q group
  xcal.py       [--wire]         one scene per board, one frame per page

  READ-ONLY
  ─────────
  check.py      structure · dead links · stale claims   (QA9)
  status.py     the three-line closing block            (QD9)
  refs.py       a paper's bibliography, cached

  THE INVARIANT EVERY PART OBEYS
  ──────────────────────────────
  the markdown is the single source. build.py only reads it, the live
  layer only appends to it, and nothing but build.py writes board.html.
```

## Content
<!-- haipipe:skill:body:start d551d6c8ba2a8eed board/haipipe-board -->

**haipipe-board** · `0.51.0` · last shipped 2026-07-29

- folder   `board/haipipe-board/`
- tools    not declared
- summary  Reader-facing Board links honor the machine-local HAIPIPE_BOARD_URL without requiring env.sh to be sourced (JL 260729).

### SKILL.md




**一块板 = 一个文件夹。** 里面一个 decision/stage 一个 `.md` page，外加一页谁都打得开的
`board.html`。Q 是 decision，S 是 lifecycle stage（JL 260729：不再叫 ruling）；两者共用一套版式，不共用关闭语义。

它取代了 `/haipipe-session`（那个是只有干活的人自己看的工作日志）。

**两条必须成立的（JL 定的）：**

- 打开就知道自己在干嘛 —— 靠 `spine`（主干）和 `## Topic`
- 知道什么时候能结束 —— 靠 `close`（关板条件）和每题的 `## Items to Finish`


- 1 · 🗂 形状
      ```
      <所属单位>/diagram/<NN>-<主题>-<YYMMDD>/       # task / project / paper
      <plugin>/skills/diagrams/<NN>-<主题>-<YYMMDD>/ # plugin skill-design Board
        board.md                    标题 · spine · close · ## Topic · ## Pipeline · ## Pages
        QA-<组名 slug>/             ← 一个 group 一个文件夹（默认，JL 260726）
          QA1-<slug>.md             一题一个文件
          QA2-<slug>.md
        QB-<组名 slug>/
          QB1-<slug>.md
          S-Seed-0-<slug>.md        命名过的 lifecycle page（有 lifecycle 才写）
        board.html                  ← build.py 生成，别手改；跟 board.md 一样留在板根
        fig/
      ```
      - **group folder 是默认的（JL 260726 拍板）**：从第一页起就一个 group 一个文件夹，
        名字是 `Q<组字母>-<组标题的 slug>`（`QA-defining-a-board/`），**不是光秃秃的 `QA/`** ——
        只写 `QA/` 等于把 id 抄第二遍，读者认不出来的恰恰是标题那半截。
        membership 从 260722 起只看路径不看注册，所以搬进文件夹是一次纯 `mv`：`## Pages` 照旧
        只写裸文件名，board.md 一个字都不用改，渲染出来除了写回用的路径属性完全一致（30 页实测）。
        页面上的 ＋Q 会写进这一组已经住的那个文件夹；新开的 group 由它第一页现开一个带名字的文件夹。
        搬一整块旧板：`python3 <skill>/regroup.py <板文件夹> --apply`（不带 `--apply` 是 dry run）。
        **⚠️ 搬完跑一次 `check.py`**：`## Pages` 写裸文件名不受影响，但 `## Links` 写的是真路径，
        跨板指到别人家某一页的那些会断（260726 搬 154 页断了 17 条，全修好了）。
        **已经按文件夹分好的板别动**，比如 paper 的 `0-lifecycle/`：`0-seed/ 1-work/ 3-display/`
        既是 subject folder 又是 S family，这条规矩它本来就满足，编号还多带了 lifecycle 顺序。
      - **所属单位** = 这块板服务于谁。task、project、paper 的板默认放在自己的 `diagram/`；
        同一个 plugin 里用来设计 skill 的板集中放在该 plugin 的 `skills/diagrams/`。
        两种位置都把板和它描述的 skill 分开：板是工作产物，skill 是交付包。
      - **NN 只给同一 topic series 排序，不是全局编号。** 一个新 topic 从 `01` 开始；
        同一 topic 后续另开板才用 `02`。所以共享的 `skills/diagrams/` 里可以有多个不同 topic 的 `01-*`。
      - **日期是开板那天，之后永不改。** 一个文件夹一个话题，后来的讨论往里追加，不另开。
      - **谁在这块板上，靠路径**：板文件夹**整棵树**里所有 `Q*.md` / `S*.md` 就是这块板的
        pages（`_`/`.` 开头的段和 `fig/` 除外）。
        `## Pages` 只管排序和分组（仍只写文件名）；漏登记的照样显示（归 ⚠️ 组）并在命令行提醒 —— **漏登记只会丑，不会丢题**。
      - **Q/S 文件可以住进它讲的那个文件夹**：`4-display/QD2-….md` 和
        `3-display/QD2-….md` 和 `3-display/S-Display-0-design.md` 都会被发现。
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
        拦住它的 Q decision 紧跟在该 S 后面。Seed 通常含 `S Seed` 和 `S Literature`；Main
        用数字 section；Appendix 用 `0, A, B...`；Submission 至少覆盖 reconcile、compile、
        review、submit。Submission 四页每一轮复用；外审意见让受影响的 Work/Display/Main/Appendix
        page reopen，再走同一组 reconcile → compile → review → submit，不为每轮复制一套页面。
        组标题仍以唯一 Q family 开头供页面写入按钮使用。
      - **Group intro (QC2, 260724)**: in `## Pages`, plain lines between a `### ` heading and its first `.md` line introduce that group. Line 1 always shows under the group header on the index; further lines expand on click. The page's ＋Q / ＋Group / 🗄 buttons edit this structure through `POST /_board/structure` (serve.py `structure_op`); archive moves Q files to `_archive/`, never deletes.

- 2 · 🧭 Session attachment and Closing Block
      Once this skill is loaded for a Board, make the attachment visible.
      **Direct Board session:** end every user-visible reply with the exact
      three-line Markdown block emitted by `status.py`; put no prose after it. This
      includes progress updates, questions, blocked replies, and the final handoff.
      **Composed session:** when an explicitly enclosing first-class skill calls
      `haipipe-board` and defines one canonical closing block for the combined
      session, the enclosing contract takes precedence. Do not append a second Board
      strip. The enclosing block MUST preserve the Board attachment with a deep
      `board:` link to the active page and must remain the only closing block.
      `haipipe-paper` is the canonical composed case. Calling Board still transfers
      no ownership of Board files, rendering, or write-back to the enclosing skill.
      Resolve the attachment in this order:
      1. the Board/page attachment injected by `serve.py`;
      2. an explicit Board path, page path, page id, or group in the request;
      3. the nearest `board.md` above the current working path;
      4. the attachment already established earlier in this conversation.
      If more than one Board remains plausible, do not guess: report a blocked
      attachment and ask which Board to use.
      The strip uses a small closed vocabulary:
      - `queue` = the page group declared by `board.md ## Pages`; a page derives its
        queue automatically, a group is its own queue, and whole-Board work is
        `board-level · cross-group`.
      - `focus` = `board | group | page`.
      - `mode` = `discussion | sourcing | implementation | review | status`.
      - `status` = `ready | working | blocked | done`.
      Sourcing never floats. `mode=sourcing` must name a page or page group that owns
      the evidence; whole-Board sourcing without a queue is blocked.
      Render the closing block immediately before replying:
      ```bash
      python3 <skill>/status.py <BOARD_FOLDER> \
        --focus <board|group:ID|PAGE_ID> \
        --mode <discussion|sourcing|implementation|review|status> \
        --status <ready|working|blocked|done> \
        --next "<one concrete next action>"
      ```
      Its complete shape is deliberately only three lines:
      ```markdown
      🧭 [BOARD · QUEUE/FOCUS](deep-link)
      ✅ done · implementation
      → one concrete next action
      ```
      Do not repeat labels, the page title, source file, or raw URL. The link wraps
      the attachment on line 1; queue and focus use their short ids.
      The Board files remain the durable record. Do **not** create a shared
      `STATUS.md`: concurrent sessions would overwrite one another and stale live
      state would look authoritative. When discussion changes a decision, item,
      comment, or log, still run the normal `sync` action in the same round; the
      closing block does not replace write-back.

- 3 · 🔨 动作
      离线（只要 `build.py`）：**view · open · add · build · sync · link · close**
      现场（要 `serve.py` 跑着）：**serve · comment**
      > **「打开 <某块板>」= view（看已有的），不是 open（开新的）。** 用户给了一个已存在的
      > 文件夹路径就走 view；只有要新建时才走 open。

- 3.1 · view — 打开一块已有的板（最常用）
      用户说「打开 `<板文件夹>`」时做这三步，**别只丢一句「打开 board.html」就完事**：
      1. **先重新生成**，免得页面是旧的：
         `python3 <skill>/build.py <板文件夹>`
      2. **推到用户的 VS Code 浏览器**（下面那段是唯一真正有效的方式，见 ⚠️）：
      ```bash
      BD=<板文件夹相对仓库根的路径>          # 例：Tools/plugins/.../diagram/01-boardform-260722
      BOARD_BASE_URL="${HAIPIPE_BOARD_URL:-$(sed -n 's/^[[:space:]]*export[[:space:]]*HAIPIPE_BOARD_URL=//p' env.sh | tail -1)}"
      BOARD_BASE_URL="${BOARD_BASE_URL:-http://127.0.0.1:5599}"
      S=$(ls -t "$TMPDIR"/vscode-ipc-*.sock 2>/dev/null | head -1)
      B=$(ls -t ~/.vscode-server/cli/servers/*/server/bin/helpers/browser.sh 2>/dev/null | head -1)
      VSCODE_IPC_HOOK_CLI="$S" "$B" "$BOARD_BASE_URL/$BD/board.html#top"
      ```
      3. 顺手报一句板的状态：几题、几条未解决评论、卡在哪。
      ⚠️ **为什么不能用 `open board.html` 或 `file://`**：Remote-SSH 的机器上 ——
      **浏览器在用户的笔记本上，文件在服务器上**。`open` 只会在服务器桌面上打开，用户什么都看不到；
      `file://` 指的是用户本机的盘，那儿没有这些文件。必须走上面那条 IPC，把 URL 交给用户那侧的 VS Code。
      **本地机器**（不是 Remote-SSH：那两个 glob 找不到东西）就直接
      `open "$BOARD_BASE_URL/<板>/board.html"` ——
      走 http（评论层才活），照样不碰 `file://`。
      `BOARD_BASE_URL` 和每次回复末尾的 `status.py` 使用同一个 reader-facing setting：
      当前环境的 `HAIPIPE_BOARD_URL` 优先，其次只读取仓库根 `env.sh` 中这一项，最后才回退到
      `http://127.0.0.1:5599`。不要为了某一台机器把 Tailscale IP 写进共享的 skill source。
      需要 `serve.py` 在 5599 上跑着（没跑就先起，见 serve 段）。`#top` 回目录、`#QA6` 直接跳某一题、`#all` 展开全部。

- 3.2 · open — 开一块**新**板
      1. 问清三件事：**这块板要解决什么**（→ `spine`）、**什么时候算完**（→ `close`）、
         **有哪几个 page**（几个 Q decision；有 lifecycle 的话，还有几个 S stage）。
         这份 page 列表要用户点头才往下走 —— 这是唯一必须停下来问的地方。
      2. 选位置并建文件夹：task/project/paper 用
         `<所属单位>/diagram/<NN>-<主题>-<YYMMDD>/`；plugin skill-design Board 用
         `<plugin>/skills/diagrams/<NN>-<主题>-<YYMMDD>/`。同一 topic series 的 NN 递增，
         不同 topic 都可从 `01` 开始。
      3. 写 `board.md`：标题、`spine:`、`close:`、`## Topic`、`## Pipeline`、`## Pages`（三个都写上）。
      4. 每个 page 都复制同一份 `ref/q-template.md`，改名决定它是哪种：
         decision → `Q<组字母><序号>-<slug>.md`；paper lifecycle page →
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
         `python3 <skill>/build.py <板文件夹>`（`<skill>` = `Tools/plugins/haipipe-toolkit/skills/board/haipipe-board`）。
         **别 `cd` 进板文件夹再 `python3 build.py .`** —— 那样找不到 build.py。
         生成只往 `board.html` 写，不碰你的 `.md`（md 是唯一来源）。
      6. **按 view 那一节把页面推到用户的 VS Code 浏览器** —— 不要只说「打开 board.html」。

- 3.3 · add — 加一题
      复制 `ref/q-template.md` → 新文件名 → 写进 `board.md` 的 `## Pages` → 重新生成。
      忘了写进 Pages 也不会丢，只会归到 ⚠️ 组。
      文件夹题（QC3）：把新文件放进它讲的那个文件夹；Pages 仍只写文件名，全板文件名要唯一。
      页面上的 ＋Q 一律把文件生成在**板根** —— 要住进哪个文件夹，自己挪（Pages 行不用改）。

- 3.4 · stage — 新建或刷新 lifecycle page
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

- 3.5 · build — 生成
      `build.py` 在 skill 目录里（不在板文件夹）。带路径调，别 cd 进板文件夹跑 `build.py .`：
      ```bash
      python3 <skill>/build.py <board 文件夹>     # 生成一次（<skill> = .../board/haipipe-board）
      python3 <skill>/watch.py <board 文件夹>     # 盯着，改任何 .md 自动重新生成
      ```
      生成只用标准库，系统自带的 `python3` 就够（3.9 也行）。
      **只有 `serve.py` 要仓库的 `.venv`** —— 它跑 `claude_agent_sdk`，那个要 3.10+。别把两条命令的解释器搞混。
      **md 是唯一来源。** 永远不要手改 `board.html`。
      Board 的共享标记住在 `assets/board-mark.svg`。`build.py` 把它内联进页面标题，并把同一份
      SVG 编成浏览器 favicon，所以 `board.html` 仍然是一份离线可用的自包含文件；不要把标记复制
      进每块板的文件夹。默认配色在 `assets/board.css` 的 `--board-mark-*` tokens 里，换配色只改
      这些 tokens，不改 SVG 的形状。

- 3.6 · serve — 让板活起来（现场层）
      一个服务器管所有板 —— 服务的是仓库根，不是某一块板：
      ```bash
      .venv/bin/python <skill>/serve.py --root <仓库根> --port 5599
      ```
      `HAIPIPE_BOARD_URL` 只决定交给读者的 domain；listener 仍由 `--host` 单独控制。
      如果 reader URL 是 Tailscale IP，启动时必须显式传同一个 `--host <tailscale-ip>`。
      Board 没有认证，且 `/_term/` 是真实 shell，所以共享 source 的 listener 默认仍是 loopback。
      跑起来之后，板不只是能读，还能：**评论直接落盘**（下一节就靠它）、在某一题上**开 chat 或 terminal 当场干活**、给某一题的 🖼 Diagram **贴一张 excalidraw 画布**（写进 md 的就是作者手写的那一行；`QD7` 还在定型）。
      ⚖️ 一题一 session · 一 session 一窗口 · N 题 N 终端 —— 详见板的 `QD1` 的 `## Law`。
      > chat（受限抽屉，`QD2`）和 terminal（真 CLI，`QD3`）这套**还在 QD 组定型中**。
      > 用法以那几题为准，别当成定死的规矩（见文末「板 ↔ SKILL.md」）。

- 3.7 · excalidraw — 一块板一个 scene，一题一个 frame
      **一块板只有一个 `fig/board.excalidraw`，每个 page 在里面占一个 frame。**
      绝不拆成一题一个文件：只有同一张画布才说得清 page 之间的**关系**，
      而那正是画图唯一比 ASCII 强的地方（`QAa2`，原 QA4a）。
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
      所以那个脚本干脆把浏览器的 storage 接管了：进来时按文件把场景喂进去（因此**不再弹 「Replace my content」**），编辑时每 1.5 秒把变化 POST 到 `/_board/excalidraw-save`。
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
      重跑是安全的，这也是它敢做成脚本的原因：id 稳定（`frame-QAa2`），
      人挪过的 frame 保住位置，人画的东西原样带走，**页面已经退休的 frame 会被删掉**。
      `--fresh` 是唯一会毁东西的模式（重排全部、丢掉手画内容），所以它永远不是默认。

- 3.8 · comment / edit — 句子上的评论和编辑（要 serve.py 跑着）
      - **评论**：hover 一句 → 点右侧 `＋`，或者选中句内文字 → 点「💬 Comment」→ 写评论 → **Save**。`serve.py`
        把它直接写在**那一句的正下方**：`> JL: comment · 260729 1502`，然后重建 html。
        没有底部评论箱，也不需要在不同句子的评论里找上下文。`## Discussion` 仍只写不钉句子的随手讨论。
      - **编辑**：double-click 一句 → 改字 → Save。正文变成最终句子；它下面自动新增一条完整
        sentence diff：`> ✎ Whole sentence with ~removed~ *added* words. · JL · 260729 1502`。
        `~…~` 是删掉的词，`*…*` 是新加的词。每次编辑一行，不另建 History。触屏设备也可从
        句子的 `⋯` 菜单进入 Edit；单击正文不占用，仍可正常选字和复制。
      - **Content 地址**：只给 `## Content` 编址。每个 `###` division 是 `Cn`；它里面的 `####`
        heading 是终止节点 `Cn.Hn`，正文 paragraph 是它的 sibling，sentence 地址是 `Cn.Pn.S1`。
        所以 `QAb3.C1.H1` 和 `QAb3.C1.P1.S1` 都合法，`QAb3.C1.H1.P1.S1` 永远不合法。
        当前一条 source line 就是一句，因此每个 P 只有 `S1`；保留 S 层是为了将来一段多句。
      - **句子操作条**：pointer 设备 hover/focus 一句 → 右侧淡入 `Cn.Pn.S1 ＋ 💬`；`＋` 在句下
        打开 Comment，`💬` 打开 Chat。touch 设备只常驻一个低调的 `⋯`，展开后显示完整地址和
        Comment / Chat / Edit，避免三个小按钮一直压住正文。
      - **句子 chat**：点击 `💬` 复用这道 Q 已有的 chat session，在抽屉顶部显示可关闭的
        Sentence Focus（完整地址、Content/Heading 显示名、句子、相邻 apparatus），并把光标放入输入框；**点击本身不调用 模型**。用户发出下一条消息时，才把焦点内容随消息交给 agent。焦点卡的 `×` 或输入框里的
        `Esc` 只清除句子焦点，不关闭 Q chat。
        地址在每次 render / live refresh 时生成，只是本次页面的 focus address，不写进 Markdown，
        也不承诺插入 Content division、Heading 或 Paragraph 后永不变号。
      - 新写入需要 serve.py，因为它必须在服务器的 Markdown 里找到那个句子；服务不在时，页面只保留
        pending line / 可复制 patch，不会创建页底评论区。
      旧式页底评论队列已废弃，不再读取、显示或迁移。

- 3.9 · sync — 干完活，同一轮里回写这一题
      **板和产物必须联动，否则板就是一份过期的漂亮东西。**
      ⚠️ **触发条件是「这一轮做了实质的活」，不是「这一轮打开了某个 page」。**
      一整段 /haipipe-board 会话里做的每件实质工作，都归属于某一个 page —— 哪怕这活是从
      聊天里的一句话开始的，从头到尾没提过题号。所以顺序是：**先认领是哪一题，再干活， 干完在同一轮回写**；一件活如果哪一题都不归，那它本身就是一道该开的新题。
      真实事故（JL 260726）：QA4a（今 `QAa2`）的整条本地 excalidraw 路线当天建完并跑起来了，`QA4a` 却还写着
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
      | `state:` | 全部打勾 → 以 ✅ 开头；有进展 → 以 🟡 开头；明确不做 → 以 ⏸️ 开头；标准标签分别是 SETTLED / PARTIAL / ON HOLD，可在后面追加人读说明 |
      | 句子下的 `> WHO:` / `> ✎` 行 | 这轮新增、回复或确认的句子评论和编辑记录 |
      然后 `python3 <skill>/build.py <板文件夹>`（或让 `watch.py` 自动跑；调法见上面 build 段）。
      **还要清掉被这轮推翻的旧说法。** 板改了，别处正文里的旧描述立刻变成自相矛盾 ——
      真实例子：版式早改成上下叠了，正文还写着「左右并排」；评论层已经引了 JS，另一题还写着「坚持零脚本」。
      零背景读者第一眼挑出来的就是这个。

- 3.10 · link — 把板和它的产物连起来
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

- 3.11 · close — 关板
      每个 page 的 `state:` 以 ✅ 或 ⏸️ 开头，并满足 `close:`，这块板才关掉。
      Q 和 S 用的是同一套状态值，翻到 ✅ 的凭据不同：Q 要 checkbox 全闭合，S 要它自己的
      **human gate 过了**（⏸️ 则是明确搁置）。首页按 named family 分别统计 S 里的 ✅。
      `close:` 那句话就是关板条件，写的时候要能验收，不是「差不多了」。

- 4 · 📐 一个 Page
      ```markdown
      # 短标题（短语，≤14 字）
      state: 🔴 OPEN          首 token 是 ✅ / 🟡 / 🔴 / ⏸️；后面可追加人读说明
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
      ## Log          260723 1030 · 改了什么 ┘
      ```
      **台面上的层次顺序是定死的**，Q 和 S 一样：
      `Opening → Diagram → Content → Items to Finish → Where we are`（Files 跟在状态后面）。
      Opening 放 Question 的第一段问句和 optional Boundary；抽屉第一行是 build 生成的
      `Structure` 页面地图（JL 260729：「just above Boundary」，纯渲染、无源可写，永不过期）；
      optional Diagram 是独立一节，
      默认折叠，点节名才展开。Question 的解释段自动成为 Opening 抽屉里的 “Why this matters”，
      Q 和 S 一致（JL 260729；此前 Q 放在 Content 首节）。S page 的 Opening 里还有
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
      - `Q*.md` = decision。checkbox 全闭合后才可 `✅ SETTLED`。
      - `S*.md` = lifecycle stage。`## Content` 是 stage substance（S 必填）；former Q-consumer questions
        become recognizable `Q-Stage-n` checklist records inside `## Items to Finish`; stage closes only
        at its human gate —— 也就是 S 的 `✅` 表示 gate 过了，首页按 family 据此计数。
      - S 的 `## Stage Contract` 不属于 Content。它只带显式 `requires` 的上游 acceptance
        conditions 和 `style-from` 的写作规范；managed 部分由 `stage.py` 写，作者拥有
        `### Provides`。Pages 顺序绝不是 dependency inference。
      - 两种 page **共用同一套四个机器状态**，由 `state:` 的第一个 emoji 决定：新开的都是 🔴，🟡 在做，⏸️ 明确搁置，✅ 的凭据按上面两条各自算。
        emoji 后可以写人读说明，例如 `✅ SETTLED`、`✅ PINNED · MISQ 2026`、`🟡 rendered · awaiting gate`；这些不是第五个状态。
        不得省略或替换首个 emoji，也不得让后缀改变它的含义。
      - Q-consumer checkbox means the answer landed, was interpreted, and was woven into Content. A
        deferred item closes only after its forward pointer is recorded.
      - `## Where we are` summarizes the actual stage state. It does not copy every consumer answer.
      正文里长内容一律写成 **`- 小标题` + 缩进两格的解释**，不要一段接一段的散句；
      整行加粗 `**…**` 是**组标题**（领着一串 item）。
      **每一页的 `## Content` 结构自定**（JL 260729）：division 的名字、编号和多少全由这一页自己的
      主题决定，`§` 编号的手稿形只是默认样，不是强制；机械约束只有两条不变——`###` 是一块能单独折的
      division，`####` 是它里面的一个段落、永远是这一级。页面只折一层，再深一级就把整节压成
      一个盒子。一块 division 只在自己确实有内容时才写：flat 的节写一个 `### §1 Introduction`
      领着段落，有 subsection 的节直接从 `### §6.1` 开始。好处是不读正文也能校验：带点的 `###`
      个数就是 subsection 数。`####` **没有图标** —— 🔹 是组标题的，别拿 `**…**` 当段落标题写；
      紧跟 `####` 的整行 `(…)` 是这一段的活儿，灰斜体留在台面上当扫读钩子。
      加一题直接复制 `ref/q-template.md`（每段都标了必填/选填）；完整语法表见 `ref/board-form.md`。
      > 老段名一律还认：`## Done when`＝`## Items to Finish`、`## Now`＝`## Where we are`、中文名同理。
      > `## Why here` 已退役 —— 它的活并进 `## Question` 的解释段并渲染到 Content；
      > 老板子里写着的旧段仍收进底部折叠区。

- 5 · ✍️ 写法（这条最容易被跳过）
      **「如果不易读，写那么多都是 rubbish。」** 详见 `ref/writing-rules.md`，最要命的三条：
      1. **不许造词** —— 每个说法要么是源文档的原话，要么在 `## Glossary` 里解释过。
      2. **过期的话要清掉** —— 板改了，正文里的旧说法就成了自相矛盾，零背景读者一眼就挑出来。
      3. **改完要用全新 agent 冷读** —— 调用 `haipipe-board-reviewer-agent`；它只读地运行
         `check.py`、按 `ref/writing-rules.md` 冷读、报告过期或矛盾说法，绝不替作者修改。
         自己在同一个对话里读测不出问题，因为你知道太多没写进去的事。

- 6 · 🚫 不许做的
      - 手改 `board.html`
      - 给板重新起日期
      - 删掉句子下的 `> JL:` 或 `> ✎` 行（它们是该句的评论／编辑记录）
      - 让页面依赖 JS 才能读 —— 脚本只能做增强。
        **不变量：删掉页面里所有 `<script>`，每一题和全部正文仍然在。** `build.py` 每次生成都断言这一条。

- 7 · 📖 板 ↔ SKILL.md：怎么保持同步
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
      - 现在已毕业的：`QAa0`（Q/S 共用源模板 → `ref/q-template.md`，原 QA2 260729 并入；原 QA4：Q/S 共用 page 版式 → `ref/board-form.md §8`，显示规格不塞进这里）· `QA6`（评论落盘）· `QA1`（板放哪，原 QC1 260729 并入）· `QC3`（Q 可住进自己的文件夹）· `QB5`（Python 按页拆进 `src/`）。
        现场层的 chat/terminal（`QD1`/`QD2`/`QD3`）还 🟡，上面只放了指针，没写成规矩。嵌入语法（原 `QF1`）已定进 `ref/board-form.md §5`；QF1 这个 page 本身 260725 退役，见板上 QF 组的说明。

- 8 · 📚 ref/
      | 文件 | 看它做什么 |
      |---|---|
      | `ref/q-template.md` | Q/S 共用 page 模板（历史文件名保留，避免旧链接失效） |
      | `ref/board-form.md` | 完整规格：文件夹、编号、段落↔页面对应、语法表、`## Links` |
      | `ref/writing-rules.md` | 怎么写才是人话 + 零背景审查的提示词和收敛判据 |
      | `ref/board-example.md` | 一块两题的最小示例 |
      | `stage.py` | 显式创建/同步 S page 的 inherited requirements 与 writing style |
      | `status.py` | 从 Board、page group 和 page 推导每次回复末尾的可见 session status strip；只读，不落状态文件 |
      | `check.py` | 结构自查（`QA9` 的机器那一半）：段落、state、引用、渲染出的 html、模板覆盖 |
      | `xcal.py` | 一块板一个 `fig/board.excalidraw`，一题一个 frame；`--wire` 把 URL 写回各题 |
      | `assets/board-mark.svg` | Board 的共享 SVG 标记；生成时内联进标题并复用为 favicon |
      独立 judge：`../agents/haipipe-board-reviewer-agent.md`。它没有写工具；作者修复后再启动一个新 reviewer。
      活的例子：`Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/` —— 这个 skill 自己的板（平铺形）。
      嵌套形（Q decisions + S stages）的活例子：`examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/`。
### The other files

34 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
assets/board-mark.svg               44 ln
assets/board.css                  1113 ln  palette + type follow html-ppt's academic-report; layout is body.single
assets/board.js                   2238 ln  Comment layer — PURE ENHANCEMENT. The prose is already real HTML;
assets/xcal-boot.js                264 ln  Injected by serve.py into the proxied Excalidraw app (QA4a).
build.py                           127 ln  board folder -> board.html (static content; scripts are optional enhancement).
check.py                           519 ln  check.py — the structural half of QA9, run against one board.
ref/board-example.md               111 ln  最小示例 —— 一块两题的板
ref/board-form.md                  389 ln  Board form — 完整规格
ref/q-template.md                  278 ln  Short title (a phrase, not a sentence)
ref/writing-rules.md                80 ln  Writing rules — how to write so it reads like human language
refs.py                             73 ln  Render a paper's real bibliography, once, into a cache the board can read.
regroup.py                         142 ln  Move a board's root pages into one named folder per Q group (QA1, JL 260726).
serve.py                          2478 ln  Serve boards AND accept comment writes — from the machine the files live on.
skillpage.py                       728 ln  One skill folder -> one Q page on a board (QC5, opened by JL 260726).
src/__init__.py                      3 ln  haipipe-board src/ (QB5): build.py and serve.py are thin entries; the code
src/body.py                        951 ln  The board's body grammar -> html (ref/board-form.md §5): inline marks, link
src/common.py                      109 ln  Shared constants + tiny helpers (QB5). Used by every page module AND by
src/dialect_paper.py              1004 ln  The `paper` dialect: resolve a manuscript's inline markers at BUILD time.
src/page_board.py                  238 ln  The cover + index + whole-page assembly (QB5: render(), asset inlining,
src/page_question.py               582 ln  One question -> one <section class="slide q"> card (QB5: the card chunk of
src/page_stage.py                  262 ln  Stage/source content on a slide (QF1, JL 260724): the `![[path]]` /
src/parse.py                       328 ln  md -> data (QB5): board.md, Q files, folder discovery, legacy blocks.
src/stage_contract.py               98 ln  Managed requirements and writing-style contracts for S pages.
stage.py                           378 ln  Create and synchronize lifecycle S pages with explicit inherited contracts.
status.py                          240 ln  Render the three-line closing block for one Board-attached session.
test_activity.py                   176 ln  Focused regression tests for QD8 board activity timing.
test_sentence_chat.py               80 ln  Contract checks for render-local sentence addressing and focused Q chat.
test_sentence_editing.py            85 ln  Regression tests for sentence-local comments and tracked edits.
test_status.py                     150 ln
vendor/xterm/addon-unicode11.js      2 ln
vendor/xterm/xterm.css             285 ln  * Copyright (c) 2014 The xterm.js authors. All rights reserved.
vendor/xterm/xterm.min.js            2 ln
watch.py                            55 ln  Watch a board folder and rebuild board.html whenever a .md changes.
xcal.py                            324 ln  board.md + the pages' ASCII figures -> ONE `fig/board.excalidraw` (QA4a).
```

<!-- haipipe:skill:body:end -->

## Items to Finish
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## Where we are
Page generated 260726 2325. Nothing ruled yet.

## Log
260727 0115 · renamed `QB6-board-skill.md` -> `Q-Skill-haipipe-board.md` and moved into the new `Q-Skill/` group; the version now rides the `state:` line as readable detail, never the filename
260726 2325 · page generated from `board/haipipe-board/` by `skillpage.py new`

<!-- haipipe:skill:log:start d551d6c8ba2a8eed board/haipipe-board -->

Converted from the skill's own `CHANGELOG.md`: 82 releases.

260729 · `0.51.0`
      - Opening's drawer now opens with a generated `Structure` row (JL: "the Structure subsection
        just above Boundary"): `render_structure` in `src/page_question.py` maps the page from its
        parsed sections — one row per section that exists, Content division names under their count,
        item/entry/file tallies — so the map is render-only and can never go stale. `.pmap` styling
        in `assets/board.css`; drawer order is now Structure → Boundary → Why this matters → S rows.
      - Specs updated in the same change (one face, both projections): `ref/q-template.md`,
        `ref/board-form.md` §8 (also repairing the stale "Q rationale becomes Content's first
        subsection" sentence), and SKILL.md's page section.
      - Design faces: QAa1 §7 owns the Structure decision; QAa0's diagram and Law carry the new
        drawer order; QAa0 §1 records the base/variant model (a page kind redefines only Content and
        ships under its consumer family); the five sibling QAa faces are marked frame.
260729 · `0.50.0`
      - Reader-facing Board links now honor the machine-local `HAIPIPE_BOARD_URL` even when the
        calling shell did not source `env.sh`. `status.py` reads only that one assignment from the
        served root; an explicit `--base-url` and the live environment still take precedence.
      - The documented view command uses the same setting instead of hardcoding loopback. Shared
        source retains `http://127.0.0.1:5599` only as the safe fallback, so this machine can hand
        readers its Tailscale URL without committing its personal IP as every clone's default.
      - Reader URL and listener bind remain intentionally separate: `HAIPIPE_BOARD_URL` chooses the
        link, while `serve.py --host` chooses who can reach the unauthenticated write and terminal
        endpoints.
260729 · `0.49.0`
      - Content-aware addresses replace page-global `Pn.Sn`. Only `## Content` is indexed:
        `###` divisions receive `Cn`, terminal `####` headings receive `Cn.Hn`, and prose receives
        sibling `Cn.Pn.S1` leaves.
      - `H` never parents prose. `QAb3.C1.H1` and `QAb3.C1.P1.S1` are valid;
        `QAb3.C1.H1.P1.S1` is invalid. Generated C/H chips make that hierarchy visible.
      - Sentence Focus shows the Content and nearest Heading display names while keeping Heading out
        of the sentence address. The focus packet carries that display path with the existing sentence
        and apparatus context.
260729 · `0.48.0`
      - Pointer devices now expose one quiet sentence action rail: `Pn.Sn ＋ 💬`. Comment opens
        directly beneath the sentence, Chat establishes sentence focus, and double-click remains Edit.
      - Sentence Chat now renders a clearable focus card in the existing Q drawer. Opening it spends no
        model turn; the next user message carries the address, sentence, and directly attached apparatus.
      - Touch devices collapse the sentence actions into `⋯`, whose menu shows the full address and
        Comment / Chat / Edit. `Esc` closes the active sentence operation without taking over normal
        single-click text selection.
260729 · `0.47.0`
      - Sentence-specific chat now reuses the existing Q session. Eligible prose receives a
        render-local `Pn.Sn` address; hover/focus exposes the address and a compact chat button.
      - Clicking the button opens that Q's drawer and sends an explicit focus packet containing the
        full page-qualified address, sentence text, and directly adjacent apparatus. No sentence
        sessions and no sentence ids are written to Markdown.
      - The legacy page-bottom comment queue was removed. Human comments and tracked edits live
        directly beneath their sentence as `> WHO:` and `> ✎` rows.
260729 · `0.46.0`
      - Why this matters renders inside Opening's drawer for Q pages too, unifying Q with S (JL 260729,
        decided on the design board's QAa1): `src/page_question.py` drops the Q branch that inserted it
        as Content's first subsection; `check.py`'s template coverage asserts the drawer row instead;
        `ref/board-form.md`, `ref/q-template.md` and SKILL.md say the new placement.
      - Content is per-page flexible (JL 260729, decided on QAa3): the `§`-numbered manuscript shape is
        the default, not a mandate; the only fixed mechanics remain the one fold level (`###` division,
        `####` paragraph). Rule text only; the renderer already accepted any division set.
      - Vocabulary: a Q page settles a "decision", not a "ruling" (JL 260729), across SKILL.md,
        ref/board-form.md, ref/q-template.md and the reviewer agent.
      - Pointer maintenance after the design board's 260729 restructure (QA4->QAa0, QA4a->QAa2,
        QA8->QAb1, QA8a->QAb3, QC1 merged into QA1, QA2 merged into the QAa faces): the graduated list
        and the excalidraw section's live ids follow the new names.
260728 · `0.45.0` · a variant tail is part of the unit's identity
      - **`S-Display-<n><letter><tail>` now resolves**, e.g. `S-Display-4al2` and `S-Display-4al5`, the same claim under two specifications. Three places stopped at the letter and each failed differently: the chip pattern rendered NO card for either; `_short()` returned `S-Display-4a` for both so `by_short` kept whichever sorted first; and the face-id derivation gave both the anchor `S-Display-4A`, which exists on neither page, so both cards silently lost their owning-page link.
      - All three now carry the tail. The legacy `display<NN><a>` form is untouched, and `S-Display-Dash` (a page, not a unit) and `S-Display-4A` (the uppercase page anchor) still do not chip, so the two identities never compete for one string.
260728 · `0.44.0` · a member may have variants, and both the parser and the minter had to learn it
      - **`src/parse.py`, the unit pattern.** A page id was `\d+[a-z]?`, a number plus at most one letter, so `S-Display-4al2-main-regression.md` matched NOTHING. The failure mode was the bad one: the file parsed as no page at all, `board.md` reported "listed in Pages but no such file exists", and the page was invisible rather than rejected with a reason. The alternation now leads with `\d+[a-z][a-z0-9]+`, so a VARIANT id parses and `4a` still parses exactly as before.
      - **`stage.py`, `resolve_filename`.** It accepted only a number or one uppercase letter, so the minter could not create `4a` either, and every block-plus-member page in the MISQ paper had been made by hand while this function's own docstring called it "the one place an S page's filename is composed". Widened to the same grammar, preserving case for a lowercase member id and still upper-casing a single appendix letter.
      - **What a variant MEANS, so the tail does not become a free-for-all:** the same claim and the same job under a different specification of the exposure or method, INHERITING its parent's letter. That inheritance is the point. Letters are reading order, so a unit reading right after `4a` would otherwise have to become `4b` and shift `4b` and `4c` down, and the MISQ board measured that cascade twice on 2026-07-27 at roughly 750 rewritten lines across 105 files.
      - **`4a-l2` is not available, on a mechanical ground.** The page-id regex stops at the first hyphen, so a hyphenated tail parses as `S-Display-4A` and collides with its own parent. The tail runs on: `4al2`.
      - **Verified on the MISQ board:** 42 pages, the new page ordered between `S-Display-4A` and `S-Display-4B`, 0 stale-contract warnings, every other page id unchanged, and `build-displays.py` shipping 11 units.
260728 · `0.44.0` · measure the master the paper SHIPS
      - **A paper may have two tex trees, and 0.43.0 measured the wrong one.** On the MISQ board `3-dist/tex/paper.tex` is the live deliverable, generated one-way from the S-Main pages by `md2tex.py`, while a root master over hand-written `sections/` still builds beside it. `_input_closure()` globbed the ROOT for `\begin{document}`, so it saw only the legacy tree and reported `??` for nine displays that were in the shipped PDF all along. It now prefers `3-dist/tex/paper.tex` when present.
      - **An `\input` resolves against the file's own directory OR the paper root.** `md2tex.py` compiles with `TEXINPUTS=".:<paper root>:"`, which is how `\input{S-Main-3-theory}` and `\input{displays/S-Display-1a-hero-concept/float}` both work from inside `3-dist/tex/`. A walker trying only one base silently loses half the tree.
      - **Net effect on that board:** one `\ref` chip still reports `??`, `fig:llm-measurement`, whose unit is deliberately folded. Verified by regenerating: `paper.pdf` at 47 pages, nine unit labels in `paper.aux`, zero undefined references.
      - **The lesson worth keeping:** "a label exists on disk" (0.42.0), "a label reaches the master" (0.43.0), and "which master" (this one) are three different questions, and only the third makes the second mean anything.
260728 · `0.43.0` · a label on disk is not a label in the document
      - **`Registry._input_closure()`.** The label index spans every `.tex` on purpose, so a section-local label still resolves. The cost was that "a `\label` exists somewhere" was reported as "this pointer works", and those are different questions: a float that no reachable section `\input`s declares its label in a file LaTeX never opens, so the `\ref` compiles to `??` while the chip painted green. `ref()` now resolves the master's real `\input`/`\include` closure once and downgrades any label declared outside it.
      - **Measured on the MISQ board before the fix:** `tab:descriptives` read `ok` EIGHT times on one page and printed `??`; `tab:main_results` read `ok` while its only declaration sat in a retired `displays/_old/` file reached solely by an orphan section. After: all 22 display chips on that page match ground truth.
      - **It downgrades the `\ref` CHIP, never the unit CARD.** A card answers "is this display built and agreed", which stays true of an unwired float; a `\ref` chip IS the claim that the pointer resolves. This is `_gate`'s worst-state-wins applied to a second thing disk cannot see, and it deliberately stops short of the cards for the same reason `[AMBER]` does not downgrade one: ambering the whole set would stop the distinction informing.
      - **No master, no judgement.** `_prints()` returns True when no `\begin{document}` file is found, so a board whose paper-root has no master is not painted amber wholesale.
260727 · `0.42.0` · a display unit is named for the page that owns it
      - **The unit-to-page join is a LOOKUP, not a guess.** `_sdisplay_read` used to derive an S-Display page name from the unit folder with `display0*(\d+)([a-z]?)` and rglob a stem. When either side was renamed the derivation still produced a face id, found no file, and returned an EMPTY state line, so the AGREED downgrade never fired and a `[RED]` blocked unit painted green on the board. Where a unit folder shares its name with its page, the page is now read directly. The derived branch is kept, and labelled as the fragile one, so a paper that has not migrated still builds.
      - **Two layouts, detected not configured.** `Registry` prefers `0-lifecycle/3-display/workspace/S-Display-*/` when it exists and falls back to `displays/display*/`. The board always reads the SOURCE tree, because `candidates/`, `versions/` and `preview.png` exist only there and a card without them cannot be judged.
      - **Both trees are excluded from the cite scan.** Under the workspace layout `displays/` holds a GENERATED copy of every float, so indexing it would declare each `\label{}` twice and report a collision against itself. `disp_parts` replaces the single `disp_rel in p.parts` test at both sites.
      - **`_short()` replaces `id.split("-", 1)[0]`.** That split was correct only while every id began with `display`; on `S-Display-4a-main-regression` the first hyphen belongs to the prefix, so every unit would have keyed on `S` and the whole set would have collapsed onto whichever sorted first.
      - **ALWAYS A CARD (JL 2026-07-27).** A unit name in prose renders as the evidence card, never as a bare page link: the card already carries the owning page's anchor and its state line, so it is a strict superset of the link. MARKER group 6 now accepts `S-Display-<n><letter>[-slug]` alongside the legacy form. The page ANCHOR keeps the uppercase short id (`S-Display-4A`), which the new alternative does not match, so the two identities never compete for one string. `S-Display-Dash`, a page and not a unit, does not match either.
260727 · `0.41.9` · a Display exposes its alternatives without selecting one
      - Every allocated paper Display now places `Display Versions` between the live artifact and the real folder tree. It lists the current `float.tex` target, every stored version, unpromoted candidate, and non-current asset as directly openable files.
      - The projection does not manufacture version chronology or approval from filenames: only `float.tex` identifies the printed artifact. The explanatory posture states that provenance and supersession require a manifest or stage record.
      - Display identities may now use an intentional alphabetic paired suffix such as `display01a` / `display01b`; marker resolution and the S-Display bridge preserve that suffix without changing LaTeX's figure counter.
260727 · `0.41.8` · every Display page reviews the same three concrete things
      - A resolved paper Display page now begins its Content with the compiled Current Float, the exact live artifact referenced by `float.tex`, and an ASCII view of the unit directory as it exists on disk.
      - The folder view marks a `source/`-only unit as legacy rather than implying that `intake/` and `recipe/` already exist. A new-style unit reports the target layout. This makes staged migration visible without moving assets or inventing provenance.
260727 · `0.41.7` · an authored PDF can be inspected beside the compiled float
      - Standard Markdown image syntax now recognizes a local `.pdf` target. `![](path.pdf)` renders a native PDF object with an `open PDF` fallback, rather than an invalid `<img>`.
      - A Display page can therefore show the generated `preview.pdf` Current Float first and, when comparison matters, show the underlying live display PDF in the next Content subsection. The two files have different review jobs and no longer have to compete for one preview slot.
260727 · `0.41.6` · a live refresh no longer throws you back to the index
      - **The live refresh silently un-routed the page.** `tick()` swaps `div.wrap` wholesale, and the
        page router is pure CSS (`body:has(.q:target) .q:target{display:block}`). `:target` binds to an
        ELEMENT, not to an id: replacing the wrap destroys the section the hash pointed at, the fresh
        one carries the same id, and the browser never re-resolves the fragment. Nothing matches, so
        `body:not(:has(.q:target)) .q{display:none}` hid every page and the index came back — with the
        hash still in the URL, which is why it read as "the refresh threw me out" rather than as a bug.
      - Fixed by re-navigating to the hash after the swap. Only a real navigation re-resolves `:target`;
        `history.replaceState` does not.
      - Reproduced and the repair verified in headless Chrome, on a minimal page with the same three
        CSS rules: before swap `stage=true index=false`; after swap `stage=false index=true` with the
        hash still present; after repair `stage=true index=false`.
      - Found by JL: "after the refresh, I was went to the index page, not the Stage page."
260727 · `0.41.5` · a sentence with evidence answers the same gesture
      - **`summary` removed from the dblclick guard, and the form now lands in the drawer body.**
        `QA8@boardform` rules that double-click opens the add-form on a BARE sentence while a drawer
        gets its own `➕ add to this sentence` row, and that row is real — `board.js` appends one to
        every `.sapp` at load. But it is reachable only once the drawer is already OPEN, so on a
        sentence carrying evidence the gesture people actually learned did nothing, silently. 116 of
        the MISQ board's sentences are already drawers, and that number only grows as the evidence
        card becomes the default phase output, so both shapes now answer double-click.
      - **The placement is the subtle half.** `mk` does `afterEl.insertAdjacentElement('afterend', …)`,
        so reusing the bare-sentence call on a drawer would insert the form INSIDE `<summary>`, where
        every click toggles the drawer and the inputs cannot be used. A drawer now passes the same two
        arguments the `➕` row path passes — insert at the end of the drawer body, while naming the
        summary's sentence as the target line — and opens the drawer first, since the two clicks
        toggled it net-zero.
      - The remaining guard clauses still cover what `summary` stood in for: the sentence text resolves
        to the inner `p`, the `.sbadge` has no `p` ancestor so `!p` catches it, and a marker is a
        `<button>`.
      - Found by JL double-clicking a sentence that had just gained a `> Value:` lane.
260727 · `0.41.4` · paper Display pages expose the editable source without replacing the float
      - A per-asset `S-Display` page keeps the standard Q-template order and places its compiled
        `preview.pdf` as the first `📚 Content` subsection. It resolves the unit from the page's explicit
        `Registry id:` or `unit:` record, not from a fragile `1a` / `01` title conversion.
      - The same subsection now links any PowerPoint source beside `open PDF`. A new source belongs in
        `recipe/`; legacy PPTX files in `source/`, `candidates/`, or `versions/` stay discoverable with
        an honest role label. PPTX is editable work material; `preview.pdf` is still the printable
        float, caption, label, and placement that a reviewer inspects.
260727 · `0.41.3` · the id regex accepts a per-unit stage token
      - **A Q-consumer id may carry digits in its stage token.** `Q-[A-Za-z]+-\d+` rejected
        `Q-Sec6Results-3`, so a paper whose per-unit stage names its unit in the id (JL's
        2026-07-27 ruling) had every bracket silently un-chipped: no error, no warning, just
        grey prose where a chip belonged. Widened to `[A-Za-z0-9]+` at all six sites —
        `dialect_paper.py` `QID` and its `\cite{TOADD}`-bracket lookahead, `body.py`'s
        `MARKER` alternation (3) and `QBRACKET`.
      - Verified on the MISQ paper: 10 of 10 bracket chips on `S-Main-6` still resolve `qref
        ok` after both sides of every binding were renamed.
260727 · `0.41.2` · folds that stay shut, and two renderer defects
      - **An item body may contain no blank line.** `body.py` calls `flush()` on a
        blank line and `flush()` closes the open item, so a converted section ended at
        its first blank line and spilled the rest onto the page as literal `- ` and
        `**bold**` text. 0.41.1 guarded only the line after the item head, which moved
        the symptom instead of fixing it. Blank lines are dropped throughout an item
        body and kept inside fences.
      - **`inline()` could not carry a mark across a code span.** Code spans were held
        out of the mark pass so `**` inside them stays literal; the same split cut
        every mark that SPANS one, so `**run \`check.py\` now**` rendered as literal
        asterisks. Broken since that split was written, on every board. Fixed by
        stashing code spans behind a sentinel, running the marks, then restoring.
      - Added `join_wrapped`: a bold phrase that the source wraps across two lines is
        rejoined, because one row per line leaves each half with an unclosed marker.
        Editing a shipped skill to satisfy a renderer would be the wrong repair.
      - All 9 boards rebuilt on the fix; none regressed. Repointed one cross-board
        link the paper board had renamed again.
260727 · `0.41.1` · agents are shipped units too, and every section folds
      - `skillpage.py` accepts a single definition `.md` as well as a skill folder, so
        `agents/haipipe-board-reviewer-agent.md` gets a page. Both carry identical
        frontmatter, so one generator covers both rather than a second that would
        drift. A single-file unit emits the tree span EMPTY rather than omitting it:
        `sync` replaces spans it can find, and a missing one would report as an older
        page every run.
      - Every numbered section is now an ITEM, so all of them fold. 0.41.0 made the
        unit's `##` a `####` paragraph heading, which never folds, and items do not
        nest either, so a top-level section had no fold at all. The board has one
        folding level inside Content and QA4 already ruled depth is read off the
        numbering. 19 collapsible sections on the skill, 4 on the agent, 0 non-folding
        headings left.
      - Scope: the `Q-Skill` group covers `skills/board/` only. A page generated for
        `haipipe-probe` was a proof and was deleted.
260727 · `0.41.0` · a named Q family for skill pages
      - **Named Q pages.** `parse.py` recognizes `Q-<Family>-<rest>.md`, so a skill
        page is `Q-Skill-haipipe-board.md` in a `Q-Skill/` group rather than `QS1-…`.
        Same shape as the named S families, same reason: a roster row is identified by
        WHAT IT IS, never by a position in a queue.
      - Split the two concerns onto two pages. `QB6 · Convert a skill folder to a
        skill page` owns the mechanism and lives in QB; everything it generates lives
        in `Q-Skill`. QC5 was renamed into QB6 rather than duplicated.
      - The version rides the page TITLE (`haipipe-board · v0.41.0`), so the index row
        prints it. Not the `state:` line, where a derived value competed with a health
        judgment; and never the filename, which would break every link on release.
      - A skill's `###` sections became collapsible ITEMS (`- N.M · title` plus an
        indented body). A `#####` heading renders as `.ph` and never folds, so
        eleven sub-sub sections had no way to collapse.
      - Fixed a blank line between an item and its body, which ENDS the item: the
        first attempt silently flattened all eleven back to prose while the markdown
        still looked right.
      - Fixed `page_id_of` in `serve.py`. `stem.split("-")[0]` collapsed every named
        page into one activity row called `Q`.
      - Fixed `group_home` walking past `## Pages`, which listed a new page inside
        `## Links` when its group was the last one.
260727 · `0.40.1` · one division per file, numbered inside
      - `SKILL.md` is now ONE `### SKILL.md` division of Content, with the skill's own
        headings two levels down inside it. 0.40.0 promoted them straight to `###`,
        which scattered nine unrelated divisions across Content and lost the fact
        that they are one file.
      - Depth comes from NUMBERING, not heading level: `##` becomes `#### N ·` and
        `###` becomes `##### N.M ·`. The board renders exactly two Content levels and
        `#{4,6}` are visually identical, so this is QA4's own `§6` / `§6.1` rule
        applied where a third level does not exist.
      - QB6 reads `3 · 🔨 动作` over `3.1 · view` … `3.11 · close`, which is the
        structure the skill actually has.
260727 · `0.40.0` · the skill becomes the page's Content
      - `skillpage.py` CONVERTS `SKILL.md` into Content subsections instead of
        embedding it: each `##` becomes a `###` division, each `###` a `####`
        paragraph heading, which is QA4's two-level Content grammar.
      - What that buys over an embed: per-section folding, a copy button per section,
        a real anchor, a place to pin a comment, and a Content heading that counts
        them. QB6 reports 11 sections.
      - Fenced blocks pass through byte for byte. `SKILL.md` holds a page-anatomy
        figure whose lines start with `## `, and demoting those would have rewritten
        14 lines of a diagram into headings.
      - The managed marker now carries the skill folder as well as the hash. `sync`
        recovered the folder from the page's `![[…/SKILL.md]]` line, which vanished
        when the embed did; a machine span must not depend on rendered content to
        know its own source.
      - `check.py` exempts managed spans from the hard-wrap rule too. It had flagged
        17 lines of quoted skill prose.
260727 · `0.39.0` · the changelog becomes Log lines
      - `skillpage.py` CONVERTS `CHANGELOG.md` into `## Log` entries instead of
        embedding it: `## [0.38.2] — 2026-07-27 — title` plus its bullets becomes one
        dated `260727 · \`0.38.2\` · title` line with the bullets as indented
        continuations, which is the grammar `sort_log` already carries.
      - Why it matters beyond format: the ACTIVITY dashboard counts one update per
        dated `## Log` line, so an embedded changelog counts as zero and a converted
        one puts every release onto the strip. QB6 went from 1 update to 59; the
        board total from 507 to 566.
      - `check.py` now skips prose-style rules (em-dash, CJK, bold-not-a-group-title)
        inside any `<!-- haipipe:… -->` span, while keeping every structural check.
        The conversion raised 79 warnings in one pass, all of them about quoted text
        the board did not write and cannot fix without falsifying the quote. The
        exemption belongs to the mechanism: a stage's inherited contract is quoted
        material for the same reason.
260727 · `0.38.2` · the skill file stops hiding
      - `<!-- haipipe:… -->` machine markers are dropped at RENDER. `strip_notes`
        keeps them in the file on purpose, because that is where stage.py and
        skillpage.py find their spans, but a marker is addressed to a script and six
        of them were printing as literal text on the first generated page.
      - Removed the `34em` clamp on `.embed.src .emb`. A `|source` embed IS the
        page's content, not a quotation inside it, and a scrollbox nested in a
        collapsible section is two controls competing for one job.
      - Moved the `SKILL.md` embed out of a `### What it is` division. A direct `###`
        in Content renders COLLAPSED, so the one thing a skill page exists to show
        was the one thing behind a click. It now sits directly under `## Content`.
        `### The other files` stays a division: it is supporting material.
260726 · `0.38.1` · a skill page shows the skill, and describes the rest
      - Split the generated material into three managed spans, one per section it
        belongs in: the annotated folder tree in `## Diagram`, the whole `SKILL.md`
        plus a description of every other file in `## Content`, and the skill's
        `CHANGELOG.md` in `## Log` under the page's own hand-written lines.
      - `## Diagram` also carries an AUTHORED workflow fence. A folder can be read
        off disk; an intent cannot.
      - **Described, not reproduced.** Only `SKILL.md` is the skill's content. Every
        other file is named, sized, and given the purpose line it states about
        itself. A first cut embedded `ref/*.md` in full; JL cut it back.
      - The file manifest is a fence, not a bullet list: its purpose lines are
        verbatim quotes carrying other files' punctuation, and editing a quote to
        satisfy the prose checker falsifies it.
      - Purpose extraction skips YAML front matter, or every `SKILL.md` reported its
        own `name:` line as its purpose.
      - QB6 renders 117,500 characters from exactly 2 embeds; 0 errors, 0 warnings on
        that page; sync idempotent and the authored workflow survives a real sync.
260726 · `0.38.0` · a page generated from a skill folder
      - Added `skillpage.py` (`new` / `sync` / `check`), a second consumer of
        `stage.py`'s pattern rather than a second mechanism: generate once, then
        refresh only a managed span, never touching what a human typed.
      - Derived and owned by the script, inside `<!-- haipipe:skill:start <hash> -->`:
        name, version, last_updated, summary, allowed-tools, folder, and the two
        embed lines. Never touched: Question, Items to Finish, Where we are,
        Comments, Log.
      - `state:` is deliberately NOT derived. A version cannot say whether a skill is
        stable or mid-rewrite, so `new` seeds 🔴 OPEN and a person rules on it.
      - Zero copy: `SKILL.md` and `CHANGELOG.md` are embedded with `![[...]]` and read
        at build time, so the page cannot go stale between syncs. Only the derived
        header can, which is what `check` reports, with the exact fix command.
      - First subject is `haipipe-board` itself, as QB6 on the boardform board. A tool
        that cannot describe its own skill describes nothing.
      - Verified: sync idempotent; a version bump caught by `check`; two sentinel
        lines in the authored sections survived a real sync; the page renders 132,256
        characters where the stub rendered 4,132.
      - Fixed on the way: the first token was `../../board/...` and the embed refuses
        `..` by design, so it rendered two visible `⚠ embed not found` blocks. `rel()`
        and `resolve_token()` now walk the renderer's own ladder, because a page that
        renders one file while sync reads another is a disagreement no test catches.
260726 · `0.37.1` · the sweep, and the link cost it exposed
      - Added `regroup.py`: moves a board's root pages into `Q<key>-<group slug>/`.
        Dry-run by default, `git mv` when tracked, `--all <root>` for a whole repo.
        The ruling had to become a command; a rule enforced by hand drifts.
      - Swept all 7 flat boards: **154 pages moved, 0 left at any board root**, every
        page count held, every board rebuilt.
      - **Found a real cost QA1 had denied.** `## Pages` lists bare filenames and needs
        no edit; `## Links` declares real relative paths and 17 cross-board links
        broke. `check.py` caught every one. They are repointed, and the correction is
        written into QA1 §1, `SKILL.md`, and `board-form.md` §1.
      - Exempted the paper `0-lifecycle/`: `0-seed/ 1-work/ 3-display/` are already one
        folder per group, and their numbers carry lifecycle order that letters cannot.
        `regroup.py` skips any board with no pages at its root.
      - Capped the folder slug at 30 characters on a word boundary.
260726 · `0.37.0` · group folders are the default, and named
      - **Ruled (JL): one folder per Q group, on every board, from page one.** Not
        size-triggered, so a board never reorganizes itself under its reader the day
        it crosses a threshold.
      - The folder is `Q<letter>-<slug of the group title>`
        (`QA-defining-a-board/`), never a bare `QA/`. A bare `QA/` writes the id
        twice and drops the group's subject, which is the half a reader cannot
        recover from the filenames inside it.
      - `＋Q` writes into the folder its group already lives in; a group with no
        pages yet gets a named folder created from its `### Q<letter> · <title>`
        heading. Only a group split across two homes falls back to the board root.
      - Moved this board onto it: 30 pages into 5 named folders, `board.md`
        untouched, and the rendered HTML identical apart from the 180 write-back
        path attributes that must change.
      - Day counts now sit ON each activity bar instead of under it, and always
        render (`·` for a real zero). A bar scaled against a 137-update day is a
        sliver on a 7-update day, and a sliver is not a measurement.
      - QA1 closed at 14/14.
260726 · `0.36.0` · the dashboard counts updates, and Diagram becomes writable both ways
      **Activity (QD8 merged into QC2 on JL's call).**
      - Changed the dashboard's unit from focus seconds to UPDATES: one dated line in
        one page's `## Log`. JL: "I don't care about the time. What I care is about
        the numbers of updates."
      - The reason it is a better unit, not merely a preferred one: the timer could
        only see a browser, and most work on these boards arrives through Claude Code
        or an editor, so it was exact about a quantity that was not the work.
      - Recovered the history the timer could never have had. It began 2026-07-26
        19:15 and saw one day; counting `## Log` reads 509 updates across 8 boards,
        129 pages, and 5 days, including the 245 lines from 07-22 to 07-25.
      - Reads `## Log` only. `## Where we are` also carries dated lines but is status
        prose, and counting both would count one change twice.
      - The span recorder still runs and nothing reads it. Its fate is an open item
        on QC2, with a recommendation to delete it.
      - Moved ACTIVITY below the page cards: the board's content leads, the
        measurement of that content closes.
      **Diagram (QA4 · QA2 · QD7).**
      - Split the rendered `🖼 Diagram` into `▧ ASCII` (open) and `✏️ Excalidraw`
        (shut). The source keeps one plain `## Diagram`; `split_diagram()` partitions
        it on the bare-URL rule `body.py` already owned, so no page was migrated. A
        shut `<details>` never displays, so 28 lazy canvas iframes stopped loading on
        open.
      - Made attaching reversible: `🗑 Remove` clears the URL line and its blank line
        and touches nothing else. Add, replace, remove returns the file byte-identical.
      - Gave every page a way in: `wireXcal` walks pages rather than Diagram
        sections, so a page with no section gets a `🖼 Add a Diagram` control where
        the section would render. The endpoint had always created it; only the entry
        point was missing.
      - Ruled that a drawing carries no signature: the md line must stay
        indistinguishable from a hand-edit, and git already answers who added it.
      - Fixed `face.dataset.file`, an undefined variable that made
        `✨ Create one for me` report "serve.py is not running" whatever was running.
      **Folder structure (QA1).**
      - `＋Q` now writes into the folder its group already lives in, falling back to
        the board root when the group's pages disagree or it has none. It recognizes
        no `QA/` naming convention, which is what makes one rule cover both reasons a
        page sits in a folder: the folder is the GROUP, or the folder is the SUBJECT
        (QC3). Flat boards are unchanged by construction.
      - Stated those two reasons as one rule in `ref/board-form.md` §1.
260726 · `0.35.0` · shared Board identity mark
      - Added `assets/board-mark.svg`, a hand-authored vector of the approved
        four-page mark with a transparent speech-shaped aperture.
      - Inlined the mark beside every generated Board title and reused the same
        source as an SVG data favicon, preserving the one-file offline invariant.
      - Added `--board-mark-*` palette tokens to `assets/board.css`; geometry stays
        in the SVG while color schemes remain a CSS-only change.
      - Added exact-geometry palette studies for Original, Clinical Teal, Warm
        Editorial, and Graphite Aurora to the Board design record.
260726 · `0.34.0` · Diagram's two halves, and where ACTIVITY sits
      - Split the rendered `🖼 Diagram` into `▧ ASCII` (open) and `✏️ Excalidraw`
        (shut), ranked rather than paired: the figure is what a reader came for and
        the canvas is where colleagues draw together.
      - Kept the SOURCE at one plain `## Diagram`. `split_diagram()` partitions the
        section on the bare-URL rule `body.py` already owned, so no page was migrated
        and a page that later gains a canvas splits itself. A URL inside a fence
        stays in the figure.
      - Stopped a board from booting every canvas on open: a shut `<details>` never
        displays, so the lazy iframes wait for a click. This board holds 28.
      - Emitted the canvas row even when empty ("No canvas attached yet") and moved
        the 🖌 attach button into it, so the affordance has a home.
      - Moved the index `ACTIVITY` section below the page cards. The board's content
        leads and the measurement of that content closes.
      - Generalized QD8's opening question away from one named reader; the stored
        span always carried an `actor` column.
260726 · `0.33.0` · three-line closing block
      - Replaced the ten-line fenced status strip with three Markdown lines:
        linked `Board · Queue/Focus`, `status · mode`, and the next action.
      - Removed repeated field labels, page title, source-file line, separators, and
        the visible raw URL. The Board attachment remains directly clickable.
      - Kept the same attachment resolution, sourcing ownership rule, composed-skill
        precedence, and no-shared-status-file invariant.
260726 · `0.32.2` · current Paper paths only
      - Removed the Paper dialect's `0-displays/` fallback. Display resolution now
        has one source, the unnumbered deliverable folder `displays/`.
      - Updated Board examples and parser comments to the first-class lifecycle
        family paths.
260726 · `0.32.1` · composition precedence and Q/S gate semantics
      - Made the reply contract composable: direct Board sessions use the exact
        `status.py` strip, while an explicitly enclosing first-class skill such as
        Paper emits one canonical block containing the deep Board link rather than
        appending two mutually exclusive blocks.
      - Limited checkbox/state staleness heuristics to Q pages. S page state is a
        lifecycle gate and is intentionally independent of remaining checklist work.
260726 · `0.32.0` · visible session attachment
      - Added a mandatory reply-ending Board status strip, following Paper's Closing
        Block pattern. It shows the Board, page-group queue, board/group/page focus,
        live work mode, next action, deep link, and owning file.
      - Added read-only `status.py`, which derives durable labels from `board.md` and
        the page parser instead of maintaining a second status ledger.
      - Injected the same closing-block contract into page and whole-Board sessions
        launched by `serve.py`, so attachment is visible even when the user did not
        explicitly name the page again.
      - Whole-Board sourcing without an owning page group is blocked. No shared
        `STATUS.md` is created; durable outcomes still use the normal Board sync.
      - Forward acceptance passed with a fresh-context agent: it read the revised
        skill, invoked `status.py` rather than hand-writing the strip, derived QD and
        QD9 from the Board files, and placed the complete block last.
260726 · `0.31.0` · one machine state token, optional readable detail
      - Formalized the renderer's live contract: the first emoji on `state:` is one of ✅, 🟡, 🔴, or ⏸️ and is the machine status; optional text after it is page-specific human detail.
      - Updated `check.py` to validate the normalized emoji rather than an exact full-line label, so real states such as `✅ PINNED · MISQ 2026` remain valid without creating a fifth status.
      - Declared `/_board/` and `/_excalidraw` as live server routes so the generated HTML checker does not mistake them for missing disk files; ordinary local links are still checked.
      - Made the template fixture source-aware: a construct present in the source but absent from HTML is renderer drift and therefore an ERROR, while a construct absent from the source is an explicit GAP.
      - Added separate Q/S placement assertions for rationale, Stage Contract, and Content headings instead of merely counting two rendered page containers.
      - Enforced the canonical required structure: Board title/spine/close/Topic/Pipeline/Pages, page title/state/owner/Question/Items/Where, and Stage Contract plus Content on S pages.
260726 · `0.30.0` · Board becomes a first-class family
      - Moved the skill package from `skills/0_utils/haipipe-board/` to
        `skills/board/haipipe-board/`, beside the paper, probe, and task families.
      - Kept the design Board at `skills/diagrams/01-boardform-260722/`; a working
        design record still does not ship inside the skill.
      - Clarified Board placement: task, project, and paper Boards use the owning
        unit's `diagram/`; plugin skill-design Boards share the plugin's
        `skills/diagrams/`. `NN` sequences one topic series, so unrelated topics may
        each start at `01`.
      - Added `../agents/haipipe-board-reviewer-agent.md`, a read-only packaging of
        the existing `check.py` plus zero-background cold-read workflow. The original
        session remains the writer and fixes every finding.
260726 · `0.29.0` · warn when a board writes markers and declares no dialect
      The `dialect: paper` seam had exactly one silent failure: a board that writes `\citep{}`, `{VAL:?}` or `[Q-…]` and forgets the two frontmatter lines renders them as plain text, produces an EMPTY marker report, and looks completely fine. Nothing said anything. On a paper board that is the loss of the family's only cross-check of prose against the `.bib` and the display units.
      `build.py` now says so, on the `else` branch that previously did nothing.
      **The trigger is the board's own CONTENT, never its folder name.** A dialect is deletable (QBc5) and `build.py` must not learn what a paper is, so it does not look for `0-lifecycle/`; it looks for marker syntax.
      **Code spans are stripped first, and that is the whole precision of the check.** A board that MEANS a marker writes it in prose; a board that DISCUSSES the syntax quotes it. Measured across the four real boards on 2026-07-26: `01-boardform-260722` has 13 mentions and `01-probe-qa-260726` has 2, all inside code fences or backticks, none meant. A naive raw match warned on both; stripping code first gives zero false positives on all four, while a real paper board with the two lines removed reports 429.
      Verified: `Paper-Personality2Opioid-MISQ2026/0-lifecycle` builds byte-identically (40 pages, 22 markers), and the same folder with `dialect:`/`paper-root:` deleted now warns loudly with the exact two lines to add.
260726 · `0.28.1`
      **Driven by a real browser at last, which found two things nothing else had.** JL asked "will it work?", and the honest answer was that nobody knew: 0.27 and 0.28 were verified against a server and a stub. Chrome is installed on this machine and Node 22 ships a WebSocket, so the DevTools protocol closed that gap.
      - **The app never started.** `proxy_excalidraw()` injected the boot script at `<head>`,
        which put it BEFORE the `window.__haipipeApp` assignment it reads, so `start()`
        returned quietly and no module was ever appended. The page rendered a correct badge
        over a blank screen. The boot tag now goes immediately AFTER the assignment. This had
        been shipped, reviewed and reasoned about twice without being noticed, because every
        test up to that point stubbed the very thing that was broken.
      - **Opening a page dirtied the repo.** Excalidraw renormalises everything it loads
        (`version`, `versionNonce`, `updated`, `boundElements` null → []), so the editor saved
        one second after opening with nothing drawn. Two halves to the fix: the tab compares
        element CONTENT rather than raw JSON, and `xcal.py` keeps an element the browser has
        enriched instead of writing its plainer version back. Without the second half the two
        would have dirtied the file in turn forever, each undoing the other.
      End to end in headless Chrome: the app mounts, our seed is what it loads, pressing `r`
      and dragging produces a rectangle, and that rectangle arrives in `fig/board.excalidraw`
      inside `frame-QB3` with the other 88 elements untouched and no page errors. Opening the
      editor twice leaves the file byte-identical the second time; two `xcal.py` runs do too.
260726 · `0.28.0`
      **A pasted image survives, as a real file in `fig/assets/` rather than as base64 inside the scene.**
      JL: *"could we make it saved? we can have an assets folder for it."* Right on both counts, and the folder is the part that matters. Excalidraw keeps images as base64 dataURLs INSIDE the document, so one screenshot is megabytes that git then re-diffs every time anyone nudges a box.
      - **Bytes out, pointer in.** `stash_files()` decodes each dataURL into
        `fig/assets/<fileId>.<ext>` and leaves `{id, mimeType, path}` in the scene.
        `hydrate_files()` does the reverse on the way out, for the elements being
        returned only. Fetched through `serve.py` the scene is self-contained and the
        editor never knows; the files map is MERGED on save, so an image saved by an
        earlier tick is never lost by a later one.
      - **Every `.excalidraw` GET now goes through the scene handler**, not only
        `?frame=` ones, because a whole-scene fetch needs rehydrating too.
      - **IndexedDB, not localStorage.** Images live in `files-db`/`files-store`, keyed
        by fileId, which localStorage seeding never touched. The boot script seeds and
        reads that store directly.
      - **The app's own module script is now HELD.** `proxy_excalidraw()` turns it into
        `window.__haipipeApp` and the boot script appends it once seeding has actually
        finished. A classic script in `<head>` was enough to beat localStorage, which
        is synchronous; it is NOT enough for IndexedDB, and an app that boots mid-seed
        renders grey placeholders. A URL with no `board=` starts the app immediately,
        so a plain visit to the editor is unaffected.
      - **An image is uploaded once.** The tab tracks which fileIds the server already
        has (seeded from the scene it loaded), so a 1.5s save tick does not re-send a
        megabyte screenshot every time a line moves.
      Verified over HTTP end to end: a PNG saved, landed byte-identical on disk, left
      no base64 in the scene, and came back byte-identical through both the frame URL
      and the whole-scene URL; a frame with no images gets an empty files map. Plus 13
      new browser-stub assertions (app held until the seed lands, a plain visit still
      boots, an image sent once and not again) and the 25 existing ones still passing.
      ⚠️ The cost of the split, worth naming because "open it in any Excalidraw" was an
      argument for owning the file: read straight off disk by the VS Code or Obsidian
      plugin, images show as missing, since the bytes are beside the scene rather than
      in it. Through the server they are there.
      ⚠️ Still open on `QA4a`: deleting an image element leaves its file in
      `fig/assets/` (removing it automatically would leave undo with nothing to come
      back to), and editing the seeded ASCII text is still reverted by the next
      `xcal.py` run.
260726 · `0.27.0`
      **The excalidraw round-trips: what you draw lands in `fig/board.excalidraw`, and opening another page no longer offers to throw it away.**
      JL, on the 0.26.0 build: *"When I edit the excalidraw, the changes won't save. And when I open another new Page, it asks me to reopen again and overwrite the current one. What I added will be gone."* Both symptoms had one cause: the open-source app loads from `#url=` and saves to the browser, so the file was in the loop at neither end.
      - **`assets/xcal-boot.js`, injected by the proxy.** `proxy_excalidraw()` now rewrites the
        app's HTML to add one classic `<script>` in `<head>`, which is the only window in
        which `localStorage` can be replaced (a module script is deferred; a classic one in
        head is not). The script seeds the editor from the scene file and, in the editing
        tab, pushes changes back. `#url=` is gone, so the "Replace my content" dialog has
        nothing to confirm and never appears.
      - **The URL changed**: `?board=<scene>&frame=<page>` replaces `#url=…`. `xcal.py --wire`
        writes the new form; `board.md`'s `excalidraw:` line is unchanged.
      - **`POST /_board/excalidraw-save` MERGES.** With `frame=`, only that frame's slice is
        replaced and the other 27 are left byte-identical, which is what lets one file be
        edited from any page. The frame's id and name are forced back on save because the
        name IS the page's link; a deleted frame is restored; deleted elements are dropped;
        the write is atomic. Without `frame=`, the whole scene is replaced.
      - **An embed reads, a tab writes.** A board page carries one iframe per page, all on one
        origin sharing one storage key, so an editable embed would be 28 editors overwriting
        each other and then reading the result back as their own. An embed gets an in-memory
        storage and persists nothing; "✏️ Edit this frame" opens the one tab that writes, and
        a lock in real storage keeps it to one tab (a second drops to read-only and says so).
        The app REFUSES to restore `viewModeEnabled` from storage, found by reading its own
        per-key policy table; `activeTool` and `zenModeEnabled` do restore, and a locked hand
        tool is better anyway because panning and zooming still work.
      Verified server-side over HTTP (a rectangle drawn into QB3 lands in that frame, the
      other 27 slices compare identical, an unknown frame name and a path outside `--root`
      are both refused) and client-side against a stubbed browser, 22 assertions covering
      both modes, the save payload, the idle tick, and lock contention. **Not yet exercised
      in a real browser**: no browser was reachable from the session that wrote it.
      ⚠️ Two edges left, both on `QA4a`: a pasted IMAGE does not survive, because Excalidraw
      keeps images in a `files` map and the endpoint writes `elements` only; and editing the
      seeded ASCII text in Excalidraw is reverted by the next `xcal.py` run, since that text
      is a generated element (drawings around it are kept).
260726 · `0.26.0`
      **A board owns one excalidraw, a page owns one frame in it, and the frame opens onto the figure that page already had.**
      - `xcal.py <board-dir>`: builds `fig/board.excalidraw` from `board.md` and the pages.
        One scene, one frame per page, one row per `## Pages` group with the group's name
        above it, each frame sized to what it holds. `--wire` also puts every frame's URL
        into its page's `## Diagram`, replacing whatever was there. It is a separate script
        from `build.py` on purpose: `build.py` runs on every file save and a scene regen
        must not.
      - **Frames are seeded** with each page's first `## Diagram` fenced block, as one
        monospace text element. JL opened `?frame=QB3` on 260726 and found a blank
        rectangle, which is exactly what had been built: 28 named frames with nothing in
        them. A scaffold and its content are two deliverables and only the second one is
        visible, so shipping the first reads as a broken feature. The seed is ONE-WAY;
        the markdown stays the source, and 25 of 28 pages had a figure to give.
      - **Re-running is safe**, which is the only reason it is a script. Every minted id is
        prefixed (`frame-QA4a`, `t-QA4a-fig`) so a regen renames nothing and no page's link
        dies; an unprefixed id is a human's drawing and is carried through; a frame a human
        moved keeps its position; a prefixed frame whose page has been retired is DROPPED,
        which is `QA4a`'s dead-frame rule. Verified by injecting both cases. `--fresh` is the
        one destructive mode and is never the default. Overlapping frames are reported,
        since a kept position plus a recomputed width can collide.
      - `check.py` gained `open-with-done-items` and `partial-with-nothing-open`. SKILL.md's
        `sync` action has always required writing a page back in the same round; nothing
        ever noticed when a session skipped it. `QA4a` said "nothing is built and nothing is
        decided" on the day its whole route was built and running (JL 260726: think about
        how to update the related Q along the session). The check only sees `state:` and the
        boxes, so it is a backstop under the rule, not a replacement for it.
      - SKILL.md: an `excalidraw` action, and `sync` now says the trigger is **substantive
        work in the session**, not opening a page. Every piece of real work belongs to some
        page even when it started as a line of chat, and work that belongs to no page is a
        new page. "Done" means written back.
      ⚠️ **Not closed: the write-back.** `#url=` loads, the editor saves to the browser, so
      nothing drawn returns to `fig/board.excalidraw`. The scene is a view of the markdown
      and not yet a place to work.
      🩹 One regex cost four pages. `^\s*<url>\s*$` looks line-anchored and is not, because
      `\s` spans newlines: it ate the blank lines around the URL, and an off-by-one on
      `hit.end()` took the `#` of the next heading with it, welding `## Diagram` to the URL
      on three pages and giving a fourth two `## Diagram` sections. All four were repaired
      and `--wire` now rebuilds the section instead of splicing into it.
260726 · `0.25.0`
      **A board can now be checked, and an author note finally behaves the way the template said it did.**
      - `check.py <board-dir>`: the structural half of `QA9`, read-only, four families.
        BOARD (`board.md` against disk, declared Links resolve, ids unique), FACE (required
        sections, the four state values, references resolve, one sentence per line, no
        em-dash, English-only), PAGE (the built html: local hrefs resolve, tags balance,
        ids unique, the zero-script invariant), and TEMPLATE (render `ref/q-template.md`
        as a Q AND an S, then assert each of QA9's 15 constructs). It reuses `src/parse.py`
        rather than carrying its own grammar. Report-only, exit 0; `--strict` exits 1 on
        ERROR and waits on JL's ruling about whether a red result blocks a change.
      - A construct the template never demonstrates is reported as a GAP rather than
        skipped, which found three on the first run: code block, group title, excalidraw
        canvas are documented and untested.
      - `parse.strip_notes`: `<!-- ... -->` author notes are dropped BEFORE the text is cut
        into sections. `ref/q-template.md` has always told authors a note "is dropped at
        generation either way" and it was not: the only strip lived in the Stage Contract
        path, so a note written anywhere else came out as escaped `&lt;!--` prose. Order
        matters and cost two attempts to learn, because `split_sections` reads a `## ` line
        INSIDE a comment as a heading, so a note listing sections was torn in half and left
        a phantom section behind. Fenced blocks are protected and `<!-- haipipe:… -->` is kept.
      - The index page's ＋ button writes Boundary and Files, which `QA2` rules "strongly
        advised", and offers the optional sections as an author note. Its stub was a second
        definition of a new face carrying 4 of the template's 14 sections; a face generated
        from it arrived with no Diagram and nothing said one was available.
      - `prime_context` counts unresolved comments and unticked items separately and names
        each. One number announced as "unresolved comments" made a cold agent notice the
        mismatch, fail to resolve it, and invent an explanation for it.
      - `CHAT_RULES` lists the current section names, with the retired ones named as
        accepted aliases, and explains what a `>` lane is and that it is addressed to the
        turn reading it. It had described a face layout retired days earlier.
      - Index rows lost their coloured left stripe (`QA10`). Every row already opens with
        the state emoji, so the bar restated it in a second language.
260726 · `0.24.0`
      **Diagram was the last body section you could only read. Now you can draw into it.**
      - `🖼 Diagram` gets a `🖌 Add an Excalidraw canvas` control (`QD7`). Paste a share URL, hit
        Save, and `serve.py` writes it on a line of its own inside `## Diagram`: the same line an
        author types by hand, so the md stays the single source and an older copy of the skill
        still renders the result. Endpoint `/_board/diagram`, control `wireXcal` in `board.js`,
        styles `.xadd`. The generator was not touched.
      - One canvas per face: a second paste replaces the first instead of stacking iframes. The
        response says `replaced: true` when it did.
      - A face with no `## Diagram` gets one created immediately before `## Content`, which is where
        the fixed on-stage order puts it, and the response warns that a canvas without an ASCII
        figure is the half that disappears when it cannot load (`QA4 §2`).
      - A URL that is not `excalidraw.com` is refused with nothing written, and the section scan
        skips fenced code blocks so example markdown inside `QA4` is never written into.
      - `serve.py` takes `--host`, still defaulting to `127.0.0.1` (`QE6`). The bind address is this
        server's only access control, since there is no auth and `/_term/` is a real shell, so any
        non-loopback bind now prints a warning line at startup. Nothing changes for anyone who does
        not pass the flag.
      - `QA4 §2` documents the Excalidraw half as a mechanism rather than a mention: one URL alone
        on its line, what it renders, and why the fallback link and the ASCII figure both stay.
260726 · `0.23.0`
      **The first Board UI taste pilot is live, bounded by QA10.**
      - All native links, buttons, disclosures, fields, and explicit tab stops now share one
        high-contrast `:focus-visible` ring; pointer interaction keeps its existing appearance.
      - Four semantic radius tokens replace unrelated one-off values: inline highlight, control,
        surface, and pill. Focused faces keep their existing zero-radius, unframed reading mode.
      - `prefers-reduced-motion: reduce` now suppresses current and future transitions and animations.
      - The pilot is CSS-only and reversible: it changes no Markdown grammar, generated structure,
        interaction contract, or dependency.
260725 · `0.22.0`
      **The page directory is now called Pages.**
      - New and migrated boards use `## Pages` for the filenames, groups, group introductions, and display order.
      - Parser and structure writers treat `Pages` as the canonical section while continuing to read old `Roster` headings.
      - Board prompts, warnings, examples, Paper page creation, and the seven active boards now use the same plain term.
260725 · `0.21.0`
      **Content gets a second heading level, and 🔹 gets its meaning back.**
      - `####` is now a first-class paragraph heading (`.ph`): no icon, one size below a group
        title, its own spacing. It used to be flattened to `**bold**` before rendering, and a
        full-line bold IS the group-title construct, so every paragraph arrived wearing 🔹 and
        claiming to lead a run of items. Deleting the icon would have hidden the mistake; the
        page was not over-decorating a paragraph, it was calling it something it is not.
        On the MISQ board the split came out 113 paragraph headings · 82 job lines · 31 group
        titles, with 🔹 left only on the 31 that really lead items.
      - A full-line `(…)` directly under a `####` heading is that paragraph's **job line**
        (`.pj`): grey italic, on stage, one line only. It is the scan hook that lets a reader
        see what each paragraph does without reading the prose, so it is not hidden behind a
        click. Only the line immediately after the heading is read this way.
      - Focus-mode spacing fix: `.q:target .ph` (0,3,0) outranked `.ph:first-child` (0,2,0), so
        the first paragraph after a section heading opened 22px low instead of 2px, and only in
        sections that begin with a heading, which is why it read as inconsistency rather than as
        a gap. `.gt` had already been patched for this once; both now share one selector.
      - **The rule these render:** Content carries exactly two levels and the depth lives in the
        numbering, not the heading level. `###` is a division that folds on its own, `####` is one
        paragraph inside it, and there is no third level because the page folds exactly one. A
        division is written only when it holds something, so a flat section carries one
        `### §1 Introduction` over its paragraphs while a subsectioned one starts at `### §6.1`.
        The shape is then checkable without reading: the subsection count is the number of `###`
        headings whose number contains a dot.
      - An S page title may carry the artifact's own number when it is offset from the board
        index (`S Main 7 · §6 Results`), so the derived Content heading reads
        `📚 Content · Main 7 §6 Results` and the two numbers stop competing on one screen.
      - New writing rule: **an ASCII figure must survive being copied.** Never draw two trees side
        by side; the column boundary is whitespace, it disappears on paste, and the right column's
        rows read as branches of the left one. Real case: a two-column comparison of two heading
        trees came back pasted as one tree with the wrong nesting.
      - Docs caught up with code that had already shipped: the levels and the job line existed only
        in `src/body.py` and `assets/board.css` and were documented in none of SKILL.md,
        `ref/board-form.md` §4/§5, `ref/writing-rules.md`, or `ref/q-template.md`. All four now
        carry them, and QA4 records the ruling, the Law, the Glossary terms, and the Lesson.
260725 · `0.20.0`
      **Sentence apparatus v1 (QA8): click a sentence, see its evidence.**
      - A plain sentence followed by `>` lines now renders as a native `<details>`: the sentence
        stays on stage with a ⚑N badge; the `>` lines fold into a drawer beneath it. Typed lanes
        name the attachments (`> Citation:` 📚 · `> Value:` 🔢 · `> Display:` 🖼 · `> Check:` ⚠️ ·
        `> Q-consumer:` 🔎 · `> Link:` 🔗 · `> Source:` 📄 · `> Note:` 📝); `> WHO:` review threads
        join the same drawer with their comment styling. Implemented in `src/body.py`
        (`render_apparatus` + the `last_p` attachment walk) and `assets/board.css`.
      - Attachment is by adjacency: a `>` run under a sentence (blank lines tolerated) belongs to
        that sentence; a run with no sentence above it renders as before, and the supporting folds
        (Discussion, Why here, Law, Lesson, Glossary, Log) never fold apparatus.
      - Zero-script invariant holds (native details). Pages change only where `>` lines already
        follow a sentence. Piloted on the boardform lab board (QA8 ruling + QA4 self-demonstrating
        subsection); the MISQ paper board is untouched pending JL's acceptance.
      - Click-to-add: `POST /_board/sentence` inserts `> Lane: text` directly under the exact
        sentence in the md (markdown-stripped anchor match, visible failure on a miss) and rebuilds.
        On the page: click a bare sentence for the lane + text form, or the "➕ add to this
        sentence" row inside any open drawer. Script-only enhancement over the no-JS reading path.
      - Sentence hover tint (accent at 8%) shows which sentence a click or selection will target.
        The form opens on DOUBLE-click, leaving single click free for reading and selection.
      - Copy is section-level: every section heading carries a ⧉ button that copies that whole
        section as clean plain text, folded drawers and item explanations included, with no badges,
        buttons, or highlight formatting. A per-sentence copy button was tried and removed.
      - Every section folds from its own heading (Content, Items to Finish, Where we are, Files), the
        native-details mechanism Diagram already used. All open by default except Diagram, since the
        reading path must survive a reader who never clicks; folding is display-only, so Ctrl-F, the
        section ⧉ copy, and the no-JS fallback are unaffected. Expand-all and ⧉ no longer toggle the
        section they sit in, and ⧉ force-opens a folded section in its clone before copying.
      - `ref/q-template.md` brought up to these rulings, then hardened by a fresh-context cold read:
        the apparatus example was itself hard-wrapped and taught the failure it warns about (a wrapped
        lane becomes its own sentence row and steals the lanes below it); the S title convention that
        feeds the Content heading was undocumented; the contract markers must not be hand-copied
        (a hand-written sha reports the page unsynchronized, and sync replaces anything between them);
        `requires:` resolves S ids bare but needs a real filename with extension for anything else.
      - Opening starts fully collapsed on S pages (JL 260725: "all the things here should be hidden").
        Why this matters, the optional Stage Record, the Stage Contract, and the contract's own parts
        all begin shut, so the lead question is the only thing on stage. Q pages are unchanged.
      - S Content holds the stage's real product only (QA4 Law, JL 260725). Inherited contract
        material belongs to `## Stage Contract`, settled flags and corrections to `## Where we are`,
        open work to `## Items to Finish`. The Content heading now NAMES the stage on S pages
        (`📚 Content · Main 7 Results`) instead of counting subsections; Q pages keep the count.
        Authored subsections under `## Stage Contract` are sync-safe: `replace_managed` rewrites
        only the span between the `haipipe:contract` markers (verified on the MISQ Results page).
      - Comment highlights are painted with inset box-shadow instead of background-color, so text
        copied into Word no longer carries the pale yellow fill; `code_or_link` stopped
        double-escaping code spans (backticked `>` rendered as `&gt;`).
260725 · `0.19.0`
      **The reading pass: sentence lines, serif prose, Stage Contract inside Opening (JL 260725).**
      - Stage Contract now renders INSIDE Opening as one collapsed disclosure after Why this matters
        and Stage Record (JL: "within the Opening. Not a separate section."). The standalone section
        between Opening and Diagram is gone; comment anchors scan it as part of Opening. Source
        anatomy is unchanged: S files keep their `## Stage Contract` section and managed markers.
      - One sentence per source line is a writing hard rule (ref/writing-rules.md). The renderer has
        always given each plain prose line its own row, so a mid-sentence hard wrap became a broken
        line on the page. Both live boards were re-flowed to sentence lines (boardform 25 faces,
        MISQ lifecycle 42 faces); prose content untouched, only line boundaries.
      - Face prose (Opening lead, paragraphs, item titles, group titles) switched to a serif reading
        stack: Charter / Georgia / Cambria with Times New Roman as the print-classic fallback. UI
        chrome (ids, pills, bars, code) keeps its sans/mono faces.
260725 · `0.18.0`
      **Display is independent, and S pages inherit explicit requirements and writing style.**
      - Canonical paper families are now Seed, Work, Venue, Display, Main, Appendix, Submission.
        Display owns the claim-to-display map, approved assets, captions, statistical labels, and
        placement consumed by Main and Appendix.
      - S metadata accepts `requires`, `style-from`, `provides`, and `contract-source-hash`. Pages
        adjacency never implies a dependency.
      - `stage.py new|sync|check` creates S pages, refreshes only the managed Stage Contract block,
        and detects upstream source changes. `build.py` remains render-only and reports stale contracts.
      - `stage.py sync --all` follows the explicit dependency graph in topological order; Pages order
        remains a navigation concern and never controls inheritance.
      - S pages render `Stage Contract` between Opening and Diagram. Required Inputs and Writing Style
        stay separate from authored Content; upstream prose is linked and summarized, never copied whole.
260725 · `0.17.1`
      **S families are stable homes, while Pipeline owns execution and revision loops.**
      - The six-family index order no longer claims every paper runs as a simple family-by-family line.
        A Pipeline may revisit Work/Displays after Narrative while keeping one stable Work group.
      - Submission pages are reused per initial submission and revision round. An external decision
        reopens affected Work, Main, or Appendix pages, then returns through reconcile, compile, review,
        and submit; it does not duplicate a new S page set for every round.
260725 · `0.17.0`
      **Paper lifecycle S pages now use readable, full-name families.**
      - Canonical filenames use `S-<Family>-<unit>-<slug>.md`, with six families in lifecycle order:
        Seed, Work, Venue, Main, Appendix, Submission.
      - Seed can carry both `S Seed` and `S Literature`; Main exposes one page per manuscript section;
        Appendix uses `0` for control and `A-F` for units; Submission makes reconcile, compile, review,
        and submit explicit gates.
      - HTML ids are readable (`#S-Main-3`, `#S-Appendix-D`), badges name the family, JSON emits
        `family`, and the index reports a separate progress fraction for each family.
      - Legacy `S0`, `SM0`, and `SA0` filenames remain parse-compatible for existing boards, but the
        authoring docs and template no longer recommend those abbreviations.
      - The MISQ paper board was migrated end to end, including a new literature-seed page and three
        terminal submission pages.
260725 · `0.16.1`
      **Paper lifecycle boards now expose the lifecycle as their primary index structure.**
      - One Pages group represents one paper stage, ordered S0 through S5.
      - The canonical S face is the first row; every Q row after it is a ruling owned by that stage.
      - Stage-only groups remain visible instead of being merged into broad QA/QB/QC buckets.
      - Group headings retain a unique Q family writer key, such as `QD · S4 · Display`, so index-side
        add/archive controls keep working.
      - The MISQ paper lifecycle board was reorganized into one paper-level frontier group plus eight
        stage groups, with S4→QD2-QD8 and S5→QE2-QE7 ownership explicit.
260725 · `0.16.0`
      **Creating an S lifecycle stage is documented, not only rendering one (QB pass).**
      The QB2 fresh-agent acceptance was re-run against the shared Q/S skill (4 Q faces + 1 S stage
      on a lab data-retention topic; SKILL.md + `ref/` only, existing boards out of bounds). Verdict
      YES, first-try build, gate respected, Stage Record lifted. Everything it had to invent was on
      the S **authoring** side, and all of it is now written down:
      - `SKILL.md` `open` steps 1 and 4 ask for Q **and** S faces, give both filename shapes
        (`Q<letter><n>-<slug>.md` / `S<order>-<slug>.md`), state S's required `## Content`, and say how
        an S is listed in `## Pages`.
      - `close` and the Face section: both kinds share the same four `state:` values, and a new face of
        either kind starts 🔴 OPEN. ✅ means "every checkbox closed" on Q and "this stage's human gate
        passed" on S (what the index counts as `stages gated`). `human-gated` is not a state value.
      - `ref/board-form.md` §2 gained the S state mapping plus the Pages rule (bare filename, free-text
        group heading, own group or mixed in); §3's example gained an S line.
      - `ref/q-template.md`: the Q-consumer `**Probe:**` line no longer assumes a paper's `1-probes/`
        tree; on a standalone board name the real route or write `not opened yet`. Its state legend now
        carries the Q-versus-S ✅ distinction.
      - The build section names the interpreter split: `build.py` / `watch.py` run on any system
        `python3`; only `serve.py` needs the repo `.venv` (the SDK requires 3.10+).
      Board-side records refreshed in the same pass: QB1's stale figures (128 lines / five actions /
      CHANGELOG 0.2.0) replaced with the 0.15.x reality, QB2's second run and a new `## Law`, QB4 noting
      that QB5's `src/` split superseded its 850-line build.py, and the `ALIAS` / `sec()` pointers in
      QB3 and QA2 repointed from `build.py` to `src/common.py`.
260725 · `0.15.2`
      **The QD2 chat drawer header is quieter, clearer, and consistent.**
      - The saturated accent banner became a neutral 56px utility bar separated by one hairline.
      - Face id is compact mono metadata; the full title uses the remaining width and ellipsizes in CSS,
        preserving the complete title in a tooltip.
      - Terminal and close are matching 32px square controls with hover and keyboard-focus states,
        accessible labels, and a stable `>_` terminal mark instead of a platform-dependent keyboard emoji.
260725 · `0.15.1`
      **QA2's source-template contract now explicitly mirrors QA4's rendered Q/S face contract.**
      - `ref/q-template.md` states the fixed visible sequence, Q-versus-S Content requiredness,
        rationale placement, Q-consumer closure rule, and optional S-only `### Stage Record` behavior.
      - The board's QA2 face now specifies the source-to-render mapping for Opening, Diagram, Content,
        Items to Finish, Where we are, Files, and supporting folds; stale Q-only wording was retired.
      - Two fresh-context acceptance rounds rendered realistic temporary boards. The first exposed that
        Stage Record optionality was only implied; after revision, the second rendered one Q and two S
        variants and passed with Stage Record both present and absent.
260725 · `0.15.0`
      **A chatbot on the index page (JL 260725 on QC2: "just add a chatbot in the index page").**
      - It is the existing QD2 drawer and QD3 terminal, opened on `board.md` instead of one question.
        No new agent, no second engine; details recorded on QD2, entry point on QC2.
      - `serve.py` accepts `file: "board.md"` as one more face: the orientation block carries the
        index's own view (spine, close, every face's state + open-comment count); board-flavored
        rules; the restricted tier's "own files" widens to any `.md` inside the board folder
        (verified: in-board Write auto-allowed, /tmp Write denied).
      - The session id lands in `board.md`'s header (`session:` under `close:`), is parsed into meta
        (`src/parse.py`) and rendered as `data-bsession` on `div.wrap` (`src/page_board.py`), inside
        the live-swap region so it stays fresh without a reload. The drawer's ⌨ opens the same
        session in a real terminal (verified: same session id, proxy 200, clean release).
      - `assets/board.js`: `chatOpen('board')`; the bottom-right fab now also shows on the index,
        labeled "🤖 Board chat"; index flavor of the action buttons (🧭 which question should I act
        on · 🔧 handle open comments board-wide); `follow()` returns to the board session when you
        navigate back to the index. `assets/board.css`: the fab shows whenever the drawer is closed.
260725 · `0.14.0`
      **Stage orientation moved into Opening, and Opening now uses a compass.**
      - The visible heading is `🧭 Opening`, replacing the question mark with an orientation icon that
        works for both Q rulings and S lifecycle stages.
      - On S faces, the automatic "Why this matters" disclosure now lives in Opening and starts open.
      - An exact direct `### Stage Record` inside S Content is lifted into Opening and starts collapsed;
        the remaining stage subsections stay under Content.
      - Q faces retain "Why this matters" as Content's first open subsection.
260725 · `0.13.3`
      **Colleagues replaces the generic assistant role.**
      - User-facing prose now says colleague or colleagues instead of assigning everyone one generic role.
      - Each colleague signs and owns work with their own initials; examples use `ZW` rather than a
        shared role identity.
      - The comment picker defaults to `JL` and `CC`, while any colleague can add their own initials.
260725 · `0.13.2`
      **Diagram is now a real section and starts closed.**
      - The fixed visible order is `Opening → Diagram → Content → Items to Finish → Where we are`;
        Files follows.
      - Opening now contains the question lead and optional Boundary. Optional Diagram renders as a
        peer-level native `<details>` section whose heading stays visible while its figure is hidden
        until clicked.
      - The figure remains in the HTML and works without JavaScript; ASCII and embedded Excalidraw
        content retain their existing rendering once opened.
260725 · `0.13.1`
      **The visible first layer is Opening, not a peer list of Question, Boundary, and Diagram.**
      - The rendered hierarchy is `Opening → Content → Items to Finish → Where we are`; Files follows.
      - Opening contains the actual question lead plus optional Boundary and Diagram. The rest of the
        Question becomes Content's first "Why this matters" subsection, so Q faces follow the same
        visible rhythm even without an explicit `## Content`.
      - The source keeps `## Question` for precision, while `## Opening` is accepted as an alias.
      - Opening uses the same section-heading hierarchy as Content, Items, and Where.
260725 · `0.13.0`
      **One face grammar now serves rulings and lifecycle stages.**
      - `Q*.md` remains a board ruling; `S*.md` is a lifecycle stage. Both are recursively discovered,
        rostered, commentable, and rendered by the same face renderer.
      - `## Content` lands between Diagram and Items. It is optional for Q and required for S; each
        direct `###` heading renders as a native collapsible subsection.
      - Former stage `Q-consumer` blocks become recognizable checklist records under
        `## Items to Finish`. The answer must land, be interpreted, and be woven into Content before
        its box closes.
      - Question settlement and stage gates have separate index summaries. A stage carries a STAGE
        badge and never inflates the question settled count.
      - Focus mode now has a real narrow-viewport layout: smaller wrapping titles, zero-width-safe
        flex/detail children, and measured `clientWidth == scrollWidth` at a 390px device viewport.
      - The first complete consumer is the MISQ paper lifecycle board: 14 Q rulings + 8 S stages, with
        the previous stage files archived and all lifecycle `_LOG_*.md` sidecars removed at the user's
        request.
260724 · `0.12.1`
      **The drawer terminal stops smearing on emoji + CJK (QD3, JL's fig/image.png).** The cause left standing after 0.9.2's cell-metrics fix: claude's TUI counts 🟡✅💬 as 2 cells (modern wcwidth) while the vendored xterm.min.js only ships Unicode 6 width tables that say 1 — every emoji shifts the row, full-screen repaints land off-cell, and the frames interleave into the smear. Vendored `@xterm/addon-unicode11@0.8.0` (new `vendor/xterm/addon-unicode11.js`, whitelisted in serve.py's `serve_asset`, loaded right after xterm.min.js, `unicode.activeVersion = '11'`); verified offline that the v11 provider returns width 2 for 🟡✅💬汉 where V6 said 1. The stacked second cause fixed with it: Menlo has no CJK, fallback glyphs overflow the measured row — the drawer terminal's fontFamily now carries PingFang SC / Hiragino Sans GB / Microsoft YaHei and `lineHeight: 1.2` adds the headroom. Addon load is soft-fail (console warning, terminal still opens), so an older running serve.py cannot brick the drawer.
      Also in 0.12.1: **`scrub_cjk_comments` scoped to `<style>`/`<script>` blocks.** Run page-wide it treated body prose as code: QD3's `GET /_board/asset/*` glob read as a `/*` comment-opener, and the span to the next `*/` (inside QE3) was silently dropped the moment CJK landed in between — five slides (QD4–QE2) gone. build.py's no-JS invariant caught it; body prose is now never scrubbed.
260724 · `0.12.0`
      **ascii inside an item's fold (JL: "for each item's hidden text, add the ascii").** An INDENTED ` ``` ` fence in an item's explanation lines is collected into that item's hidden text (dedented, rendered as `<pre class="ip">`), instead of flushing the item and landing as a sibling block. Column-0 fences keep the old sibling behaviour, so the face stays title-only and the diagram lives behind the click — the QA4 item shape (heading + summary + prose) is unchanged, the ascii just joins it. This deliberately revisits the 1705 ascii-in-item experiment that 0.11-era reverted: that revert traded ascii away to get the QA4 shape; now both hold at once. First user: the CMS board's QC10 (AMI → CABG), all 6 items. CSS: `.bd pre.ip` one size down, horizontal scroll of its own. Regression: boardform board (28 questions) rebuilds unchanged.
260724 · `0.11.0`
      **A board can sit on an existing tree (QC3), show other files' content live (QF1), and the Python got its src/ split (QB5).** All three driven by the first board laid directly over a paper's `0-lifecycle/`.
      - **folder questions (QC3, JL ruling).** A question is a `Q*.md` at ANY depth under the board folder: `q_files()` discovery (rglob, skipping path segments starting `_`/`.` and `fig/`), Pages keeps bare filenames, duplicate basenames warn and keep the first, the page's data-file carries the board-relative posix path, serve.py vets it (`vet_qpath`: no absolute, no `..`, basename must look like a Q file), archiving flattens into the board's `_archive/`, watch.py watches the whole tree. Flat boards untouched (regression: unchanged question set).
      - **embeds (QF1, JL: "can a markdown file incorporate another file?").** `![[path]]` / `![[path#Section]]` on its own line pulls another file's content into the slide at build time, by reference — zero copy, zero drift, zero dialect knowledge. `src/page_stage.py` renders generically (atx AND setext headings, fences, lists, quotes, `|` record lines) under a "live from source" header; every failure mode (missing file, non-md/txt, heading not found) is a visible warning box, never a silent gap; no recursive expansion. Comments on embedded text keep living in the FACE's `## Comments` and re-anchor against the re-rendered embed at rebuild. Still open on the board: the paper-side anchors handshake (haipipe-paper-stage contracts).
      - **src/ split (QB5, JL named the page modules).** build.py 995 → 70 lines, code moved VERBATIM to `src/{common,parse,body,page_board,page_question,page_stage}.py`; serve.py imports `QNAME`/`vet_qpath`/`q_files` from `src/common.py` instead of duplicating. Byte-identical proven on board.html AND `--json` BEFORE any feature landed.
      - **bugfix, found by the byte-identical gate:** the old single-function `render()` reused `lab`, so any question WITH comments wore the comments count in its state pill (`✅ 💬 Comments (0 open / 7) …`) instead of its state label. Reproduced first to prove the move pure, then fixed (`cm_lab` in `src/page_question.py`).
      - **doc slides (QF2, JL: "no need to generate QB3-claims.md").** A Pages line `doc: <path> <path>…` renders the listed source files DIRECTLY as one slide (id = first file's stem, title = its own `#`/setext title) — no Q wrapper at all. Doc slides are views, not questions: no state pill, no Items counting, no comment target, excluded from the settled count and the bar. Files are explicit, so `_LOG_*.md` can be shown even though `_` paths are excluded from Q discovery.
      - First consumer: `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/` — 14 ruling Q slides + 8 doc slides after JL's scope ruling ("I think 14 ruling faces"): every stage renders straight from its own docs (0-seed, 1a-resource, 1b-claims, 2a-venue, 2b-pitch, 3-narrative, 4-display + _DISPLAY_REQUEST, z-structure), while QA1 + QD2..QD8 + QE2..QE7 keep Q files, live embeds, and comment write-back (verified over HTTP on 5599). The settled bar counts the 14 rulings only.
260724 · `0.10.0`
      **The index becomes editable (QC2, JL): groups introduce themselves, and the board's structure is writable from the page.**
      - New Pages grammar: plain lines between a `### ` group heading and its first `.md` entry are the GROUP INTRO. Line 1 renders as an always-visible sentence under the group header; further lines become the click-to-expand "what this group is for, why it is here" body. Rendered as a native `<details>`, so strip-scripts still leaves the whole board readable; `parse_dir` collects intros into `meta["groups"]` and the `--json` path carries them for free.
      - One structure writer: `structure_op()` in serve.py behind `POST /_board/structure`, imported by the console's boards_api (QE3: one writer set, never reimplemented). Ops: `add_group` (letter auto-picked, optional hook/body intro), `add_question` (seeds a stub Q file in the house shape, numbers past the group's max, lists it at the group's tail), `archive_question` (logs the move in the Q's `## Log`, moves the file to `_archive/` inside the board, drops the pages line; NEVER deletes), `archive_group` (refuses while the group lists any question).
      - Page controls (board.js/css): ＋Q on each group header, ＋Group at the index tail, hover 🗄 on rows and headers with a two-click "sure?" confirm and an inline mini form (no native dialogs). Wired into `__boardRewire`, so they survive QD6's in-place swaps; after each op the server rebuilds and the watcher refreshes the page under you.
      - Index rows carry `data-f` (their file name) and group headers carry `data-g`, so the page controls address md reality instead of guessing from display text.
      - Verified: a full add→archive round trip leaves board.md byte-identical; refusal paths (non-empty group, unknown op, taken letter) exercised over HTTP on 5599 and through the console relay on 8093; the boardform board's five groups now carry real intros (moved out of `## Pipeline`, which keeps only the overall narrative, so nothing is said twice).
260724 · `0.9.2`
      **The terminal self-heals, and its columns stop lying.** JL's screenshot (QD3's Lesson) showed reconnect banners knocking six times on a terminal that had been RELEASED — reconnecting cannot revive a dead ttyd — over a TUI mangled by drifting column math.
      - after 2 failed reconnects the drawer now respawns the terminal through `/_board/term` (`--resume` restores the session) instead of knocking to 6 and giving up.
      - `fitTerm` reads xterm's real rendered cell size (fallback to the old constants) and refits 350ms after connect — the pty and the pane agree on width, claude repaints clean.
260724 · `0.9.1`
      **No button closes the chatbot anymore.** JL clicked the drawer's "↻ Reload to see the result" and lost the drawer — that button predated live refresh and did a hard `location.reload()`, which tears down everything the scripts built. All four reload sites (the drawer's post-write button, the drawer's ↻, the dock panel's ↻, the discussion-add success) now call `window.__boardRefresh` — the QD6 in-place swap, run immediately — so content updates under you and the drawer stays open mid-conversation. Labels renamed to "↻ Refresh in place" / "↻ Refresh". First edit made directly in `assets/board.js` since the QB4 split — checked with `node --check` on the real file.
260724 · `0.9.0`
      **Live refresh, an honest wait line, and the QB4 split.** Three JL asks in one afternoon of drawer-testing.
      - **live in-place refresh (QD6).** "When the chat changed something, refresh automatically — and my chat interface is still there." The page HEAD-polls its own URL every 4s (both servers send Last-Modified; the console's page route gained HEAD) and, on change, swaps ONLY `div.wrap`: content updates under you, scroll restored, "↻ board updated" toast, held while text is selected. The chat drawer (mid-stream included), terminal, and comment dock hang off `<body>` and never notice. No Node, no reload, drawer survives — that requirement decided the design.
      - **the wait line tells the truth (QD2).** serve.py emits `stage` events ("booting claude — the full tier loads the whole skill registry…", "session up — sending your message") so the drawer shows real progress instead of a static "…thinking"; the collapsed thinking block is labeled `💭 Thinking (N chars — click to reopen)`. Verified along the way: resumed sessions DO stream thinking now (the explicit `thinking={enabled}` option cured yesterday's loose end ②).
      - **build.py split into assets (QB4).** 2,488 → 850 lines: the page's JS and CSS now live as REAL files — `assets/board.js` (1,173 lines, `node --check`s in place) and `assets/board.css` (465 lines) — read and inlined at build, output still ONE self-contained board.html. Byte-identical proven on a frozen board (split vs. mechanically re-joined build), a proof that caught two wrapper-newline slips before they shipped. The grammar's home stays the skill; `haichat-board/` keeps importing it.
260724 · `0.8.0`
      **The gate shows the change (duplicating the VS Code extension, step 1).** JL: "what is the backend of the vscode claude plugin? I want to duplicate it." The backend is the `claude` binary over the stream-JSON agent protocol — exactly what the drawer already drives through `claude_agent_sdk`; the visible delta was the gate.
      - serve.py's permission ask events now carry `detail`: Edit → old/new strings; Write → the file's current content vs. the proposed; MultiEdit → per-edit pairs (capped at 6); Bash → the command. Truncated (4k/edit) — a gate preview, not a diff viewer.
      - the drawer renders it: − red blocks, + green blocks, commands verbatim, above Allow once / Always / Deny. Strip-scripts invariant unaffected (the gate only exists in the live layer).
      - honest status: emitted JS node-checked; a live gate-pop E2E is still owed (full-tier boots load the ~150-skill registry and outran the test window).
      - next duplication step (QD2 ④): one persistent claude process per session, like the extension — also the cure for those slow boots.
260724 · `0.7.1`
      **`## Files` links actually open.** JL clicked `cms_production.do` on the CMS board and nothing usable happened — the link machinery (`resolve()`'s walk-up + `## Links`) was fine; the serving side wasn't.
      - `EXT` widened: `.do .R .sql .tex .bib .toml .csv .tsv .ps1 .log` now count as path-like, so backticked references to them resolve (existence-checked, as always).
      - `serve.py` serves source-ish suffixes as `text/plain` — they display in the browser instead of downloading (default mimetypes made `.do` an octet-stream).
      - The first consumer moved: `boards_api.py` now lives in HAIChat-SPACE's **`haichat-board/`** sibling project (own service on 8094; `haichat-inlab` imports the same router). Its page serving widened to any existing file under the space root, read-only, matching serve.py — that is what makes a `## Files` click work in the console.
260724 · `0.7.0`
      **English output + the parser as a service.** JL: "put all the things in English, no Chinese anymore — in the board html or markdown."
      - **the emitted page is fully English.** All user-visible chrome strings in `build.py` translated (index labels, tooltips, comment badges, the CLI summary line); `<html lang="en">`; comment quotes render as `“…”`. New `scrub_cjk_comments()` drops CJK-bearing CSS/JS comments from the **emitted** page only — the source keeps its comments for developers; the build asserts the page still reads with scripts stripped, as before.
      - **comment grammar widened to curly quotes.** `CM_HEAD` (build.py) and `resolve` (serve.py) accept `“…”` alongside `「…」`/`"…"`, and `serve.py`'s writer now writes `“…”`. Found the hard way: an English board written with curly quotes parsed to zero comments — they silently vanished from the page (~19k chars of body reappeared after the fix).
      - **`build.py <dir> --json`** — the parser half exposed as a service (the boardform board's QE3: one grammar, two render paths). Emits meta + per-question `{state, owner, done/total, comments_open/total, sections}` from the same code the HTML is built from, so JSON and HTML cannot disagree (asserted in the consumer's tests).
      - **first external consumer: `haichat-inlab`'s `boards_api.py`** (HAIChat-SPACE, branch `feat/haichat-board`) imports `build.py`/`serve.py` from this skill dir — SPACE mounting, board discovery, page serving, and the comment/discuss/resolve write-backs, none of it re-implemented. Design record: the boardform board's QE2/QE3.
      - **terminal smoothness (QD3 ①–④):** the drawer terminal now auto-reconnects with backoff (the xterm survives, scrollback intact; the post-auth resize makes claude repaint), sends a same-size resize op every 30s as keepalive, refits via ResizeObserver when the pane resizes, and pre-warms the xterm assets on ⌨ hover (assets only — never `POST /_board/term`, which takes HOLD).
      - the skill's own board (`diagram/01-boardform-260722/`, 23 questions) fully translated to English — body, JL quotes, comments, logs.
260723 · `0.6.0`
      **The question page was reordered so a stranger can read it.** JL: "currently it is very very hard for a fresh eye to understand." The diagnosis was ordering, not wording — the page gave you *what we did* before *what we're deciding and why*.
      - **on-stage order is now fixed: intent first, state second.** `Question → Boundary → Diagram → Items to Finish → Where we are → Files`. Previously `Now` sat above `Done when`, so a reader hit a wall of implementation detail before learning the goal, and `Why here` — the single most orienting paragraph — was buried fifth.
      - **`## Question` became a lede plus bullets.** It renders through `body()` now: the first paragraph is the 21px lede, and 2–4 bullets carry *why it's hard / what breaks if we don't decide / what it affects downstream*. The acceptance bar is stated in QA4's `## Law`: **read this one section and a zero-context reader knows what the question is.**
      - **new `## Boundary` section** (`.bnd`, grey rule) — what the question covers and, more importantly, what it does **not**, naming the question that owns the excluded part. Without it readers bring another question's expectations to this one. Optional but strongly recommended.
      - **new `## Files` section** (`.fls`, blue rule, last on stage) — which files this question touches, and what each one's role is. Read the question, then know where to go; change a file, then know which question to write back to. Paths in backticks become clickable through `board.md`'s `## Links`. Optional but strongly recommended.
      - **`## Done when` → `## Items to Finish`, `## Now` → `## Where we are`.** Plainer names for a fresh reader.
      - **`## Why here` retired** — its job moved into `## Question`'s bullets. Boards that still carry the section parse fine; it renders in the bottom folds, so no content is lost.
      - **no board breaks.** `ALIAS` now maps one slot to many names, so `Done when`/`Items to Finish`, `Now`/`Where we are` and the old Chinese names all resolve. Every existing question file rebuilt untouched.
      - **QA2 and QA4 reopened (`✅ → 🟡`).** The layout and the template were both settled under the old structure — this change invalidates them. QA4 carries the new `## Law` and a `## Lesson` worth keeping: *it was closed ✅ that same morning and reopened by one sentence from JL, because the finish line never included "a stranger can read it."* Every one of the board's questions was then converted to the new shape — Question as lede-plus-bullets, plus `## Boundary` and `## Files`, with `## Why here` folded in and removed (18/18, verified against the *rendered* page rather than the markdown, because a substring check gets fooled by headings that appear inside ascii fences — QA2 lost a whole section to exactly that). Still owed: the fresh-agent cold read.
260723 · `0.5.0`
      - 新增 **view** 动作：「打开 <板文件夹>」= 看已有的板，不是开新板。
        之前只有 open（开新板），第 5 步还只写「打开 board.html 给用户看」而没给命令，
        新 agent 会去跑 `open board.html` —— 那是在**服务器**桌面上开，用户（Remote-SSH，
        浏览器在自己笔记本上）什么都看不到。现在写明唯一有效的方式：
        通过 VS Code IPC socket + `browser.sh` 把 `http://127.0.0.1:5599/<板>/board.html` 推过去。
      - frontmatter 的 description 补上「打开这块板」触发词，并写明 view ≠ open、禁用 `open`/`file://`。
      - open 第 6 步改成「按 view 那节推到用户的 VS Code 浏览器」。
      - 清掉写死的「14 题」（板的题数会变，写死必过期）。
260723 · `0.4.3`
      A compose box in every question's Discussion — write a thought in bulk, it lands in `## Discussion`.
      - **`## Discussion` gets a textarea.** Inside each question's Discussion fold there is now a box + signer dropdown + "➕ Add to discussion". Type a thought — a whole block, *not* pinned to a sentence the way a comment is — pick a signer, press Add: serve.py appends it as `> WHO: …` to that question's `## Discussion` and rebuilds; a reload shows it. Reuses the existing write path (new `/_board/discuss`, sibling of `/_board/comment`) and is fence-aware like the comment fix, so it never lands in a `## Discussion` line shown inside a code example. With serve.py not running the button says to hand-write it instead. The box is inert static HTML without the script, so the invariant (strip every `<script>`, the prose survives) still holds. Decided the simple way (JL): into `## Discussion`, not a new section — reuses the free-form thread that already exists.
260723 · `0.4.2`
      A third level of hierarchy inside a section — the **group topic** — plus the comment-writer bug that surfaced it.
      - **a whole-line-bold `**…**` becomes a group topic.** A line that is entirely bold is no longer just a bold paragraph; it renders as a 🔹-marked, slightly-larger heading that leads a cluster of items — sitting between the section heading (`.ch`, underlined, 📍/🎯/💡) and the item names (`.bt`, `▸`). Three visible levels now: 📍 section ＞ 🔹 group ＞ ▸ item. The 🔹 is the default marker; write an emoji at the start of the bold line (`**🎨 …**`) and it becomes the marker instead — the icon is *authored*, never guessed by the generator (build.py has no LLM, and guessing an emoji from keywords is exactly the kind of machine-guess the writing rules forbid). Mixed-bold lines (`**a** b`) are untouched — only fully-bold lines convert. Documented across `ref/q-template.md` (the `## Now` example), `ref/board-form.md` §5 (syntax table) and §8 (on-stage hierarchy). QA4 asked for it — recorded through the board's own comment layer.
      - **the Question block shows its name.** Every other section renders a label (📍 Now, 🎯 Done when, 💡 Why here); the question line carried only a bare `❓`. It now has a small `❓ Question` eyebrow (`.ql`, accent, above the question text), matching the rest. QA4's remaining open comment asked for exactly this — resolved and re-anchored on close (the `❓` moved into the label, so the quote moved to the question text).
      - **serve.py no longer writes comments into fenced examples.** `add_comment` matched the *first* `## Comments` heading in the file — including the one inside QA4's `md 段落→页面位置` code fence — so a comment on that slide landed in the example, not the real section. It now skips ``` fences when locating `## Comments` / `## Log`. The stray comment was moved back to QA4's real `## Comments`. (A running serve.py must be restarted to pick this up.)
260723 · `0.4.1`
      Doc-consistency pass out of the first fresh-agent acceptance read (the QB2 known-gap): a new agent, given only `SKILL.md` + `ref/`, opened a real board, built it, and the build.py-invocation drift it hit got fixed across the ref spec. `SKILL.md`'s open/build sections had already been corrected; `ref/board-form.md` had been left stale — exactly the cross-file drift this skill warns about.
      - **`ref/board-form.md` synced to the `<skill>/build.py` call.** §7 still showed the bare `python3 build.py <folder>`, which fails if you `cd` into the board folder (the script lives in the skill dir, not the board). It now reads `python3 <skill>/build.py <board 文件夹>` with the same "don't cd in" note the SKILL.md open/build sections carry. The last bare shorthand in SKILL.md's `sync` section was corrected too.
      - **`ref/board-form.md` §2 gains the slug + default-state rules.** `-<slug>` is short lowercase English, parser-ignored; a freshly-opened Q is always `state: 🔴 OPEN`. Both were in SKILL.md's open steps but missing from the "full spec".
      - **`ref/board-form.md` §3 marks board.md's required vs optional sections.** The Q-file spec (§4) already listed 必填/选填; board.md did not — `## Topic` / `## Pipeline` / `## Pages` required, `source:` / `## Links` optional, now stated.
      - **known-gap surfaced, not folded in.** The acceptance read hit a question the current model has no home for — where a note that is off the board's `spine` but worth keeping should go (not ⏸️ ON HOLD, which is on-topic-deferred; not a forced Q). Drafted as a question for the skill's own board; left off SKILL.md per the graduation rule (undecided stays out of the manual). Distinct from the existing `QB3` (migrate the two older boards).
260723 · `0.4.0`
      The single-Q slide layout (QA4) is settled and closed. The focus-mode slide got the polish that finally answered its last open fork — *what belongs on stage vs. folded* — and the rule graduated into the spec.
      - **section headings gain a line + an `expand all`.** Each of 📍 Now / 🎯 Done when / 💡 Why here now has an underline and, when it holds collapsible items, a right-aligned `expand all` that opens/collapses every item and code block in that section at once. Pure enhancement (`.secall` + a delegated click handler): strip the script and each item is still individually openable, all text stays in the DOM.
      - **code blocks fold by default.** A ```` ``` ```` block in the prose renders as a one-line `</> code · N 行` disclosure, revealed on click or via `expand all`; `## Diagram` (the headline picture) is the one that stays open (`body(txt, fold_code=False)`). So a slide's first glance is a clean column of item names + the diagram, not walls of code.
      - **the big title copies with a space.** `<span class="hid">QA4 </span>…` — the id and title were glued on copy (`QA4Single…`) because the gap was CSS `margin`, not a character; a real space now sits inside the badge so the heading copies as `QA4 Single-Q slide layout`.
      - **QA4's `## Law` graduated into `ref/board-form.md §8`**, not SKILL.md — display spec stays in the spec doc, keeping SKILL.md lean (QB1's rule). The on-stage/folded rule, up-down `Now`/`Done when` stacking, long-Q scrolling (no truncate/split), no-16:9-lock, and the copyable-title note all live there now. Graduated list: `QA2 · QA4 · QA6 · QC1`.
260723 · `0.3.0`
      The graduation mechanism — SKILL.md is now defined as the board's settled questions, distilled. Plus the live layer (serve.py) gets a foothold in the manual.
      - **板 ↔ SKILL.md, written down.** New SKILL.md section: this file is the crystallisation of the skill's own board (`diagram/01-boardform-260722/`). A question that reaches `✅ SETTLED` graduates its `## Law` into SKILL.md; questions still `🟡/🔴` do NOT enter the manual — so a "just-decided" rule never gets written as iron law (QD1's permission rule was written hard, then overturned — the cautionary case). SKILL.md is therefore always *the sum of settled rulings, no more*. The rule lives in QB1's `## Law`.
      - **serve.py enters the manual.** New `serve` action: one server serves the whole repo root (`serve.py --root <root>`), giving every board live commenting-to-disk plus chat/terminal per question. The old `comment` text ("stage in localStorage → Sync to md") was stale — QA6 shipped Save-immediately-writes-to-disk; the section now says so, with the browser Sync/Copy path demoted to the serve.py-not-running fallback.
      - **chat / terminal held as provisional.** The QD group (drawer via claude_agent_sdk, terminal via ttyd) is real and running but still `🟡` — SKILL.md carries only a pointer to it, not rules, per the graduation mechanism.
      - **actions regrouped** — offline (`open · add · build · sync · link · close`, needs only build.py) vs live (`serve · comment`, needs serve.py).
260723 · `0.2.0`
      `SKILL.md` written. Comments become first-class. The zero-script promise is restated as what it actually protects.
      - **`SKILL.md` + three `ref/` files** — the skill is now readable by someone who was not in the room: `ref/q-template.md` (copy this to add a question), `ref/board-form.md` (full spec: folder, numbering, section↔page map, syntax table), `ref/writing-rules.md` (how to write it so people understand, plus the cold-read prompt and its convergence test). `ref/board-example.md` was replaced — it still held the pre-0.1 single-file `[BOARD]`/`[Qn]` form.
      - **`## Comments`** — inline comments pinned to a sentence, each with its own state: `- [ ] JL 「quoted sentence」 · 260723 1100` plus an indented body; `[x]` marks it solved. Open comments highlight their sentence in the prose and force the fold open; solved ones grey out and strike through. A quote that no longer matches the prose is flagged **⚠ anchor lost** on the item and in the fold label — a comment can never silently detach. `## Discussion` stays as the free-form thread.
      - **in-page commenting** — select a sentence, press 💬, write, Save. Comments stage in `localStorage` and go to the md in one shot via "Sync to md" (File System Access API) or "Copy". Any 1–4 letter initials work, not just the original defaults; new names are added from the dropdown and remembered, and each gets a stable colour.
      - **`watch.py`** — rebuilds on any `.md` change, so "Sync to md" → refresh is a closed loop with no Claude Code in it.
      - **topic/explanation bullets** — `- heading` plus indented lines renders as a bolded lead with its explanation underneath; `## Done when` items take the same shape. Long passages stop being walls of sentences.
      - **`## Log` takes a time** — `260723 1030 · what changed`; the time is optional.
      - **titles are phrases, ≤14 chars** — the full question belongs in `## Question`. The board's own ten titles went from 43 chars at worst down to 8–15.
      - **the invariant replaced the rule.** 0.1.0 asserted "zero `<script>` in the output". That became false the moment commenting shipped, and it was never the real guarantee anyway. What is asserted now: **strip every `<script>` and each question plus the full prose is still there** (checked on every build). Scripts may only enhance.
      Known gaps (tracked on the board at `0_utils/diagram/01-boardform-260722/`): "Sync to md" has never been run end to end (QA6), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), and comments already written into md have no check for a broken anchor after the prose is edited.
260722 · `0.1.0`
      First working version. Board = a folder; `build.py` turns it into one static page.
      - **board form** — `<unit>/diagram/<NN>-<topic>-<YYMMDD>/` holds `board.md` (title · `spine:` · `close:` · `## Topic` · `## Pipeline` · `## Pages`) plus one `Q<A><n>-<slug>.md` per question, plus generated `board.html` and `fig/`.
      - **binding is by PATH** — every `Q*.md` in the folder is on the board; `## Pages` only sets order and grouping. An unlisted file still renders (under ⚠️) and warns on stderr — a missed pages entry can never drop a question.
      - **Q file sections in English** — `## Question / Diagram / Done when / Now / Why here / Glossary / Discussion / Log`. Chinese section names still parse, so older boards build unchanged.
      - **`## Done when` is a checklist** — `- [ ]` / `- [x]`, with an auto count (`3/5`) in the panel header.
      - **`## Diagram`** — a fenced ASCII diagram per question, readable in the md and rendered as-is in the page.
      - **`## Log`** — dated one-line history per question (`260722 · what changed`).
      - **state labels** — `✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD`.
      - **zero `<script>` in the output, asserted at build time.** Every question is a real `<section>`; collapsibles are native `<details>`; navigation is plain anchors. The page cannot render blank.
      - **focus mode is pure CSS** — `:target` + `:has()` show one question full-screen, unbounded (no card border/radius/fill), 38px title, prev/next/index links. Same file serves both reading and projecting; there is no separate `deck.html`.
      Known gaps (tracked on the board at `0_utils/diagram/01-boardform-260722/`): `SKILL.md` is not written (QB1), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), inline comments are half-built (QA6 — the md syntax parses, the CSS does not exist yet).

<!-- haipipe:skill:log:end -->
