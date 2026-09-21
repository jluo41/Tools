# HAI-Pipe Writing 家族评审

## 快照与范围

- 日期：2026-09-20。评审基线：提交 **f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217**。
- 按初始清单并对照当前磁盘，Writing 目录中有且只有 2 份现行 SKILL.md，二者均已通读全文；技能目录的其余现行说明和写作参考也已逐份核对。
- 本轮开始及结束时，Writing 目录在基线提交上没有本地差异。共享工作树的其他 references 子模块显示已改动，evaluations/ 下有并行评审文件；这些漂移不属于本报告写入范围。本轮没有创建分支或 worktree，也没有修改技能、代码、测试或其他会话报告。
- 本轮是文档评审，没有运行技能、脚本、测试或外部服务。为验证文档所述含义，只读检查了 humanizer 的 slop.py、Writing 的 wdiff.py、score.py，以及 anti_slop.py 的参数入口。

## 覆盖清单

| 范围 | 当前磁盘内容与覆盖 | 排除项或缺口 |
|---|---|---|
| 技能一 | plugins/haipipe-toolkit/skills/writing/haipipe-writing/SKILL.md（394 行），全文 | 无 |
| 技能一的配套说明 | writing/haipipe-writing/ref/ai-tells.md、anti-slop-adapter.md、anti-slop-attribution.md、anti-slop-rules.json、change-record.md、holes.md、plain-rules.md、realize-from-plan.md、weaving.md、writing-dna-adapter.md；9 份 Markdown 和 1 份 JSON 均已读 | 外部 Writing DNA、anti-slop 来源库不在本次内部文档评审范围 |
| 技能二 | plugins/haipipe-toolkit/skills/writing/haipipe-paper-revise-humanizer/SKILL.md（151 行），全文 | 无 |
| 技能二的配套说明 | writing/haipipe-paper-revise-humanizer/ref/pattern-catalog.md、before-after.md、venue-sciwrite.md 均已读；同时阅读其 CHANGELOG.md、cli/slop.py | pattern-catalog.md 是仓库内 vendored 的现行参考，已读；上游 academic-humanizer 子模块是技能标明的 provenance-only 来源，未读、未调用 |
| Writing 家族入口 | writing/README.md、writing/CHANGELOG.md 已检查；重点核对了版本头、迁移说明和当前集成声明 | CHANGELOG 是历史记录，不属于每次运行加载的指令；haipipe-writing 的旧历史条目未逐条做文案审校 |
| Page 写作交接 | page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md、structure-run.md、writing-step-template.md、interactive-execution-policy.md、post-run-analysis.md；page/haipipe-page/ref/user-check-packet.md，均已读全文 | 这些属于 Page 家族，仅因 Writing 明确依赖或交接给它们而作边界抽查，不代表完成 Page 家族评审 |
| Paper 边界抽查 | paper/README.md 和 haipipe-paper、haipipe-paper-workflow、haipipe-paper-venue 的相关契约；核实旧依赖是否存在 | 不是 Paper 家族全文评审；项目级 S/Venue Page 数据不在仓库，无法核验某个真实 Paper 项目的运行输入。工作树中找不到 prose-quality.md、haipipe-paper-revise hub、haipipe-paper-revise-content 或旧 S-page 文件 |
| 未读实现材料 | 未读 Writing CLI 中与本报告无关的 holes.py、agree.py 完整实现及 tests/ 两个测试文件 | 不影响所审文档的路径、界面、写作规则和 Run 边界判断；没有执行测试 |

## 总体判断

Writing 的通用修订边界较强：对局部修改先声明范围，冻结未触及的主张、顺序、引用和声音；不确定时选择更小改动，并把范围外问题作为建议。这些规则容易保护作者已完成的工作。Page 交互手册对 Run、Version、Step 的边界也写得具体：一个 Step 是一轮完整的限定工作，不是每次聊天或工具调用；多个段落不能因此自动扩成 Run。Structure Run 将 SHAPE、SURVEY 明确作为同一 Run 内的动作，是应保留的好例子。

