# 0_utils：当前问题、证据与修复计划

## 后续实施状态（2026-09-20）

已完成本计划中可在当前工作区落实的本地修订，并按下表更新 R1–R12。原评估、问题证据和建议验收条件保留作审计记录；本节是当前待办状态的准据。逐技能改动、验证范围和限制见[实施状态报告](0_utils-fix-status.md)，验证收据副本见[验证材料索引](0_utils-validation/README.md)。

| 编号 | 当前状态 | 已完成的修订与验证 | 尚待外部条件的部分 |
|---|---|---|---|
| R1 | 本地修订并检查 | call-peer 不再导入时搜索 Physician-SPACE；帮助、无 pair 与 SDK 前置检查在本机通过 | Provider 调用及配置 SDK 的成功流程未执行 |
| R2 | 本地修订并复核 | 移除退役 Adopt，修正路线、Cell/coverage；计数现为 `C + N + J`，涵盖 held Commission，最多一个 release；fresh-context owner 一致性复核通过 | 未调度真实 Design 工作 |
| R3 | 修订并检查 | Converter 将入口及部分批次失败传播为非零退出；本地缺失输入和混合批次场景通过 | — |
| R4 | 修订并检查 | 新增隔离执行目录、保留重复尝试、execution receipt、日志和中断状态；成功、失败、同秒重复及 SIGTERM 场景通过 | 无 nbconvert/浏览器的渲染验证；helper 只记录 Step，不创建 owner Run |
| R5 | 修订并验证 | Pause 后 Stop 使用 TERM+CONT；27/27 隔离控制检查通过，含多 session | 真实摄像头/检测/API 与其他操作系统未测 |
| R6 | 本地修订并检查 | call-peer、notebook、meal-cam 与 task-table 将 skill 工具位置和目标项目分开；含空格目标路径已验证 | 其他操作系统和其他安装布局未测 |
| R7 | 修订并检查 | 通用 remote-error 与 CMS profile 分开；generic 情景、报告模板和回复边界已检查 | 未在真实 CMS 项目或远程服务运行 |
| R8 | 修订并检查 | field-test 改指当前 standing-authorization 契约，并说明范围及 owner gate | 无真实 FIELD target/grant，未执行 FIELD |
| R9 | 本地前置检查修订 | Whoop skill 先检查 checkout、脚本、解释器、credential loader 和 callback；缺少配置 checkout 时能在 setup 前识别 | 配置 checkout 不存在；OAuth、token refresh、sync、scheduler 未验证 |
| R10 | 修订并检查 | 区分共享 pair 名和 callee 原生 display name，保留 session ID/cwd 为身份依据 | Provider session 创建/恢复未执行 |
| R11 | 修订并检查 | response-format 仅约束聊天；文件跟随自身模板，示例顺序已对齐 | 已检查示例文本，未做 viewport 渲染 |
| R12 | 按可用范围完成 | 四项 fresh-context 检查、Python 3.9 本地检查、Python 语法及 whitespace 检查已留证 | 真实 FIELD、相机/模型/API、Whoop OAuth、Provider/SDK 成功路径和跨平台检查仍待相应环境 |

工具静态检查中 8 个技能直接通过 stock Codex validator；另外 2 个保留 Claude `argument-hint` 扩展字段，在临时副本移除此字段后通过。此项是 validator 对平台扩展字段的兼容限制，不代表十个源文件都能不经处理直接通过该 validator。R2 的 `C + N + J` 取代下文原验收文字中的旧特例 `1 + N + J`；仅当此前没有 hold 时二者的 Commission 数相同。

本节的证据只支持所列的本地及隔离场景，不代表真实 provider、相机、OAuth、FIELD 或远端服务已成功。本地已完成事项不再作为后续待办；剩余工作限于表中注明的环境依赖。

初始评估日期：2026-09-20。初始评估时 HEAD：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。

## 结论与范围

原评估中的主要文档问题已有修订，不能再把原报告当作当前待办清单。本次重读原报告和 **10/10 个当前 SKILL.md**，定向检查实现、模板及跨家族契约后，确认仍有启动失败、错误成功状态、Run 记录覆盖、暂停后无法正常结束，以及 Workflow 样例偏离当前 Design 契约的问题。

本文列出 **5 项 P1、6 项 P2，以及 1 项 P2 验收缺口**。P1 优先处理无法完成操作、误报成功、覆盖结果或改变工作流闭合条件的问题；P2 处理可移植性、文档冲突和交互成本。编号 R1–R12 是本次清单，F1–F9 指原报告。

在最初评估阶段只新增本文，没有编辑技能、代码、配置、原报告或其他家族文件。那一阶段工作区已有 9 个 utility skill 的修改及多个家族、submodule 的既有变动；均予以保留。当时没有运行测试、fresh-context 实测、provider CLI、摄像头、OAuth、Anthropic、Whoop 或远端服务；相应代码判断来自静态检查，验收项尚未执行。后续授权的修订与验证记录在本报告开头及关联实施状态报告中。

