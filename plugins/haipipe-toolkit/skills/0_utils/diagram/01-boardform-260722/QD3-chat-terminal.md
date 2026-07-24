# Terminal version: the real CLI
state: 🟡 PARTIAL
owner: JL
method: ttyd 起进程 + serve.py 反代过 5599；claude 开在 SPACE 根，一题一 session
session: d650c47e-0d7d-464d-8405-a98a545fe552

## Question
每个 Q 除了受限的抽屉，能不能再有一个**自己的真终端** —— 就是完整的 Claude Code，功能一个不少？

- 为什么难
  终端要跑在文件所在那台机器上，还得穿过 Remote-SSH 只转发了一个端口的限制；多块板、多题同时开，还不能互相撞端口。
- 不定会怎样
  抽屉终究是重搭的，遇到要跑命令、要用技能的活就卡住 —— 没有真终端，板就只能干「改文字」这一类轻活。
- 定了会影响什么
  跟 `QD2` 的分工从此不再是「安全 vs 不安全」（QD2 现在也能全开），而是**形态不同**：抽屉是重搭的对话框，终端是原样的 CLI。

## Boundary
- ✅ 这题管
  **真终端这一种形态**：怎么起、怎么穿过单端口、多板多题怎么不撞、进程怎么回收。
- ❌ 这题不管
  规则本身 —— 那是 `QD1`；也不管网页抽屉 —— 那是 `QD2`。

## Diagram
```
   浏览器（JL 的笔记本）                       服务器（文件在这台）
   ┌──────────────────┐                       ┌──────────────────────────────┐
   │ 板A/QD3 标签      │ /_term/cc6638…/ (WS)  │ ttyd -i haiboard/cc6638.sock  │
   │ 板A/QA6 标签      │ ───────────────────►  │   claude --resume a0c6698a    │
   │ 板B/QD3 标签      │        全部走          │ ttyd -i haiboard/3d798.sock   │
   │  …N 个标签…      │  已转发的 5599 反代    │   claude --session-id <uuid>  │
   └──────────────────┘ ◄───────────────────  │ …一题一个 unix socket，无端口 │
      每个标签 = 一题                          └───────────┬──────────────────┘
      = 一个 key = 一个 session      cwd = SPACE 根 ▼
                                    ~/.claude/projects/-Users-…-Physician-SPACE/<uuid>.jsonl
   key = sha1(Q 文件绝对路径)[:12]  ← 跨所有板唯一，板A/QD3 和板B/QD3 天然不撞
   cwd = 整个 repo（不是板文件夹）   ← 会话能读它讨论的代码；session 归档在 repo 根的 project 目录

   为什么走 5599 反代 + unix socket：只有 5599 转发到笔记本；不用端口池，
   一题一个 socket 文件（没有"分哪个端口 / 会不会占满"）。ttyd -b 挂子路径，serve.py 原样转（含 WS）。
```

## Items to Finish
- [x] 每个 Q 卡片上有一个 ⌨ 入口
      抽屉头部一个 ⌨，切过去整个抽屉变成这一题的真终端（iframe）。
- [x] 点它进的是**这一题自己的**那个会话
      有 session 就 `--resume`；没有就 serve.py 生成 uuid 写回头部、`--session-id` 用它。
      不会开出空终端，也不会冒出第二个 session。
- [x] 决定用哪条路
      **既不是 myrlin，也不是手写 node-pty，而是 ttyd + serve.py 反代。** 理由见 Now。
- [x] 端到端验过它真的能用
      从 5599 反代连 WebSocket，屏上是这一题的真会话（a0c6698a，带着之前的历史），
      发「只回 BOARDLIVE」当场收到回复。不是「应该能」，是实测过。
- [x] 能同时开多题
      多开几个板页面标签即可（每标签一题），不需要单独的「弹出」按钮。实测两个 ttyd 并存。
- [x] 端口 → unix socket，多板不撞
      不再抢 TCP 端口：一题一个 unix socket，key = 路径 hash 全局唯一。
      实测：同名 QD3 在两块板下 key 不同（cc6638… vs 3d798…），互不干扰。
- [x] 进程能自动收，不留孤儿
      启动先扫 TERM_DIR 杀掉上一轮遗留（不靠退出信号，最可靠）；退出再尽力收一次；
      `/_board/killall` 一键全关；关整个板页面时 `pagehide` beacon 通知释放。
      实测：造一个 stale ttyd → 启动 serve.py → 它被自动杀掉、socket 删掉。