主要问题集中在 humanizer：它仍依赖已删除的 S-page / revise 架构；科学意义保真门槛和强制改写规则彼此冲突；它给出的首个示例以“保留事实”为名加入了原文没有的数据和研究结果。Writing 的 Page 接口总体自然、范围清楚，但主技能和配套用户模板仍有 Phase 用法、记录要求矛盾和工具行为描述不准等可验证问题。

## 按影响排序的发现

### W1 · P1 · Humanizer 仍指向已退休的 S-page / revise 宿主

**证据：** humanizer SKILL.md:68-70 要求读 S-Venue-0-venue.md 和 ../../paper/haipipe-paper/ref/prose-quality.md；:87-90 又要求读 owning S page 的 Stage Contract、style-from 合约和 pinned venue page；:96 要求由 haipipe-paper-revise 选择 candidate-diff mode。当前 paper/README.md:3-7、:134-136 明确说明编号 S-stage runtime 已退休、删除，新工作不得引用旧 S-page。仓库中也不存在上述 prose-quality 文件、revise hub、revise-content worker 或 S-page。当前 Paper 的入口改为 Story、Section、Round 等 Page Type；haipipe-paper/SKILL.md:28-40 给出了目前 Page 路由。

**影响：** 从新上下文开始执行时，agent 无法读取必需的合同、场馆和模式设置。若它自行把项目文件猜成旧 S page，四道改写门槛会失去权威来源；若它停下，则连普通 humanizer 请求也无法依技能完成。现行文件把这写成必做步骤，并非可选的历史兼容路径。

**建议：** 由 Paper/Page 所有者把输入改接到当前 Page 的 Story Section row、当前 venue contract 和 Page Run Ticket，并在 Ticket 或 Page 明确记录权威文件路径。若其中任一缺失，停止语言编辑并报告具体缺项。不要只把旧路径换成新名称，也不要默认当前 Paper 已有完全等价的 revise worker 或 candidate-diff 开关。

**英文改写示例：**

Before: “Note venue from S-Venue-0-venue.md. Read ../../paper/haipipe-paper/ref/prose-quality.md.”

After: “Read the current Section Page’s approved Story row and its pinned Venue contract from the paths named in the Page Run Ticket. If either contract is missing or retired, stop before editing and report the missing input. Do not infer a replacement policy.”

这段仍需 Paper/Page 所有者确认最终字段和路径后才能落地。

### W2 · P1 · 科学意义门槛与“删减 / 弱化”规则相互冲突

**证据：** venue-sciwrite.md:16-18 要求不得增删主张、改变限定语或引用；:34 说数值和引用完整性由 CHECK 负责且不得改写；:38 要保留 evidence-tied hedging 和精确术语。相反，pattern-catalog.md:102-106 要求把引用压到“一两个最重要的来源”；:108-111 要量化或删去 somewhat、relatively 等表达；:150-160 允许补证据指针、弱化主张并给出新范围。humanizer SKILL.md:89-94 也将意义不变作为所有编辑的硬门槛。

**影响：** 同一段落可能被同时要求“保留每个引用/限定语”和“删引用/弱化语句”。直接修改会改变原文论点或证据链；默认自动应用时，作者可能只看到修改后的版本，直到 CHECK 才发现主张边界已变化。

**建议：** 设定明确优先级：当前 Page/venue 合同和意义保真优先于通用去 AI 规则。Humanizer 不新增证据、不删 citation key、不改 claim strength、不替作者量化。它可改引述句型、指出堆叠引用或不清楚的限定语，并把需要内容或证据决策的句子交还相应 owner。

**英文改写示例：**

Before: “Unbacked claim → add the evidence pointer or soften.”