原报告：[0_utils.md](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/0_utils.md)。本报告的行号指本次读取的工作树，后续并行修改可能使行号变化；引用的节名、函数名和字段可用于重新定位。

## 1. 初始评估时的逐技能状态（已由上方实施状态取代）

“已有修订”表示修改存在，不等于功能已验收。“未见原问题残留”只针对本次评估范围。

| 技能 | 当前状态 | 已处理的内容 | 本次仍需处理 |
|---|---|---|---|
| [call-peer](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/SKILL.md) | 部分修订，入口仍有阻塞 | wrapper 路径、动态 cwd、默认 skill 路径、operation 用词 | R1 启动依赖；R6 安装路径；R10 名称契约 |
| [diagram-ascii](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/diagram-ascii/SKILL.md) | 原问题在文本层已处理 | emoji 可选；主文及图库路径已改 | R12 验收；本次未确认新的功能阻塞 |
| [field-test](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/field-test/SKILL.md) | 尚未修改；发现跨家族引用漂移 | 保留预先写 expectation、隔离 FIELD context、按证据结算的方法 | R8 旧 auto-charter 指引 |
| [meal-cam-logger](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/SKILL.md) | 文档及实现已有修订，控制流程未闭合 | 正确 CLI、episode 模型、唯一 receipt、空 session、skip、正常结束写回 | R5 暂停后停止；R6 路径；R12 控制与外部服务验收 |
| [notebook-cell-python](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/notebook-cell-python/SKILL.md) | 文档已有修订，仍有执行/Run 问题 | converter 路径、nbconvert 清理、Step 用词 | R3 退出码；R4 同日覆盖与 receipt；R6 环境/路径 |
| [remote-error](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/remote-error/SKILL.md) | 通用化尚未完成 | 通用模板、条件化落盘位置、五个 Steps、Session 与 Run ID 区分 | R7 通用规则、profile 选择、回复及结算仍有冲突 |
| [response-format](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/response-format/SKILL.md) | 激活与特例已处理，仍有小范围越界 | 删除无依据的 always-on；明确 table-only/remote-error 特例 | R11 文件格式边界；R12 组合验收 |
| [table-task / task-table](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-task/SKILL.md) | Run 行语义已处理，命令可移植性未完成 | 移除 live Phase/Cycle 定义；修正 renderer 路径 | R6 路径解析及 shell 引号；R12 渲染验收 |
| [table-workflow / workflow-table](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/SKILL.md) | 抽象模型改善，Design 样例仍不正确 | 明确 Workflow 是 Run Specs 列表；统一五个 Space 名称 | R2 退役 Adopt、路由和计数；R12 一致性验收 |
| [whoop-connect](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/whoop-connect/SKILL.md) | 误导性承诺已处理，外部接入未验证 | 不收聊天 secret；不凭 token 文件声称已连接/定时同步；Run 闭合加条件 | R9 前置检查与回调配置；外部实现仍是依赖 |

两个表格技能的目录名与调用名不同是既有约定，本次不把它列为缺陷。没有新增第 11 个 utility skill。

## 2. 原 F1–F9 逐项复核

| 原问题 | 当前证据 | 处置结论 |
|---|---|---|
| F1：task-table 仍用 Phase/Cycle 定义 Workflow 行 | `table-task/SKILL.md` 15–17、36–41、118–125、306–308 已改为 Run Spec；Task Folder 仍是一行 | 原具体问题已处理；保留粒度区分 |
| F2：schema 仍用 Plan/Create/Review | `table-workflow/SKILL.md` 59–75；`ref/workflow-table-schema.md` 160–187、235–240 已统一 Goal/Design/Insight/Run/Delivery | 原 roster 问题已处理；但不能据此判整份样例正确，见 R2 |
| F3：Meal Cam 路径、参数、行为说明错误 | `meal-cam-logger/SKILL.md` 29–56、61–73、121–129；`meal_cam_loop.py` 36–59、248–269 与 episode/FPS 说明对应 | 原 CLI/检测模型问题已处理；没有实际开摄像头验证 |
| F4：skip 不会进入进程；stop/无 bite 无完整 receipt | `meal_cam_loop.py` 159–178、188–214、283–314；`episode_tracker.py` 60–72；skill 90–118 禁止读“最新文件” | 删除最近 episode、启动 receipt、正常结束写回已有实现；暂停后停止仍有 R5 |
| F5：Whoop 聊天收密钥、无证据承诺 7am 同步 | `whoop-connect/SKILL.md` 34–45、78–88、116–142 已禁止这些行为 | 原安全/证据承诺已处理；真实本地接入尚未完成，见 R9 |
| F6：不存在的路径 | call-peer 198–206、table-task 241、notebook 44–48/221–222、diagram 255 及图库 31 已改；`pair_sync.py` 178–181 从自身文件解析 skill | 部分处理；call-peer 仍无法在此树启动，已安装 skill 的路径还会解析到目标项目，见 R1/R6 |
| F7：通用 remote-error 套 CMS 模板；内部称 Phase | `remote-error/SKILL.md` 84–89、120–134、234–266；通用模板 3–6、59–66；profile 标题改为 Step | 五个 Step、通用模板和落盘边界已处理；主文后半仍强制 CMS gate/ID，见 R7 |
| F8：格式 always-on 无入口，特例冲突 | `response-format/SKILL.md` 21–30；`remote-error/SKILL.md` 298–301 | 原激活与优先级问题已处理；本次仅确认根 `CLAUDE.md` 不存在，未实测平台加载 |
| F9：diagram 强制密集 emoji | `diagram-ascii/SKILL.md` 16–18、121–123、440–445 | 原风格问题已处理；不再要求每个标签/六种以上 emoji |

