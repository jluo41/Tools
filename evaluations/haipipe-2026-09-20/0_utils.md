# 0_utils 技能族评估报告

## 摘要

评估日期：2026-09-20。基线提交：f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217。

覆盖初始清单中的 **10/10 个当前技能**，没有发现清单外的 0_utils/SKILL.md。meal-cam-logger 与 whoop-connect 仍在 0_utils；当前磁盘上没有 0_connect 目录。

整体判定：**部分符合，有数项会使新鲜上下文误路由、无法运行或误导用户的 P1 问题。** table-workflow 正文已清楚写出 Run 边界；但 table-task 仍把 Workflow 行定义为 Phase/Cycle，table-workflow 的 schema 样例仍保留已退役的 Plan/Create/Review 空间。Meal Cam 文档启动命令与同目录实现不符。Whoop 要求用户把 Client Secret 发到对话，却保证密钥“从未共享”，并在无配置步骤或证据时承诺每日自动同步。

Workflow/Run 总判定：**部分符合**。当前明文中仍有 Phase 概念：table-task、whoop-connect、meal-cam-logger、remote-error；其中一些实际是一个用户任务里的内部步骤，应改称 Step/操作，而不是机械地拆成多个 Run。table-workflow 已明确把每行设为独立闭合的 Run Spec，并把 click、Step、重试、工具调用留在 Run 内部。它的 YAML 也使用 run_specs 列表，Routes 表达顺序与分支。建议直接写明“Workflow 是 Run Specs 列表，Routes 描述列表项间的关系”，并保留 Run Spec 与实际 Run Instance 的区分。

## 1. 快照、范围与限制

本次只写本报告，没有修改技能、代码、配置或其他评估报告。没有执行这些操作技能，没有调用 Claude、Codex peer、Whoop、Anthropic、CMS 服务器或摄像头，也没有运行测试、门禁、生成器或笔记本。下文的行为判断属于**桌面走查**，不是用户现场测试。

开始评估时工作区已有其他变动：references/cite-guard、grant-writer-skills、paper-rag-skill、paperspine、reprorun、research-agent-skills、research-co-pilot、scipilot-figure-skill 显示为修改状态；evaluations/ 显示为未跟踪目录。它们不是本报告写入的改动。共享 Brief 与 inventory 已读取；根 README 明确标注为 2026-08-02 的历史盘点，未把其中的 8 个 util / 3 个 connect 数字当作当前事实。

Run 判定采用共享 haipipe-run 契约：一个 Run 有一个有界目标、可寻址身份、actor/action、闭合规则、耐久 receipt，并能独立闭合（haipipe-run/SKILL.md:21-25, 82-98）。因此，用户请求、脚本调用、模型/API 调用、反馈回合或代码 Step 本身不会自动成为 Run（同文件:113-118）。Brief 的“Workflow 是 Runs 列表”与 haipipe-run 的“Workflow Definition 是 Run Spec 图”可同时表达为：Workflow 的计划清单列出 Run Specs，Run Spec 上的 Route 指向其他清单项；执行后产生的实际 Run Instances 另列在运行时视图。

## 2. 清单核对与支撑材料