After: “If a claim lacks visible support, do not add evidence or weaken the claim. Mark the span and return it to the claim or evidence owner. Continue only when the source or approved wording is supplied.”

Before: “Cite the one or two works that matter and say why, not a bracketed list.”

After: “Clarify why each cited work matters while preserving every existing citation key. Do not remove citations during humanization. If the relevance of a citation cluster cannot be judged from the supplied text, flag it for the author.”

### W3 · P1 · 学术改写示例加入了原文没有的研究事实

**证据：** before-after.md:5-18 把一个泛化的图表示学习句子改成了包含 noise-aware reweighting、three citation benchmarks、minority-class F1 改善 3–6 points 和 majority-class accuracy 在 1 point 内等信息的段落。Before 并未给出这些方法、数据集、指标或结果；说明文字却称“kept the precise factual claims”。这与同一技能的意义不变、不可编造数字/引用规则相反。NIH 示例明确称为 constructed example，并在 :53-54 警告不能编造 PI 数据；首个学术示例没有相同提示。

**影响：** 这个示例是每次审计都要读取的 live 参考，比抽象规则更容易被模仿。Agent 可能学到可以把空泛主张“补具体”，即使输入没有支持数据。

**建议：** 将首例标成 synthetic, unrelated examples used only to show edit shapes，明确 Before 和 After 不是同一研究、After 的数字是假设占位；或改成同一主张的语义保真最小改写。缺乏材料时把具体证据写成待补输入，不能直接填进输出。保留已有明确的“examples are move shapes”说明，并让每个示例自身都能体现这一点。

**英文改写示例：**

Before: “We demonstrate through extensive experiments that our method outperforms existing approaches.”

After: “We evaluate the method against existing approaches. If the supplied Results support a comparative claim, name the reported metric, comparator, and evidence pointer; otherwise, leave the claim unresolved for the author.”

这保留示例的教学意图，不伪造数据或引用。

### W4 · P1 · Paper-host diff 的 CHECK 不会检查 Paper-host Note

**证据：** humanizer SKILL.md:98 说 wdiff.py 使用 --host paper 生成 Note 并由 check 审核；writing/ref/change-record.md:91-100 规定 Paper 格式是 > Note: ~~removed~~ **inserted**。但 writing/cli/wdiff.py:152-168 的 check 只遍历以 > ✎ 开头的行（:157），因此不会验证任何 > Note 行；空 Paper 文件也会返回零条记录问题。工具接口 :180 还把 --who 默认设为 CC，而 venue-sciwrite.md:46 要求 candidate Note 使用已核实的 model label，humanizer 的示例命令没有传 --who。

**影响：** Agent 会以为候选 diff 已通过检查，作者可能看到格式坏掉或署名错误的 Note。此处尤其影响 explicit candidate-diff 模式下的人类复核。

**建议：** 工具支持 Paper host 的 Note 校验后再声称它检查了此格式；否则文档应明确 check 只验证 board 的 ✎ 记录，不验证 Paper Note。候选命令要显式传入 Ticket/宿主确认的 model label 和约定日期。不要依赖默认 CC。

**英文改写示例：**

Before: “...returns the word-level marks already in this host’s notation, and check audits them.”

After: “Emit the Paper-host candidate with the verified author/model label. Validate it with a Paper-aware Note checker. Until that checker is available, report that the Note was generated but not mechanically checked.”

### W5 · P1 · 当前 Phase 用语和跨家族所有权未对齐

**证据：** humanizer SKILL.md:133-140 仍把现行图标题写成 “REVISE phase”，并称 revise-content、humanizer、results 是其中的 workers。Writing SKILL.md:189 和 ref/realize-from-plan.md:142-145 仍把当前路由写成 “owning phase”。ref/holes.md:52、:90 还有 “paper phase” 与 “EVIDENCE phase”。这些是当前引用中的路由语言，不是都能按历史文本处理。另一方面，Page 交互合同已明确一个 Run 可容纳多个 Step/Version 和许多内部调用：interactive-writing-run.md:16-20、:87-89；structure-run.md:20-29 也把 SHAPE/SURVEY/CLOSE 定为同一 Run 内的 Step/cycle。user-check-packet.md:214 的现行用户响应模板仍要求 “no Content yet · phase <PHASE>”。:5、:25 的 “phase receipt” 是否指旧持久记录尚未定义清楚。