没有为这次报告重做上述已完成修改，也不建议全局替换历史 CHANGELOG 中的旧术语。

## 3. 原始问题、证据与修复方案（初始评估记录）

### R1 · P1：call-peer 修正了命令路径，但启动仍依赖另一个仓库

**文件与证据：**

- [SKILL.md:198](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/SKILL.md:198) 强制执行 `$REPO_ROOT/.venv/bin/python`；当前 Tools-SPACE 没有该文件。
- [run_cli_agent.py:34](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/scripts/run_cli_agent.py:34) 的 `_repo_root()` 要求候选目录同时有 `pyproject.toml` 和 `code/`，否则抛出 Physician-SPACE 错误；42 行在 import 时调用。
- [run_paired_cli.py:26](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/scripts/run_paired_cli.py:26) 与 [pair_sync.py:38](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/scripts/pair_sync.py:38) 均导入该模块。只读 resolver 也因此受影响。
- 本次只读检查了 cwd 和脚本祖先目录：没有满足此 resolver 的候选。`run_native_agent.py` 与 `run_shared_agent.py` 的 root resolver 也有相同假设；native SDK 路径另外依赖 `haiutils.agent_sdk`。

**影响：** 照更新后的说明仍会先遇到 Python 路径缺失；改用现成 Python 也不能绕过 import 时的 root 错误。用户看到“路径已经修好”，实际仍无法读取 pair 或启动明确请求的 peer。

**修法：** 将 skill 安装位置、用户工作目录、可选 SDK 项目依赖分开解析。普通 CLI 与只读 registry 操作不应依赖 Physician-SPACE 的 `code/`。选定并验证可用 Python；只在明确选择 SDK 模式时检查 SDK 依赖。延迟有副作用或环境要求的初始化，保留 pair 身份检查及只读约束。

**验收：** 在 Tools-SPACE 和一个无 `code/pyproject.toml` 的目标项目中，帮助/参数解析及只读 pair 查询可用；缺少 manifest 明确返回未注册，不能调用 provider 或写 registry。普通 CLI 的依赖检查通过后才允许进入实际 provider 调用。SDK 模式缺依赖有独立说明，不阻塞普通模式。

### R2 · P1：Workflow 表格样例重新引入已退役的 Design Adopt Run

**文件与证据：**

- [table-workflow/SKILL.md:138](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/SKILL.md:138) 仍教四种 Run Spec；146、152–164 行包含 Adopt、人类二次决定及 `1 + N + J + 1`。
- [workflow-table-schema.md:189](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/ref/workflow-table-schema.md:189) 的 Generate `fail: HOLD`、Verify `pass: adopt`、217–229 行 Adopt declaration 继续保留旧闭合逻辑。
- [run-catalog.md:48](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/ref/run-catalog.md:48) 保留 `Design.adopt`，66 行示例仍允许 agent 的 `fail: HOLD`；[skill-coverage.md:19](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/ref/skill-coverage.md:19) 引用 `adopt@runtime`。
- 当前权威 [haipipe-design-workflow/SKILL.md:24](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:24) 规定 Commission → Generate → Verify → Delivery，41 行计数为 `1 + N + J`，44–46 行限制 HOLD 为 Commission 的人类决定，61–64、137–142 行说明 Delivery 是只读投影。180–186 行明确新 writer 不得创建 `rdNN_adopt_*`。

**影响：** 表格作者仍会多安排一个人类审批、增加 Run 计数，并在 agent 失败时走错误路线。修正 Space 名称没有修正实际用户交互和闭合条件。这是本次相对于原 F2 补充确认的问题。

**修法：** 以当前 Design owner 为依据，同步主文、schema、catalog、coverage 的 Spec 列表、路由、计数和 Delivery 显示条件。删除 live `Design.adopt` 示例，保留其明确标记的历史语义；Generate 失败和 Verify 无效按 owner 规定回到相应队列。Delivery 只展示通过 Verify 的同一个结果，不创建新的 Run 或审批。

**验收：** 从当前 declaration 渲染的清单只有 Commission、Generate、Verify 三种 Design Run；计数是 `1 + N + J`。Verify pass 后直接 ready for Delivery；agent 分支不产生人类 HOLD；主文、schema、catalog、coverage 无悬空 `adopt@...`，且所有 Cell/Route 可解析。

