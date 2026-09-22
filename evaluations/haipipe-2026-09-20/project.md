# Project 家族评估报告

评估日期：2026-09-20  
基线提交：`f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217`  
范围：`plugins/haipipe-toolkit/skills/project/`

## 快照与范围

- 初始 `git status --short` 显示 8 个外部 reference 子模块有修改（`cite-guard`、`grant-writer-skills`、`paper-rag-skill`、`paperspine`、`reprorun`、`research-agent-skills`、`research-co-pilot`、`scipilot-figure-skill`），并有未跟踪的 `evaluations/`；其中当时已有 `BRIEF.md`、`inventory.json`、`sessions.json`。这些改动不在本报告技能范围内。
- 复核前重新检查，Project 技能目录无工作树差异。本报告是本 session 唯一写入；未编辑技能、代码或其他 session 报告。
- 完整阅读范围内两份当前 `SKILL.md` 和其当前操作说明。仅静态阅读审计脚本；没有执行被评估的技能、脚本、外部服务或测试。下文所有用户流程都是桌面演练，不是实际运行或用户测试。

## 覆盖清单

初始清单列出 2 个技能；磁盘上恰有这 2 份当前 `SKILL.md`，未发现遗漏的第三个 Project/meeting 技能。

| 当前技能 | 覆盖情况 | 相关支持材料与边界 |
|---|---|---|
| `project/haipipe-project/SKILL.md` | 全文 | `README.md`、`ref/project-structure.md`、`ref/code-structure.md`、`fn/project.md`、`fn/repo-project.md`、`fn/audit.md`、`fn/update.md`、`fn/feedback.md`、`fn/digest.md`、`feedback/README.md` 均全文阅读；`scripts/audit_projects.py` 静态全文阅读，未执行。 |
| `project/haipipe-project-meeting/SKILL.md` | 全文 | `CHANGELOG.md` 全文阅读并按历史材料处理。检查了它指向的 Page Outline/Content 路由相关材料及 Board Meeting 退役提示；这些属于外部 owner，仅用于核对交接目标，不计入 Project 家族技能数。 |
| 家族及技能变更记录 | 历史背景 | `project/CHANGELOG.md`、`haipipe-project/CHANGELOG.md` 查看相关条目；不把历史措辞当作当前操作规则。旧档案、历史 session、其它家族的全量技能和运行时 UI 未纳入本次完整审查。 |

当前 Project 目录的支持材料已全部纳入上表。跨家族核对仅限于判断当前 owner 路径和 Workflow/Run 定义；`haipipe-insight`、`haipipe-design`、`haipipe-workflow` 不是本报告的完整审查对象。

## 总体判断

Project 根目录契约的核心取舍值得保留：先创建短小的 `README.md` 与 `project.yaml`，空 world 按需创建；`profile` 与 `git_mode` 分开声明；普通 update 不搬动子世界、子模块和生成物，而是记录迁移债务。对应证据在 `haipipe-project/SKILL.md:37-51,95-109`、`ref/project-structure.md:70-74,97-120` 和 `fn/update.md:11-36`。创建时只问缺失值、默认研究型项目的规则也清楚（`fn/project.md:13-15`）。

Meeting 的核心分界同样清楚：会议是 Page 之上的共享源记录；决定和问题路由到受影响 Page 的 Outline 或 Task，不把整份 transcript 复制到 Page（`haipipe-project-meeting/SKILL.md:16-20,45-59`）。它保存来源路径、保留旧 Page-local 记录只读，方向合理。

最大的实质问题是会议目录位置互相冲突，并且按会议技能写到项目根目录会被 Project 审计脚本判为违规。其次，`audit --all` 的项目发现规则会静默漏掉 `Project-*` 目录；README、skill 描述和 setup/audit procedures 对支持哪些 Project root 也不一致。其余主要问题是新手命令没有展示必需 mission 参数、会议输入与时间语义没有说透，以及 `applications/` 目录与 Insight/Design owner 的表述还未处处直连。

## 优先问题

### P1 · 会议目录契约冲突，且项目根审计会拒绝会议技能创建的目录