| 技能 | 当前清单 | 阅读的当前材料 | 范围限制 |
|---|---|---|---|
| call-peer | 有 | 全文；同目录 5 个脚本的入口、参数与身份相关代码 | 未完整审计所有 wrapper 实现；未调用 provider 或读取 peer transcript；没有 CHANGELOG.md |
| diagram-ascii | 有 | 全文、CHANGELOG.md、ref 下 8 个图库文件 | 未生成/渲染图，也未实际测量 emoji 字宽 |
| field-test | 有 | 全文、CHANGELOG.md；针对 auto-charter 的 haipipe-insight 相关段落 | 未派 subagent、未执行真实目标任务 |
| meal-cam-logger | 有 | 全文、CHANGELOG.md、meal_cam_loop.py、episode_tracker.py | 未读 bite_detector.py 与两个 test_*.py；未运行摄像头或 API |
| notebook-cell-python | 有 | 全文、CHANGELOG.md、当前 converter 脚本 | 当前树中没有文档声称的 code/scripts/clean_notebook.py；未创建或运行 notebook |
| remote-error | 有 | 全文、CHANGELOG.md、CMS/Stata profile、issue-file-template；交叉阅读 haipipe-run 边界 | 未访问 CMS 服务器、Stata、数据、同步工具或门禁 |
| response-format | 有 | 全文、CHANGELOG.md、插件 README；检查根目录和插件下 CLAUDE.md/AGENTS.md 是否存在 | 根目录没有 CLAUDE.md；没有声称实际验证自动加载行为 |
| table-task | 有 | 全文、CHANGELOG.md、task-table-schema.md、renderer 的 CLI、agents/openai.yaml；交叉读取当前 workflow-table | 未运行 renderer、--check 或门禁 |
| table-workflow | 有 | 全文、CHANGELOG.md、workflow-table-schema.md、run-catalog.md、skill-coverage.md、agents/openai.yaml；交叉读取 haipipe-run | 未创建或渲染真实 Workflow declaration |
| whoop-connect | 有 | 全文、CHANGELOG.md | 当前 workspace 没有 Health-Sync/whoop 目标程序；未访问 Whoop 网站、收集凭据或触发同步 |
| 额外发现 | 无新增 SKILL.md | 核对 0_utils 当前目录与插件 README | 插件 README 仍把 0_connect 列为独立家族，当前 skills 树没有该目录 |

两个表格技能的目录名和可调用 skill 名不同：table-task 的 frontmatter/UI 名称是 task-table；table-workflow 的是 workflow-table；agents/openai.yaml 与调用提示对应这些名称。按现有 UI 证据，这是目录路径与调用名的分工，不单独判为错误。相反，task-table 内部对 workflow-table 的 Phase/Cycle 定义确实已过时。

## 3. 总体评价与应保留的写法

值得保留的清晰做法：

- call-peer 先根据用户动词选择 READ_EXISTING_PEER 或 START_OR_RESUME_PEER；含糊请求默认只读，并禁止为澄清而启动 provider（call-peer/SKILL.md:40-51）。这是本组最好的意图路由示例。
- field-test 预先冻结期望、把设计与执行上下文分开、记录 friction 而不是事后猜测，并说明派出的 subagent 是不同 context、不是另一个 Run（field-test/SKILL.md:17-38, 41-67）。
- table-workflow 的独立闭合条件，以及 click/comment/feedback turn 应保留为 Gate 或 Step 的规定清楚直接（table-workflow/SKILL.md:79-87, 158-163）。它也正确区分计划 Run Spec、实际 Run Instance、Workspace 与只读展示面。
- response-format 把 answer-first、scan 与详细解释分层，并声明仅用于聊天、不控制交付文件（response-format/SKILL.md:28-63）。这能让用户先看到结论；其激活来源与其他技能的特例仍需协调，见 F8。

## 4. 优先问题

### F1 · P1：task-table 继续把旧 Phase/Cycle 模型教给用户

**证据。** table-task/SKILL.md:15-16 说“不适用于 Phase/Cycle design contract”；:36-38 说 workflow-table “one row per Phase/Cycle contract”；:118-124 再把 sibling ownership 写成“Phase/Cycle plan”和“workflow phase contract”；:304-306 重复“一行一个 Phase/Cycle contract”。相邻当前契约在 table-workflow/SKILL.md:79-87 中规定每行是独立闭合的 Run Spec，并明确排除 Phase、Step、Version、retry、actual Run Instance 等其他行粒度（:231-239）。haipipe-run/SKILL.md:193-205 也明确没有 Phase authority layer。

**问题与影响。** 这不是兼容字段：Phase/Cycle 出现在当前 description、模型说明、表格边界及相关契约中，并定义设计表的一行是什么。用户会收到互斥答案；Agent 可能按 Cycle 排表，或把单次可闭合 Run 错合并进循环。

**建议。** 把 live 定义统一成“Workflow 清单列出独立闭合的 Run Specs；Task Table 仍按 Task Folder 一行；Runs Overview 显示实际 Run Instances”。如果旧数据读取器还需 Phase/Cycle 字段，应明确标成 compatibility-only，不留在当前 skill description 或边界表。

### F2 · P1：table-workflow 正文与 schema 使用不同的 Design/Insight Workspace roster