**影响：** 读者分不清 Phase 是旧 workflow unit、Paper/Page 的某个功能位置，还是一条 Run 内部工作；旧 revise 图又把一个已删除的 S-stage 链伪装成当前编排。面向人的 Page 状态模板会继续输出 Phase。若机械地将每个 Phase、工具或人工回复替换成 Run，则又会破坏已正确写明的 Step / Run 边界。

**建议：** Humanizer 先重新接入当前宿主，再由宿主确认哪些被单独委托的工作是一个 Run、哪些只是某个 Run 内部的 Step。将当前路由用词改为 owner/contract 名，并在需要时“恢复现有 Run 或请 host 委托一个 Run”；保留 OUTLINE、EVIDENCE 等权威名称。Page 模板显示已核实的当前 Run/id/status，或者明确 “none commissioned”，不得为了填模板新建 Run。旧 changelog 的 “phase spine” 与迁移注释中的 paper/2-phase/0-draft 是历史来源，可保留为史料。

**英文改写示例：**

Before: “If the problem is the plan, evidence, or promise, route back to the owning phase instead of repairing it in prose.”

After: “If the problem belongs to the plan, evidence, or promise, return it to that owner. Resume its active Run, or ask the host to commission a Run when new work is needed.”

Before: “REVISE phase: revise-content → humanizer → results.”

After: “The owning Paper/Page Workflow lists the Runs in the required order. This humanizer runs only when a current Run commissions its venue-specific language pass. Reading, auditing, editing, and checking are internal Steps; the host defines the Run’s scope, order, and acceptance.”

The second rewrite is illustrative only; W1 must be resolved before this skill can be assigned a current Paper Run.

Page 用户状态示例：

Before: “no Content yet · phase <PHASE>”

After: “No Page Content yet · current Run: <verified Run id and status, or ‘none commissioned’>”

### W6 · P1 · 当前共享结构仍把 Application 写成 Insight / Design 的 join

**证据：** 本轮约束要求 Insight 和 Design 是独立一等 family、没有 Application parent。当前 skills/STRUCTURE.md:144-149 却将 insight、design 列为两行，随后将 application 定义为 “the Insight/Design join and its delivery channels”。writing/README.md:14-16 也把 application 当成一类负责 reports 的家族，haipipe-toolkit/README.md:14 仍在总览图中写 Paper / Application。

**影响：** Writing 桶向读者传播的所属关系与本轮要求相冲突。其他技能可能继续把独立的 Insight 或 Design 工作路由进 Application 父层。

**建议：** 由 Structure/应用家族的所有者修正共享分类与 Paper/Application 图；Writing README 只描述 Writing 自己的 prose ownership，不再用 Application 作为跨家族分类参照。此为跨家族协调项，本报告没有修改相关文件。

## 次级发现

### W7 · P2 · 句子拆分说明互相矛盾

humanizer SKILL.md:115 要求 30 词以上的复合句 “compress, don’t split”；pattern-catalog.md:119-122 则说 “Split them”。venue-sciwrite.md:30 只允许在句子仍然表达一个完整意思时修 clause stack。Agent 无法知道是压缩、拆分，还是交由作者。应以意义和句子功能为条件，并统一三个文件的规则。

**英文统一示例：**

Before: “Sentences over ~30 words with 3+ subordinate clauses (compress, don’t split).”

After: “Shorten a clause-stacked sentence when it expresses one complete idea. Split it only when it contains distinct claims, preserving every claim, qualifier, and citation.”