### R3 · P1：Notebook converter 会把已识别的失败作为成功退出

**文件与证据：** [convert_to_notebooks.py:203](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/notebook-cell-python/convert_to_notebooks.py:203) 在无输入、无目录、无文件时 `return 1`；269–270 行入口只调用 `main()`，没有把其返回值交给进程退出码。234–243 行批量模式捕获单个异常后继续打印 `✓ Done!` 并 `return 0`。

**影响：** 单文件缺失等已处理失败可向 shell 返回成功；批量部分甚至全部失败也被总结为完成。Agent、CI 或 wrapper 可能继续交付不存在/不完整的 notebook。此项通过源码控制流确认，未运行重现场景。

**修法：** 入口传播 `main()` 的返回值。批量转换统计成功/失败，对任一失败返回非零，并输出准确的汇总及失败文件列表；允许保留成功的输出，但不得宣称整批成功。

**验收：** 无输入、不存在的输入、空目录均非零退出；批量混合成功/失败时非零退出且列出失败；全部成功才返回零。wrapper 不得在 converter 非零后打印成功。

### R4 · P1：Notebook 每次调用都称 Run，但同日执行覆盖同一结果，缺少闭合记录

**文件与证据：** [notebook-cell-python/SKILL.md:192](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/notebook-cell-python/SKILL.md:192) 将每次 wrapper 调用定义成 Run；209–215 行只用日期与脚本名确定 `RUN_DIR`，同一天再次执行使用相同路径，`NOTEBOOK` 也始终相同。197–227 行 wrapper 没有保存独立的 Run ID、最终 status、错误或 receipt。

**影响：** 两次调用可能覆写同一 CSV/PNG/notebook。用户不能区分哪次结果成功，旧输出还可能留在失败运行目录中。仅有 `runs/` 文件夹和命令调用不足以满足共享 Run 契约。

**修法：** 若把每次 wrapper 作为独立 Run，使用现有 Run owner 分配的身份或唯一实例 ID；输出与终态 receipt 按该实例隔离，包含 target、actor/action、start/end、status、exit code 和产物指针。复用同一 Run 时保留 attempt/version 历史，不能静默覆盖。若只是转换 helper，就称为所属 Run 的 Step，不自动分配 Run。`_LATEST` 和固定 notebook 路径可以是展示指针，不应是唯一历史证据。

**验收：** 同日两次执行的结果都能单独寻址；脚本失败和转换失败都有真实终态，旧产物不被当作本次成功。`.py` 仍是 source of truth，转换与可选 notebook 执行不会被重复计为额外 Runs。

### R5 · P1：Meal Cam 的 Pause → Stop 顺序无法按说明正常闭合

**文件与证据：** [meal-cam-logger/SKILL.md:119](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/SKILL.md:119) 用 `SIGSTOP` 暂停整个进程；139–150 行 Stop 只发 `SIGTERM` 并等待，没有恢复进程。[meal_cam_loop.py:159](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/scripts/meal_cam_loop.py:159) 的 SIGTERM handler 只设置 `stop=True`，结束写回依赖该进程继续执行到 `finally`。被停止的进程无法执行这些 Python 代码，直到收到恢复信号。

**影响：** 用户先暂停、再说结束，receipt 可以一直处于 running，无法拿到已承诺的最终时长；skill 只报告没有确认停止，却没有可执行的恢复路径。

**修法：** 优先使用进程内的 pause 状态，让进程仍能处理 stop/skip；最小 POSIX 修订应明确待终止进程的恢复信号顺序。控制命令验证 PID 对应本次 session；新 shell 同时恢复 PID file、log、receipt 三个地址。定义 Duration 是否包含暂停时间，并明确正在等待摄像头/API 时停止可能延迟。

**验收：** Start → Pause → Stop 能在定义的正常控制时限内退出并写终态；无 bite、skip 后 stop、pause/resume 后 stop 均读取同一 receipt。两个同时运行的 session 不互相控制；超时只报告未确认，不捏造 end。Windows 不宣称支持 POSIX 信号；SIGKILL/断电不能正常闭合的限制继续保留。

### R6 · P2：安装后的工具位置与目标项目位置仍混用，示例还假设本地环境存在

**文件与证据：**

- [call-peer/SKILL.md:198](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/SKILL.md:198)、[meal-cam-logger/SKILL.md:61](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger/SKILL.md:61)、[table-task/SKILL.md:241](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-task/SKILL.md:241) 将当前 Git 根目录当作 toolkit 根。
- [notebook-cell-python/SKILL.md:202](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/notebook-cell-python/SKILL.md:202) 从任务定位目标项目后，在 221 行向该项目拼接 toolkit 路径；206–207 行无条件 `source .venv/bin/activate` 与 `env.sh`。当前 Tools-SPACE 两者都不存在。
- `table-task/SKILL.md` 243–250 行使用未加引号的 `python3 $G`，在 Bash 等会分词的 shell 下，带空格的路径会被拆开。
- [install.sh:11](/Users/jluo41/Desktop/Tools-SPACE/install.sh:11) 支持全局和其他项目安装，因此运行 skill 的目标项目不必包含 `plugins/haipipe-toolkit/`。