**证据。** 当前正文给出的 workspace_roster 是 goal/Goal、design/Design、insight/Insight、runtime/Run、delivery/Delivery（table-workflow/SKILL.md:55-71）；Design 工作表也把 Insight 与 Design 分列，Insight 只读显示 Commission 使用的洞察（:134-142）。同一技能的完整 schema 样例仍定义 plan/Plan、create/Create、review/Review、runtime、delivery（ref/workflow-table-schema.md:154-165, 183-187），最终矩阵仍是 Plan/Create/Review/Run/Delivery（:235-240）。

**问题与影响。** Skill 说 Plan、Create、Review 已退役（table-workflow/SKILL.md:66-68），schema 却仍以这些名称示范 live declaration，且没有 Insight 列。依照 schema 建表的新作者会得到已退役空间、失去独立的 Insight 投影；Agent 不知道应服从正文还是“complete normalized grammar”。

**建议。** 同步 schema 中的 workspace id、label、Cell coordinates、Matrix 与范例，并保留稳定 ID runtime 的规则。正文当前已正确把 Insight 和 Design 作为独立空间/家族标识；不要为解决样例漂移而把 Insight 挪成 Design 的父家族。插件 README 仍列 0_utils 与 0_connect 为并列目录（plugins/haipipe-toolkit/README.md:114-130），但当前目录树没有 0_connect；由插件树索引 owner 一并更新。

### F3 · P1：Meal Cam 文档与当前执行脚本不对应，按文档启动会失败

**证据。** Meal-cam-logger/SKILL.md:29-38 描述三个阶段：每隔 5 秒抓帧并询问 Claude vision、按相邻检测标签去重、每个新食物都写进 Foods 列表；启动命令在 :55-64 还调用 Tools/plugins/health/.../meal_cam_loop.py 并传 --interval 5。当前同目录脚本的 CLI 只定义 --source、--fps、--cooldown-sec、--max-gap-sec、--output-dir、--model（scripts/meal_cam_loop.py:32-47）；没有 --interval。实际实现用 MediaPipe 检测咬合，在新 eating episode 首次才请求 vision，并记录 episode 时间段与 bite count（脚本 :1-18, 180-207；episode_tracker.py:41-65）。实际输出标题是 Episodes，不是旧文档示例的 Foods（脚本 :106-126）。当前 workspace 的脚本路径为 plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/scripts/meal_cam_loop.py。

**问题与影响。** 两套契约会在 parse_args 处冲突；即使修正路径，--interval 仍无法识别。Fresh agent 可能报告摄像头已启动，但实际进程不会启动；即使改了参数，也会向用户描述错误的检测频率、vision 调用次数和输出结构。

**建议。** 以当前实际脚本为准，统一脚本位置、--fps 含义、MediaPipe 本地帧检测、每个 episode 首次图片的 API 调用规则、Anthropic key 要求及文件结构。启动后先确认该 PID 对应进程存活，再回复“on”；用户指定的时间间隔应映射成可支持的 FPS，或者明确不支持。更新隐私说明，告诉用户哪些帧被送往 Anthropic、何时发送。

### F4 · P1：Meal Cam 的“跳过/停止/汇总”承诺不由后台进程支持

**证据。** Skill 说“skip that last one”可从“in-memory list”弹出并重写文件，随后又说需手动改 Markdown（SKILL.md:79-94）；loop 使用 EpisodeTracker 内存状态逐次重写文件（meal_cam_loop.py:191-207），tracker 没有删除 episode 的接口，只暴露 episodes 副本（episode_tracker.py:41-65）。Stop 时脚本只输出 stop log，不在 finally 中写最终 end/duration（meal_cam_loop.py:214-224）；但文档承诺读取最新文件并汇报当前 session 时长（SKILL.md:98-118）。脚本只在首个 bite 时创建 session file（:191-197），没有 bite 的新 session 不会生成文件。

**问题与影响。** Agent 无法从另一个 shell 修改后台进程里的 tracker；手工删除文件条目后下一次 rewrite 仍会恢复它。停止时记录的 End 是最近一次 bite 的时间，不一定是用户停止时间；如果本次没有 bite，按目录取“最新文件”可能读到旧 session。