### W8 · P2 · six-layer audit 与可执行的 slop.py 能力不一致

humanizer CHANGELOG.md:2 称六层审计 “becomes CODE”。但 cli/slop.py:31-84、:143-164 是对节奏、词形和部分 pattern 的统计，不会检查 venue contract、claim-evidence fit 或资助模式；SKILL.md:72-80 也未说明何时调用它，或它不能替代逐句审阅。代码 docstring :4 还列出 --control 参数，实际解析器 :167-172 没有该选项。

**影响：** “six-layer audit”容易被理解成工具已覆盖全部六层，实际语义判断仍靠 agent。复制 docstring 的调用还会失败。

**建议：** 把 slop.py 明确写成可选节奏/模式筛查器，补可复制的当前用法，删去不存在的 --control；声明结果是工作列表，不是科学意义、AI 来源或接受判断。

### W9 · P2 · Writing 对标题评分工具的描述会漏检标题

haipipe-writing/SKILL.md:255-257 说 score.py 会在读者看到前标出标题。实际 cli/score.py:72、:96-100 默认排除标题，只有 --headings 才处理标题；它也只将达到分数门槛的标题列入 worklist。新上下文 agent 照文档默认调用会漏过标题检查。

**英文改写示例：**

Before: “score.py flags a heading before anyone reads it.”

After: “Run score.py FILE --headings to add selected headings to the review worklist. A score is a prompt for human review, not a judgment that the heading is unclear.”

### W10 · P2 · 无文字变化的 Page Step 有相互冲突的记录要求

haipipe-writing/SKILL.md:76-79 先说 Step 的 before/after 和原因 “are always required”；:86-88 又说没有文本变化时不要返回 Before/After 或 preference card。Page writing-step-template.md:113-124 也规定只有 material wording change 才建立 Track Changes card。

**影响：** Agent 可能为 acceptance/no-op Step 捏造 Before/After，或因为不改文案而违反 “always required”。

**英文改写示例：**

Before: “The Step’s before/after text and reasons are always required.”

After: “For each prose-changing Step, save clean Before/After text and the local reason. For a Step with no prose change, record the disposition and reason without a Before/After card.”

### W11 · P2 · Writing README 的集成状态和节编号已过时

writing/README.md:27-29 说 humanizer “should become a consumer” of wdiff “rather than grow a second copy”；“until then” 两种 dialect 才写在 change-record.md §3。现行 humanizer SKILL.md:98 和 haipipe-writing/SKILL.md:391 已说它调用 wdiff.py；change-record.md 的 Paper/Board 格式映射在 §4，§3 是 placement。

**建议改为：**

After: “Both writing hosts use cli/wdiff.py for word-level diffs. The shared change-record reference documents the Board and Paper output dialects in §4.”

### W12 · P2 · 直接应用的反馈没有清楚的作者复核 / 撤回说明

humanizer SKILL.md:64-83 规定默认直接应用、不给用户预先批准，并把注释放给 CHECK；:83 又说作者可加 “> USER:” 以 restart。前者是 LaTeX 内联注释，后者看起来像 Board lane，但没有说明在哪个文件添加、restart 由谁执行、已应用的改动怎样拒绝或撤销。另，主技能 :72-80 要求 AUDIT + APPLY “in one pass”，但必读的 pattern-catalog.md:29-39 规定先单独列出 audit findings（do not edit yet），随后 Rewrite、Report；:247-249 又要求返回清理后全文和摘要。候选模式则依赖 W1 所述的已不存在 hub。

**影响：** 默认自动修改可以是明确的产品选择，但作者的下一步不够清楚。CHECK、接受修改和退回某一处修改容易混在一起。

**建议：** 统一审计与编辑的顺序，说明 audit list 是否要展示给用户，或仅作为内部清单。完成回复明确改了哪个文件与范围、哪些判断留给 CHECK/作者、如何针对单处修改提出异议，以及原文/候选分别在哪里。把已应用和已被接受继续区分。