**影响：** 在本仓库修好了前缀，并不能使全局安装或其他项目中的调用正确。用户可能被要求切换错误的工作目录，产物位置随之变化；依赖缺失也可能在处理开始后才暴露。

**修法：** 使用已加载 SKILL.md 的实际目录解析 bundled script，另设目标项目/cwd/output。允许调用者明确提供 toolkit 路径并验证存在。解释器和项目环境在执行前检查；可选环境文件按项目配置加载，不默认存在。所有 shell 路径参数加引号。

**验收：** 仓库内、全局安装、其他 Git 项目、包含空格的目录都能定位同一个 bundled tool，同时保持正确目标 cwd/output。缺解释器/包时在产生误导性成功消息前给出准确缺项；不自动创建冒充原项目配置的 `env.sh`。

### R7 · P2：remote-error 的通用模式仍被 CMS 规则与强制提问覆盖

**文件与证据：** [remote-error/SKILL.md](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/remote-error/SKILL.md) 存在以下同文件冲突：

- 120–134、234–238 行允许无 profile、无 static gate；33–35 行却要求总是说 gate green，393 行要求 `<UNIT> n/<total>`，418–419 行把 fixed 限定为 gate green。
- 通用 [issue-file-template.md:11](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/remote-error/ref/issue-file-template.md:11) 接受 `unassigned` ID；主文 405 行仍要求六字符 ID。
- 203–215 行把“每行注释必须完整一句”和 `[ID]` 当作 generic laws；CMS profile 92–98 行实际把它们列为该环境规则。
- 主文 49–51 行把任意 `r(nnn)`/`.do` 自动路由 CMS；[profile-cms-stata.md:6](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/remote-error/ref/profile-cms-stata.md:6) 甚至包含一般 `.ps1`/`results/<run>/log/`。这些特征不足以唯一确定 CMS 环境。
- 427–434 行要求每次都问 commit/push，包括 `need-more-log`、`no-repo-change`；84–114 行的命名/换 session 仪式也会给简单故障诊断增加交互。

**影响：** 新 agent 可能给非 CMS 项目套规则、虚构 gate 或为了满足格式填出不存在的 ID。用户在没有改动时仍被要求决定提交；一次简单排错被拆成多次人工操作。

**修法：** 将 ID、注释、gate 输出和状态词严格放入选中的 profile；generic outcome 记录“改了什么、做了哪些检查、仍未远端复跑”。profile 选择需项目证据或已知配置，Stata/PowerShell 特征只作为候选线索。回复要求按实际产生的内容启用；只有有可提交变更且确有待决事项时才提提交问题，复用已提供的 session 名称和授权。

**验收：** 一个没有 profile/gate/issue ID 的 Python 远端错误仍能产出通用报告，不声称 gate green，不写 CMS 路径，不补六字符 ID。非 CMS 的 `.do`/`.ps1` 不自动加载 CMS。CMS 情形保留自己的 gate 和数据约束；未改文件时没有空“我改了什么”或提交请求。

### R8 · P2：field-test 仍引用已消失的 auto-charter 小节

**文件与证据：** [field-test/SKILL.md:131](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/field-test/SKILL.md:131) 指向 `haipipe-insight §The auto charter`，并描述运行前新签 charter、把 gates 批到两端。当前 [haipipe-insight/SKILL.md:318](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:318) 已改为 Bounded standing authorization，实际 schema 在 [authorization.md:3](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/ref/authorization.md:3)：引用已有明确授权，不重复索取；绑定 board/runtime/targets/actions/expiry；空 run_ids 不授权 Run execution；签名和新计算 release 不包含在授权中。

**影响：** FIELD commission 可能链接不到规则，或把已经给出的授权再问一遍；也可能误以为“自动化”让所有 gates 都可批处理。此前状态表的“未改动”不代表当前跨家族引用仍正确。

**修法：** 更新到现行引用，用 target family 自己的授权规则，限定哪些动作可批处理；已有授权只记录来源和范围。保留独立 context、冻结 expectation、monitor 只读等原方法，不把 monitor/desk/消息轮次变成 Runs。

**验收：** 新 context 能沿引用读到真实 schema；已授权的机械操作不重复提问，越界操作停在所属 gate；新计算 release/handoff signature 不因 field-test 自动化被放行。

### R9 · P2：Whoop 先要求用户建 app/配置凭据，后检查接入程序是否存在

**文件与证据：** [whoop-connect/SKILL.md:59](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/whoop-connect/SKILL.md:59) 先引导建 app，70–74 行写死 `http://localhost:8080/callback`，78–84 行要求按 checkout 文档完成本地 credential setup；94–107 行才定位 checkout 并检查脚本和安全加载方法。当前 `plugins/` 下没有 `whoop_listen.py`/`whoop_sync.py`，旧硬编码外部目录也不存在。