会议技能规定单项目会议写到 `<project>/meetings/<YYMMDD-HHMM>/`，SPACE 级会议写到 `<SPACE>/meetings/...`（`haipipe-project-meeting/SKILL.md:24-31,35-43`）。项目结构参考则把 `meetings/` 明确画在 `diagram/meetings/`（`haipipe-project/ref/project-structure.md:134-146`），项目入口也把会议放在 `diagram/` 描述里（`haipipe-project/SKILL.md:29-34`）。两者都在当前材料里，没有说明哪个只是旧布局。

这不只是文档画法不同。审计脚本的根目录 allowlist 只有 `tasks`、`discoveries`、`diagram`、`papers`、`applications`、`external`（`haipipe-project/scripts/audit_projects.py:16-24`）；根目录中不在 allowlist 且未声明为迁移债务的目录会成为错误（同文件 `:150-160`）。因此，照会议技能创建 `<project>/meetings/` 后，现有 `audit` 静态逻辑会把它报告为 `undeclared noncanonical root`。脚本没有在本评估中运行；这是根据代码分支的静态判断。Board 服务的退役提示也指向 project/SPACE 级会议（`servers/_host/serve.py:600-608`），支持会议 owner 在 Project/SPACE 层，但不能解决它究竟在 Project 根还是 `diagram/` 下。

**建议：**选定唯一规范路径后，同步 Project 树图、项目入口、meeting skill 输出字段和审计 allowlist。现有 Project/SPACE 路由材料多数写的是 owner 根下 `meetings/`，因此较一致的选择是承认 `meetings/` 为可选根级目录；若决定留在 `diagram/meetings/`，则应改 meeting skill 的路径和返回值，不能保留两套写法。

### P2 · `audit --all` 会漏掉受支持的 `Project-*` 名称

项目结构参考明确说不要根据 `Proj...` 和 `Project-...` 的名称拼写决定 Project 属性（`haipipe-project/ref/project-structure.md:119-120`）。但脚本的 `--all` 发现规则只使用 `root.glob("Proj*")`（`scripts/audit_projects.py:182-190`）。创建命令接收任意 `<id>`，没有强制 `Proj` 前缀（`fn/project.md:7-15`、`fn/repo-project.md:8-15`）。

**影响：**若合法 Project 目录叫 `Project-...`，单项目审计可传路径检查它，批量审计却不枚举它。用户看到“所有项目”的结果可能误以为已覆盖完整。

**建议：**让批量审计按 `examples/` 下的 Project manifest/明确结构发现项目，不以名称前缀作为唯一条件；或者在创建契约中正式限制 ID 前缀，并删除“不要根据 Proj/Project 拼写路由”的现行文字。前者更符合现有契约。

### P2 · 描述、README、setup 与 audit 对 sibling world 支持范围说法不一

Project 技能 frontmatter 声称支持 `examples/` 及 `examples-nlp/` 一类 sibling domain world（`haipipe-project/SKILL.md:3-9`），但 README 把范围说成 `examples/`（`haipipe-project/README.md:3`），`new` 与 `repo` procedure 将创建路径固定为 `examples/<id>`（`fn/project.md:20-21,26-30`；`fn/repo-project.md:26,31-35`），`audit.md` 也称 `--all` 检查 examples 下项目并示例只传一个 examples root（`fn/audit.md:3-15`）。审计脚本的 `--all` 默认 root 却同时是 `examples` 和 `examples-nlp`，而且允许通过可重复的 `--root` 传其它路径（`scripts/audit_projects.py:182-190,220-227`）。

**影响：**新手无法判断 sibling world 是只可审计、也可创建，还是仅在某些命令下支持；不同 agent 可能在不同根目录执行同一个 `new` 请求。

**建议：**按 verb 明确列路径参数和默认值：例如 `new`/`repo` 限定 `examples/`，而 `audit --all` 可扫多个 sibling roots；或者为创建命令增加明确的 root 参数。README、frontmatter 和 procedure 采用同一说明。

### P2 · 创建入口没有展示 mission 参数，尽管它是必需字段

入口列出的命令是 `/haipipe-project new <id> [--profile ...] [--git-mode workspace]`（`haipipe-project/SKILL.md:53-58`）；README 也只列 `<id>` 和 profile（`haipipe-project/README.md:5-12`）。实际创建 procedure 支持 `--mission`，并在缺少 id 或 mission 时询问（`fn/project.md:7-15`）；而审计器将非空 `mission` 作为必需项（`scripts/audit_projects.py:136-139`）。

