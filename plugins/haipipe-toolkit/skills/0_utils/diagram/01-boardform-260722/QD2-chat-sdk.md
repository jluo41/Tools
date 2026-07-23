# SDK version: the chat box
state: 🟡 PARTIAL
owner: CC
method: claude_agent_sdk + serve.py 的 /_board/chat，权限三档可选（受限 / 完整 / 全放行）
session: ccda0c28-ef7e-47e0-a7e1-c13abc4f4cea
## Question
在网页里直接开一个对话：它读这一题的内容和未解决评论，改这一题的 md。
权限该多开？—— JL 定：给三档，从「只改这一题」到「跟 CLI 一样全工具全技能」，默认停在「完整·问我」。

## Diagram
```
  浏览器右侧抽屉                     serve.py（在文件所在这台机器上）
  ┌──────────────────┐   POST      ┌────────────────────────────────┐
  │ QD2  标题        │ /_board/chat│ claude_agent_sdk               │
  │ ┌ 气泡 ────────┐ │ ──────────► │  cwd = SPACE 根（整个 repo）    │
  │ │ 逐字流出来   │ │             │  能读它讨论的代码，不只板文件夹 │
  │ └──────────────┘ │ ◄────────── │  can_use_tool ─ 闸门（三档权限）│
  │ 🔧 处理 N 条评论 │  一行一条    │    受限：只改这一题的文件       │
  │ Opus4.8 / high   │  JSON        │    完整·问我：动别的弹权限（CLI）│
  │ [输入] [⏹]      │              │    完整·不问：bypass 全自动     │
  └──────────────────┘             └───────────┬────────────────────┘
                                               │ 改完顺手 build.py
                                               ▼  刷新页面就看到渲染结果
```

## Done when
- [x] 能起会话、读板文件、正确作答
      `claude-agent-sdk 0.2.126`，实测通过。
- [x] auth 不用另外做
      SDK 调机器上的 `claude` CLI，直接继承已登录的 OAuth（`~/.claude/.credentials.json`）。
      跟 `haichat-inlab` 一样 —— 翻过它的源码，对 OAuth 零特殊处理。
- [x] 成本压到能接受
      默认 $0.92 → 收窄后 **$0.24**，续聊一句 **$0.012**。
- [x] 会话能接上，而且看得见
      `session:` 写在 Q 文件头部，跟 `state:` / `owner:` 并列。
- [x] 页面上有入口
      每张卡片一个 `💬 Chat`，右侧整条抽屉（照 haichat-inlab 的 drawer）。
- [x] 逐字流式
      `include_partial_messages` → `content_block_delta`，NDJSON 边发边收。实测 8.1 秒见第一段字。
- [x] 能选模型和 effort
      Opus 4.8 / Sonnet 5 / Haiku 4.5 × low→max，默认 **opus + high**。
- [x] 跑一半能停
      ⏹ → `/_board/stop` 立旗子（下一条消息处收工）+ 浏览器 `AbortController`。
- [x] 按评论办事
      开抽屉先同步没写盘的评论，然后一个按钮「🔧 处理 N 条未解决评论」发现成的 prompt。
- [x] 硬闸门被真正触发过了
      逼它真的对 `board.md` 发一次 `Edit`，被工具层拦下：
      `denied: ['Edit -> …/board.md']`，`board.md` 一个字没变。
      拦截比对的是**解析后的绝对路径**，不是文件名字符串。
- [x] 回复里的 markdown 能渲染
      抽屉里自带一个小渲染器（标题 / 列表 / 代码块 / 行内代码 / 粗斜体），
      先转义再渲染，不引第三方库。流式过程中也是渲染态。
- [x] 权限做成三档，默认「完整·问我」（JL 260723）
      抽屉底部一个下拉：受限这一题 / 完整·问我 / 完整·不问。
      完整档 setting_sources=["user","project","local"] → **Skill 工具可用，实测看得到约 150 个技能**。
      「完整·问我」逐个弹权限（＝ CLI 默认行为），「完整·不问」= bypassPermissions 零提示。