**影响：** 用户可能做完网页操作才发现没有可用的本地接入程序；指定的 callback 也尚未与真实 listener 配置核对。当前文本已经避免不实成功声明，但操作顺序仍会造成返工。

**修法：** 把 checkout、依赖、credential loader、callback URI、启动命令和非密钥状态接口的检查移到 Step 1 之前。从已经验证的 listener 配置给出 redirect URI。程序不在本 workspace 时明确依赖和下一步；实际 OAuth/sync 功能由外部项目补齐或验证，不能用文档改写冒充已实现。每日 scheduler 保持独立范围，不为完成连接任务自动增加定时作业。

**验收：** 无 checkout 时在要求建 app 前报告缺项；有 checkout 时 callback 与配置一致。只有本次 callback 成功且 token 存储更新才报告授权成功；旧 token 文件不算新成功。全程不接收/打印 secret，不凭连接成功声称刷新、同步或调度已验证。

**不确定性：** 本次仅检查工作树和旧指定目录，未搜索整个用户机器，不能断言用户没有其他 Health-Sync checkout。Whoop 网页字段、套餐、OAuth 可用性和外部脚本实现未联网核验。

### R10 · P2：call-peer 文档要求同名，wrapper 却禁止同名

**文件与证据：** [call-peer/SKILL.md:78](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/SKILL.md:78) 要求双方共用一个 human-readable name，86 行说原样传给 Claude `--name`。[run_paired_cli.py:47](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/call-peer/scripts/run_paired_cli.py:47) 默认加 provider 后缀；61–65 行拒绝与 pair/caller 相同的 callee 名称。

**影响：** 正常运行后的名字和文档承诺不同；agent 若试图遵守同名规则，反而触发错误，容易误判成需要新建或修复 pair。

**修法：** 文档明确 pair 的共享名字与各 native session 的显示名字不同，示例给出后缀及 `--callee-session-name` 用法。身份继续以 provider/session ID/cwd 为准；不因显示名差异创建重复会话。

**验收：** 默认名字与文档示例一致；合法自定义名字可用；禁止的同名输入给出同一规则的解释；status/read 请求始终定位原 session ID。

### R11 · P2：response-format 声明只管聊天，却夹带文件标题规则

**文件与证据：** [response-format/SKILL.md:35](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/response-format/SKILL.md:35) 先说不适用于文件，36–38 行紧接着宣称仓库文件必须 ASCII underline headers、不能用 `##`。当前 [workflow-table-schema.md:3](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/ref/workflow-table-schema.md:3)、[issue-file-template.md:21](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/remote-error/ref/issue-file-template.md:21) 及多个 SKILL.md 本身就使用 `##`。

**影响：** 聊天格式规范可能迫使 agent 重排与当前模板一致的文档，增加无关 diff；作者也无法同时满足“不要影响文件”和“文件不能用 ##”。

**修法：** 文件只遵守所在目录/文档模板的规则；从聊天 skill 移除不适用于整个仓库的标题假设。保留显式激活、table-only/remote-error 特例。其余严格 scan-point 字数等属于风格选择，本次不凭个人偏好列为功能缺陷。

**验收：** 同时加载 response-format 和文档型 skill 时，聊天遵守已启用格式，文件保留所属模板的标题结构；不产生仅为聊天排版要求的文件改动。

### R12 · P2 验收缺口：现有修订还没有可据以关闭问题的行为证据

**证据：** [README.md:133](/Users/jluo41/Desktop/Tools-SPACE/README.md:133) 要求 skill 变更后从 fresh context 调用真实任务，确认路由、执行和产物。本任务此前实施记录只报告 whitespace 检查及未运行测试；本次也是源码复核。Meal Cam 现有两个 `test_*.py` 分别面向 bite detector 和 food identification，不能据其存在推断新的 pause/skip/receipt 生命周期已覆盖。`table-workflow/ref/skill-coverage.md` 59–68 行也要求行为状态有 receipt，无证据应为 `?`。

**影响：** “文件已更新”会被误读成“技能已可用”，尤其容易遗漏跨 skill 输出冲突、无服务环境的错误分支和多 session 控制问题。

**修法：** 把文档静态复核、隔离的本地行为验证、fresh-context 场景及需要外部条件的实测分别留证。按下面的验收清单执行，记录使用的工作树内容、命令、输入、结果与限制；未做的项目明确标为 pending，不假定通过。

**验收：** 每个已修改技能都有对应场景和可打开的证据；无法进行的 Whoop/camera/provider/CMS/Windows 检查逐项注明原因与负责人。报告不把静态一致性、进程退出、API 成功和真实远端复跑混为一种 pass。

## 4. Workflow = list of Runs：初始评估判定口径

### 判定口径