**建议。** 为删除/更正提供进程可读控制通道或明确回复暂不支持；停止信号处理时写最终停止时间，并用本次 PID/session ID 绑定输出文件，禁止用“目录里最新一份”代替当前 session。三段流程按一场 meal session 处理更合理：一个 meal-session Run，Start、Monitor、Stop 是内部 Steps，而不是三个独立 Runs。

### F5 · P1：whoop-connect 把密钥传递说成私密，同时声称未配置的定时同步已生效

**证据。** whoop-connect/SKILL.md:70-76 要求用户把 Client ID 和 Client Secret 粘贴进 Discord，随后却保证 “These stay on your machine only and are never shared.” :84-99 又把密钥写入 .env 并以内联环境变量启动 listener。:119-130 在发现 tokens.json 后保证“每早 7 点自动同步”，但从建 app、认证、检查 tokens 到 sync whoop 的步骤（:40-145）没有创建或验证 scheduler 的命令、Job ID 或 receipt。

**问题与影响。** 用户会在错误的保密陈述下把 Client Secret 发进聊天，随后 secret 还被插入 shell command 文本。这个交互无法支持“仅在本机”的承诺。Agent 在未安装 scheduler 或未核验其状态时也可能对健康数据同步作出错误承诺。

**建议。** 不要要求用户把 Client Secret 发到对话；设计本地输入/secret-store 流程，消息中只返回是否配置成功。把“连接成功”与“定时任务成功”分成有独立证据的结果；没有 scheduler/job/receipt 就只能说“已授权，可手动同步”，不可说“每天自动同步”。三层用户流程目前叫 Phase 1–3（:27, 40, 80, 119），但它们没有各自 Run receipt/独立闭合。建议先定义一个有连接目标和 receipt 的 Whoop-connection Run，并把网页操作、OAuth、人类点击和验证作为其 Steps/Gates；只有确实有独立结果与闭合规则的子目标才拆成多 Run。

### F6 · P1：数个可执行说明指向当前树中不存在的位置

**证据与例子。**

| 文件 | 文档路径 | 当前树里的位置/缺失项 |
|---|---|---|
| call-peer/SKILL.md:197-204 | Tools/plugins/haipipe-toolkit/skills/0_utils/scripts/run_paired_cli.py | 实际脚本在 plugins/haipipe-toolkit/skills/0_utils/call-peer/scripts/run_paired_cli.py；命令还把 cwd 固定为 Physician-SPACE |
| table-task/SKILL.md:239-249 | $(git root)/Tools/plugins/.../0_utils/task-table/ref/render_task_table.py | Tools/ 不存在；文件在 plugins/haipipe-toolkit/skills/0_utils/table-task/ref/render_task_table.py |
| notebook-cell-python/SKILL.md:41-62, 211, 238-240 | code/scripts/convert_to_notebooks.py 与 clean_notebook.py | 当前 converter 在技能自己的目录；没有 code/scripts/ 目录或 clean_notebook.py |
| notebook-cell-python/SKILL.md:117-120 | Tools/plugins/diagram-skill/skills/diagram-ascii | 当前技能实际位于 plugins/haipipe-toolkit/skills/0_utils/diagram-ascii |
| diagram-ascii/SKILL.md:255-274、ref/03-folder-tree.txt:31-39 | Tools/plugins/haipipe-toolkit/skills/... | 当前插件树使用 plugins/haipipe-toolkit/skills/... |

只读路径检查确认当前 workspace 没有这些 Tools/ 或 code/scripts/ 位置。Whoop 文档另把目标目录硬编码到 /Users/jluo41/Desktop/jluo41-repo/Health-Sync/whoop（whoop-connect/SKILL.md:84-115）；该外部应用不在本次 workspace，故不判断它在用户机器上的实际状态。

**影响。** 新鲜 Agent 按手册执行会得到“文件不存在”，而文档让它误认为那是 canonical path。Call-peer、task-table 和 notebook 都把错误路径放在主要命令，导致核心操作不可执行。

**建议。** 使用可解析的当前插件路径或技能目录变量；cwd 从已确认的目标项目得出，不能把示例用户目录固化成默认值。清理缺文件的 clean 命令，或随 skill 提供真实实现。同步树形图库和跨技能链接；找不到可执行文件时明确停止/询问，不要猜目录。