- [ ] 安全边界要定成白纸黑字的规矩
      「写成文」的意思：把「谁能连、能碰什么、认证怎么做」全部明确写下来定死，别含糊留在脑子里。
      已有的护栏更强了：ttyd 只监听 unix socket 文件（连 TCP 端口都没有），只能从 5599 反代进，
      key 必须是已登记的 12 位 hex。没定的还是：ttyd 本身不认证，谁连到 5599 谁就能用；
      对外暴露前必须先定认证。

## Where we are
做出来了，就在页面里。抽屉头部 ⌨ 进终端，再点变 💬 交回 session。

- 终端画在抽屉里，用 xterm.js，不再套 iframe（JL：closer to myrlin / A）
      抽屉里直接跑 xterm.js（vendored，serve.py 从 /_board/asset/ 供），自己拿它连 ttyd 的
      WebSocket，说 ttyd 的子协议（auth 一条、尺寸一条、输入 '0'+data、输出帧首字节 '0'）。
      省掉 iframe 那层：没有 webview CSP、加载更快、能自己控制 fit/reconnect。
      ttyd 仍在后端当 PTY，只是前端不再是它的页面，而是我们自己的 xterm。
      验证：代理的 WS 握手是浏览器合法的（101 + Sec-WebSocket-Accept 精确匹配）；
      claude 输出经这条 WS 流到 xterm；坑见 Lesson。
- 走的是 ttyd + 反代，不是 myrlin，也不是手写 node-pty
      · myrlin 是一整个应用（AGPL、单独一个服务），拿来当「板里的一个终端」太重。
      · 手写 node-pty + xterm 要自己管进程、滚屏、重连，约 150 行起步。
      · ttyd 是个只干一件事的小工具（`brew install ttyd`），一条命令就把 `claude` 变成网页终端。
        serve.py 本来就在服务这个页面，顺手当反代 —— 最省。
- 一开就知道自己在哪一题（JL 260723）
      起终端时给 `claude` 灌一段 `--append-system-prompt`：这是哪块板、哪一题、这题问什么、
      还有几条评论没解决、文件在哪。用系统提示、不占一个回合、也不让它自动跑 ——
      你一打开，claude 就已经知道自己在干嘛，等你说话。ttyd 标签页标题也改成「QD3 · 标题」。
      实测：全新终端里问「我在做哪块板哪一题」，不给任何背景，它直接答「QB3 — Migrate the two old boards」。
- claude 开在 SPACE 根，不是板文件夹（JL 260723）
      `ttyd` 起 `claude` 时 cwd = 整个 repo。为什么：一题的会话经常要碰它讨论的代码
      （比如「迁旧板」得改板文件夹外的东西），只给板文件夹太窄。
      cwd 一改，两件事跟着变：① 系统提示给的是「相对 repo 根的路径」而不是光文件名；
      ② session 归档到 repo 根的 project 目录（`~/.claude/projects/-Users-…-Physician-SPACE/`）。
      代价见 Lesson：改 cwd 会把旧的板文件夹会话留在原地，各题在 root 下重新起。
- 一题一 session 是强制的（见 ⚖️ Law）
      终端首次开：serve.py 先生成 uuid、写进这一题头部 `session:`，再 `claude --session-id <uuid>`。
      所以「首次是在终端里开的」也不会留下一个没记录的 session。实测过：给没 session 的题开终端，
      头部立刻多出 `session:`；再开是 reused，同一个 id。
- N 题 N 终端，靠多开板页面的标签
      想同时看好几题的终端，就在浏览器里多开几个板页面标签，各自的抽屉互不相干。
      比一个「弹出」按钮干净，而且关标签时 pagehide 能把那个终端收掉。
      LAW 只拦「同一题的抽屉 + 终端」（同一个 `.jsonl`），不拦不同题。
- 全走 5599，底层是 unix socket 不是端口
      每题一个 unix socket（`haiboard-terms/<key>.sock`），没有端口池、不会占满。
      URL 是 `/_term/<key>/`，key = `sha1(Q 文件绝对路径)[:12]` —— **多块板各自的 QD3 天然分开**。
      serve.py 把 `/_term/<key>/…` 转给对应 socket：普通 HTTP 直接转，WebSocket 走 `Upgrade` 裸倒。