用户可读表述为 **Workflow 是 Runs 列表**。精确建模时，计划清单列出 Run Specs，Routes 只连接清单项、表达依赖/分支/循环；运行时视图列出实际 Run Instances。一个 Spec 可以实例化多次；计划数量不是实际完成数量。

以 [haipipe-run/SKILL.md:82](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/run/haipipe-run/SKILL.md:82) 的六项标准判断 Run：bounded target、稳定类型/身份、actor/action 与 Ticket/Spec、闭合规则、耐久终态 receipt、独立闭合。内部计算、API 调用、人类点击、Step、重试、聊天轮次、展示卡片不自动成为 Run。

当前 `0_utils` 非 CHANGELOG 文档的 `Phase/Phases` 定向检索，仅返回 table-workflow 的“行不能是 Phases”否定规则；这不违反命名要求。**词语检查已经改善，语义验收仍不能省略。**

| 技能 | Workflow/Run 判定 | 依据与待办 |
|---|---|---|
| call-peer | 不拥有 Workflow；用词已符合 | 48 行 read-only operation；pair/session 是身份关联，不自动算 Run。R1/R10 影响可执行性及可理解性 |
| diagram-ascii | 不拥有 Workflow；可作为展示 | Stage/progress 列是内部阶段；`ref/05-progress-tracker.txt` 35–40 行以 Run 为行、Load/Train/Eval 为列。只有展示已有 Run 时才计数 |
| field-test | 方法边界可保留；授权交叉引用待修 | commission 按内部 steps；独立 FIELD context 不等于新增业务 Run。按 R8 更新授权，不把 desk/judge/message 数当作 Run 数 |
| meal-cam-logger | 本地 session 边界基本具备，闭合部分符合 | 13–16 行一餐一 Run、Start/Monitor/Stop 为 Steps；有唯一 receipt，但 R5 使暂停分支无法闭合。若接入 haipipe 运行库存，还需核对 owner/type/actor/Ticket 绑定 |
| notebook-cell-python | 不符合完整 Run 标准 | 193 行自动称每次调用为 Run，而 R4 缺少独立身份/receipt 且可覆盖。不得靠换词过关 |
| remote-error | 用词与身份区分已符合 | 84–89 行 Session 与 remote Run ID 分开；五项是 Steps。R7 不应为通用报告补造 Run/ID/gate |
| response-format | 不适用 | reply section/scan point 不是 Run；R11 是文档边界问题 |
| table-task | 行粒度符合 | Task Table 按 Task Folder；Workflow 按 Run Spec；runtime 按 receipt-backed Run。R6 不改变这些粒度 |
| table-workflow | 抽象定义符合，Design 实例不符合当前 owner | 31–33 行明确列表与 Routes；R2 仍多算已退役 Adopt，需要同步后才能整体通过 |
| whoop-connect | 条件性符合，实测未完成 | 34–39 行要求真实身份/receipt，没有则不宣称 durable Run close；app 创建/OAuth/验证为 Steps，scheduler 独立且未配置 |

全族验收应同时回答：是否仍把 Workflow 单元叫 Phase；每个新增 Run 是否能通过六项标准；同一实例跨 Space 展示是否只计一次；Step/Version/retry 是否保持在所属 Run 中。历史 CHANGELOG、否定规则和普通图表的 Stage 轴无需机械替换。

## 5. 初始评估时的跨家族事项与不确定性

1. **Design owner → table-workflow：** R2 需要以当前 Design workflow 为来源。不要为了保留 utility 样例而恢复 Adopt 或新增审批；同步前重新读取 owner，防止共享工作树继续变化。
2. **Insight owner → field-test：** R8 跟随现行 authorization schema。原报告中“Application 是 Insight/Design 父层”的主文问题目前已处理：`haipipe-insight/SKILL.md` 明确 peer families/InsightBoard，`application` 仅保留为 legacy scope token。本次也已将 `agents/openai.yaml` 的短描述更新为 “Task and InsightBoard work”，其余指令保留。未对整个 Insight 家族做完整复审。
3. **目录索引：** `plugins/haipipe-toolkit/README.md` 129 行现在将 connector skills 放在 `0_utils`，`skills/0_connect` 不存在；原索引问题已处理。根 README 的历史盘点不应当作当前清单反复改写。
4. **Run owner / Task owner：** R4 先确认 notebook 是 helper Step 还是独立 Run；native 身份/receipt 交给现有 owner。不要让 utility 自建与 Task Table 不兼容的第二套库存。
5. **安装器 owner：** R6 依据现有 global/project 安装行为解决 skill 定位；本次不要求更改安装器。若后续确需改安装器，两个平台行为和来源目录需同步核对。
6. **外部状态：** 未核验 provider/SDK 版本、OAuth 服务、MediaPipe/OpenCV 原生日志是否会输出 URL、实际相机/API 停止延迟。脚本自己的 URL 隐藏不能证明下层库也完全不记录 URL；这属于待验证风险，本文没有断言发生了泄露。完整 call-peer transport、camera detector、renderer 的代码审计也不在本次复核承诺内。