### F7 · P1：remote-error 的通用模式依赖 CMS 专属模板，且把内部 Steps 叫成 Phases

**证据。** remote-error 自称 engine-neutral，并为未知环境规定“run the phases on the generic laws”（SKILL.md:113-129）；但最终 Issue shape 固定引用 ref/issue-file-template.md（:241-245, 436-442）。模板路径被硬编码为 _WorkSpace/0-CMS-Store/Issue-From-CMS-Server/，并要求 CMS server、Stata 的状态语义（ref/issue-file-template.md:1-8, 63-72）。本体和专用 profile 还把 READ、REASON、FIX、LINES、LESSON 称为 five phases（SKILL.md:116-138, 171, 289-310, 431；profile-cms-stata.md:34, 52, 82, 104, 120）。

**问题与影响。** 无 profile 的未知环境虽可继续处理，却没有环境无关的模板；Agent 仍可能写出 CMS 专属路径/状态。五个分析动作各自在同一故障处置 round 内，没有独立 Ticket/Result/receipt；这不是五个 Runs。称它们为 Phase 既违反术语要求，也容易诱使作者把内部步骤当成 Run 单元。

**建议。** 用“步骤”表示五个内部动作；一个有界远程故障处置是否构成 Run，按 Ticket/Spec、独立闭合与耐久 receipt 判定。把通用 Issue schema 放入无关引擎的模板，或让 Profile 明确提供模板、状态和路径；未知 Profile 时让用户给 register/path，并只承诺通用报告形状。CMS profile 的逐步信息可留在专用 profile，但步骤标题应使用 Step。

### F8 · P2：聊天格式规范的激活机制缺失，特例没有明确优先级

**证据。** response-format/SKILL.md:21-23 声称 repo 的 CLAUDE.md 指向此处、使其 always-on；当前 checkout 没有根 CLAUDE.md。它要求答案在第一行，后续每个 section 为编号 scan points（:28-44, 58-67）。task-table/SKILL.md:202-206 则在用户说“Show me the table”时要求以 Structure Tree 与渲染表格开头并输出 “Nothing else”。remote-error/SKILL.md:289-304 声称遵循 response-format，也强制一套五段式回复形状。

**问题与影响。** 技能说格式始终开启，但引用的全局加载文件不在当前仓库。两个子技能又为特定请求定义专用回答形状，却没明确它们是否覆盖 answer-first/编号 scan 规则。Assistant 无法同时保证“第一行是一句答案”和“回复只能是表格”。

**建议。** 确认 response-format 的真实加载入口；未部署时把“always-on”改为“显式调用或被其他指令加载时生效”。为 table-only 回复和 remote-error 定义明确的 scoped exceptions，或让特例格式本身满足通用 scan 结构。保留文档内容不受 chat layout 管理的边界。

### F9 · P2（风格取舍，不是功能缺陷）：diagram-ascii 把 emoji 密度设为强制默认

**证据。** diagram-ascii/SKILL.md:18 要求 “as many as possible”，每个 box/header/row/status 使用 emoji，并把六种以上 emoji 当作目标；:440-445 把无 emoji 的 plain-text labels 定为 anti-pattern。另有具体例子让 Agent 保留纯文本路径（:245-250），并提醒路径后缀已明示文件/目录时省略类型 emoji（:203-209）。

**问题与影响。** 用户可以要求其他格式（:35-37），所以不是违反请求的固定行为；但默认图表里的“越多越好”可能挤压标签、增加屏幕阅读器负担，且与等宽表格 emoji 两格计算的规则一起增加排版负担。它把风格偏好写成验收项。

**建议。** 保留 emoji 作为可选图例/状态锚点，不把“6 种以上”或“每个标签都带 emoji”设成目标。优先保证文字标签完整与可访问，等宽对齐依照当前表格规则处理。保留 natural-by-default 的 reply 约束和 optional reply boxes，它们已正确撤销旧通用箱体格式。

## 5. Workflow / Run 逐项判定