- 进程生命周期收口了
      · 启动先清上一轮遗留（扫 socket 目录杀残留 ttyd）—— 主力，不依赖能不能接住退出信号
      · 退出时 atexit / SIGTERM 再尽力收一次
      · `/_board/killall` 一键全关；`/_board/terms` 列出在跑的（跨板一起列）
      · 关板页面时 pagehide beacon 通知服务器释放抽屉里那个终端

**还没定死的：**

- 安全边界只剩「认证」这一条没写成文
      护栏已经不弱：unix socket（没有 TCP 端口可扫）、只能从 5599 反代进、key 必须已登记。
      唯一的口子：ttyd 本身不认证 —— 谁连到 5599 谁就能用。现在是纯本地 + SSH 转发，够用；
      哪天对外暴露，必须先加认证。这一条留着，等真要暴露再定。
- 关标签自动释放：抽屉里的能收，别的靠兜底
      关整个板页面时，抽屉里开着的那个终端会被 pagehide beacon 收掉。
      要一次清干净所有终端，用 `/_board/killall`（或重启 serve.py，启动时自动清残留）。

## Files
- `serve.py`
  `terminal()` / `proxy_term()` / `reap_stale_terms()` —— ttyd + unix socket + 反向代理 + 进程回收。
- `build.py`
  页面上切到终端那个入口。

## Lesson
**空壳 session（记了 id 却没聊过）会让 --resume 秒退，终端一开就死。**
`claude --session-id <uuid>` 起一个 session，但**只 boot 交互界面、没发过消息**的话，jsonl 不落盘。
下次开终端读到头部那个 id → `claude --resume <id>` → 「No conversation found」→ claude 立刻退出 →
ttyd 关连接 → 终端刚出 ttyd 的握手字节就黑掉。排查时表现成「收到 365 字节就断」。
修法：开终端前看**磁盘上有没有那段对话的 jsonl**，有才 `--resume`，没有（空壳或全新）用 `--session-id`。
抽屉那边同理：resume 前先查 jsonl 在不在。

**HOLD 卡住会让「打不开」看起来像 bug，其实是没释放干净。**
一个没跑完 / 没正常结束的抽屉或终端，会把这一题的 HOLD 留住，之后所有 open 都被
「session 正被…占着」挡下。排查 xterm 时，一个陈旧的 drawer-HOLD 挡了每一次终端 open，
让浏览器 mountTerm 永远拿不到 key —— 看着像 xterm 坏了，其实是 HOLD 没清。
兜底：`/_board/killall` 清所有 HOLD + 终端；真正的修是让每条路径的 finally 都可靠 release。

**会话跟着 cwd 走，改 cwd 就等于换一批会话；迁移 jsonl 不管用。**
`~/.claude/projects/` 下的目录名是 cwd 的斜杠换成横杠编出来的，一个 cwd 一个 project。
把 cwd 从板文件夹改成 SPACE 根之后：
  · 旧的板文件夹会话还在原来的 project 目录里，但从 root 敲 `claude --resume <旧 sid>` 找不到它。
  · 试过把那 6 个 jsonl 复制到 root 的 project 目录 —— **resume 还是不认**（发命令后文件不增长），
    因为会话是绑在原 cwd 上的，光挪文件骗不过它。
所以这次的做法是：清掉各题头部的旧 `session:` 行，各题在 root 下重新起一个 session（`--session-id`）。
旧会话没删，还在板文件夹的 project 目录里，真要看，`cd` 进那个板文件夹 `claude --resume` 就行。
**教训**：cwd 是会话的归属，不是一个可以随便改的参数 —— 改它 = 这一题从头开始。

**首次开会话要自己定 id，别让它自己生。**
`claude` 不带参数会自己造一个新 session id，我们抓不到 → 一题会攒出好几个 session。
用 `--session-id <uuid>`：我们先生成、先写回头部，再让终端用这个。一题一 session 才守得住。

**只有 5599 转发过来，所以终端必须反代，连 WebSocket 一起。**
每开一题多转发一个端口不现实。ttyd 的 `-b <base>` 让它认自己挂在子路径下，
serve.py 除了普通 HTTP，还要处理 `Upgrade: websocket`（终端的输入输出全走 WS）——
握手转发对了才有字符流。

