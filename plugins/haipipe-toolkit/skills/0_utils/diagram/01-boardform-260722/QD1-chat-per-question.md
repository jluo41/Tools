# A chat session per question
state: 🟡 PARTIAL
owner: JL
method: 定分级、读写权限、对话去哪；实现分给 QD2 / QD3

## Question
给板上每个 Q 挂一个自己的对话 —— 这件事本身要先说清楚：板级和题级各管什么？题级能读能写到什么程度？对话本身存到哪去？

- 为什么难
  一题一个对话，就必然要回答「同一条 session 能不能两个窗口同时开」。答错了轻则互相覆盖，重则 Claude Code 自己 fork 出第二条历史。
- 不定会怎样
  这是这块板唯一一个会**改变工作方式**的问题。定不下来，循环就还是「你在页面上评论 → 我在别处读 → 我再改 md」，中间永远隔着一次转述。
- 定了会影响什么
  它是 `QD2`（抽屉）、`QD3`（终端）、`QD5`（板级 agent）共同的地基 —— 那条 LAW 一改，三题都得跟。

## Boundary
- ✅ 这题管
  **规则**：板级 vs 题级的分工、一题一 session、一 session 一窗口、session id 存哪。
- ❌ 这题不管
  具体怎么实现 —— 网页抽屉是 `QD2`、真终端是 `QD3`、作用域放大到整块板是 `QD5`。

## Diagram
```
  board 级（就是「session for top」这个对话）
  ┌────────────────────────────────┐
  │ 开新题 / 关题 · 改 build.py、serve.py · 跨题的决定 │
  └───────────────┬────────────────┘
                  │  每题一个 session（id 写在该题头部 session: 行）
      ┌───────────┼───────────┐
      ▼           ▼           ▼
  ┌────────┐  ┌────────┐  ┌────────┐
  │ QA6    │  │ QD3    │  │ QB1    │  ← 题级，一题一 session
  └────────┘  └────────┘  └────────┘
   两个前端，同一个 session：
     💬 抽屉（QD2）   权限跟 CLI 一样：读随便读，写自己那题直接过，
                      写别的 / 跑命令 → 弹出来问你
     ⌨ 终端（QD3）   完全不受限，就是一个真 Claude Code

  为什么这个板天生适合：一题一个文件 —— context 边界和 session 边界都是现成的。
```

## Items to Finish
- [x] 说清楚 board 级和题级各管什么
      board 级 = 这个「session for top」对话：开/关题、改 build.py 和 serve.py、跨题的决定。
      题级 = 一个 Q 自己的 session：只围着这一题干活。写在 ## Law 和 ## Why here 里。
- [x] 定下题级 session 的读写权限
      **JL 拍板：跟 Claude Code CLI 一样，该问就问。** 不再是我原来硬编码的「只能改这一个文件」。
      读随便读；写这一题自己的文件直接放行；写别的文件 / 跑 Bash → 弹权限问你（允许一次 / 总是 / 拒绝）。
      终端（QD3）完全不受限。规则见 ## Now。
- [x] 定下对话本身去哪
      对话就是那个 session，**留着**：落在 `~/.claude/projects/<板文件夹>/<sid>.jsonl`，
      抽屉和终端都能 resume。板的 md 只留结果（`## Now` / `## Log`），不抄对话原文。
- [ ] 写清楚两个 agent 同时改同一个文件时怎么办
      LAW 已经挡住「同一题的抽屉 + 终端」（HOLD）。还没挡的：board 级这个对话和某题的抽屉
      可能同时动同一个文件 —— 这一条还没约定。**这也是这题还留 🟡 的唯一原因。**
- [x] 选实现路线
      两条都要：QD2（网页抽屉）日常用，QD3（真终端）当逃生口。都做完了。

## Where we are
三条框架问题都有答案了，剩最后一条（两个 agent 同改一个文件）没定。

- 分级
      board 级只有一个 —— 就是我们现在这个对话，JL 说的「session for top」。它管全局：
      开题关题、改生成器和服务器、跨题决策。题级每题一个，只围着那一题。
- 读写权限（JL 中途拍的板）
      原来 QD2 是我硬编码「题级只能改这一个 Q 文件」。JL 说「还是正常给权限吧，跟 CLI 一样」，
      于是改成：只读工具自动放行；写这一题自己的文件自动放行；写别的文件或跑 Bash → 页面上弹一个
      「允许一次 / 总是允许 / 拒绝」的提示，跟 CLI 那个弹窗一个意思。终端那条本来就不受限。
- 对话去哪
      不是「留不留」的选择题 —— 对话就是 session，本来就落在 `~/.claude/projects/` 下的 jsonl 里，
      抽屉和终端随时 resume。板的 md 只记结果。所以「板越来越长」这个顾虑，题级反而解掉了：
      每题的来回不进这个 top 对话，各自待在各自的 jsonl。
- 只剩一条没定
      board 级对话和某题抽屉同时改同一个文件，没有约定。日常够用（很少真撞），但要写下来才算完。

## Files
- `serve.py`
  `HOLD` / `RUNS` / `TERMS` —— 「一 session 一窗口」就是靠这几张表兜住的。
- 每题的 `.md` 头部
  `session:` 行就是那一题的 session id 存放处。

## Law
一题一个 session；会话开在 SPACE 根；N 题可以同时开 N 个终端。（JL 260723）

- 会话开在 SPACE 根，不是板文件夹
      抽屉（QD2）和终端（QD3）里的 `claude`，cwd 都是整个 repo（SPACE），不是板文件夹。
      为什么：一题的会话经常要碰它讨论的代码 —— 只给板文件夹太窄。
      因此 session 归档在 repo 根的 project 目录（`~/.claude/projects/-Users-…-Physician-SPACE/`）。
      写权限还是收着的（受限档只改这一题的文件），但**读的视野是整个 repo**。