- [x] 受限档真的关得住
      can_use_tool 在 default 模式下对 Bash 不一定被调用（实测 Bash 直接放行了），
      所以受限档改用 `disallowed_tools` 硬关 Bash/Task/Skill/Web —— SDK 层黑名单，不过回调。
      实测：受限档里逼它跑 Bash，报「Bash exists but is not enabled in this context」。
- [x] 系统语言默认英文
      CHAT_RULES / FULL_RULES 都写「Answer in English by default」；抽屉 UI 全英文。
- [ ] 长任务怎么办
      现在一个 HTTP 请求从头等到尾。跑十分钟的任务会顶到超时。
      （注：这一条跟之前那个「写操作挂住」**不是**同一个根 —— 那个已经查清并修好，见 Lesson。）

## Now
能用了。你在页面上点 `💬 Chat` 就是它。

- 三档权限，抽屉底部下拉选（JL 260723 定，默认「完整·问我」）
      · 受限这一题 —— setting_sources=[]，只读 + 改这一题的文件，Bash/Task/Skill/Web 硬关，便宜（$0.24，无技能）
      · 完整·问我 —— 全工具 + 全技能，动别的东西弹给你点允许 / 总是允许 / 拒绝（＝ CLI 默认）
      · 完整·不问 —— permission_mode=bypassPermissions，零提示全自动（= --dangerously-skip-permissions）
      切到「完整」会加载技能注册表，一条消息回到 ~$0.9；受限档没这笔。
- 能调技能了
      完整档 setting_sources=["user","project","local"] → Skill 工具出现，实测它数出约 150 个技能，
      能点名 diagram-ascii、haipipe-paper 之类。这正是「跟 CLI 一样开放」要的。
- 三档的权限机制各不相同
      受限：`disallowed_tools` 硬关危险工具（can_use_tool 对 Bash 不一定被调，靠黑名单最稳）。
      完整·问我：permission_mode=default + can_use_tool，逐个弹（写 allowed_tools 或换 mode 都会绕过回调 —— inlab 的坑）。
      完整·不问：permission_mode=bypassPermissions，干脆不给回调。
- 一开就知道自己在哪一题（JL 260723）
      system_prompt 里拼进一段定位（`prime_context`）：板 + 题号 + 题目 + 这题问什么 +
      几条评论没解决 + 文件路径。所以你一开抽屉、第一句话它就已经知道背景，不用你交代。
      实测：受限档不给背景直接问「你挂在哪一题」，它答出 QB2 · Fresh-agent acceptance test。
- 会话开在 SPACE 根，不是板文件夹（JL 260723）
      `ClaudeAgentOptions(cwd=...)` 改成整个 repo。跟 QD3 终端一致 —— 会话要能读它讨论的代码，
      只给板文件夹太窄。系统提示给的是「相对 repo 根的路径」而不是光文件名。
      受限档仍然只能改这一题的文件（can_use_tool 比对绝对路径）；完整档才放开。
      跟 QD3 同一条 Lesson：改 cwd 会把旧会话留在原板文件夹，各题在 root 下重起。
- Python 用仓库自己的 venv
      SDK 要 3.10+，系统 `python3` 是 3.9.6。仓库 `.venv` 是 3.13.14，够用；
      它没有 pip 是因为 **uv 管的**：`uv pip install --python .venv/bin/python claude-agent-sdk`。
- 三步用法（JL 定的）
      ① 开抽屉先同步没写盘的评论 → ② 点「🔧 处理 N 条未解决评论」→ ③「↻ 刷新页面看结果」。
      服务器改完 md 会顺手重新生成 html，所以刷新就够。

## Why here
QD1 问的是「分几级、边界在哪」，这一题只管**这一种实现**：网页里的受限抽屉。
把它单拎出来，是因为它跟 QD3（终端版）的取舍完全不同 —— 一个受限一个不受限，
该同时存在，不该在同一题里互相干扰。