**先翻有没有现成的轮子，但"现成"不等于"该用"。**
myrlin-workbook 的发现路径跟我们落盘位置一字不差，一度以为直接接上就行。
但它是一整个应用；我们要的只是「板里嵌一个终端」。最后用了更小的 ttyd + 自己的反代。
翻轮子是对的，选轮子看的是"要的那一小块"有多大，不是"它能做多少"。

## Glossary
ttyd：把一个命令行程序变成网页里可用终端的小工具。`-i` 绑地址、`-b` 挂子路径、`-W` 允许输入。
反代（reverse proxy）：serve.py 把 `/_term/<port>/…` 的请求原样转给本地那个 ttyd，
    浏览器只跟 5599 打交道，不用知道 ttyd 在哪个端口。
WebSocket / Upgrade：一条一直开着、双向传字符的连接。终端的键入和输出都走它。
AGPL-3.0：myrlin 的许可证。当独立工具用无所谓，抄进自己的东西再分发才受约束。

## Discussion
> JL: 我在想能不能也加入这个呢？给一个 terminal 的图标？
> JL: 然后我想每一个 question page，他对应的 terminal 是他自己的。
> JL: 我不知道 myrlin 这个 package 能不能帮你 —— github.com/therealarthur/myrlin-workbook
>> CC0723: 翻了源码，发现路径跟我们一致。但它是一整个应用，太重；最后用 ttyd + serve.py 反代自己嵌了。

## Comments
- [ ] JL 「❓ Question 每个 Q 除了受限的抽屉，能不能再有一个自己的真终端 —— 就是完整的 Claude Code，功能一个不少？」 · 260723 2038
      We need to change this to English as well, must to make this can be well written and easier to follow, and also list several bullets.
- [ ] JL 「跟 QD2 是同一个需求的两种实现，但取舍完全相反：」 · 260723 1511
      我们已经改了，你看看QD2，现在跟QD3一样了。
- [x] JL 「when we open the terminal/chatbot, give some prompt so they know which question and board they're working on」 · 260723 1500
      >> CC0723: 做了。开场用 `--append-system-prompt`（抽屉那边拼进 system_prompt）灌一段定位：
      板 + 题号 + 题目 + 这题问什么 + 几条评论没解决 + 文件路径。不占回合、不自动跑。
      实测：全新终端/抽屉，不给背景直接问「我在哪一题」，都答得出 QB3 / QB2。
- [x] JL 「I want to make the chat or claude opened in the SPACE dir, not in the board」 · 260723 1430
      >> CC0723: 改了。`ttyd` 和抽屉里的 `claude` 现在都开在 SPACE 根（`cwd = 整个 repo`），
      实测终端里 `pwd` = SPACE 根、能看到全部 skills。代价：旧的板文件夹会话留在原地，
      各题在 root 下重新起 session（迁移 jsonl 试过，resume 不认 —— 见 Lesson）。QD1/QD2 一起更新了。
- [x] JL 「跟 QD2 是同一个需求的两种实现，但取舍完全相反：」 · 260723 1420
      我们已经改了，你看看QD2，现在跟QD3一样了。
      >> CC0723: 对，看了 QD2 —— 它现在也是三档权限、默认「完整·问我」＝ 跟 CLI 一样能干任何事，
      不再是「只受限」。改写了 Why here：两题差别不再是「安全 vs 不安全」，而是形态不同 ——
      QD2 是带可调闸门的 SDK 对话框，QD3 是没闸门的真 CLI 本体。
- [x] JL 「跟 QD2 是同一个需求的两种实现，但取舍完全相反：」 · 260723 1358
      我们已经改了，你看看QD2，现在跟QD3一样了。
      >> CC0723: 同上，Why here 已改。删掉「取舍完全相反 / QD2 受限」的旧说法，改成按形态区分。
- [x] JL 「安全边界写死成文」 · 260723 1355
      什么意思？
      >> CC0723: 「写死成文」= 把「谁能连、能碰什么、认证怎么做」白纸黑字定死、写下来，别含糊留脑子里。
      这条 Done-when 标题改成「安全边界要定成白纸黑字的规矩」，并加了一行解释这句话的意思。
      现在只剩「认证」这一条没定：ttyd 自己不认证，谁连到 5599 谁就能用，对外暴露前必须先加认证。