**影响：**入口看不出使命句从哪里传入；如果 agent 只按入口签名 scaffold，随后审计会失败，或者用户得等创建后才知道还要补 mission。`profile` 默认 research 的适用条件只在 procedure 里说明，也不是入口可见信息。

**建议：**在入口命令和 README 写出 mission 方式、必填性与默认值条件；保留“只询问缺失值”的好行为。

### P2 · “Application”仍像一个独立 owner，削弱了 Insight/Design 双家族映射

Project 参考的 owner 表是正确的：`applications/` 目录由 `haipipe-insight` 和 `haipipe-design` 负责（`ref/project-structure.md:84-95,167-176`），主技能 owner map 也分别写了两个技能（`haipipe-project/SKILL.md:79-93`）。这与“Insight、Design 是独立一等家族、没有 Application 父家族”的要求一致；没有证据表明 Project 技能当前真的路由到一个 `haipipe-application` 技能。

但相关 onboarding/反馈文案仍把 `Application` 单独列作内部 grammar 或首个内容类型（`haipipe-project/SKILL.md:19-21`；`fn/repo-project.md:45-47`），反馈映射写成 `Paper/Application/Board/Page internals -> their owning skill`（`fn/feedback.md:101-114`），没有像目录 owner 表那样把 Application 语境具体分到 Insight 或 Design。新手或 agent 可能把 `applications/` 理解为有一个上层 Application skill，再猜选哪个子技能。

**建议：**保留 `applications/` 作为存储目录名称（若这是现有布局要求），但在首次出现时定义它只是目录，实际 owner 是 Insight 和 Design；把“首个 Application”改成“首个 Insight 或 Design artifact”，反馈路由也按这两个 owner 写清楚。另一个跨家族 stale pointer 见“跨家族问题”。

### P2 · Meeting intake 的工作区与日期语义不够明确

Meeting skill 让 agent 选 `<SPACE>/meetings/`，但本技能没有定义如何从当前 Project 推得 `<SPACE>` 的具体路径（`haipipe-project-meeting/SKILL.md:22-31`）。文件名是 `YYMMDD-HHMM`，同时说明由 server/executing agent 写入时间且“不信任 client clock”（同文件 `:29-31`），却没有说日期代表会议实际发生时间还是记录创建时间。对补录旧会议尤其不清楚。

此外，procedure 说明 digest 应包含 decisions、open questions、reading path，但没有说明接受的输入形式或当归属无法判断时何时先问人（同文件 `:33-43,45-72`）。`unrouted` 返回项会列出需要 owner decision 的条目，这是好的兜底，但“settled decision”还是“open question”等关键分类可能影响 Outline/Task 写入。

**建议：**明确定义 `<SPACE>` 为包含 Project roots 的 workspace 根，或给出解析规则；把目录时间定义成可信的“记录创建时间”，会议发生时间另记在 digest；说明可接收笔记/transcript，并在 owner、决定状态或目标 Page 无法可靠识别时先列出待确认分类再写入受影响 Page。

### P2 · 当前反馈路由仍把 `phases` 作为活动关键词；Project 侧没有可见的 Workflow/Run 定义

两份范围内的 `SKILL.md` 没有把 Phase 当作当前工作单元。Project 技能还明确把 Task/Discovery/Page/Run 的内部 grammar 留给 owner（`haipipe-project/SKILL.md:19-21`），同时 owner map 将 Task 映射到 BJTR 并指出 `Run = identity`（同文件 `:79-93`）。Meeting 的任务交接也准确写作 `new Run or rerun`（`haipipe-project-meeting/SKILL.md:45-59`）。

唯一仍在 live procedure 中的词是反馈关键词 `workflow, IPO, phases, plan workflow -> haipipe-workflow`（`fn/feedback.md:101-114`）。它是路由关键词，不是在定义 workflow 阶段；因此属于术语/兼容清理，不是发现了一个新的 Phase 数据结构。`fn/project.md:45` 的 `Run:` 和 digest 的 `## Run:` 是普通“运行命令”的祈使用法，不应被改造成独立 Workflow Run。