- 题级会话一打开就被灌定位（JL 260723）
      不管抽屉还是终端，开场都塞一段 `prime_context`：这是哪块板、哪一题、这题问什么、
      几条评论没解决、文件在哪。抽屉走 system_prompt，终端走 `--append-system-prompt`。
      不占回合、不自动跑 —— 会话一开就知道自己在干嘛，不用人每次交代。
- 一个 Q ⇄ 一个 session
      session id 写在这一题文件头部的 `session:` 行，一题就一个。
      不管这个 session 是在网页抽屉里第一次开的，还是在终端里第一次开的，都指向同一个 id ——
      终端首次开会自己生成 uuid（`claude --session-id`）写回头部，不会冒出第二个没记录的 session。
- 同一个 session，同一时刻只有一个窗口
      抽屉和终端读写的是磁盘上同一个 `.jsonl`。同一题不能又开抽屉又开终端，
      否则会互相盖、或者 fork 出第二段历史。服务器用 HOLD 强制这条。
- 终端身份 = Q 文件路径 hash（跨板全局唯一）
      不是端口、不是「QD3」这种名字。两块板各自的 QD3 路径不同 → key 不同 → 天然分开。
      底层是一题一个 unix socket，没有端口池。
- 不同的题，各开各的
      QA6 的终端和 QD3 的终端是两个不同的 session，想同时开就同时开。
      N 道题 = N 个终端 = N 个 session，互不相干。要同时看，多开几个板页面标签。

## Lesson
**SDK 起的会话就是一个真的 Claude Code 会话。**
`claude_agent_sdk` 底下调的就是 `claude` CLI，记录跟平时的会话放在同一个地方：
`~/.claude/projects/<cwd 编码>/<session-id>.jsonl`（cwd 现在是 SPACE 根）。
**推论**：抽屉（QD2）和终端（QD3）不是两条路，是**同一个 session 的两个前端**。
这一条决定了 QD3 不用重新发明会话管理 —— 它只是换一个窗口去看同一段对话。

**会话绑在 cwd 上，改 cwd = 换一批会话。**
project 目录名就是 cwd 编出来的，一个 cwd 一个目录。把 cwd 从板文件夹改成 SPACE 根之后，
旧会话留在原板文件夹的 project 目录里，从 root 敲 `--resume <旧 sid>` 找不到；
连把 jsonl 复制到新目录都骗不过 resume（实测不认）。所以改 cwd 那次，各题的 session 都在 root 下重起了。

**先问「跑在哪台机器上」，再选方案。**
浏览器在 JL 的笔记本上，`claude` 在服务器上。所以不管走哪条，
真正跑 Claude 的一定是服务器那一侧，页面只是个窗口。

## Glossary
board 级 / 题级：一个对话的作用范围。board 级管整块板（开题、改生成器、跨题决策）；题级只管一个 Q。
headless session：不开终端界面、由程序调起来的 Claude 会话。

## Discussion
> JL: 我如何接一个 chatbot，打开它其实就是打开 Claude Code，然后它 take 这个页面当作 input and context？可以选择点它开或者不开。
> JL: 比如我评论完之后，打开 haichat，他就读我这个内容，更改 markdown 和 html 之类的。
> JL: 我们现在这个 claude session，就是 session for top，对吧？然后我们如何给每个 question 开一个 terminal 呢？
> JL: could we make a new Q for chat, one for terminal version, and then other one for the claude_agent_sdk version.
>> CC0723: 拆了。这一题只留「分级和边界」这三个还没答的问题；SDK 版归 QD2，终端版归 QD3。

## Comments
- [x] JL 「open claude in the SPACE dir, not in the board; same to QD1 and QD2」 · 260723 1430
      >> CC0723: 定成板级 LAW：抽屉和终端里的 claude 都开在 SPACE 根（读的视野是整个 repo，
      写权限仍收着）。QD2/QD3 一起更新了。副作用：改 cwd 会重置会话，各题在 root 下重起 —— 见 Lesson。
- [x] JL 「QD1 A chat session per question How do you want to update this as well?」 · 260723 1655
      >> CC0723: 三条框架题其实中途都有答案了：读写权限被 JL 拍成「跟 CLI 一样」、对话就是留在 jsonl 里、
      分级写进了 Law/Why here。都打了勾，只留「两个 agent 同改一个文件」这一条 —— 也是它还 🟡 的唯一原因。

## Log
260723 · 按新结构重写：Question 展开成「一段话 + 要点」，补 `## Boundary` 和 `## Files`；退役的 `## Why here` 并进 Question
260723 1745 · Law 加一条：题级会话一打开就被灌定位（prime_context，抽屉/终端各一套）—— 见 QD2/QD3
260723 1730 · JL 定：claude 开在 SPACE 根（不是板文件夹）—— 写进 ## Law，QD2/QD3 一起改。
              会话读的视野变成整个 repo；改 cwd 重置了会话（旧的留原地），补进 Lesson
260723 1655 · 按实际进展更新：三条框架题已答（读写权限 JL 拍成 CLI 式 / 对话留在 jsonl / 分级写进 Law），
              只剩「两 agent 同改一文件」未定；Diagram 和 Now 重写；删掉 Law 里已废的 ↗
260723 1445 · JL 定：拆成三题。这一题只留框架问题，实现分给 QD2（SDK）和 QD3（终端）
260723 1215 · JL 提出「每个 Q 挂一个 chat」，新开 QD 组和这一题