这里的“部分”不代表要把所有 Phase/Stage/操作改写成 Run：如果动作共享一个目标、结果和闭合规则，就留在同一个 Run 内。人类确认、计算中的一小步、工具调用、反馈回合、Step、Stage 或 retry 都不能单独因为名称而成为 Run。

| 技能 | 判定 | 证据与边界 |
|---|---|---|
| call-peer | 部分符合 | 不定义 Workflow；“read-only phase”（SKILL.md:48）只是两种用户操作顺序，不是 Run。应改为“complete the read-only operation first”，不要把读 transcript 自动变成独立 Run。 |
| diagram-ascii | 不适用 | 是绘图技能，不拥有 Workflow contract。Stage/Load/Clean/Train/Eval/Deploy 是阶段格（SKILL.md:314-332；ref/05-progress-tracker.txt:4-28）；多次实验的 Run 可作行（同文件:31-41）。这是“阶段不是 Run”的好例子；建议明确仅当每格有独立目标/闭合时才画作 Run。 |
| field-test | 不适用 | 这是技能行为验证方法，不是 Workflow 建模器。它把 commission 条目称 ordered steps、一行一个 commission step，并把外层 real field execution 记为 run（SKILL.md:41-77, 90-125）。没有 Phase 术语，也没有把 desk、judge 或消息轮次列作 Runs。 |
| meal-cam-logger | 不符合 | 当前正文显式定义 Three phases/Phase 1–3（SKILL.md:29-38, 42, 77, 98）；一场录制 session 更适合作为一个有 session file receipt 的 Run，Start/Monitor/Stop 是内部 Steps。 |
| notebook-cell-python | 部分符合 | 以 runs/run-N.sh 管理每个脚本输出，执行实例边界合理（SKILL.md:181-215, 224-231）。仅把 cell progress markers 称为“between phases”（:98）；应叫 sections/Steps，而不是 Run。artifact creation/conversion 是否形成多个 Runs，应按独立闭合判断。 |
| remote-error | 部分符合 | 5 个 Phase 是一次故障处置内的 READ/REASON/FIX/LINES/LESSON 步骤，不是五个独立 Run（SKILL.md:132-160）。需要 Step 名称，并明确 session label 是 chat/context 名，不等于 Run ID 或 receipt。 |
| response-format | 不适用 | 聊天排版规则不定义业务 Workflow；section/scan point 不是 Run。 |
| table-task | 不符合 | 将 Workflow 计划行多次定义为 Phase/Cycle；与本 Brief 和 table-workflow 当前 Run Spec 行粒度冲突（SKILL.md:15-18, 36-40, 117-124, 304-306）。 |
| table-workflow | 部分符合 | Run 边界严格，排除 Phases、Steps、Versions、retries、calls 和 views（SKILL.md:79-87, 231-239；schema:120-138）；规范称 Workflow 为 directed graph，虽 schema 使用 run_specs 列表且每行有 Run-owned Routes。建议增加“list of Run Specs, with Routes linking the entries”一句以直接满足简洁的 list model，Run Instances 继续单列。 |
| whoop-connect | 不符合 | Overview 与标题把 app setup/auth/confirmation 称为 3 phases（SKILL.md:27-31, 40, 80, 119），没有定义独立 Run 身份、close gate 或 receipt。建议将有独立结果的连接目标建为一个 Run，网页操作、OAuth consent、token check 为 Steps/Gates；只有真的创建并验证 scheduler，才另列定时同步 Run。 |

有意保留为历史材料的词语包括各技能 CHANGELOG.md 中的旧名称、旧格式、历史原话及已退役术语。它们不是当前操作说明，不建议全局替换。table-workflow 对 Phases 的否定式检查也不违规。Notebook 的“phases”是代码内进度的泛称，应改成 section/Step；diagram 的 Stage/Grid 是图的轴，也不需要改叫 Run。用户规则要求描述 Workflow 单元时用 Run；它不要求把每个顺序动作都升格为 Run。

## 6. 代表性桌面走查

以下仅根据当前说明与只读代码逐步推演，不是实测。