**建议：**活动关键词用 `Workflow, Run Spec, Run Type, routes, IPO workflow`；如需接收旧用户措辞，让 agent 依据反馈语义映射，而不在当前分类表主动展示 `phases`。Project 根目录只需一句精简定义或权威链接：Workflow 是 Runs 的列表；运行细节继续交给 Task/Run owner，不把每个审计脚本调用、反馈回合或内部 Step 另算 Run。

## Workflow/Run 指标

| 技能 | 结论 | 证据与解释 |
|---|---|---|
| `haipipe-project` | **Partial** | 没有 Phase-based unit，且明确不重述子世界语法；Task 下写 `Run = identity`。不足是没有给 Project 新手“Workflow 是 Runs 列表”的简明锚点，活动反馈映射仍有 `phases` 关键词。入口的 `Run:` 脚本标题是祈使动词，不是运行单元。 |
| `haipipe-project-meeting` | **N/A（不拥有 Workflow）** | 不定义 workflow；把任务后续写成 `new Run or rerun`，没有额外 Run 身份或 Phase 术语。会议记录与下游 Task Run 是不同对象。 |

范围内没有发现把每个 Step、反馈回合或工具调用提升成 Run 的现行规则。历史 changelog 中出现 `phase 2/3` 是旧项目演进叙述（例如 `haipipe-project/CHANGELOG.md:24-34`），应按历史记录看待。低层 API 是否保留兼容字段属于 Workflow owner 的决定，不能据此把 Project/Meeting 的普通命令执行称为 Run。

## 代表性桌面演练

以下只按文档做桌面演练，没有真的调用任何技能或用户测试。

1. **新建项目并要求首个 Task。** `new` procedure 会在 ID/mission 缺失时只问缺失项，默认无根软件制品时 profile 为 research，且不创建空 world（`fn/project.md:13-41`）。这是易开始的路径；但入口没有显示 mission 参数和默认规则。更顺的开场可以是：

   > 可以。若这条请求里还没有项目代号和一句话使命，请补齐这两项；默认 `profile=research`、`git_mode=workspace`。我会先建 `README.md` 与 `project.yaml`，不空建目录。你已要求的首个 Task 随后交给 Task owner 建立。

2. **把现有组织仓库接成 Project。** `repo` 明确要求 `--org`、默认私有、远端存在时 Adopt、不覆盖已有本地目录；公共仓库要先确认，并会分别报告 Project 与 workspace pointer commit（`fn/repo-project.md:8-27,31-50,64-67`）。路径边界清楚。人需要先知道“要新建还是接管”，文档按远端存在自动选 Adopt/CREATE，适合保留；返回时也应继续展示两个 pointer 状态。

3. **记录影响两个 Projects 的会议并路由决定。** Meeting skill 会选 `<SPACE>/meetings/`，逐项路由 Page 问题、Page 决定、计划/内容修改或 Task work；但 Project reference 同时给出 `diagram/meetings/`，落盘后审计也会拒绝根级 `meetings/`。`D<nn>`、`WRITE cycle`、`Task Folder` 对新手不透明。

   更易懂的交互可以先说：

   > 我可以从笔记或 transcript 生成一份会议摘要，列出已决定事项和未解决问题。因为它影响多个项目，我会把源记录放在共享 workspace 的会议目录；确定归属的条目关联到对应 Page 或 Task。归属或状态不明确的条目会先列给你确认。

   最终目录路径需等 P1 冲突解决后再展示，不应让人选两套规范。

4. **恢复旧项目并做全量审计。** `audit` 是只读的，报告根字段并声明不验证 child internals；需要改变才走 `update`，并且不自动搬移 submodule/Result/代码树（`fn/audit.md:10-27`、`fn/update.md:11-36`）。这些边界明确，适合恢复使用。批量结果在脚本层有漏项风险，尤其 `Project-*` 不会被发现；审计界面也要明确扫描了哪些 roots 和发现数量，避免把不完整的“all”误读为全覆盖。

## 关键段落改写建议

以下是英文 source 的英文改写示例，保留当前含义并消除已识别歧义；仅供后续修订，不是本轮修改。

### 1. 把 Project 与会议文件夹树统一到根级 `meetings/`

**Before**（`project-structure.md:134-143`）：

```text
diagram/
├── project/       mission, boundary, architecture, durable decisions
├── boards/        project-level Task/Insights and other Board surfaces
└── meetings/      optional meeting records tied to this Project
```

**After（建议采用 meeting skill 的 Project/SPACE 根路径）**：