## Lesson
**`query()` 会在 prompt 生成器吐完之后关掉输入流，`can_use_tool` 就没地方回话了。**
症状很怪：读得了、写就挂，报 `Tool permission request failed: AbortError: Stream closed`。
原因是权限回调的「放不放行」是通过 stdin 那条控制通道回给 CLI 的。
`query(prompt=<一次性 async generator>)` 在那条消息发完之后就把输入流关了 ——
读操作往往赶在关闭之前问完，所以能过；写操作问得晚，通道已经没了，CLI 等到超时就报错。
换成 `ClaudeSDKClient`（整轮把连接开着）之后立刻正常。
**`haichat-inlab` 用的一直是 `ClaudeSDKClient` 而不是 `query()`** —— 抄的时候把这一条漏了。
教训：抄别人代码时，连**为什么用这个 API 而不是那个**一起抄。


**一个端口只能有一个服务器。**
排查「页面没反应 / chat 没 response」，最后是两件事叠在一起：
① 反向 DNS —— `SimpleHTTPRequestHandler.address_string()` 默认对客户端 IP 做 `getfqdn()`，
   这台机器上每个请求卡 7.8 秒。覆盖掉，直接返回 IP。
② 同时跑着两个 `serve.py` 抢 5599，连接随机落到其中一个。
   现在 `--daemon` 双 fork 脱离终端，启动前先确认端口干净。
修完之后 150KB 的页面 0.001 秒返回。

## Glossary
can_use_tool：SDK 的工具闸门回调。每次模型要用工具都先问它一句放不放行。
effort：模型在一个回答上肯花多少心思，low→max 五档。

## Discussion
> JL: 我倾向用 claude_agent_sdk，可以加。auth 用 OAuth 就行。
> JL: 为什么不用最好的 model？用 claude 4.8 opus，或者我们可以选择 model 和 effort 之类的。
>> CC0723: 加了两个下拉，默认 opus 4.8 + high。
> JL: 这个 chat 我怎么 stop 呢？有什么比较丝滑的方法？
>> CC0723: 发送键跑起来变 ⏹，点它服务器那边立旗子、浏览器这边 abort。

## Comments
- [x] JL 「open the terminal/chatbot with a prompt so they know which question and board」 · 260723 1500
      >> CC0723: 抽屉的 system_prompt 里拼进 `prime_context`（板/题号/题目/未解决评论/文件）。
      实测不给背景直接问，答得出 QB2。终端那边用 --append-system-prompt 同一套，见 QD3。
- [x] JL 「I want to make the chat opened in the SPACE dir, not in the board (same to QD1/QD2)」 · 260723 1430
      >> CC0723: 抽屉的 `cwd` 从板文件夹改成 SPACE 根，跟 QD3 一致 —— 会话现在能读整个 repo 的代码。
      受限档仍只改这一题的文件；完整档放开。旧会话留在原板文件夹，各题在 root 下重起（见 QD3 Lesson）。
- [x] JL 「maybe we have the robot icon for the chatbox?」 · 260723 1345
      >> CC0723: 换了 🤖。顺带解决一个混乱：右下角原来两个都是 💬（🤖 前是 💬 Chat，
      上面还有 💬 Comment），挤一起分不清。现在 🤖=跟 AI 对话，💬=人写评论，一眼分开。
- [x] JL 「could you put it in the right bottom conner?」 · 260723 1330
      >> CC0723: 一开始理解反了，把整个抽屉挪到了角落。JL 澄清：抽屉保持 haichat-inlab 那样的
      整条右侧，要放到右下角的是**「💬 Chat」这个打开聊天框的图标**（原来埋在每张卡片头部那一行）。
      已改：抽屉恢复整条右侧；加了一个右下角悬浮的 💬 Chat，聚焦看某一题时出现，点它开这一题的抽屉。
- [x] JL 「只能改这一题的 md。要怎么做，代价多少？」 · 260723 1305
      应该不止改md，其他很相关的file也可以改。
      尽量跟claude code cli 一致吧。
      >> CC0723: 做了。权限做成三档，默认「完整·问我」＝ 跟 CLI 一样：全工具 + 全技能，
      能改任何相关文件，动别的东西弹给你点允许（不再锁死一个文件）。「受限」档留着当便宜选项，
      「完整·不问」= bypassPermissions 全自动。实测完整档能调技能（看得到约 150 个）。
- [x] JL 「能起会话、读板文件、正确作答」 · 260723 1240
      但有个问题就是这个output 是streaming out的吗？我感觉不是诶。