1. **“Show me the task status tree.”** task-table 提供 tree-only 输出、按 Task 深度截止，并强调表来自磁盘而非手工填写（table-task/SKILL.md:28-34, 151-156, 236-255）。这个路径对人清楚；但要把 plan workflow 输出成表格时，skill 又称其为 Phase/Cycle contract，和 workflow-table 当前 Run Spec 模型冲突。
2. **“Start meal cam; use defaults.”** 技能会选 webcam 与 5s 并执行 --interval 5 命令。当前脚本不在该 Tools/plugins/health 路径，也没有 interval 参数；因此不能确认“on”。正确交互应该说明失败原因，不能先说相机已开启。
3. **“Connect my Whoop.”** 用户被要求把 secret 发到 Discord，又被告知 secret 没有共享。OAuth 完成后，只查 tokens.json 就回复每日 7am 同步已启用。文档既没准确描述 secret 传输，也没有 scheduler 创建与检查步骤。
4. **“Read the peer’s progress, then ask it to continue.”** Intent router 次序正确：先只读现有 transcript，完成后才执行明确授权的 provider call（call-peer/SKILL.md:46-49）。但当前命令会找不到 Tools/.../scripts/run_paired_cli.py；新鲜 Agent 应指出路径无法解析，不能切换 pair 或创建重复 peer。
5. **“Make this Python script viewable in a notebook.”** source-of-truth、脚本运行、可选 notebook execution 的区分容易理解（notebook-cell-python/SKILL.md:64-71, 125-153, 181-215），但主命令指向不存在的 code/scripts/ converter，clean step 也缺失。Agent 无法按“canonical sequence”完成转换或清理。
6. **“Here is a server error; explain and fix it.”** 远端限制、静态 gate 不代表服务器实测、不得宣称 fix works 等证据纪律值得保留（remote-error/SKILL.md:24-33, 166-185）。未知环境仍会套用 CMS issue 模板，并输出 Phase 风格 chat 结构；文本没有说明应采用通用 register schema 还是 CMS 专属形式。
7. **“Show four experiment runs across Load, Train and Eval.”** progress tracker 的 multi-probe grid 用每行一个 Run、Load/Train/Eval 作列（diagram-ascii/ref/05-progress-tracker.txt:31-41），恰好保留 Run 与内部阶段轴的区别。建议模板文字明确这些是 Run 内的 Steps/checkpoints。

## 7. 关键段落前后改写建议

下列英文替换文本与英文源文同语种，不直接修改文件。

### task-table 的行粒度

Before: “Not for a Phase/Cycle design contract”; “one row per Phase/Cycle contract.”

After:
~~~text
Not for a Workflow Run-Spec list; that is /workflow-table.
A Workflow lists planned Run Specs. Routes connect those Runs; the runtime view lists actual Run Instances.
A Task Table remains one row per Task Folder and projects ticket/receipt-backed Runs beneath it.
~~~

### table-workflow 的设计 Workspace roster

Before: schema 示例使用 plan/Create、create、review、runtime、delivery；正文称 Plan、Create、Review 已退役，并定义 Goal、Design、Insight、Run、Delivery。

After:
~~~yaml
workspaces:
  - {id: goal, label: Goal, purpose: commission scope}
  - {id: design, label: Design, purpose: author and adopt candidates}
  - {id: insight, label: Insight, purpose: read the signed Design Handoff}
  - {id: runtime, label: Run, purpose: read-only Run presentation}
  - {id: delivery, label: Delivery, purpose: preview adopted work}
~~~

schema 的 Cells 与矩阵需同步引用这些稳定 id，而不只是改表头。

### Meal Cam 的 Run 边界与流程文案

Before: “Three phases: Start, Monitor, Stop.”

After:
~~~text
Workflow: Meal capture.

One meal session is one Run, closed when the user stops capture and its session receipt is finalized. Start, Monitor, and Stop are Steps inside that Run; the camera loop and vision requests do not create additional Runs.
~~~

这个 Run 定义与当前同目录脚本的单 session 文件/一份 tracker 状态相符；还需先让 CLI、日志、stop finalization 和人类纠错能力与实现对齐。

### remote-error 的五个 Phase

Before: “The five phases are the same everywhere. The commands are not.”

After:
~~~text
This procedure has five Steps: READ, REASON, FIX, LINES, and LESSON. They belong to one remote-error round and do not create five Runs. The selected Profile supplies environment-specific commands and, when needed, the report schema.
~~~