```text
<project>/
├── meetings/      optional project-level meeting records
└── diagram/
    ├── project/   mission, boundary, architecture, durable decisions
    └── boards/    project-level Task/Insights and other Board surfaces
```

同一修订应把 `meetings` 加到 Project 根 allowlist，并从 `diagram/meetings/` 描述中移除它。

### 2. 让新手在第一屏看到必需的 mission

**Before**（`haipipe-project/SKILL.md:55-58`）：

```text
/haipipe-project new <id> [--profile <profile>] [--git-mode workspace]
    Create README.md + project.yaml. Create no empty worlds. Read fn/project.md.
```

**After**：

```text
/haipipe-project new <id> --mission "<one-sentence purpose>" [--profile research|software|hybrid]
    git_mode defaults to workspace. If id or mission is missing, ask only for that value.
    Create README.md + project.yaml; create no empty worlds.
```

### 3. 直连 Insight 与 Design，不把 Application 写成技能 owner

**Before**（`fn/repo-project.md:45-47`）：

```text
The first Task, Discovery, Board, Paper, Application, or external dependency
creates its own world through the owning skill.
```

**After**：

```text
Create a world only when the first artifact is requested. Route Task, Discovery,
Board, and Paper work to their owning skills. For non-academic consumer work
under applications/, use haipipe-insight or haipipe-design; there is no parent
Application skill family.
```

### 4. 去掉活动反馈路由中的旧 Workflow 单位词

**Before**（`fn/feedback.md:104-110`）：

```text
workflow, IPO, phases, plan workflow -> haipipe-workflow
```

**After**：

```text
Workflow, Run Spec, Run Type, routes, IPO workflow -> haipipe-workflow
```

## 跨家族问题与协调项

- **Project/Meeting → 审计器（Project owner）**：根级会议路径在 `haipipe-project-meeting/SKILL.md:24-31`；Project 结构另画 `diagram/meetings/`（`haipipe-project/ref/project-structure.md:134-143`）；审计白名单和非规范目录错误位于 `scripts/audit_projects.py:16-24,150-160`。这是同一目录契约的重复分歧，应由 Project 家族一次性统一。
- **Project → Insight/Design（Project owner + Insight owner）**：Project 根表正确地将 `applications/` 分别指向 `haipipe-insight`、`haipipe-design`（`ref/project-structure.md:89-90,176`）。但当前 `skills/insight/haipipe-insight/SKILL.md:34-36` 称其物理位置在 `skills/application/`；文件实际路径是 `plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md`。这条过时路径会重新暗示 Application 是父家族，应由 Insight owner 修正。此处只作窄范围核对，没有完整审阅 Insight 家族。
- **Project → Workflow（Workflow owner）**：Project 把 Run grammar 留给 child owners；本次有限核对的 `skills/task/haipipe-workflow/SKILL.md:4-6,19-29` 当前定义 Workflow 为由 Run Specs 的 routes 编译出的 graph，并用 `Workflow Definition = Run Specs + graph`。同文件 `:51-53` 又注明低层 JavaScript API 可能保留 `phase` progress-group metadata，且只作 display label。前者需由 Workflow owner 按用户要求确认是否应表述为“Workflow 是 Runs 的列表”；后者是明确的 API 兼容/显示字段说明，不是 Project/Meeting 里的活跃执行单位。本次不是 Workflow 家族完整审查。

## 建议修订顺序

1. 先决定会议目录的唯一规范位置，并同步 Project root tree、meeting skill、audit allowlist；否则正常会议写入会导致项目不合规。
2. 修正 `audit --all` 的项目发现方式，并明确它扫描的 roots 与名称边界。
3. 对齐 `examples/` 与 sibling domain roots 在每个 verb 的支持范围。
4. 把 mission 与 Project 默认值放进第一屏，并用一句话解释用户可从 `new`、列表、`audit`、`update` 继续操作。
5. 明确 `applications/` 是存储目录，路由到独立的 Insight 或 Design family；通知 Insight owner 修正过时路径。
6. 删除或标记反馈路由中的旧 `phases` 关键词，并由 Workflow owner 决定 Runs-list 定义和低层兼容字段的表述。
7. 补齐 meeting intake 的 `<SPACE>`、记录时间、输入材料与模糊归属处理说明。