## Log
260723 1745 · 开场定位：system_prompt 拼进 prime_context（板/题/问什么/评论/文件），一开抽屉就知道背景；实测答得出 QB2
260723 1730 · JL 定：抽屉的 claude 也开在 SPACE 根（cwd = 整个 repo），跟 QD3 一致 ——
              会话能读它讨论的代码；系统提示改用相对 repo 根的路径。受限档仍只改这一题的文件
260723 1720 · JL 说「关掉它们」：把所有 serve.py / ttyd / 终端 socket 全部收干净，5599 及各终端端口无监听。
              板文件和代码都在，随时能重起。⚠️ 排查时发现别的 session/agent 也在同时改 serve.py（scope 被改宽成整个 repo）和 QA2/QA5 —— 重起服务器前先确认只有一个 session 在管，别再抢实例。
260723 1710 · 加「折叠思考块」（JL 要的）：服务器把 thinking_delta 发成 `{"t":"think"}`，抽屉渲染成
              可折叠的 💭 Thinking（边想边展开，答案一到收起，点标题再展开）。client 已做并推送。
              两条已知未闭环：① 要看思考得有个跑当前代码的服务器（现已按 JL 要求关闭）；
              ② resume 已有 session 的题不流思考（QD2/QA4/QA6/QD3），只有全新 session 才有 ——
              是 Claude Code resume 的行为，不是 bug。隔离 probe 证明代码路径对（EXACT server 配置 → thinking_delta=3）。
260723 1640 · 修两个 bug（JL 报的）：① 每条回复都误报「改动已写盘」+ Reload —— 服务器新增 `wrote` 标记，
              只有真跑过 Edit/Write 才说写盘、才重新生成 html；只读消息不再触发。
              ② 空回复回退文案和几处提示还是中文，全部改英文（"(no text reply…)" 等）
260723 1620 · 系统语言默认英文（CHAT_RULES/FULL_RULES + 抽屉 UI 全部英文）；结掉 1305 那条评论
260723 1615 · 受限档改用 disallowed_tools 硬关 Bash/Task/Skill/Web —— can_use_tool 对 Bash 不一定被调；实测拦住了
260723 1610 · 权限做成三档（受限/完整·问我/完整·不问），默认完整·问我；完整档加载技能，实测看得到约 150 个
260723 1345 · 打开聊天框的图标 💬 → 🤖，跟评论 dock 的 💬 区分开（跟 AI 对话 vs 人写评论）
260723 1340 · 纠正：抽屉保持整条右侧（haichat-inlab）；把「💬 Chat」打开图标做成右下角悬浮，
              聚焦看某一题时出现 —— JL 要的是开的图标在角落，不是整个抽屉搬过去
260723 1330 · （一度误改成右下角浮动框，已回退）
260723 1535 · 抽屉里加 markdown 渲染（自带小渲染器，先转义再渲染，流式过程中也渲染）
260723 1530 · 闸门首次被真正触发：逼它 Edit board.md，工具层拦下，board.md 未变
260723 1525 · 修好写操作挂住：query() 会关掉输入流 → 换成 ClaudeSDKClient
260723 1520 · 抽屉改叫对话框
260723 1420 · 逐字流式打通，实测 8.1 秒见字
260723 1415 · 模型/effort 选择，默认 claude-opus-4-8 + effort=high
260723 1410 · 停止键：⏹ → /_board/stop + AbortController
260723 1405 · 抽屉改成右侧整条（照 haichat-inlab 的 drawer）
260723 1400 · 修两个把服务打瘫的问题：反向 DNS 卡 7.8 秒；两个实例抢同一端口
260723 1335 · 三步用法：先同步 → 一键处理评论 → 刷新
260723 1310 · 对话窗做好：每张卡片一个 💬 Chat，按题存历史
260723 1305 · 照 haichat-inlab 改成 can_use_tool 硬闸门
260723 1250 · /_board/chat 打通；成本 $0.92 → $0.24
260723 1445 · 从 QD1 拆出来单独立题（JL 定：chat / terminal / sdk 各一题）