- [x] JL 「跟 QD2 是同一个需求的两种实现，但取舍完全相反： QD2 受限、安全、只能改一个文件；这一题不受限、能干任何事、也就没有护栏。」 · 260723 1354
      我们已经改了，你看看QD2，现在跟QD3一样了。
      >> CC0723: 同上。QD2 现在默认「完整·问我」也能改任何相关文件，不再是「只改一个文件」；
      Why here 已按新事实重写（形态之分，非受限之分）。
- [x] JL 「Wait, here each terminal is one port? for the QD3? will that be too hard to manage?」 · 260723 1640
      >> CC0723: 端口数量不是问题（一块板就几个并发终端），难的是生命周期。
      改成了 unix socket（无端口池）+ 全局 key（多板不撞）+ 启动清残留 + killall。实测都过。
- [x] JL 「suppose in the future we have several boards open at the same time, how do we handle that?」 · 260723 1640
      >> CC0723: 服务器层面早就是一个 serve.py 服务整个仓库（已验 3 板并存）。
      终端身份改成按 Q 文件绝对路径 hash，跨板全局唯一 —— 两块板各自的 QD3 天然分开。
- [x] JL 「127.0.0.1 refused to connect. I have this.」 · 260723 1550
      >> CC0723: 端口没转发（跟之前 3000 那次同一类）。改成全走已转发的 5599 反代，
      ttyd 用 -b 挂子路径，WebSocket 也一起转。实测 GET 200、WS 101。
- [x] JL 「in the questions, I cannot open two claude terminal version at the same time?」 · 260723 1600
      >> CC0723: 能，被 UI 挡了不是 LAW。不同题是不同 session，多开几个板页面标签即可。（↗ 弹出按钮后来按 JL 意见删了。）

## Log
260723 · 按新结构重写：Question 展开成「一段话 + 要点」，补 `## Boundary` 和 `## Files`；退役的 `## Why here` 并进 Question
260723 1810 · 结掉 4 条评论：QD2 已改成三档权限（默认完整），Why here 从「受限 vs 不受限」重写成
              「形态之分」（带闸门的 SDK 对话框 vs 无闸门的真 CLI）；「安全边界写死成文」改成白话并加解释
260723 1745 · JL 要「开场给个 prompt 让它知道在哪一题」。加 prime_context()：终端用 --append-system-prompt、
              抽屉拼进 system_prompt，灌板/题号/题目/未解决评论数/文件路径。实测终端和抽屉都能直接答出自己在哪一题
260723 1730 · JL 定：claude 开在 SPACE 根，不是板文件夹。改了 serve.py 两处 cwd（终端 + 抽屉）+
              系统提示改用相对 repo 根的路径；实测终端 pwd = SPACE 根、加载全部 skills。
              旧 6 个会话迁移失败（resume 不认跨 cwd 的 jsonl），清掉各题 session: 行、root 下重起；见 Lesson
260723 1650 · 删掉 ↗「弹到新标签」按钮（JL：不需要）—— 多题终端改成「多开板页面标签」，更干净，pagehide 也能收
260723 1645 · 端口→unix socket + 全局 key（多板不撞）+ 生命周期收口（启动清残留/killall/beacon）；实测全过
260723 1630 · 端到端验证 QD3 终端：经 5599 反代驱动 WebSocket，resume 到 a0c6698a，发指令当场收到回复 —— 确认真能用
260723 1610 · 终端做出来了：ttyd + serve.py 反代过 5599（含 WebSocket），抽屉 ⌨ 进 / ↗ 弹标签
260723 1600 · 一题一 session 补严：终端首次开用 --session-id 写回头部，不再冒出没记录的 session
260723 1550 · 修 refused to connect：全走 5599 反代，WS Upgrade 一并转发
260723 1315 · 当场验证路 ①：这个对话就是板文件夹里的真 Claude Code CLI（session a0c6698a-…）
260723 1445 · 从 QD1 拆出来单独立题（JL 定：chat / terminal / sdk 各一题）
260723 1440 · 翻了 myrlin-workbook 源码：发现路径跟我们一致 —— 但最后没用它，太重
260723 1355 · 确认题级 session 就是真的 Claude Code 会话，终端和抽屉是同一个会话的两个前端