### W13 · P2 · humanizer 首段对 we 的语法定义自相矛盾

pattern-catalog.md:24 称 we 是 “third-person plural”；同一文件 :138 正确称其为 “First-person plural”。英语语法上前者错误，容易误导对人称和声音的说明。将 :24 改成 “first-person plural (we)”。

### W14 · P2 · Writing 元数据与变更记录顺序不一致

haipipe-writing/SKILL.md:13 声明版本 0.18.0。其 CHANGELOG.md:1 最新页眉也是 0.18.0，但 :300-303 却把 0.19.0 新条目附在历史列表尾部。humanizer SKILL.md:13 的 last_updated 是 2026-08-05，而 CHANGELOG.md:1 有 0.3.0 · 260908。版本/日期不易判断，且 agree.py 所述的“最新变更记录”检查会被错误排序绕过。应先确定实际发布版本，再把新条目置顶并同步 frontmatter；humanizer 同步更新日期。

## Workflow / Run 指标

| 技能或交接 | 结论 | 证据与判断 |
|---|---|---|
| haipipe-writing | **partial** | 正确把 Page Run allocation 和 human acceptance 留给 host（SKILL.md:61-64），并限制不创建 sentence/Step/tool-call 子 Run（interactive-writing-run.md:87-89）。但主技能 :189、realize-from-plan.md:144、holes.md:52、:90 仍有当前 “phase” 路由词；Page 用户模板 user-check-packet.md:214 仍将 phase 输出给人。也没有在 Writing 合同中明说 “A Workflow is a list of Runs”。 |
| haipipe-paper-revise-humanizer | **fail** | 当前架构图 :133-140 直接使用 “REVISE phase” 并列出 workers；它没有把这些步骤绑定到当前 Workflow 中一个 Run，且其所谓宿主和关键依赖已退休或不存在。不能把 READ、AUDIT、SECOND PASS、六个 Layer 机械地各改成一个 Run：这些是一次工作内部步骤和审查维度。 |
| Page interactive handoff | **partial，跨家族** | Run / Version / Step 的边界细，SHAPE 与 SURVEY 是同一个 Structure Run 的 cycles；但 user-check-packet.md:214 仍要求显示 “phase <PHASE>”。“phase receipt” 是否兼容字段需要 Page owner 确认。 |

本报告没有发现把 wdiff 工具调用或普通用户回复独立算作 Run 的有效规则。历史变更记录中的 phase spine、paper/2-phase/0-draft 迁移路径和原始引用应保留为历史证据；lane run 指注释行块，不是 Workflow Run，宜改称 annotation block 以免混淆。

## 人类交互桌面走查

以下是基于文档的 desk walkthrough，不是 live 用户测试或运行时观察。

### 1. 普通句子局部修改

请求：“只把第 2 句的 large 换成 substantial。” Writing SKILL.md:33-57 的范围保护能正确限制目标；它也要求披露必要的相邻 seam。若确有文字变化，当前 Step 记录应包含干净的 Before/After 和原因；若最终没有文字改变，则只记录处置和原因，不造变更卡片。

建议回复：“已将第 2 句的 ‘large’ 改为 ‘substantial’。其他句子和论点未改。这里是完整段落：[完整保存文本]。我只检查了这处语法和上下文；如果你要改整段，我们可以另定范围。” 若原词更准确，应说明并提供候选，不能把一个局部要求扩成通篇重写。

### 2. Page 中的单句反馈

请求：“继续这个 Page Run，把 S2 改得更直白。” interactive-writing-run.md 要求复用现有 Run、读目标句和其依赖 Bullet、保留原反馈、只做限定修改，并在返回时区分 agent-applied 与 human-accepted。完成候选后按 user-check-packet 返还段落和三个链接；链接末尾后不附额外状态块。这个边界有助于用户立刻复核，也不把短句编辑升级为新 Run。