## 6. 原建议实施顺序、依赖与关闭标准

以下内容记录首次评估提出的实现顺序、依赖和验收标准，不表示这些工作仍全部待做。各项当前状态见本报告开头的 R1–R12 表；工作批次只是计划组织，不自动分配业务 Run。

| 顺序 | 工作 | 依赖 | 完成时应留下的证据 |
|---|---|---|---|
| 1 | 固定当前来源快照；落实 R2 的 Design Spec/Route/Delivery 口径 | 重新读取 Design owner；保留并行变动 | 主文、schema、catalog、coverage 一致的矩阵；无新 Adopt；`1+N+J` |
| 2 | 修 R1 call-peer 入口；一并处理 R6 的 toolkit/target/env 定位和 R10 名称文档 | 明确 skill 实际位置与目标 cwd 的解析规则 | 不启动 provider 的帮助/只读场景；两种仓库布局及带空格目录证据 |
| 3 | 修 R3 converter 退出码，再修 R4 wrapper Run/receipt | R6 的 Python/工具路径；Run owner 对身份/receipt 的决定 | 失败退出码、混合批量结果、同日两次运行及失败 receipt；旧结果保留 |
| 4 | 修 R5 Meal Cam 控制及日志地址恢复 | 已有 receipt/skip 实现；R6 的启动路径 | 无 bite、skip、pause→stop、双 session 的隔离验证；外部 API/camera 单列 |
| 5 | 修 R7 通用排错规则、R8 授权引用、R11 文件格式边界 | CMS/Insight 当前 owner；保留已有显式授权 | 无 profile 与 CMS 两类报告；授权边界场景；聊天+文件格式组合场景 |
| 6 | 修 R9 Whoop 前置检查 | 真实 Health-Sync checkout 与安全本地配置接口 | 缺 checkout 时早停；存在时确认 callback/新 token 证据；不承诺 scheduler |
| 7 | 完成 R12 验收，逐项关闭或注明外部依赖 | 先完成对应修订；验证期间冻结被测文件 | 十技能覆盖表、expectation/friction/receipt、明确 pass/fail/pending |

R2、R1/R6、R5、R7/R8/R11 可以由各自 owner 在不交叉编辑同一文件的前提下独立推进。R3 的失败状态传播必须先于 R4 的“成功 Run”验收；否则 receipt 可能把 converter 的假成功固化。R9 的外部依赖不应阻塞其余本地修复。

### 每技能最小验收场景

| 技能 | 场景 | 通过标准 |
|---|---|---|
| call-peer | 只读进度；未注册 pair；错误 caller；显式启动的前置解析 | 只读不调用 provider/改 manifest；名字和身份不混淆；入口可用；真实调用另记 |
| diagram-ascii | 用户要求纯文本四节点图；Run×Step 进度表 | 无强制 emoji；标签清楚；不将四个 Step 误算四个 Run |
| field-test | 使用已存在的有限授权生成 commission | expectation 提前冻结；FIELD 看不到 prediction；不重复授权、不扩大范围 |
| meal-cam-logger | 空 session、skip、pause→stop、启动失败、多 session | 同一实例文件贯穿始终；终态真实；控制无串扰；非正常断电限制明确 |
| notebook-cell-python | 成功转换、缺输入、批量部分失败、同日重复运行 | exit code 真实；不覆盖历史；Run/Step 与 receipt 对应 |
| remote-error | 无 profile/gate 的故障；CMS 故障；证据不足 | 通用和 CMS 规则分开；报告路径已知；不虚构 gate/ID/远端成功；无空提交问题 |
| response-format | 普通回复、table-only、remote-error、同时写 Markdown 文件 | 激活来源明确；特例不混排；文件保持所属模板 |
| table-task | 有 planned/failed/unknown receipts 的真实 task tree；带空格目录 | 每 Task 一行，状态来自 receipt；无证据不 Done；renderer 能被定位 |
| table-workflow | 当前 Design Workflow 与对应 runtime 投影 | 三种 Spec、五个 Space、路由和 Cell 正确；Delivery 不新增 Run；计数一致 |
| whoop-connect | 缺接入程序、旧 token、新 callback 成功三种情况 | 前置检查先于用户配置；旧 token 不报新连接；授权、同步、调度分开声明 |

## 7. 原交付与关闭规则

首次评估时交付的是问题与计划报告。用户随后授权实施，本次已在原计划之外更新实施状态，并另存逐技能报告及验证证据。原评估保留为历史快照，早前工作区修订继续保留。状态按“修订已落盘 → 静态复核 → 对应行为证据”记录；需要真实服务或平台而未执行的检查标为 pending。

整体完成要求：所有 P1 关闭；P2 有修复或明确、可核验的外部依赖；十技能没有漏项；Workflow 列表、Run Spec/Instance、内部 Step 与当前 owner 一致。不能仅凭 Phase 检索为零、whitespace 检查通过或九个 SKILL.md 已修改，就宣称整个家族可用。
