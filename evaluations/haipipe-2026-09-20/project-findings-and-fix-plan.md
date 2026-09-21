# Project 家族：复核后的问题清单与修复计划

日期：2026-09-20。当前 HEAD：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`。本报告补充 [原评估](/Users/jluo41/Desktop/Tools-SPACE/evaluations/haipipe-2026-09-20/project.md)，涉及原评估误判或过时信息时，以本次复核结论为准。

最先应修复的是单项目会议目录与 Project 审计之间的冲突。随后应统一项目查找范围，修复反馈“写入后列不出来”的流程，并更新会议到 Page 写作的交接规则。本报告列出 10 项问题或契约缺口，分别给出证据、影响、修复方案和验收条件。

本 session 没有另行授权的修复执行任务。本次只新增本补充报告；实施、迁移、测试和外部服务操作均属于下面的后续计划。

## 复核快照与覆盖

Project 家族目前仍为 **2 个技能、16 个文件**。两份 `SKILL.md` 和全部 11 份当前支持文件均重新完整阅读；3 份 changelog 仅作历史来源，亦已复核。审计脚本采用静态阅读，没有调用被评估技能或执行审计。本文验收用例尚未运行。

| 覆盖对象 | 本次核对内容 |
|---|---|
| [haipipe-project](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md) | 全文；README；`ref/project-structure.md`、`ref/code-structure.md`；`fn/project.md`、`repo-project.md`、`audit.md`、`update.md`、`feedback.md`、`digest.md`；`feedback/README.md`；`scripts/audit_projects.py`。 |
| [haipipe-project-meeting](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md) | 全文；owner 解析、目录、保存、下游路由、返回值、legacy 规则。 |
| 历史材料 | 家族 changelog 与两份技能 changelog；没有将旧命名、退役技能或历史版本视为当前行为。 |
| 跨家族核对 | 当前 Insight 入口、共享 `skills/STRUCTURE.md`、Workflow 入口、Page Content 的请求分流与发布条件、Board 的旧 meeting 接口提示；仅核对相关段落，不声称完整审阅这些家族。 |
| 仓库约束 | 根 `AGENTS.md`、README 的技能修订验证说明、原始评估 BRIEF；作为本次评估与未来实施的边界。 |

Project 目录在本次复核开始时相对 HEAD 没有差异。仓库其它位置已有大量未提交改动，包括 Insight、Page、Board、共享 README/STRUCTURE 和外部 reference 子模块；这些都先于本次写入存在。特别是 Insight 已更新至当前工作树中的 `1.6.0`。提交号本身不能代表这些文件的当前内容，因此下列跨家族结论以本次读取的工作树为准，不能把观察到的他处修改算作本 session 的修复成果。

## 原报告的更正与状态变化

| 原结论 | 本次结论 | 依据 |
|---|---|---|
| `Proj*` 会漏掉 `Project-*`。 | **撤回，这是误判。** `Project-...` 本身以 `Proj` 开头，能够被该 glob 匹配。不得为这个错误理由修改审计器。 | [审计发现规则](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/scripts/audit_projects.py:188)。真正需要明确的是非 `Proj` 前缀 ID、多个 roots 和 state 的选择规则，见 F02。 |
| 跨两个 Projects 的会议写入后也会触发 Project 根审计失败。 | **缩小适用范围。** 确认的冲突发生在 `<project>/meetings/`；正常批量 Project 审计不会把 `<SPACE>/meetings/` 当作某个 Project 的根目录。原桌面演练混用了这两个位置。 | [Meeting owner 路径](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:25) 与 [审计枚举范围](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/scripts/audit_projects.py:182)。 |
| mission 未出现在入口，因此创建后可能直接审计失败。 | **降为入口可发现性问题。** 正确加载 procedure 的 agent 会在创建前询问缺失 mission。没有证据表明正常遵循 procedure 会遗漏它。 | [new 的缺失值规则](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/project.md:13)。 |
| Insight 入口仍指向 `skills/application/`。 | **当前工作树已修复，不再列为待办。** 现在写 `skills/insight/`，并明确 Insight 与 Design 为独立 peer families；`application` token 标为 legacy selector。 | [当前 Insight 入口](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:32)、同文件 `Family boundary` 段（第 40 行）。 |
| Project 没写出 Workflow 定义本身就应算不符合。 | **收窄判据。** Project 明确只拥有根目录；缺少重复定义不是独立缺陷。保留需要清理的活动词 `phases`，并要求实际 Workflow 定义与用户的 Runs 列表模型一致。 | [Project 责任边界](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:19)。依赖图可以表达列表中 Runs 的关系，不能仅因存在 graph 就判定违背该模型。 |

## 问题与拟修复方案

优先级含义：P1 为正常流程会遇到的直接契约冲突；P2 为范围、路由、恢复或 owner 方面的实质缺口；P3 为可发现性或术语改进。文字缺口与已证明的实现行为分别标记，未观察到的损害不按已发生事实报告。

### F01 · P1 · 单项目会议目录与根目录规范、审计 allowlist 冲突

**状态：确认存在；静态可推导审计后果。** 影响 `haipipe-project` 与 `haipipe-project-meeting`。

**证据：**[Meeting / Resolve the owner](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:25) 明写 `<project>/meetings/<YYMMDD-HHMM>/`；[Project / diagram](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/ref/project-structure.md:139) 却将其画成 `diagram/meetings/`。主入口的 [Canonical root](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:31) 也将 meetings 放在 `diagram/` 描述中。脚本 [WORLD_DIRS](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/scripts/audit_projects.py:16) 不含 `meetings`，[未知根目录分支](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/scripts/audit_projects.py:156) 会报 `undeclared noncanonical root`。

**影响：**agent 按会议技能正常存一份单项目会议记录，随后 Project audit 会把新目录当违规。把它写成 migration debt 又会错误地把新规范产物当作旧债务。人会同时看到两个“规范位置”。

**拟修复：**采用 dedicated meeting skill 已明确的 `<owner>/meetings/`，将 `meetings/` 加入 Project 可选根目录与审计 allowlist；同步入口、README、root tree、world 表和 `diagram/` 说明。保留 lazy creation。现有 `diagram/meetings/` 或 Page-local 记录进入兼容读取说明，不在普通 update 中自动搬移。

**验收：**其它字段合规的 Project 加入根级 `meetings/` 后仍为 `ok`；只有保存首个真实会议才创建目录；根级 `results/` 等既有禁项仍被识别；SPACE 级会议保持在 SPACE 范围；规范示例中只有一个新会议写入位置。

### F02 · P2 · 项目根、ID 发现与“all/active”的范围契约未统一

**状态：roots 不一致已确认；非标准 ID 与 state 行为需要明确产品契约。** 影响 Project 的创建、列表、audit 和 update。

**证据：**[技能描述](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:4) 承诺 `examples/` 和 sibling domain worlds；[README 开头](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/README.md:3)、[new / Preflight](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/project.md:20) 和 [repo 路径](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/repo-project.md:34) 只用 `examples/`。[audit 示例](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/audit.md:14) 显式只扫描 examples，但脚本 [project_paths](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/scripts/audit_projects.py:184) 默认扫描 examples 和 examples-nlp，并只枚举 `Proj*`。入口 [bare command](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:75) 说列出 active Projects；枚举函数不按 manifest state 过滤。空结果进入 [main](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/scripts/audit_projects.py:234) 后没有独立“零项目”说明。

**影响：**同样说“所有项目”，按 procedure 或直接用脚本会得到不同 roots。对创建规则只要求 readable/stable 的 `CGM-Pilot` 这类假设 ID，若按现文允许创建，它不会被 `Proj*` 批量发现；这是契约间的条件性不一致，尚未证明当前真实项目有此漏项。paused/archived 是否算在“active”之外也没有说明。

**拟修复：**集中定义 Project root 解析与选择规则，所有 verbs 引用同一段。建议默认创建于 `examples/`，允许显式指定 sibling root；批量操作报告实际 roots、发现数和 state 范围。发现机制采用“带 manifest 的直接子目录 + 旧 `Proj*` 候选”，从而兼顾任意合规 ID 与缺 manifest 的旧项目；其它名称的旧项目仍可显式传路径。保持 `_backup` 排除。对 paused/archived，建议只读 audit 展示全部并标明 state，普通 update 默认 active；这是拟定规则，实施时需与列表说明一并落定。

**验收：**`Proj...` 与 `Project-...` 均覆盖；允许创建的非前缀 ID 也能被找到；缺 manifest 的旧候选仍有诊断；默认与显式 roots 的规则一致；拼错或空 root 不显示成“全部合规”；用户能看出本次查了哪些项目。此项无需“修复 Project-* glob”。

### F03 · P3 · 第一屏缺少 mission、继续使用与辅助命令的入口

**状态：可发现性缺口；原报告的创建失败推断已撤回。** 影响 Project 新手体验。

**证据：**[Commands](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:56) 与 [README Commands](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/README.md:8) 未显示 `--mission`；[new Inputs](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/project.md:8) 实际支持该参数且要求补齐缺失值。主入口对 new/repo/audit/update 都有明确 `Read fn/...`，对 [feedback/digest](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:71) 只有 “Existing feedback capture and confirmed transcript harvest”。入口也没有 meeting 命令的指引。

**影响：**人不知道一句话使命可随请求直接给出，或该用哪个命令继续旧项目。fresh-context agent 需要自行找到辅助 procedure。`BJTR`、world、profile、Git mode 同时出现，简单启动被内部名词遮住。

**拟修复：**补齐 `[--mission "..."]` 和条件性默认值说明；明确使命信息可来自已给出的自然语言，不强迫重复写 flag。增加一组按意图组织的入口：创建、列出现有项目、审计、更新、保存会议、记录工具反馈；为 feedback/digest 补准确 procedure 链接。bare command 展示当前状态、可点击项目入口和一条具体下一步。现有项目走 update/继续内容 owner，避免再次 scaffold。

**验收：**ID/mission 已给定时不重复询问；缺什么只问什么；软件/混合项目按请求选择 profile；不创建空 worlds；新手能从入口找到 meeting 与反馈；不需要先学习 BJTR 才能开始或恢复。

### F04 · P2 · 目录类别与独立 Insight/Design 家族的表述仍混杂

**状态：Project 内是语义范围不清；共享家族清单仍有当前术语不一致。**

**证据：**正确的 [Project owner map](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:85) 直接写 `haipipe-insight + haipipe-design`。但 [ref / Worlds and flow](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/ref/project-structure.md:93) 无限定地说 “An Insight is a Page type on the Task/Insights Board”；[repo first artifact](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/repo-project.md:45) 和 [feedback map](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/feedback.md:108) 仍单列 `Application`。共享 [STRUCTURE / Current skill buckets](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/STRUCTURE.md:148) 仍列 `application — the Insight/Design join and its delivery channels`。当前 [Insight 入口](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:22) 则区分 Task-side 与 InsightBoard 两种 scope，并在第 40 行明确独立 peer families。

**影响：**人可能把所有 Insight 都理解为 Task Page，或者把 `applications/` 目录理解为技能父家族。Project 本身没有证据表明在调用 `haipipe-application`，因此这里不宣称存在实际错误派发。

**拟修复：**把 `An Insight ...` 限定为 `A Task-side Insight Page ...`；说明 `applications/` 是产物存储目录，具体工作由独立 Insight 或 Design owner 处理。setup 和 feedback 的路由写出具体 owner。协调共享 STRUCTURE 维护者移除/更正退休的 Application 家族项，保留需要的历史存储路径与已标明的 legacy command selector。当前已修复的 Insight 物理路径不再重复修改。

**验收：**任务数据解释、InsightBoard 工作、Design 工作能分到正确 owner；当前家族图没有 Application 父层；不因整理技能家族而移动已有 `applications/` 内容；Task-side Insight 的规则不会被泛化到所有 Insight。

### F05 · P2 · 会议输入、时间、来源路径与中断恢复缺少最小约定

**状态：已确认契约缺口；碰撞、重复写入或错误归属均为待验证场景，未声称发生过。** 影响 Meeting。

**证据：**[Resolve the owner](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:22) 使用 `<SPACE>` 而未说明解析基准；第 29 行要求可信执行端时间，但没有解释文件夹时间对应录入时间还是会议发生时间。[Record shape](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:35) 只有分钟粒度名称，并要求已保存记录永不改写；[provenance](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:57) 要求 repository-relative digest path，却未定义嵌套 submodule 时指哪个 repository；[Return](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:68) 只有地址列表，未给出逐条已完成/待完成的恢复规则。

**影响：**补录旧会议时日期可能误读；一分钟内两条新记录会争用同一地址。会议源已保存、部分 Page 已更新后重试，agent 不知道怎样只补未完成项。SPACE 会议路由到独立 Project repo 时，来源相对路径也可能有两个解释。

**拟修复：**增加简短 intake 与 resume 段，接受已有笔记或 transcript，并从已有上下文解析影响范围。将 folder timestamp 定义为记录创建时间，在 digest 单列会议发生时间（可未知）和时区。SPACE 依据明确工作区边界解析，不能把最近的 Project submodule Git 根直接当 SPACE。相对路径必须声明所属仓库/工作区基准。digest 的决定/问题用稳定锚点；恢复时按源路径与锚点读取目标的已有 provenance，只补未完成项。新会议同名时分配唯一地址，具体后缀方案需先核对读取方；重试同一会议复用源记录。保留源记录不可改写的原则，用补充记录表达后续修正。

**验收：**单项目、跨项目、补录旧会议、同分钟两会议、部分路由后重试均有确定行为；已路由项不会重复追加；每条来源可从相应 Page 解析；只在 owner/决定状态等真实信息缺失时提问，明确授权的整理不增加一轮普遍审批。

### F06 · P2 · 会议的“内容修改”交接把起草与发布合并了

**状态：当前跨家族路由文字不一致，已确认。** 影响 Meeting 与 Page。

**证据：**[Meeting / Route effects](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:53) 将 `content change` 一概交给 `haipipe-page-content · WRITE cycle`。当前 [Page Content / Which request is this?](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-content/SKILL.md:38) 明确把 `Draft, revise, discuss sentences` 路由到 interactive writing → SHAPE + haipipe-writing；Content 负责接受后的 adoption。其 [release barrier](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-content/SKILL.md:54) 以及 [Entry gates](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-content/SKILL.md:95) 还要求完整的 writing/evidence 与人的接受记录。

**影响：**会议里“改一下开头”可能被送到发布入口，再被退回 SHAPE 或卡在发布条件上。接收技能有自己的 gate，本次没有证据证明会实际越过 gate 发布；确认的问题是发起方交接范围过宽。

**拟修复：**将会议路由拆成“修改草稿/讨论措辞”和“采用已接受文本/发布”。前者沿当前 Page interactive writing 路由，后者携带人的明确接受、目标版本及来源交给 Content。Task 后续工作也交给 Task/Run owner 决定新 Run、续做 Step 或 rerun；会议摘要本身不产生新执行权限。

**验收：**“改一句话”成为已有 Writing Run 内的适当 Step；“发布已接受版本”满足 Page 条件后才进入 Content；仅保存/路由会议决定不会自行 dispatch 无授权 Task 执行；记录、应用修改与发布结果在返回中可区分。

### F07 · P2 · feedback 的写入范围和 list 范围不同，部分 owner 没有路径映射

**状态：确认存在的操作说明矛盾。** 影响 Project 的 feedback、digest。

**证据：**[Inbox paths](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/feedback.md:147) 定义 skill root 为 `skills/project/`，但第 159、160 行将反馈写往 sibling `../task/haipipe-workflow/feedback/` 与 `../task/haipipe-task/feedback/`。[List](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/feedback.md:178) 却只搜索 “under the project skill root”。[反馈 README](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/feedback/README.md:32) 承诺 “ALL feedback/ inboxes”。关键词表第 107、108 行还允许 Discovery、Paper、Board、Page，而路径表未给出这些 owner 的统一解析办法；Meeting 也未显式列出。

**影响：**用户刚收到“已归档到 Task inbox”，执行建议的 `feedback list` 却看不到该条，容易重复提交。`move <file> <skill>` 也依赖同一不完整路径表。

**拟修复：**建立一份可解析的 owner→skill directory→inbox 映射或同等明确的解析规则，让 capture/list/move/digest 共用。list 遍历可路由目标集合，不能只遍历 Project 子树；未知 owner 留在 Project fallback 并解释原因。Meeting、Insight、Design 用明确 owner。保持惰性 inbox、同主题合并、原话保存、fixed 后重开规则。

**验收：**Project、Meeting、Task、Workflow 和选定跨家族 owner 的反馈均可 capture 后立即 list 找到，并支持 owner filter 与 move；已知但未建 inbox 不报错；同主题 recurrence 不产生重复；枚举不扩散到无关第三方目录。

### F08 · P2 · digest 的通用入口绑定了 Claude transcript 假设，名称选择示例会丢失歧义

**状态：宿主范围说明不足、示例与歧义处理规则冲突；不是已复现的数据丢失。**

**证据：**[根 README](/Users/jluo41/Desktop/Tools-SPACE/README.md:3) 说明集合面向 Claude Code 与 Codex；[digest / Resolve](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/digest.md:34) 的指定 session 路径和 [transcript store](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/digest.md:93) 却固定为 `~/.claude/projects/`。第 102 行名称查找使用 `head -1`，下一行又要求多结果时列候选。第 113 行明确这只是可适配的 extraction pattern，因此不能把它当作已运行实现；但直接复制示例会先失去多个候选。第 71 行输出 `src L<nn>`，抽取后的来源行号与原始 transcript 对应方式尚未定义。

**影响：**在另一个宿主找不到过去的 session 时，用户可能被误导为会话不存在。重名会话可能选错；反馈原话很难回到准确来源核对。无参数读取当前对话的路径仍然成立。

**拟修复：**保留当前对话模式；过去会话通过明确的宿主适配或用户给出的 transcript 路径读取。无可用适配时说明限制与下一步，不猜其它宿主的存储路径。先收集全部名称匹配再选择；存在歧义才询问。候选保留 session/turn ID 或可回查的原始行定位，不能生成没有对应关系的行号。继续复用 F07 的 router，并保留现有确认后写入与 `--dry-run` 不写入语义。

**验收：**当前会话、单一命中、多个同名命中、不可访问历史会话与已提供 transcript 都有明确结果；每项候选可回查原文；确认前零写入；dry-run 即使用户随后同意也不直接归档。

### F09 · P2 · repo 的 ADOPT 分支没有写清现有根文件的保留与失败后恢复

**状态：procedure 缺口；没有证据证明现实现会覆写文件。**

**证据：**[repo / Preflight](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/repo-project.md:25) 对已存在远端选择 ADOPT，但 [Create or adopt](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/repo-project.md:37) 对两条分支都写 “Inside the Project, create only: README.md, project.yaml, .gitignore”，没有分别说明已存在文件如何处理。[提交次序](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/repo-project.md:49) 指定 Project commit/push 后再 workspace pointer commit，但没有中途失败的恢复说明。相比之下，[update / Safe mutations](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/update.md:11) 已明确定义保留人的 narrative、只补缺失字段等边界。

**影响：**不同 agent 对“create only”可能作不同解释；已有仓库 README、ignore 规则、manifest 与新建仓库的处理容易混在一起。中断后用户无法从“两个 pointer 状态”知道该继续 push、更新 pointer 还是重新接管。

**拟修复：**CREATE 与 ADOPT 各列一个短分支。ADOPT 读取已有根文件，复用 update 的安全补齐规则，保留 README narrative 和现有 ignore 条目；只有无法从已有资料确定的必需信息才询问。提交步骤只包含本次请求造成的变更。每一层完成后返回实际 commit/push/pointer 状态，失败时指出最后成功边界与具体恢复动作。

**验收：**已有 README/.gitignore 的接管保留原有内容；有效 manifest 无多余改写；已有本地路径仍遵循当前停止/更新边界；模拟 Project push 失败时不声称整体成功，恢复不会重新创建远端或重复初始化。验证使用隔离 fixture/服务替身，避免真实建仓。

### F10 · P3 · 活动反馈词表仍有 `phases`，Workflow 说明需要服从同一权威

**状态：确认的术语残留；未发现本家族把 Phase 定义为当前执行对象。**

**证据：**[feedback map](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/fn/feedback.md:109) 写 `workflow, IPO, phases, plan workflow`，未标明旧输入兼容。Project [职责声明](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project/SKILL.md:19) 将内部 grammar 交给 owner；Meeting [task work](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/project/haipipe-project-meeting/SKILL.md:54) 正确使用 `new Run or rerun`。两份当前 SKILL.md 均无 Phase 工作单元。

**影响：**活动词表继续宣传被替换的概念名，但不能据此断言还有 Phase schema。反过来，把 digest 的内部步骤或 audit 的普通“Run this command”改成独立 Run，会扩大本家族的责任并破坏用户要求。

**拟修复：**活动示例和路由词表使用 Run/Workflow；如需识别历史反馈中的旧词，将其限制为明确标记的输入兼容。Project 侧可链接共享定义；如果出现定义，就精确写 “A Workflow is a list of Runs.”。Run Spec、Run Instance、依赖关系与 Routes 由 Workflow/Run owner 解释，Project 不复制一套 schema。

**验收：**两技能及当前支持材料不再把 Phase 作为当前 workflow 单位；人机每轮反馈、命令调用、内部 Step 不另建 Run；历史 changelog 与明确兼容字段经人工分类后保留；自然语言询问工作流时能得到 Runs 列表及必要的关系说明。

## Workflow/Run 指标与共享问题

用户要求 **“A Workflow is a list of Runs”** 是本计划的验收条件。它不要求把所有技能包装成 Workflow，也不要求删除 Runs 之间的依赖、分支或重试关系。概念介绍先给出 Runs 列表，再由 owner 解释关系，能同时满足可读性和执行需求。

| 范围 | 当前判定 | 拟达到状态 |
|---|---|---|
| Project 主技能的 Workflow 定义 | **N/A**：明确不拥有内部 Workflow/Run grammar。正确使用 Run 引用。 | 保持职责边界；必要时给一句定义并链接共享权威。 |
| Project live procedures 的单位术语 | **Partial**：feedback 中有未标为兼容的 `phases`。没有 Phase 执行对象证据。 | 当前术语为 Run；兼容输入不作为新的单位展示。 |
| Meeting | **N/A（Workflow 定义）／引用用语通过**：后续任务使用 Run/rerun。 | F06 修正下游写作路由；会议记录与每条决定不自动成为一个 Run。 |
| 历史 changelog | 历史材料，不记作当前单位违反。 | 保留准确历史，不做全局替换。 |

跨家族协调项如下；本轮不修改这些文件，也不重复派发已修复的问题。

| 责任方 | 当前证据 | 协调内容与不确定性 |
|---|---|---|
| Project + Meeting | F01，两种路径及 allowlist。 | 一次性同步根目录规范、文档与检查器；优先采用 owner 根下 meetings。 |
| 共享文档维护者 + Insight/Design | [STRUCTURE:148](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/STRUCTURE.md:148) 仍列 Application bucket；[Insight:40](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md:40) 已明确同级家族。 | 更新共享目录/家族表，保留必要的历史存储目录。Insight 旧物理路径问题已关闭，仅做回归核对。 |
| Page owner | [Content 请求分流](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-content/SKILL.md:38) 与 Meeting 的 content change 路由不一致。 | F06 以当前 Page 路由为准，不改写 Page 发布语义。该接收文件第 11、87 行仍有 live `phase` 用词，交 Page 家族统一清理。 |
| Workflow/Run owner | [Workflow 定义](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-workflow/SKILL.md:4) 当前从 Run Specs graph 开始；第 22 行给 definition/graph，第 25 行已有 Run 列表示意；[第 51 行](/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-workflow/SKILL.md:51) 允许低层 `phase` progress metadata。 | 将人可见定义改为用户要求的 Runs 列表，明确 graph 表达 Runs 的关系。API 字段是否不可移除，本次未验证；保留时必须注明兼容范围，避免在 UI 中回到 Phase 单位。不能凭 graph 存在就删除依赖关系。 |
| 各反馈 owner | F07 路由存在跨目录目标。 | 共用目标解析范围；只列已确认 owner，不建立一个新的 Application 层。 |

## 实施顺序与依赖

以下是后续实施计划。表中的“验收”均指修复后的检查，本轮尚未执行。

| 顺序 | 工作包 | 主要产物 | 依赖与完成条件 |
|---|---|---|---|
| 1 | 锁定共用目录与路由契约：F01、F02、F04 | Project root/path 规则、owner 表、实际扫描范围定义。 | 先采用本报告建议默认值；明确 state、非前缀 ID 与 sibling roots 规则后，才能改批量枚举。先确认当前并行改动，按最新文件合并。 |
| 2 | 修正根审计与文档：F01、F02 | `audit_projects.py` 与 root README/reference 同步修改。 | 依赖顺序 1；隔离样例覆盖 meetings、legacy、允许 ID、多个 roots、零发现。满足标准后再让其它流程依赖其结果。 |
| 3 | 完善开始/恢复与 repo 接管：F03、F09 | 入口、README、new/repo/update procedures。 | 依赖 root 规则；保留 lazy worlds、profile/git_mode 分离和安全 update。CREATE/ADOPT 与中断恢复各有明确返回。 |
| 4 | 完善会议保存、继续与交接：F05、F06 | Meeting intake、唯一地址、provenance、resume 和路由表。 | 依赖 F01 的规范目录；使用当前 Page/Task owner 的 gate 与写作接口。不能凭会议摘要推断人的接受或执行授权。 |
| 5 | 修复反馈与 digest：F07、F08、F10 | 共用 inbox 目标解析、完整 list 范围、宿主适配说明、来源定位、当前 Run 词表。 | 依赖 F04 owner 表；先保证 capture/list/move 共用范围，再验证 digest 批量写入，避免摘要成功却查不到反馈。 |
| 6 | 共享文档同步与整体验收 | 按各 owner 边界提交共享措辞修订；更新相关技能 changelog。 | 不覆盖已存在的 Insight/Page/STRUCTURE 修改。Workflow 定义与兼容字段交其 owner；本家族无需等一场全仓库重构才解决 F01/F07。 |

建议保留的规则：Project 只拥有 root；README/YAML 为最小起点；world 首次使用才创建；普通 update 不搬 submodule、Result 或代码树；审计结论不延伸到子世界内部；会议源只保留一份；反馈合并保留原话；digest 写入仍有现行确认与 dry-run 边界。

## 验收场景与交付标准

| 场景 | 可观察的合格结果 | 关联 |
|---|---|---|
| 新建 research / software / hybrid 项目，含已给出的 ID、mission | 资料充分就直接继续；只生成所需根文件；首个内容按用户请求交给 owner；软件根代码规则正确。 | F02、F03 |
| 单项目首场会议；已有 diagram/Page-local 历史会议 | 新源落在唯一规范路径且 Project audit 接受；历史记录不被普通更新搬移。 | F01 |
| 批量 audit 包含 Proj、Project、非前缀 manifest、缺 manifest 旧候选、paused/archived、_backup、错误 root | 与已公布的发现和 state 规则一致；报告扫描范围、数量、跳过原因；不把零项目说成全部通过。 | F02 |
| Adopt 已有 README、.gitignore、manifest 的仓库；模拟 push 中断后继续 | 保存现有内容与无关修改；只补必要合同；准确报告最后成功动作并恢复下一步。 | F09 |
| 同分钟两场会议、旧会议补录、源已保存但只路由一半时重试 | 地址不冲突；日期语义可读；原记录保留；已完成路由不重复，未完成项继续。 | F05 |
| SPACE 会议影响两个 submodule Projects | owner 正确，接收 Page 的来源能定位到 SPACE 中的同一源记录。 | F05 |
| 会议要求改一句、随后采用已接受稿、另有 Task 行动 | 分别进入 Writing Step、受 gate 约束的 Content、Task owner；不由一次摘要隐式授权全部执行。 | F06、F10 |
| 向 Project、Meeting、Task、Workflow 投递工具反馈，随后 list/filter/move，再重复相同主题 | 写入与列表范围一致；显示正确 owner；同主题合并、fixed 回归重开均保持原话。 | F07 |
| 当前/过去/同名多个 session 的 digest，以及 dry-run | 来源可回查；歧义时让人选择；确认前不归档；dry-run 无写入；不支持的宿主给出明确替代输入方式。 | F08 |
| 用普通语言询问“项目下一步、工作流、Insight、Design” | 回答能展示 Workflow 的 Runs 列表、准确 owner 与下一动作；当前概念和图中无 Phase 单位或 Application 父家族。 | F03、F04、F10 |

实现时先用小型临时 fixture 验证审计器和文件路由；需要远端动作的 procedure 用替身说明 CREATE/ADOPT/失败恢复，不使用真实项目作为试验品。文档和技能改完后，依照 [根 README 的 fresh-context 要求](/Users/jluo41/Desktop/Tools-SPACE/README.md:133)，由 fresh-context subagent 在隔离的真实感任务中确认技能选择、文件加载、交接与输出。这一步属于未来修复的验收，不能把本轮桌面复核宣称为已通过的执行验证。

完成标准是上述有条件行为可重现、每个仍保留的兼容词都有明确用途、shared owner 与当前路径一致，并能向新人说明“现在保存了什么、哪些修改已应用、还有哪一项需要继续”。未决定的扫描 state、会议碰撞命名和跨仓库来源基准，应在对应工作包开始时定成一条规范并体现在验收样例里，不能由不同 procedure 各自猜测。