现有 handoff 仍会遇到 W5 的用户可见 Phase 字段。修复后建议状态行展示实际当前 Run 和状态；如果并未委托 Run，就直说没有 Run，而不是创建一个空 Run。

### 3. 从大纲与证据起草

请求：“按已批准的 Outline 和证据起草这一段。” realize-from-plan.md:13-40、:65-77 要求检查 paragraph job 和每条 claim 的 Evidence Result；材料不足时回到 OUTLINE/EVIDENCE owner。这能保护 claim authority。现行文案“route back to the owning phase”会让新 agent 错找已废弃的 Phase；按 owner 和已有 Run 路由会更明确。

建议回复：“这个段落的 Evidence Result 没有支持主张 X。我没有弱化或补写该主张。请由 Evidence owner 补足支持，或由 Outline owner 调整已批准的 proposition；在那项决定完成前，我不会把这个缺口写成事实。”

### 4. 学术稿件去 AI 习惯

请求：“改掉 AI 味，但保留所有科学含义、限定语和引用。” 规则本意是保护科学内容，但新上下文 agent 会先遇到已删除的 S/Venue 路径；若它继续，引用集中规则和意义不变规则又给出相反动作。首个 Before/After 样例也展示了凭空加入数值与结果的风险。

安全、清楚的响应应是：“我还不能按这个技能编辑：当前 Page Run Ticket 没有可读的 Section/venue contract（或其中标识的路径已失效）。请补齐现行合同后继续。在拿到证据之前，我不会添加定量结果、移除引用或改动限定语。” 若走 author-selected candidate 模式，应明确原文未改、Note 的位置和机械校验是否实际完成。

## 跨家族待协调项

- **Paper**：humanizer 继续依赖已删除的 S-page、prose-quality 和 revise hub，且要求旧的 REVISE 顺序。Paper 当前 README 与路由已转为 Story / Section Page。Paper 的 haipipe-paper-workflow/SKILL.md:21-30 又仍显式定义 journey phase 和 Page phase；haipipe-paper/SKILL.md:28-40 仍要求 current Page phase。请协调 Paper、Page workflow、Humanizer 与 Run/Step 总合同的映射；本报告未将整个 Paper 家族的结构自行改写。
- **Page**：user-check-packet.md:214 的 Phase UI 文案直接由 Writing handoff 引用；:5、:25 的 phase receipt 是否仅旧名不明确。该文件应由 Page owner 更新并确认字段是否仍被运行时消费者读取。
- **结构 / Application / Insight / Design**：skills/STRUCTURE.md:144-149 将 Application 叫作 Insight/Design 的 join，与本轮“一等且独立、无 Application parent”的硬性标准不符。由 Structure/对应家族所有者修正；Writing README 不应再把 application 当成 writing 所属关系的分类例子。

## 建议修正顺序

1. 先由 Paper 与 Page owner 恢复 humanizer 在当前 Page Run 下的输入、Venue / claim contract 和输出归属；在依赖路径未修复前，不应把此技能介绍为可直接运行的现行 Paper worker。
2. 将证据、限定语和引用保真置于通用“去 AI”改写规则之前；修正会鼓励编造事实的学术 Before/After 示例。
3. 修正或限制 Paper-host wdiff checker 的承诺，给出正确作者标签，并统一 sentence split 规则。
4. 修复 live Phase 用语与面向用户的状态模板；在 host contract 上补一句：“A Workflow is an ordered list of Runs. A worker performs only the work commissioned within its current Run; its internal Steps and tool calls do not allocate Runs.”
5. 修复 score.py 与 slop.py 文案、无文案 Step 记录规则、README §4 引用和变更记录顺序。
6. 明确直接应用后的作者异议/接受方式和 humanizer 完成摘要；订正 we 的语法人称。

以上均为评审建议，本轮未实施代码或技能修改。