同样把“phase 5”改成“Step 5”，而不是创建第五个 Run。

### Whoop 的凭据提示和成功声明

Before: “Please copy and paste both here”; “These stay on your machine only and are never shared.”

After:
~~~text
Enter the Client ID and Client Secret in the local credential prompt. Do not paste the Client Secret into this chat. Tell me when local setup confirms both values are stored.
~~~

运行后的成功答复应按证据区分：
~~~text
WHOOP authorization is connected. I have not confirmed a daily sync schedule.
~~~

只有创建并观察到 scheduler/job 的有效状态或 receipt 后，才把第二句改成“Daily sync is scheduled.”

## 8. 跨家族事项

- **Insight owner / coordinator：** 当前 haipipe-insight 仍列出“application | board — resolve an Application root”（skills/insight/haipipe-insight/SKILL.md:240-245），并把 Insight 与 Design 的四项权责称为 “Application's four domain authority transfers”（:266-271）；又把 application-wf 列作跨 board receipt/handoff 责任方（:336-350）。这与全局要求“Insight 和 Design 是独立 first-class 家族，不由 Application 作父家族”直接冲突。交给 Insight/共享 taxonomy owner 清理当前操作说明；本 scope 不改它。
- **table-workflow owner：** 当前正文正确把 Insight、Design 各自作为独立 Workspace/家族标识，表中 Insight 输入只读；schema 样例未同步是本报告 F2。同步 schema 与工作样例，不要把该只读交互误读为 Application 父子关系。
- **插件家族索引 owner：** plugins/haipipe-toolkit/README.md:129 仍列 0_utils/ 0_connect/ 并称 utilities/connectors，当前目录不存在 skills/0_connect，而 whoop-connect 在 0_utils。应更新目录导览；根 README 的旧计数明确标注 2026-08-02，保留为历史盘点，不当作当前目录定义。
- **共享格式 owner：** response-format、table-task、remote-error 各自描述聊天层输出；明确 table-only/remote-error 专用形状是否为 response-format 的 scoped exception，避免技能之间争夺回复首行与章节形状。

## 9. 推荐修正顺序

1. 先修表格家族语义：table-task 去掉当前 Phase/Cycle 行定义；Workflow 改为 Run Specs 列表并保留 actual Run Instance 视图；同步 table-workflow schema/样例为 Goal、Design、Insight、Run、Delivery。
2. 先停止两个连接流程中的用户误导：Meal Cam 把参数、真实实现、Session Run 的关闭/纠错与最终 receipt 对齐；Whoop 不收聊天 secret，不声称没有配置证据的自动同步。
3. 修复所有不存在的命令路径与缺失工具：call-peer、table-task、notebook-cell-python、diagram-ascii；缺文件或参数不支持时要求 skill 如实报告。
4. 精准改名 live Phase 用法：Workflow 单位叫 Run/Run Spec；同一 Run 内部的处置步骤、摄像头控制和代码 section 则叫 Step、操作或 section。不要改历史 CHANGELOG。
5. 统一 reply-output 特例，校准 response-format 的加载说明；补全 remote-error 的 engine-neutral 模板边界和图表 emoji 的可选性。
6. 将 Insight 的 Application 父级词汇与 0_connect 家族索引分别交给各自 owner 整理，并与共享 coordinator 对齐。

## 最终判断

覆盖完整：**10/10 个当前 utility skills**，没有当前技能文件漏读。用户桌面走查未执行；没有运行测试或服务。最高影响是旧 Phase/Cycle workflow 定义、workflow schema 的已退役 Workspace 样例、Meal Cam 的文档/CLI 不匹配，以及 Whoop 的密钥/定时同步误导。

Workflow/Run **部分符合**：table-workflow 的 Run Spec / Run Instance / Step 边界清晰，Progress Tracker 有 Run 行与阶段列的良好示例；但 task-table 仍把设计行定义成 Phase/Cycle，Meal Cam/Whoop 把用户流程称作 3 个 Phase，remote-error 把一次处置内的 5 个 Steps 称 Phase。修订时把 Workflow 写成 Run 列表，用 Runs 表达可独立闭合单元；内部动作仍留作 Steps/操作，不要逐项升格为 Run。
